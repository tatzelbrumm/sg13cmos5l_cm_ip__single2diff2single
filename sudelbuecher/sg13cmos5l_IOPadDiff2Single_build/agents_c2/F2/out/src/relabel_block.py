# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 stage B2: rename the leaf cells' local supply texts inside the routed d2s_block to the pad-level nets.
    python3 relabel_block.py <d2s_block.gds>        (in place)

In the pad, the 1.2 V ring rails carry the texts vdd / vss; d2s_mpdda_pd's local names vdd / vddo (= iovdd) and
vss / vsso (= iovss) must not reach the pad's flat netlist as well (magic's extraction may join same-named texts).
Inside the block: vdd, vddo -> iovdd; vss -> iovss; vsso dropped (SB's source keeps the pwr_f2 text iovss_o, its own
path to the P frame's p+ ring; it is not iovss inside the block). The cell libraries in cells/ keep their own texts
for the cells' standalone LVS; only the copies inside d2s_block change. Runs after route_block.py (the router finds
the cells' supply pins by these texts)."""
import sys

import klayout.db as db

RENAME = {"vdd": "iovdd", "vddo": "iovdd", "vss": "iovss", "vsso": None}
ly = db.Layout()
ly.read(sys.argv[1])
n = {k: 0 for k in RENAME}
for c in ly.each_cell():
    for li in ly.layer_indexes():
        for s in list(c.shapes(li).each()):
            if s.is_text() and s.text_string in RENAME:
                new = RENAME[s.text_string]
                n[s.text_string] += 1
                if new is None:
                    c.shapes(li).erase(s)
                else:
                    t = s.text
                    t.string = new
                    s.text = t
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[1], opt)
print("relabel_block:", ", ".join("%s %d" % kv for kv in n.items()))
