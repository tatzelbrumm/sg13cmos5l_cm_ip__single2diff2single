# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Run IHP's DRC / LVS on a cell and summarise. Agent F, C2 2026-10-31.
  python3 checks.py drc <gds> <cell> <run_dir>          run_drc.py --no_density --mp=4; counts per rule from every
                                                        .lyrdb; flags 'generated an exception' in the log
  python3 checks.py lvs <gds> <cdl> <cell> <run_dir> [implicit]   run_lvs.py --disable_tap_extraction"""
import glob
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

T = "/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech"


def drc(gds, cell, d):
    import shutil; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    cmd = ["python3", T + "/drc/run_drc.py", "--path=" + gds, "--topcell=" + cell, "--no_density", "--mp=4",
           "--run_dir=" + d]
    p = subprocess.run(cmd, capture_output=True, text=True)
    log = p.stdout + p.stderr
    open(os.path.join(d, "run.log"), "w").write(log)
    exc = [l for l in log.splitlines() if "exception" in l.lower()]
    counts = {}
    for f in glob.glob(os.path.join(d, "*.lyrdb")):
        root = ET.parse(f).getroot()
        for it in root.iter("item"):
            c = it.find("category").text.strip("'")
            counts[c] = counts.get(c, 0) + 1
    print("DRC %s: %d violations %s; exceptions in log: %d; lyrdb files: %d"
          % (cell, sum(counts.values()), counts or "", len(exc), len(glob.glob(os.path.join(d, "*.lyrdb")))))
    for l in exc[:5]:
        print("   ", l)
    return counts, exc


def lvs(gds, cdl, cell, d, implicit=False):
    import shutil; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    cmd = ["python3", T + "/lvs/run_lvs.py", "--layout=" + gds, "--netlist=" + cdl, "--topcell=" + cell,
           "--run_dir=" + d, "--disable_tap_extraction"]
    if implicit:
        cmd.append("--implicit_nets=*")
    p = subprocess.run(cmd, capture_output=True, text=True)
    log = p.stdout + p.stderr
    open(os.path.join(d, "run.log"), "w").write(log)
    ok = "Congratulations" in log or "MATCH" in log and "MISMATCH" not in log
    tail = [l for l in log.splitlines() if "match" in l.lower() or "error" in l.lower()][-4:]
    print("LVS %s: %s" % (cell, "MATCH" if ok else "NOT MATCHED"))
    for l in tail:
        print("   ", l.strip()[:200])
    return ok


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "drc":
        drc(*a[1:4])
    else:
        lvs(a[1], a[2], a[3], a[4], len(a) > 5)
