# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""P's library with the pin labels of tub_p20x1_c3 removed (labels only, no geometry; as C2 F2): the router's
placement check reads every label in the hierarchy and would take the tub's own d / g / s labels for shorts with
s2d_inputs_c3's pins.   python3 strip_tub_labels.py <s2d_p3_cells.gds> <out.gds>"""
import sys
import klayout.db as db
ly = db.Layout()
ly.read(sys.argv[1])
t = ly.cell('tub_p20x1_c3')
for li in ly.layer_indexes():
    if ly.get_info(li).datatype in (2, 25):
        t.shapes(li).clear()
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[2], opt)
