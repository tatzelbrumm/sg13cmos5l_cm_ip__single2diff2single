# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Render tree_nmos.gds to tree_nmos.png with the PDK layer properties (2026-11-07, Claude Opus 5.5).
python3 render_tree_nmos.py [gds] [png]"""
import os
import sys
import klayout.lay as lay

here = os.path.dirname(os.path.abspath(__file__))
gds = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "tree_nmos.gds")
png = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "tree_nmos.png")
lyp = os.path.join(os.environ.get("PDK_ROOT", "/foss/pdks"), os.environ.get("PDK", "ihp-sg13cmos5l"),
                   "libs.tech/klayout/tech/sg13cmos5l.lyp")
v = lay.LayoutView()
v.set_config("background-color", "#ffffff")
v.set_config("grid-visible", "false")
v.set_config("text-font", "1")
v.load_layout(gds, True)
v.load_layer_props(lyp)
v.max_hier()
hide = {(51, 0), (5, 2), (8, 2), (44, 0)}            # HeatTrans, PCell pin layers, ThickGateOx (covers all)
it = v.begin_layers()
while not it.at_end():
    p = it.current()
    if (p.source_layer, p.source_datatype) in hide:
        p.visible = False
        v.set_layer_properties(it, p)
    it.next()
v.zoom_fit()
v.save_image(png, 3000, 1000)
print("wrote", png)
