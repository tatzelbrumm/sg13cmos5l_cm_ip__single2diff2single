# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""LVS by extraction with klayout.db (LayoutVsSchematic + NetlistComparer), IHP sg13cmos5l HV MOS only.
Written 2026-10-28 by Claude. IHP's LVS deck is not in the uploaded PDK copy (no libs.tech/klayout/tech/lvs).

Device recognition follows the derivations of the DRC decks (ihp-sg13cmos5l.drc, sg13cmos5l_maximal.drc):
  N+Activ = Activ not under pSD; P+Activ = Activ under pSD; gate = Activ & GatPoly;
  sg13_hv_pmos = gate on P+Activ in NWell under ThickGateOx, bulk = NWell;
  sg13_hv_nmos = gate on N+Activ outside NWell under ThickGateOx, bulk = substrate;
  a gate outside ThickGateOx (LV device) is reported as an error, there must be none.
Connectivity: S/D, ties and GatPoly -Cont- M1 -Via1- M2; NWell - N+ tie; substrate - P+ tie. Texts on 8/25 and
10/25 name nets. Two passes: (1) with all labels, to find shorts (a net carrying two label names) and opens
(one label name on two nets); (2) with the top cell's own labels only, compared with the reference netlist.

    python3 lvs.py <gds> <cell> <reference.cdl> [subckt|-] [report.lvsdb] [--join] [--flat-ref]
    --flat-ref: the reference file is read whole (all subckts) and flattened (hierarchical reference)
"""
import os
import sys
import collections
import klayout.db as db


def extract(gds, cellname, labels="all", join=False, combine=True):
    ly = db.Layout()
    ly.read(gds)
    cell = ly.cell(cellname)
    if labels == "top":                      # drop label texts below the top cell
        for c in ly.each_cell():
            if c.cell_index() != cell.cell_index():
                for l, d in ((8, 25), (10, 25), (8, 2), (10, 2)):
                    li = ly.find_layer(l, d)
                    if li is not None:
                        for s in list(c.shapes(li).each()):
                            if s.is_text():
                                c.shapes(li).erase(s)
    cell.flatten(-1, True)                   # flat extraction: one circuit, every label names a net of it
    lvs = db.LayoutVsSchematic(db.RecursiveShapeIterator(ly, cell, []))
    if join:
        lvs.join_net_names("*")
    mk = lambda l, d, n: lvs.make_polygon_layer(ly.layer(l, d), n)   # texts only from 8/25 and 10/25
    act, poly, cont, m1, v1, m2, psd, nw, tgo = (mk(1, 0, "act"), mk(5, 0, "poly"), mk(6, 0, "cont"), mk(8, 0, "m1"),
                                                 mk(19, 0, "v1"), mk(10, 0, "m2"), mk(14, 0, "psd"), mk(31, 0, "nw"),
                                                 mk(44, 0, "tgo"))
    nsd_l = mk(7, 0, "nsd")
    pact = (act & psd) - nsd_l
    nact = act - pact
    chip = db.Region(cell.bbox()).sized(int(20 / ly.dbu))
    sub = chip - nw                     # substrate (no PWell block in these cells)
    gate = act & poly
    pg_hv = (gate & pact & nw) & tgo
    ng_hv = (gate & nact) - nw
    ng_hv = ng_hv & tgo
    lv_gates = gate - tgo
    psd_sd = (pact & nw) - poly
    nsd_sd = (nact - nw) - poly
    ntap = (nact & nw) - poly
    ptap = (pact - nw) - poly
    for r, n in ((pact, "pact"), (nact, "nact"), (pg_hv, "pg"), (ng_hv, "ng"), (psd_sd, "psd_sd"),
                 (nsd_sd, "nsd_sd"), (ntap, "ntap"), (ptap, "ptap"), (lv_gates, "lvg")):
        lvs.register(r, n)
    lvs.register(sub, "sub")
    lvs.extract_devices(db.DeviceExtractorMOS4Transistor("sg13_hv_pmos"),
                        {"SD": psd_sd, "G": pg_hv, "P": poly, "W": nw})
    lvs.extract_devices(db.DeviceExtractorMOS4Transistor("sg13_hv_nmos"),
                        {"SD": nsd_sd, "G": ng_hv, "P": poly, "W": sub})
    for r in (psd_sd, nsd_sd, ntap, ptap, poly, m1, m2, nw, sub):
        lvs.connect(r)
    for a, b in ((psd_sd, cont), (nsd_sd, cont), (ntap, cont), (ptap, cont), (poly, cont), (cont, m1),
                 (m1, v1), (v1, m2), (nw, ntap), (sub, ptap)):
        lvs.connect(a, b)
    for (l, d), m in (((8, 25), m1), ((10, 25), m2)):
        li = ly.find_layer(l, d)
        if li is not None:
            lvs.connect(m, lvs.make_text_layer(li, "t%d" % l))
    lvs.extract_netlist()
    nl = lvs.netlist()
    if combine:
        nl.combine_devices()
    return lvs, ly, lv_gates.count()


def label_check(gds, cellname):
    """Pass 1: every label name on exactly one net, every net with at most one label name."""
    lvs, ly, _ = extract(gds, cellname, "all")
    c = lvs.netlist().circuit_by_name(cellname)
    tapnames = {"well", "sub!"}                # labels of the ntap1 / ptap1 PCells: aliases of the tie net
    shorts = [n.name for n in c.each_net() if n.name and len(set(n.name.split(",")) - tapnames) > 1]
    names = collections.Counter()
    for n in c.each_net():
        if n.name:
            for s in n.name.split(","):
                names[s] += 1
    opens = sorted(k for k, v in names.items() if v > 1)
    return shorts, opens, sorted(names)


def compare(gds, cellname, cdl, subckt=None, lvsdb=None, join=False, out=sys.stdout, flat_ref=False):
    lvs, ly, nlv = extract(gds, cellname, "all" if join else "top", join)
    nl = lvs.netlist()
    c = nl.circuit_by_name(cellname)
    nl.case_sensitive = False                  # the SPICE reader makes the reference case-insensitive
    sub = subckt or cellname
    import re
    if flat_ref:                                 # hierarchical reference (subckts of primitive libraries): flatten
        ref = db.Netlist()
        ref.read(cdl, db.NetlistSpiceReader())
        ref.flatten()
    else:
        blk = re.search(r"^\.SUBCKT\s+%s\b.*?^\.ENDS\b[^\n]*" % re.escape(sub), open(cdl).read(), re.S | re.M | re.I)
        tmp = (lvsdb or "lvs") + ".ref.cdl"      # only the compared subckt (the library .cdl also has rhigh)
        open(tmp, "w").write(blk.group(0) + "\n")
        ref = db.Netlist()
        ref.read(tmp, db.NetlistSpiceReader())
        os.remove(tmp)
    rc = ref.circuit_by_name(sub)
    for cc in list(ref.each_circuit()):        # keep only the subckt compared
        if cc.name.lower() != sub.lower():
            ref.remove(cc)
    ref.combine_devices()                      # parallel fingers on both sides, as LVS decks do
    rc.name = cellname
    for p in rc.each_pin():                     # layout pins = nets named like the reference pins
        net = c.net_by_name(p.name())
        pin = c.create_pin(p.name())
        if net is not None:
            c.connect_pin(pin, net)
    lvs.reference = ref
    comp = db.NetlistComparer()
    ok = lvs.compare(comp)
    if lvsdb:
        lvs.write(lvsdb)
    # summary
    xref = lvs.xref()
    out.write("LVS %s vs %s:%s -> %s\n" % (cellname, cdl.split("/")[-1], sub, "MATCH" if ok else "MISMATCH"))
    out.write("  LV gates (outside ThickGateOx): %d\n" % nlv)
    for cp in xref.each_circuit_pair():
        a, b = cp.first(), cp.second()
        for dp in xref.each_device_pair(cp):
            d1, d2 = dp.first(), dp.second()
            if dp.status() != db.NetlistCrossReference.Match:
                out.write("  device %s: layout %s / ref %s\n" % (dp.status(), d1.expanded_name() if d1 else "-",
                                                                d2.expanded_name() if d2 else "-"))
        for np_ in xref.each_net_pair(cp):
            n1, n2 = np_.first(), np_.second()
            if np_.status() not in (db.NetlistCrossReference.Match, db.NetlistCrossReference.MatchWithWarning):
                out.write("  net %s: layout %s / ref %s\n" % (np_.status(), n1.expanded_name() if n1 else "-",
                                                             n2.expanded_name() if n2 else "-"))
    # device table, layout side after combination, nets named by their reference partner
    rname = {}
    for cp in xref.each_circuit_pair():
        for np_ in xref.each_net_pair(cp):
            if np_.first() is not None and np_.second() is not None:
                rname[np_.first().cluster_id] = np_.second().expanded_name().lower()
    agg = []
    for d in c.each_device():
        t = lambda k: rname.get(d.net_for_terminal(k).cluster_id, d.net_for_terminal(k).expanded_name())
        agg.append("  %-13s D=%-9s G=%-9s S=%-9s B=%-5s W=%8.3f L=%7.3f" % (d.device_class().name, t("D"), t("G"),
                   t("S"), t("B"), d.parameter("W"), d.parameter("L")))
    out.write("  layout devices after parallel combination: %d\n" % len(agg))
    out.write("\n".join(sorted(agg)) + "\n")
    return ok


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    join = "--join" in sys.argv
    flat_ref = "--flat-ref" in sys.argv
    gds, cellname, cdl = a[0], a[1], a[2]
    subckt = a[3] if len(a) > 3 and a[3] != "-" else None
    lvsdb = a[4] if len(a) > 4 else None
    shorts, opens, names = label_check(gds, cellname)
    print("labels: %d names; nets with two label names (shorts): %s; names on two nets (opens): %s"
          % (len(names), shorts or "none", opens or "none"))
    ok = compare(gds, cellname, cdl, subckt, lvsdb, join, flat_ref=flat_ref)
    sys.exit(0 if ok and not shorts else 1)
