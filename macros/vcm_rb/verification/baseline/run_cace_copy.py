# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Run a pad's CACE suite with changed default conditions, without changing the pad macro.

Writes a temporary copy of the pad's yaml (_rb_<tag>.yaml, default_conditions changed by --set) into the pad's
verification/cace/, runs `cace <copy> -s schematic -p <group> -j N` per group with the macro library path the pad
Makefile's sim-cace exports, copies CACE's summary.md and a CSV per group (scripts/cace/cace_to_csv.py; for collated
Monte Carlo groups, every run's .data line) to --out, and deletes the copy, _runs, _docs and netlist again.

usage (repo root env: export PDK_ROOT=/foss/pdks; source .designinit):
  python3 -I run_cace_copy.py --pad sg13cmos5l_IOPadDiff2Single --yaml sg13cmos5l_IOPadDiff2Single.yaml \
      --set vref=1.2 vicm=1.2 vterm=1.2 --groups dc_params ac_params --tag d2s_1v2 --out <dir> [-j 4]
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

ap = argparse.ArgumentParser()
ap.add_argument("--pad", required=True)
ap.add_argument("--yaml", required=True)
ap.add_argument("--set", nargs="*", default=[])
ap.add_argument("--groups", nargs="+", required=True)
ap.add_argument("--tag", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("-j", type=int, default=4)
a = ap.parse_args()

repo = Path(__file__).resolve().parents[4]
cdir = repo / "macros" / a.pad / "verification" / "cace"
out = Path(a.out).resolve()
out.mkdir(parents=True, exist_ok=True)
y = yaml.safe_load(open(cdir / a.yaml))
for kv in a.set:
    k, v = kv.split("=")
    y["default_conditions"][k]["typical"] = float(v)
copy = cdir / f"_rb_{a.tag}.yaml"
yaml.safe_dump(y, open(copy, "w"), sort_keys=False)

# the macro library path, as the pad Makefile's sim-cace makes it
xlp = cdir / ".xschem_library_path"
subprocess.run(["xschem", "-x", "-q", "-r", "--rcfile", str(cdir / "../../schematic/xschem/xschemrc"), "--command",
                f"set fp [open {xlp} w]; puts $fp $XSCHEM_LIBRARY_PATH; close $fp"], cwd=cdir,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
paths = [p for p in xlp.read_text().strip().split(":") if "/macros/" in p and f"/macros/{a.pad}/" not in p]
env = dict(os.environ, XSCHEM_USER_LIBRARY_PATH=":".join(paths))
log = open(out / f"cace_{a.tag}.log", "a")
status = 0
for g in a.groups:
    shutil.rmtree(cdir / "_runs", ignore_errors=True)
    t0 = time.time()
    r = subprocess.run(["cace", copy.name, "-s", "schematic", "-p", g, "-j", str(a.j), "--no-progress-bar"], cwd=cdir,
                       env=env, stdout=log, stderr=subprocess.STDOUT)
    dt = time.time() - t0
    runs = sorted(glob.glob(str(cdir / "_runs" / "RUN_*")))
    if runs:
        shutil.copy(Path(runs[-1]) / "summary.md", out / f"summary_{g}.md")
        if "collate" in y["parameters"][g]["tool"]["ngspice"]:
            names = y["parameters"][g]["tool"]["ngspice"]["variables"]
            rows = []
            for f in sorted(glob.glob(str(Path(runs[-1]) / "parameters" / g / "**" / "*.data"), recursive=True)):
                for line in open(f):
                    if line.strip():
                        rows.append(line.split())
            with open(out / f"{g}.csv", "w") as f:
                f.write(",".join(str(n) for n in names) + "\n")
                for row in rows:
                    f.write(",".join(row) + "\n")
            print(f"{g}: collated, {len(rows)} data lines -> {out / (g + '.csv')}")
        else:
            rc = subprocess.run([sys.executable, str(repo / "scripts/cace/cace_to_csv.py"), copy.name, g, runs[-1],
                                 str(out / f"{g}.csv")], cwd=cdir)
            status |= rc.returncode
    print(f"{g}: cace exit {r.returncode}, {dt:.0f} s", flush=True)
    status |= r.returncode
for d in ("_runs", "_docs", "netlist"):
    shutil.rmtree(cdir / d, ignore_errors=True)
for f in (copy, xlp):
    f.unlink(missing_ok=True)
sys.exit(status)
