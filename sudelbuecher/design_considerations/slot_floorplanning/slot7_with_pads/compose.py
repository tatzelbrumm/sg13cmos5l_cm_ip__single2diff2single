# Compose slot_7 (sg13cmos5l_cm_slot7 main) with the two custom pads at their harness positions and render PNGs.
import klayout.db as db, klayout.lay as lay, sys
S = sys.argv[1]
top_ly = db.Layout(); top_ly.dbu = 0.001
top = top_ly.create_cell('slot7_with_pads')
def place(path, cell, trans):
    src = db.Layout(); src.read(path)
    c = [x for x in src.top_cells() if x.name == cell][0]
    new = top_ly.create_cell(cell)
    new.copy_tree(c)                       # copies the hierarchy; clashing sub-cell names get unique names
    top.insert(db.DCellInstArray(new.cell_index(), trans))
# chip coordinates (um): slot_7 at its wrapper position; pads per magic/sg13cmos5l_padframe.mag (delivery-test),
# transform "0 -1 416000 1 0 452000/474000" at magscale 0.005 um = R90, plus the frame offset 16.1 um
place(f'{S}/slot_7.gds', 'slot_7', db.DCplxTrans(1, 0, False, 1379.95, 2170.05))
place(f'{S}/sg13cmos5l_IOPadSingle2Diff.gds', 'sg13cmos5l_IOPadSingle2Diff', db.DCplxTrans(1, 90, False, 2096.1, 2276.1))
place(f'{S}/sg13cmos5l_IOPadDiff2Single.gds', 'sg13cmos5l_IOPadDiff2Single', db.DCplxTrans(1, 90, False, 2096.1, 2386.1))
top_ly.write(f'{S}/slot7_with_pads.gds')
print('bbox', top.dbbox())
def render(fname, box, w, h):
    v = lay.LayoutView(); v.load_layout(f'{S}/slot7_with_pads.gds', True)
    v.load_layer_props('/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/sg13cmos5l.lyp')
    v.max_hier(); v.set_config('background-color', '#ffffff'); v.set_config('grid-visible', 'false')
    v.set_config('text-visible', 'false')
    v.zoom_box(box); v.save_image(f'{S}/{fname}', w, h); print('wrote', fname)
render('slot7_with_pads.png', top.dbbox(), 2400, 1000)
render('slot7_pad_interface.png', db.DBox(1880, 2255, 1960, 2465), 900, 2100)
