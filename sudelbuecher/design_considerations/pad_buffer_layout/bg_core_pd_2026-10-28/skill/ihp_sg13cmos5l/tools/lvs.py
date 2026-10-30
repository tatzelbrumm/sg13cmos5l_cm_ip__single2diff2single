# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""LVS by extraction with klayout.db (LayoutVsSchematic + NetlistComparer), IHP sg13cmos5l: HV MOS, rhigh, pnpMPA.
rhigh is a two-terminal resistor with R in squares (L / W); pnpMPA a 3-terminal BJT with the substrate as collector
(reference: R lines with R = l / w, Q lines "Q<n> c b e pnpMPA AE=4p PE=8u").
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
    polyres = mk(128, 0, "polyres")
    pact = (act & psd) - nsd_l
    nact = act - pact
    chip = db.Region(cell.bbox()).sized(int(20 / ly.dbu))
    sub = chip - nw                     # substrate (no PWell block in these cells)
    # rhigh (sg13cmos5l rhigh PCell): the body is drawn on PolyRes (128/0) alone; GatPoly (5/0) only forms the two
    # contact heads that abut the body's ends. poly_c (GatPoly outside PolyRes) is the conductor.
    res_body = polyres
    poly_c = poly - polyres
    gate = act & poly_c
    pg_hv = (gate & pact & nw) & tgo
    ng_hv = (gate & nact) - nw
    ng_hv = ng_hv & tgo
    lv_gates = gate - tgo
    psd_sd = (pact & nw) - poly
    nsd_sd = (nact - nw) - poly
    ntap = (nact & nw) - poly
    ptap = (pact - nw) - poly
    # pnpMPA (sg13cmos5l): emitter = P+ Activ in NWell that touches no gate; base = that NWell (tied by the n+ base
    # ring = ntap); collector = substrate (the p+ collector ring = ptap), via a global net
    pnp_e = (pact & nw).not_interacting(gate)
    pnp_b = nw.interacting(pnp_e)
    tC = lvs.make_layer("pnp_tc")
    for r, n in ((pact, "pact"), (nact, "nact"), (pg_hv, "pg"), (ng_hv, "ng"), (psd_sd, "psd_sd"),
                 (nsd_sd, "nsd_sd"), (ntap, "ntap"), (ptap, "ptap"), (lv_gates, "lvg"), (poly_c, "poly_c"),
                 (pnp_e, "pnp_e"), (pnp_b, "pnp_b")):
        lvs.register(r, n)
    lvs.register(sub, "sub")
    lvs.extract_devices(db.DeviceExtractorMOS4Transistor("sg13_hv_pmos"),
                        {"SD": psd_sd, "G": pg_hv, "P": poly_c, "W": nw})
    lvs.extract_devices(db.DeviceExtractorMOS4Transistor("sg13_hv_nmos"),
                        {"SD": nsd_sd, "G": ng_hv, "P": poly_c, "W": sub})
    # rhigh as a two-terminal resistor; R in squares (L / W, sheet "rho" = 1): the reference writes R = l / w
    lvs.extract_devices(db.DeviceExtractorResistor("RES", 1.0), {"R": res_body, "C": poly_c})
    no_c = lvs.make_layer("pnp_noc")                                 # empty collector layer: substrate collector
    lvs.extract_devices(db.DeviceExtractorBJT3Transistor("PNPMPA"), {"E": pnp_e, "B": pnp_b, "C": no_c, "tC": tC})
    for r in (psd_sd, nsd_sd, ntap, ptap, poly_c, m1, m2, nw, sub):
        lvs.connect(r)
    for a, b in ((psd_sd, cont), (nsd_sd, cont), (ntap, cont), (ptap, cont), (poly_c, cont), (cont, m1),
                 (m1, v1), (v1, m2), (nw, ntap), (sub, ptap)):
        lvs.connect(a, b)
    for r, host in ((pnp_e, psd_sd), (pnp_b, nw)):         # terminal annotation layers of the pnp
        lvs.connect(r)
        lvs.connect(r, host)
    lvs.connect(tC)
    lvs.connect_global(tC, "SUBSTRATE")
    lvs.connect_global(sub, "SUBSTRATE")
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
    lvs, ly, nlv = extract(gds, cellname, "all" if join else "top", join, combine=False)
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
    by_name = {}
    for n in c.each_net():                      # case-insensitive (net_by_name is not, after case_sensitive=False)
        for nm in (n.name or "").split(","):
            if nm:
                by_name.setdefault(nm.lower(), n)
    for p in rc.each_pin():                     # layout pins = nets named like the reference pins
        net = by_name.get(p.name().lower())
        pin = c.create_pin(p.name())
        if net is not None:
            c.connect_pin(pin, net)
    nl.combine_devices()                        # after the pins: series resistors do not merge across a port
    for dc in ref.each_device_class():          # sums of series / parallel parts: compare with a relative tolerance
        if isinstance(dc, db.DeviceClassResistor):
            dc.equal_parameters = db.EqualDeviceParameters(db.DeviceClassResistor.PARAM_R, 0.0, 1e-6)
        elif isinstance(dc, db.DeviceClassBJT3Transistor):
            dc.equal_parameters = (db.EqualDeviceParameters(db.DeviceClassBJT3Transistor.PARAM_AE, 0.0, 1e-6) +
                                   db.EqualDeviceParameters(db.DeviceClassBJT3Transistor.PARAM_NE, 0.0, 1e-6))
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
        dc = d.device_class()
        if isinstance(dc, db.DeviceClassResistor):
            agg.append("  %-13s A=%-9s B=%-9s R=%10.3f sq (L=%.3f W=%.3f)" % (dc.name, t("A"), t("B"),
                       d.parameter("R"), d.parameter("L"), d.parameter("W")))
        elif isinstance(dc, db.DeviceClassBJT3Transistor):
            agg.append("  %-13s C=%-9s B=%-9s E=%-9s AE=%7.3f NE=%g" % (dc.name, t("C"), t("B"), t("E"),
                       d.parameter("AE"), d.parameter("NE")))
        else:
            agg.append("  %-13s D=%-9s G=%-9s S=%-9s B=%-5s W=%8.3f L=%7.3f" % (dc.name, t("D"), t("G"),
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
