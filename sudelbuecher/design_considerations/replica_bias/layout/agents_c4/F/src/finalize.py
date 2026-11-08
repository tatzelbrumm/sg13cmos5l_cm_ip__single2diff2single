# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): the routed block -> out/pad_ref_rb.gds.
    python3 finalize.py <routed.gds> <out.gds> <rb_place.py>
- the straps of rb_place.STRAPS (Metal2): rb_casc's vdd (its band's vdd track and the three dummy tracks tied to it)
  joins the vddh rail by one strap of the track's own width at the pin's height. A router landing there had filled
  the gaps between those tracks (same net) into a plate wider than Mn.e_w next to vbnc (M2.e); so rb_casc's vdd is
  not routed, the strap's area is a Metal2 keep-out for the router, and the strap is drawn here;
- the rows' local supply texts become the macro's pin names (vdd -> vddh, vss -> vssh), so that one net carries one
  name in the flat extraction;
- cells not under pad_ref_rb are dropped; the top cell keeps its port pins (Metal2 10/2 + 10/25) and frame_f's rails."""
import sys

import klayout.db as db

ly = db.Layout()
ly.read(sys.argv[1])
top = ly.cell('pad_ref_rb')
keep = {top.cell_index()} | set(top.called_cells())
for c in [c for c in ly.each_cell() if c.cell_index() not in keep]:
    ly.delete_cell(c.cell_index())
g = {}
exec(open(sys.argv[3]).read(), g)
for b in g['STRAPS']:
    top.shapes(ly.layer(10, 0)).insert(db.DBox(*b))
REN = {'vdd': 'vddh', 'vss': 'vssh'}
n = 0
for c in ly.each_cell():
    for li in ly.layer_indexes():
        for s in c.shapes(li).each():
            if s.is_text() and s.text_string in REN:
                s.text_string = REN[s.text_string]
                n += 1
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(sys.argv[2], opt)
print('texts renamed: %d; cells: %s' % (n, sorted(c.name for c in ly.each_cell())))
