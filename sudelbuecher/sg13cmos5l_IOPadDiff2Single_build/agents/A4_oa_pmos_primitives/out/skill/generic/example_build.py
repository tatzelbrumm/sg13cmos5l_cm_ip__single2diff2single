# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""example_build.py: build every score of patterns.md with one process adapter, no library needed (devices drawn by
the adapter), and write <out>.gds + <out>.cdl. 2026-10-28, Claude.

    python3 example_build.py <adapter.py> <out_basename> [patterns.md]
    e.g. python3 example_build.py ../ihp_sg13cmos5l/adapter.py /tmp/x
"""
import os
import sys
import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generator as G   # noqa: E402

if __name__ == "__main__":
    P = G.load_adapter(sys.argv[1])
    out = sys.argv[2]
    pat = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "patterns.md")
    ly = db.Layout()
    ly.dbu = G.DBU
    txt = []
    for s in G.parse_scores(open(pat).read()):
        cell, devs, info = G.build(ly, P, s)
        pins = sorted(set([d[1] for d in devs] + [d[2] for d in devs] + [d[3] for d in devs]) -
                      set(n for d in devs for n in (d[1], d[3]) if n.startswith(s.get("inner", "#")[:2])) -
                      {s.get("bulk", "")})
        txt.append(G.cdl(s["name"], pins, devs))
        b = [v * G.DBU for v in info["bbox"]]
        print("%-10s %.3f x %.3f um" % (s["name"], b[2] - b[0], b[3] - b[1]))
    o = db.SaveLayoutOptions()
    o.write_context_info = False
    o.gds2_write_timestamps = False
    ly.write(out + ".gds", o)
    open(out + ".cdl", "w").write("\n".join(txt))
