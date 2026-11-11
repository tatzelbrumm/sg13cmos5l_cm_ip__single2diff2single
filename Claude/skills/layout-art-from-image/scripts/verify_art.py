#!/usr/bin/env python3
"""Verify the art: XOR against the untouched slot7, clearance to existing metal, PDK DRC and LVS before / after.

usage: verify_art.py [--slot SLOT_GDS] [--cdl SLOT_CDL] [--work DIR] [--skip-runs]
 - XOR:  merged GDS with the cell tughra_art deleted, versus the original slot_7.gds, every layer/datatype, flattened.
 - clearance: distance of the art on each metal layer to the existing shapes of that layer (and of the other metals).
 - DRC: PDK run_drc.py (all tables incl. density and antenna) on the original and on the merged GDS; rules and marker
        counts compared; density ratios before / after.
 - LVS: PDK run_lvs.py (deep, tap extraction off, as the slot7 README does) on both against slot7's CDL.
Writes art/verify_report.md and art/verify_report.json; the tool logs go to art/verify/.
"""
import argparse, json, os, re, subprocess, sys, shutil, collections
import xml.etree.ElementTree as ET
import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pdk_layers as pl

ap = argparse.ArgumentParser()
ap.add_argument("--slot", default=os.environ.get("SLOT7_GDS", "/home/user/sg13cmos5l_cm_slot7/final/gds/slot_7.gds"))
ap.add_argument("--cdl", default=os.environ.get("SLOT7_CDL", "/home/user/sg13cmos5l_cm_slot7/netlist/slot_7.cdl"))
ap.add_argument("--work", default="/tmp/tughra_verify")
ap.add_argument("--skip-runs", action="store_true", help="reuse DRC/LVS runs already in --work")
a = ap.parse_args()
MERGED = os.path.join(HERE, "slot7_with_art.gds")
ART = os.path.join(HERE, "tughra_art.gds")
OUT = os.path.join(HERE, "verify")
os.makedirs(OUT, exist_ok=True); os.makedirs(a.work, exist_ok=True)
env = dict(os.environ, PDK_ROOT="/foss/pdks", PDK="ihp-sg13cmos5l")
TECH = pl.TECH
rep = {}


def flat_region(ly, cell, li):
    return db.Region(cell.begin_shapes_rec(li)).merged()


# ---------------------------------------------------------------- XOR
def xor_check():
    orig = db.Layout(); orig.read(a.slot)
    m = db.Layout(); m.read(MERGED)
    art_cell = m.cell("tughra_art")
    n_inst = sum(1 for c in m.each_cell() for i in c.each_inst() if i.cell_index == art_cell.cell_index())
    m.delete_cell(art_cell.cell_index())
    res = {"instances_of_art_cell": n_inst, "layers": {}, "total_xor_polygons": 0}
    otop, mtop = orig.cell("slot_7"), m.cell("slot_7")
    keys = set()
    for ly in (orig, m):
        for li in ly.layer_indexes():
            i = ly.get_info(li); keys.add((i.layer, i.datatype))
    for (l, d) in sorted(keys):
        lo, lm = orig.find_layer(l, d), m.find_layer(l, d)
        ro = flat_region(orig, otop, lo) if lo is not None else db.Region()
        rm = flat_region(m, mtop, lm) if lm is not None else db.Region()
        x = ro ^ rm
        res["layers"][f"{l}/{d}"] = x.count()
        res["total_xor_polygons"] += x.count()
    # labels
    def labels(ly, top):
        out = collections.Counter()
        for li in ly.layer_indexes():
            for s in top.begin_shapes_rec(li).each() if False else []:
                pass
        for li in ly.layer_indexes():
            it = top.begin_shapes_rec(li)
            while not it.at_end():
                sh = it.shape()
                if sh.is_text():
                    out[(ly.get_info(li).layer, ly.get_info(li).datatype, sh.text_string, sh.text_trans.disp.x, sh.text_trans.disp.y)] += 1
                it.next()
        return out
    res["labels_equal"] = labels(orig, otop) == labels(m, mtop)
    res["cells_after_removal_equal"] = sorted(c.name for c in orig.each_cell()) == sorted(c.name for c in m.each_cell())
    return res


# ---------------------------------------------------------------- clearance
def clearance():
    ln = pl.layer_numbers()
    orig = db.Layout(); orig.read(a.slot)
    art = db.Layout(); art.read(ART)
    otop, atop = orig.cell("slot_7"), art.cell("tughra_art")
    m = db.Layout(); m.read(MERGED)
    inst = [i for i in m.cell("slot_7").each_inst() if m.cell(i.cell_index).name == "tughra_art"][0]
    dx, dy = inst.trans.disp.x, inst.trans.disp.y
    res = {"origin_um": [dx * m.dbu, dy * m.dbu], "layers": {}}
    # existing shapes: FEOL (every layer that is not metal / via / boundary / text) and each metal
    def existing(name):
        occ = db.Region()
        for li in orig.layer_indexes():
            i = orig.get_info(li)
            if i.datatype in (1, 25):
                continue
            hit = (i.layer not in pl.NON_FEOL) if name == "FEOL" else (i.layer == ln[name + ".drawing"][0])
            if hit:
                occ += db.Region(otop.begin_shapes_rec(li))
        return occ.merged()
    occs = {n: existing(n) for n in ["FEOL"] + pl.METALS}
    for L in [pl.POLY] + pl.METALS:
        l, d = ln[L + ".drawing"]
        if art.find_layer(l, d) is None:
            continue            # layer not used by the art
        artR = db.Region(atop.begin_shapes_rec(art.find_layer(l, d))).transformed(db.Trans(dx, dy)).merged()
        entry = {"art_polygons": artR.count(), "art_area_um2": artR.area() * 1e-6}
        for n, occ in occs.items():
            dist = None
            if not (artR.sized(int(60 / m.dbu)) & occ).is_empty():          # something within 60 um: bisect to 5 nm
                lo, hi = 0.0, 60.0
                for _ in range(14):
                    mid = (lo + hi) / 2
                    if (artR.sized(int(mid / m.dbu)) & occ).is_empty():
                        lo = mid
                    else:
                        hi = mid
                dist = round(hi, 3)
            entry[f"vs_{n}"] = {"overlap_um2": (artR & occ).area() * 1e-6, "touches_within_um": dist}
        bb = artR.bbox()
        entry["min_distance_to_slot_edge_um"] = min(bb.left, bb.bottom, otop.bbox().right - bb.right, otop.bbox().top - bb.top) * m.dbu
        res["layers"][L] = entry
    # no-fill markers: present on every listed layer, and each art layer lies inside its marker
    nf = {}
    for name in ["Activ.nofill", "GatPoly.nofill", "Metal1.nofill", "Metal2.nofill", "Metal3.nofill", "Metal4.nofill", "TopMetal1.nofill"]:
        li = art.find_layer(*ln[name])
        r = db.Region(atop.begin_shapes_rec(li)).transformed(db.Trans(dx, dy)) if li is not None else db.Region()
        nf[name] = {"gds": list(ln[name]), "boxes": r.count(), "box_um": [round(v * m.dbu, 3) for v in (r.bbox().left, r.bbox().bottom, r.bbox().right, r.bbox().top)] if not r.is_empty() else None}
    allart = db.Region()
    for L in [pl.POLY] + pl.METALS:
        li = art.find_layer(*ln[L + ".drawing"])
        if li is not None:
            allart += db.Region(atop.begin_shapes_rec(li)).transformed(db.Trans(dx, dy))
    nfreg = db.Region(atop.begin_shapes_rec(art.find_layer(*ln["Metal1.nofill"]))).transformed(db.Trans(dx, dy))
    nf["art_inside_nofill_box"] = (allart - nfreg).is_empty()
    # nofill markers of the other layers equal the Metal1 one
    nf["all_markers_identical"] = all((db.Region(atop.begin_shapes_rec(art.find_layer(*ln[n]))) ^ db.Region(atop.begin_shapes_rec(art.find_layer(*ln["Metal1.nofill"])))).is_empty()
                                      for n in ["Activ.nofill", "GatPoly.nofill", "Metal2.nofill", "Metal3.nofill", "Metal4.nofill", "TopMetal1.nofill"])
    res["nofill"] = nf
    return res


# ---------------------------------------------------------------- DRC / LVS runs
def run(cmd, log):
    with open(log, "w") as f:
        p = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, env=env, cwd=a.work)
    return p.returncode


def parse_rdb(path):
    t = ET.parse(path).getroot()
    cnt = collections.Counter(); dens = {}
    for it in t.iter("item"):
        c = it.findtext("category").strip("'")
        cnt[c] += 1
        txt = " ".join(v.text or "" for v in it.iter("value"))
        m = re.search(r"ratio_percent\s*:\s*([0-9.]+)", txt)
        if m:
            dens[c] = float(m.group(1))
    return dict(cnt), dens


def drc(tag, gds):
    rd = os.path.join(a.work, "drc_" + tag)
    if not a.skip_runs:
        shutil.rmtree(rd, ignore_errors=True)
        run(["python3", TECH + "/drc/run_drc.py", f"--path={gds}", "--topcell=slot_7", f"--run_dir={rd}", "--mp=2", "--antenna"],
            os.path.join(OUT, f"drc_{tag}.log"))
    rdbs = [f for f in os.listdir(rd) if f.endswith(".lyrdb")]
    cnt, dens = {}, {}
    for f in rdbs:
        c, d = parse_rdb(os.path.join(rd, f))
        for k, v in c.items():
            cnt[k] = cnt.get(k, 0) + v
        dens.update(d)
    return {"markers": cnt, "density_ratio_percent": dens, "rdb_files": rdbs}


def lvs(tag, gds):
    rd = os.path.join(a.work, "lvs_" + tag)
    log = os.path.join(OUT, f"lvs_{tag}.log")
    if not a.skip_runs:
        shutil.rmtree(rd, ignore_errors=True)
        run(["python3", TECH + "/lvs/run_lvs.py", f"--layout={gds}", f"--netlist={a.cdl}", "--topcell=slot_7",
             f"--run_dir={rd}", "--run_mode=deep", "--disable_tap_extraction"], log)
    txt = open(log).read()
    g = lambda k: (re.search(r"\|\s*%s\s*\|\s*(.*?)\s*\|" % k, txt) or [None, "?"])[1]
    ext = [f for f in os.listdir(rd) if f.endswith(".cir") or f.endswith(".spice")] if os.path.isdir(rd) else []
    return {"status": g("Status"), "outcome": g("Outcome"), "warnings": g("Warnings"), "errors": g("Errors"), "netlists": ext}


def main():
    rep["xor"] = xor_check()
    rep["clearance"] = clearance()
    rep["drc"] = {"original": drc("base", a.slot), "merged": drc("merged", MERGED)}
    rep["lvs"] = {"original": lvs("base", a.slot), "merged": lvs("merged", MERGED)}
    # LVS netlists identical?
    try:
        def netlist(tag):
            rd = os.path.join(a.work, "lvs_" + tag)
            for f in sorted(os.listdir(rd)):
                if f.endswith("_extracted.cir") or f.endswith(".cir"):
                    return open(os.path.join(rd, f)).read()
        nb, nm = netlist("base"), netlist("merged")
        norm = lambda s: re.sub(r"^\*.*$", "", s, flags=re.M)
        rep["lvs"]["extracted_netlists_identical"] = (norm(nb) == norm(nm)) if nb and nm else None
    except Exception as e:
        rep["lvs"]["extracted_netlists_identical"] = f"not compared: {e}"
    b, mg = rep["drc"]["original"]["markers"], rep["drc"]["merged"]["markers"]
    rep["drc"]["new_rules_violated_by_art"] = sorted(set(mg) - set(b))
    rep["drc"]["marker_count_changes"] = {k: [b.get(k, 0), mg.get(k, 0)] for k in sorted(set(b) | set(mg)) if b.get(k, 0) != mg.get(k, 0)}
    json.dump(rep, open(os.path.join(HERE, "verify_report.json"), "w"), indent=1)

    L = ["# Verification report (generated by verify_art.py)", ""]
    x = rep["xor"]
    L += ["## XOR: merged GDS with the art cell removed vs the original slot_7.gds", "",
          f"- instances of `tughra_art` removed: {x['instances_of_art_cell']}",
          f"- XOR polygons over all {len(x['layers'])} layer/datatypes (flattened): **{x['total_xor_polygons']}**",
          f"- text labels identical: {x['labels_equal']}; cell list identical after removal: {x['cells_after_removal_equal']}", ""]
    L += ["## Clearance of the art to existing shapes (um)", "",
          "| art layer | polygons | area (um2) | overlap with any existing shape on the metals / front end (um2) | closest approach to existing shapes of its own kind (um) | to slot edge |", "|---|---|---|---|---|---|"]
    for Ly, e in rep["clearance"]["layers"].items():
        kinds = ["FEOL"] + pl.METALS
        ov = sum(e[f"vs_{k}"]["overlap_um2"] for k in kinds)
        own = "FEOL" if Ly == pl.POLY else Ly
        same = e[f"vs_{own}"]["touches_within_um"]
        L.append(f"| {Ly} | {e['art_polygons']} | {e['art_area_um2']:.1f} | {ov:.3f} | {'> 60' if same is None else f'{same:.2f}'} (vs {own}) | {e['min_distance_to_slot_edge_um']:.1f} |")
    L += ["", "(Closest approach is found by bisection: the art grown by d first touches existing shapes at d. \"FEOL\" = every front-end layer (Activ, GatPoly, Cont, wells, implants...). Figures against the other layers are in verify_report.json.)", ""]
    nf = rep["clearance"]["nofill"]
    L += ["## No-fill markers", "", "| layer | GDS | boxes | box (um, slot coordinates) |", "|---|---|---|---|"]
    for k, v_ in nf.items():
        if isinstance(v_, dict):
            L.append(f"| {k} | {v_['gds'][0]}/{v_['gds'][1]} | {v_['boxes']} | {v_['box_um']} |")
    L += ["", f"- all art layers lie inside the marker box: {nf['art_inside_nofill_box']}; the seven markers are identical: {nf['all_markers_identical']}", ""]
    L += ["## DRC (PDK run_drc.py, all tables, density and antenna on)", "",
          f"- rules violated by the original slot_7: {sorted(rep['drc']['original']['markers'])}",
          f"- rules violated by the merged GDS: {sorted(rep['drc']['merged']['markers'])}",
          f"- **rules newly violated because of the art: {rep['drc']['new_rules_violated_by_art']}**",
          f"- marker count changes (original, merged): {rep['drc']['marker_count_changes']}", ""]
    L += ["| density rule | original (%) | merged (%) |", "|---|---|---|"]
    dd0, dd1 = rep["drc"]["original"]["density_ratio_percent"], rep["drc"]["merged"]["density_ratio_percent"]
    for k in sorted(set(dd0) | set(dd1)):
        L.append(f"| {k} | {dd0.get(k, '-')} | {dd1.get(k, '-')} |")
    L += ["", "## LVS (PDK run_lvs.py, deep, tap extraction off, against slot7 netlist/slot_7.cdl)", "",
          "| | status | outcome | warnings | errors |", "|---|---|---|---|---|"]
    for k in ("original", "merged"):
        v = rep["lvs"][k]
        L.append(f"| {k} | {v['status']} | {v['outcome']} | {v['warnings']} | {v['errors']} |")
    L += ["", f"Extracted layout netlists identical (comments ignored): {rep['lvs'].get('extracted_netlists_identical')}", ""]
    open(os.path.join(HERE, "verify_report.md"), "w").write("\n".join(L))
    print("\n".join(L))


main()
