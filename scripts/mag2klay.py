#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""mag2klay.py -- Magic layouts of the chipalooza analog switches -> KLayout editing sources (<cell>.klay.gds).

    python3 -I scripts/mag2klay.py --harness ~/EDA/sg13cmos5l_ocd_chipalooza --out macros/ocd_analog_switches/layout/klayout

Steps (this is what produced the files, 2026-11-03):
  1. For each cell, Magic (batch mode, the IHP magicrc of the PDK) loads the .mag from the harness checkout with the same search
     paths as the harness's own run_extract_*.sh (`paramcells`, `../../../magic/sg13cmos5l_stdcell`) and runs `gds write`.
  2. The standard cells (sg13cmos5l_inv_4, _antennanp, _decap_4) are vendor-cell stubs in the harness checkout: Magic cannot copy
     them from the PDK GDS in every setup and then writes its own stub geometry.  They are replaced here by the cells of
     $PDK_ROOT/$PDK/libs.ref/sg13cmos5l_stdcell/gds/sg13cmos5l_stdcell.gds (shapes copied by GDS layer/datatype).
  3. KLayout (python module `klayout`) writes <cell>.klay.gds; the top cell name equals the file name.
Needs: magic (>= 8.3.600), `pip install klayout`, an IHP PDK (PDK_ROOT, PDK=ihp-sg13cmos5l) or --magicrc / --stdcell-gds.
Nothing is written into the harness checkout.
"""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import klayout.db as db

CELLS = [  # (cell, directory of the .mag relative to the harness checkout)
    ("analog_switch_small", "dependencies/sg13cmos5l_ocd_ip__analog_switches/magic"),
    ("analog_switch_med", "dependencies/sg13cmos5l_ocd_ip__analog_switches/magic"),
    ("analog_pswitch_small", "dependencies/sg13cmos5l_ocd_ip__analog_switches/magic"),
    ("sw_lvl_shift", "dependencies/sg13cmos5l_ocd_ip__analog_switches/magic"),
    ("gate_drive_med", "dependencies/sg13cmos5l_ocd_ip__analog_switches/magic"),
    ("xgate", "dependencies/sg13cmos5l_ocd_ip__biasgen/magic"),
]
STD = ("sg13cmos5l_inv_4", "sg13cmos5l_antennanp", "sg13cmos5l_decap_4")


def run_magic(magic, rc, cwd, cell, out_gds, harness):
    tcl = (f"addpath paramcells\naddpath sg13cmos5l_stdcell\naddpath {harness}/magic/sg13cmos5l_stdcell\n"
           f"load {cell}\nselect top cell\ngds write {out_gds}\nquit -noprompt\n")
    r = subprocess.run([magic, "-dnull", "-noconsole", "-rcfile", str(rc)], input=tcl, text=True, cwd=cwd,
                       capture_output=True, timeout=600)
    log = r.stdout + r.stderr
    bad = [l for l in log.splitlines() if l.startswith("Calma output error") and "vendor" not in l and "Structure name" not in l]
    return log, bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--harness", required=True, help="checkout of sg13cmos5l_ocd_chipalooza")
    ap.add_argument("--out", required=True, help="output folder for <cell>.klay.gds")
    ap.add_argument("--magic", default="magic")
    ap.add_argument("--magicrc", help="default: $PDK_ROOT/$PDK/libs.tech/magic/ihp-sg13cmos5l.magicrc")
    ap.add_argument("--stdcell-gds", help="default: $PDK_ROOT/$PDK/libs.ref/sg13cmos5l_stdcell/gds/sg13cmos5l_stdcell.gds")
    a = ap.parse_args()
    pdk = Path(os.environ.get("PDK_ROOT", "")) / os.environ.get("PDK", "ihp-sg13cmos5l")
    rc = Path(a.magicrc) if a.magicrc else pdk / "libs.tech/magic/ihp-sg13cmos5l.magicrc"
    stdgds = Path(a.stdcell_gds) if a.stdcell_gds else pdk / "libs.ref/sg13cmos5l_stdcell/gds/sg13cmos5l_stdcell.gds"
    harness, out = Path(a.harness).resolve(), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    std = db.Layout()
    std.read(str(stdgds))
    ok = True
    for cell, rel in CELLS:
        with tempfile.TemporaryDirectory() as tmp:
            tmpgds = Path(tmp) / f"{cell}.gds"
            log, bad = run_magic(a.magic, rc, harness / rel, cell, tmpgds, harness)
            if not tmpgds.exists() or bad:
                print(f"FAIL {cell}: Magic output missing or errors: {bad[:3]}")
                ok = False
                continue
            L = db.Layout()
            L.read(str(tmpgds))
            tops = [c.name for c in L.top_cells()]
            if tops != [cell]:
                print(f"FAIL {cell}: top cells {tops}")
                ok = False
                continue
            lm = db.LayerMapping()
            lm.create_full(L, std)
            replaced = []
            for n in STD:
                if L.has_cell(n):
                    tc, sc = L.cell(n), std.cell(n)
                    assert sc.child_cells() == 0, f"{n}: PDK cell has children"
                    tc.clear()
                    tc.copy_shapes(sc, lm)
                    replaced.append(n)
            L.write(str(out / f"{cell}.klay.gds"))
            print(f"OK   {cell}: {L.cells()} cells, std cells replaced from the PDK: {replaced or 'none'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
