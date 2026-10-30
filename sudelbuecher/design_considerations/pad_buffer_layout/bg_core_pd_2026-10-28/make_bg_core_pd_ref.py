# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Reference netlist (CDL) of the assembled bg_core_pd for LVS, composed from the primitives' own netlists
(generator.compose_reference: MOS, R and Q lines; the PMOS cells' internal bulk nw tied to vdd by the merged well).
Written 2026-10-28 by Claude (Opus 5.5).

    python3 make_bg_core_pd_ref.py configs/bg_core_pd.py bg_core_pd_ref.cdl
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import generator as G  # noqa: E402

cfg = G.load_config(sys.argv[1])
ports = ["vdd", "vss", "iout", "en_3v3", "en_3v3_b"]          # port order of the hand netlist (bias_ref_pd.spice)
txt = G.compose_reference(cfg["NAME"], ports, cfg["INSTANCES"], cfg["CDLS"], ties=cfg.get("TIES"))
hdr = ("* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
       "* %s reference for LVS, composed from the primitives' netlists by make_bg_core_pd_ref.py (Claude, "
       "2026-10-28)\n* sources: %s\n" % (cfg["NAME"], ", ".join(os.path.basename(f) for f in cfg["CDLS"])))
open(sys.argv[2], "w").write(hdr + txt)
print("%s: %d device lines" % (sys.argv[2], sum(1 for l in txt.splitlines() if l[:1] in "MRQ")))
