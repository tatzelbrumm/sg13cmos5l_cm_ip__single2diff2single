# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Layout primitives for pad_ref_rb, collected from the drawn s2d pad cell (session C3, DRC clean, LVS match).

The replica bias copies the pads' devices, so its layout should copy the pads' layout structures too: the same device
cells (finger geometry, contacts, well surround) and, where the replica sits next to its siblings, the same rows.
This script reads macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/sg13cmos5l_IOPadSingle2Diff.klay.gds (read only:
the pad layout stays unchanged), keeps the source rows below and their device cells, renames every kept cell to
`rbsrc_<name>` (leaf devices to a descriptive `rbsrc_{n,p}hv_w<W>_l<L>[_ng<n>]`), checks each copy against its source
by XOR, and writes
  pad_ref_rb_primitives.gds   top cell pad_ref_rb_primitives: every kept cell, one per line, with its name on TEXT 63/0
  primitives.tsv              every leaf device cell: type, W, L, ng (measured from Activ AND GatPoly), bbox, source name
  mapping.tsv                 every device of pad_ref_rb (source netlists) -> leaf primitive -> pad row it replicates

usage: python3 -I collect_primitives.py      (needs the klayout Python module; writes into this directory)
"""
import csv
import re
from collections import Counter
from pathlib import Path

import klayout.db as db

HERE = Path(__file__).resolve().parent
MAC = HERE.parents[2]
SRC = MAC / "sg13cmos5l_IOPadSingle2Diff/layout/klayout/sg13cmos5l_IOPadSingle2Diff.klay.gds"
NETS = [MAC / "pad_ref_rb/netlist/source/pad_ref_rb.spice", MAC / "vcm_rb/netlist/source/vcm_rb.spice",
        MAC / "vref_s2d_rb/netlist/source/vref_s2d_rb.spice"]

# source rows of the s2d pad (agents P and N of session C3) and what each holds there
ROWS = {
    "bias_tree_noab_p_c3": "s2d bias tree, PMOS: PBN 5/6, PBNC 2/6, dummy 2/6 (MDBP), TGP 1/0.45",
    "bias_tree_noab_n_c3": "s2d bias tree, NMOS: NI 6/6, NBP 6/6, NBPC 2.4/6, dummy 2.4/6 (MDBN), TGN / TDN 1/0.45",
    "s2d_tails_hi_f": "unit tails: 8 x 5/6 on vbp in one iovdd well (BP among them)",
    "tub_p20x1_c3": "unit input device 20/1 ng=2 in its own well (bulk = source)",
    "s2d_inputs_c3": "16 tubs (12 units + 4 dummies), two rows of 8",
    "s2d_casc_n_f": "NMOS cascodes: 8 x 15/3 on vbnc (CX / CY / CXC / CYC), 4 dummies 2/3, BNC 1/8",
    "sinks_6x6_s2d_c3_core": "fold sinks: 14 x 6/6 on vbn (SX / SY, BN, BN twin), 4 dummies 2/6",
    "s2d_sinks_cmfb_c3_core": "CMFB sinks: 8 x 6/6 on vbn, 4 dummies 2/6",
    "s2d_cload_c3": "load capacitors CLP / CLN 12x12 hv NMOS, TPN / TNN 1/0.45",
    "s2d_loads_f": "PMOS loads: 12 x 6/4 in one iovdd well, 4 x 1/4 (the 1/4 finger the averaging diodes need)",
}

LAY = dict(activ=(1, 0), poly=(5, 0), psd=(14, 0), nwell=(31, 0), tgo=(44, 0), text=(63, 0))
UNIT = 1e-6


def um(x):
    return f"{x:g}".replace(".", "p")


def measure(ly, c):
    """(type, W per finger, L, ng) of a leaf device cell from its own shapes."""
    li = {k: ly.find_layer(*v) for k, v in LAY.items()}
    reg = lambda k: db.Region(c.begin_shapes_rec(li[k])) if li[k] is not None else db.Region()
    gates = (reg("activ") & reg("poly")).merged()
    poly = reg("poly")
    dims = []
    for g in gates.each():
        b = g.bbox()
        pb = next((p.bbox() for p in poly.each() if p.bbox().overlaps(b)), b)
        w, l = (b.height(), b.width()) if pb.height() > b.height() else (b.width(), b.height())
        dims.append((round(w * ly.dbu, 3), round(l * ly.dbu, 3)))
    typ = "p" if not reg("nwell").is_empty() and not reg("psd").is_empty() else "n"
    if not dims:
        return typ, 0, 0, 0
    (w, l), ng = Counter(dims).most_common(1)[0]
    return typ, w, l, ng


def leaf_name(typ, w, l, ng):
    return f"{typ}hv_w{um(w * ng)}_l{um(l)}" + (f"_ng{ng}" if ng > 1 else "")


def devices():
    """pad_ref_rb's MOS devices: (cell, name, type, W total, L, ng) from the source netlists."""
    out, sub = [], None
    for f in NETS:
        for l in f.read_text().splitlines():
            if l.lower().startswith(".subckt"):
                sub = l.split()[1]
            m = re.match(r"^X(\S+)\s+\S+\s+\S+\s+\S+\s+\S+\s+sg13_hv_([np])mos\s+(.*)$", l, re.I)
            if m:
                p = dict(kv.split("=") for kv in m.group(3).split())
                w, ln = float(p["w"].rstrip("u")), float(p["l"].rstrip("u"))
                out.append((sub, m.group(1), m.group(2), w, ln, int(p.get("ng", 1))))
    return out


# which pad structure each replica copies (the replica relation, see README.md)
REPLICATES = {
    ("bias_tree_rb", "TGN"): "bias_tree_noab_n_c3 TGN", ("bias_tree_rb", "TDN"): "bias_tree_noab_n_c3 TDN",
    ("bias_tree_rb", "TGP"): "bias_tree_noab_p_c3 TGP", ("bias_tree_rb", "NI"): "bias_tree_noab_n_c3 NI",
    ("bias_tree_rb", "NBP"): "bias_tree_noab_n_c3 NBPC (2.4/6 on ni)", ("bias_tree_rb", "BP"): "bias_tree_noab_p_c3 dummy 2/6 slot, as diode",
    ("bias_tree_rb", "PBNC"): "bias_tree_noab_p_c3 PBNC", ("bias_tree_rb", "BNC"): "s2d_casc_n_f BNC (1/8 in the cascode row)",
    ("bias_tree_rb", "MDPBN"): "bias_tree_noab_p_c3 PBN 5/6 slot, kept as a dummy (D = S = B = vdd, gate vbp)",
    ("vcm_rb", "TR"): "s2d_tails_hi_f unit tail (or bias_tree_noab_p_c3 PBN 5/6 slot)", ("vcm_rb", "BT"): "s2d_tails_hi_f unit tail",
    ("vcm_rb", "MR"): "tub_p20x1_c3 (s2d_inputs_c3)", ("vcm_rb", "BA"): "tub_p20x1_c3 (s2d_inputs_c3)",
    ("vcm_rb", "BB"): "tub_p20x1_c3 (s2d_inputs_c3)",
    ("vcm_rb", "SH1"): "bias_tree_noab_n_c3 dummy 2.4/6 slot (MDBN)", ("vcm_rb", "SH2"): "2.4/6 finger next to NI (new slot)",
    ("vcm_rb", "CY"): "s2d_casc_n_f CY finger 15/3 on vbnc", ("vcm_rb", "SY"): "sinks_6x6 SY finger 6/6 (or bias_tree_noab_n_c3 NBP 6/6 slot)",
    ("vcm_rb", "SU"): "1/4 finger of s2d_loads_f, but in its own well: NEW small tub (no s2d structure)",
    ("vcm_rb", "SL1"): "1/4 PMOS in its own well: NEW small tub", ("vcm_rb", "SL2"): "1/4 PMOS in its own well: NEW small tub",
    ("vcm_rb", "BD"): "sinks_6x6 6/6 finger (mirror pair BD / BM)", ("vcm_rb", "BM"): "sinks_6x6 6/6 finger (mirror pair BD / BM)",
    ("vcm_rb", "CB"): "s2d_cload_c3 CLP / CLN 12x12", ("vcm_rb", "SPD"): "s2d_cload_c3 TNN / TPN 1/0.45",
    ("vref_s2d_rb", "F1"): "s2d_casc_n_f 15/3 finger on vbnc", ("vref_s2d_rb", "F2"): "s2d_casc_n_f 15/3 finger on vbnc",
    ("vref_s2d_rb", "F3"): "s2d_casc_n_f 15/3 finger on vbnc", ("vref_s2d_rb", "F4"): "s2d_casc_n_f 15/3 finger on vbnc",
    ("vref_s2d_rb", "SF"): "sinks_6x6 end device 2/6 (a dummy there)",
    ("vref_s2d_rb", "CB1"): "s2d_cload_c3 CLP / CLN 12x12", ("vref_s2d_rb", "CB2"): "s2d_cload_c3 CLP / CLN 12x12",
    ("vref_s2d_rb", "SPD"): "s2d_cload_c3 TNN / TPN 1/0.45",
}


def main():
    src = db.Layout()
    src.read(str(SRC))
    ly = db.Layout()
    ly.read(str(SRC))
    keep = set()
    for r in ROWS:
        c = ly.cell(r)
        keep.add(c.cell_index())
        keep.update(c.called_cells())
    ly.delete_cells([c.cell_index() for c in ly.each_cell() if c.cell_index() not in keep])
    # rename: leaves descriptively, rows with the prefix only
    rows, leaves = [], []
    for c in list(ly.each_cell()):
        old = c.name
        if c.child_cells() == 0:
            t, w, l, ng = measure(ly, c)
            c.name = "rbsrc_" + (leaf_name(t, w, l, ng) if w else old.replace("$", "_"))
            b = c.bbox().to_dtype(ly.dbu)
            leaves.append(dict(cell=c.name, source=old, type=t, W=w * ng, L=l, ng=ng, finger_W=w,
                               bbox_w=round(b.width(), 2), bbox_h=round(b.height(), 2)))
        else:
            c.name = "rbsrc_" + old
            rows.append((old, c))
    # XOR check of every kept cell against its source (flattened geometry, all layers)
    bad = []
    for c in ly.each_cell():
        s = src.cell(next(r["source"] for r in leaves if r["cell"] == c.name) if c.child_cells() == 0
                     else c.name[len("rbsrc_"):])
        for li in ly.layer_indexes():
            info = ly.get_info(li)
            si = src.find_layer(info)
            a = db.Region(c.begin_shapes_rec(li))
            b = db.Region(s.begin_shapes_rec(si)) if si is not None else db.Region()
            if not (a ^ b).is_empty():
                bad.append((c.name, str(info)))
    # top cell: rows on the left, leaves on the right, one per line, labelled
    top = ly.create_cell("pad_ref_rb_primitives")
    txt = ly.layer(*LAY["text"])
    y = 0
    for old, c in sorted(rows, key=lambda x: x[0]):
        b = c.bbox()
        top.insert(db.CellInstArray(c.cell_index(), db.Trans(-b.left, y - b.bottom)))
        top.shapes(txt).insert(db.Text(c.name, db.Trans(b.width() + 2000, y + b.height() // 2)))
        y += b.height() + 4000
    y = 0
    for r in sorted(leaves, key=lambda r: r["cell"]):
        c = ly.cell(r["cell"])
        b = c.bbox()
        top.insert(db.CellInstArray(c.cell_index(), db.Trans(110000 - b.left, y - b.bottom)))
        top.shapes(txt).insert(db.Text(c.name, db.Trans(110000 + b.width() + 2000, y + b.height() // 2)))
        y += b.height() + 3000
    ly.write(str(HERE / "pad_ref_rb_primitives.gds"))
    with open(HERE / "primitives.tsv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(leaves[0]), delimiter="\t")
        w.writeheader()
        w.writerows(sorted(leaves, key=lambda r: r["cell"]))
    # mapping: every device of pad_ref_rb to a leaf primitive
    by = {(r["type"], r["W"], r["L"], r["ng"]): r["cell"] for r in leaves}
    miss = []
    with open(HERE / "mapping.tsv", "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["cell", "device", "type", "W", "L", "ng", "primitive", "replicates (s2d pad structure)"])
        for sub, name, t, wd, ln, ng in devices():
            prim = by.get((t, wd, ln, ng), "MISSING")
            if prim == "MISSING":
                miss.append((sub, name))
            w.writerow([sub, name, t, wd, ln, ng, prim, REPLICATES.get((sub, name), "")])
    render()
    print(f"{len(rows)} rows, {len(leaves)} leaf devices -> {HERE / 'pad_ref_rb_primitives.gds'}")
    print(f"XOR against the s2d pad cell: {'identical' if not bad else bad}")
    print(f"pad_ref_rb devices without a primitive: {miss if miss else 'none'}")


def render():
    """PNG overview (cell names on TEXT 63/0, IHP layer colours)."""
    import klayout.lay as lay
    v = lay.LayoutView()
    v.load_layout(str(HERE / "pad_ref_rb_primitives.gds"))
    v.load_layer_props(str(Path("/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/sg13cmos5l.lyp")))
    v.max_hier()
    for k, val in (("background-color", "#ffffff"), ("grid-visible", "false"), ("text-visible", "true"),
                   ("default-text-size", "1.6"), ("text-font", "1")):
        v.set_config(k, val)
    v.zoom_fit()
    v.save_image_with_options(str(HERE / "pad_ref_rb_primitives.png"), 1800, 1400, 0, 0, 0, db.DBox(), False)


if __name__ == "__main__":
    main()
