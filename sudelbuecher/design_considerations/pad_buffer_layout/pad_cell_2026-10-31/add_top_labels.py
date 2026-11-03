# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Add the pad cell's port labels to its top cell (texts only; no geometry changes). C2, phase 4.

python3 add_top_labels.py <in.gds> <out.gds>

Why: the macro's LVS targets (sak-lvs.sh: run_lvs.py --run_mode=deep, flag_missing_ports; magic + netgen) take the
ports from labels in the top cell. In F2's pad candidate the core pins are labelled only inside `d2s_block` and the
ring rails only inside IHP's rail cells, so LVS saw no top-level iovdd / iovss / vdd / vss and named the core pins
`$24.<pin>`. The texts below sit on shapes of the same net in the same place as the existing sub-cell labels (core pins:
Metal2 pin boxes at the top edge; rails: Metal3 rail centers, x = 40).
"""
import sys
import klayout.db as db

LABELS = [  # (text, layer, datatype, x, y) in µm
    ('iovdd', 30, 25, 40.0, 78.75),   # Metal3 iovdd rail 66–91.5
    ('iovss', 30, 25, 40.0, 47.25),   # Metal3 iovss rail 34.5–60
    ('vss', 30, 25, 40.0, 149.0),     # Metal3 vss rail 140–158 (1.2 V ring)
    ('vdd', 30, 25, 40.0, 169.0),     # Metal3 vdd rail 160–178 (1.2 V ring)
    ('vinp', 10, 25, 6.205, 179.715), ('vinn', 10, 25, 6.745, 179.715), ('vref', 10, 25, 7.285, 179.715),
    ('iref', 10, 25, 44.545, 179.715), ('en_3v3_b', 10, 25, 45.085, 179.715), ('en_3v3', 10, 25, 45.625, 179.715),
]

if __name__ == '__main__':
    src, dst = sys.argv[1:3]
    ly = db.Layout()
    ly.read(src)
    top = ly.top_cell()
    have = {s.text.string for li in ly.layer_indexes() for s in top.shapes(li).each() if s.is_text()}
    for name, l, d, x, y in LABELS:
        if name not in have:
            top.shapes(ly.layer(l, d)).insert(db.DText(name, db.DTrans(x, y)))
    opt = db.SaveLayoutOptions()
    opt.write_context_info = True
    ly.write(dst, opt)
    print('top-cell texts:', sorted({s.text.string for li in ly.layer_indexes() for s in top.shapes(li).each() if s.is_text()}))
