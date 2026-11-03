# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""P2's library with the pin labels of tub_p20x1_c2 removed (no geometry change): the generator's placement check
reads every label in the hierarchy and takes the tub's own s / d / g labels for shorts with d2s_inputs_c2's pins.
    python3 strip_tub_labels.py <d2s_p2_cells.gds> <out.gds>"""
import sys
import klayout.db as db
ly = db.Layout()
ly.read(sys.argv[1])
t = ly.cell("tub_p20x1_c2")
for li in ly.layer_indexes():
    if ly.get_info(li).datatype in (2, 25):
        t.shapes(li).clear()
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[2], opt)
