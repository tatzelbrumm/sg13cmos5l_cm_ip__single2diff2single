import klayout.db as db, sys
A="/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent"
ly=db.Layout(); ly.read(A+"/inputs/pad_buffer_cells.gds")
cell=ly.cell(sys.argv[1]); L=tuple(int(x) for x in sys.argv[2].split("/"))
rec = len(sys.argv)>3 and sys.argv[3]=="rec"
win = db.DBox(*[float(v) for v in sys.argv[4].split(",")]) if len(sys.argv)>4 else None
li=ly.find_layer(*L)
r = db.Region(cell.begin_shapes_rec(li)) if rec else db.Region(cell.shapes(li))
r.merge()
for p in r.each():
    b=p.bbox().to_dtype(ly.dbu)
    if win and not b.overlaps(win): continue
    print(("rect " if p.is_box() else "poly ")+str(b), "" if p.is_box() else p.to_dtype(ly.dbu))
