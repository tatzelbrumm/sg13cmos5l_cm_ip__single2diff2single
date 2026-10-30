import klayout.db as db, sys
ly = db.Layout(); ly.read(sys.argv[1]); t = ly.top_cell()
for l in ((1,0),(8,0),(31,0)):
    li = ly.find_layer(*l)
    for s in t.shapes(li).each():
        p = s.dpolygon if not s.is_box() else db.DPolygon(s.dbox)
        print(l, 'holes', p.holes(), 'pts', [ (round(q.x,3), round(q.y,3)) for q in p.each_point_hull()])
        for h in range(p.holes()):
            print('   hole', [ (round(q.x,3), round(q.y,3)) for q in p.each_point_hole(h)])
# Metal3 rails
for name in ('Metal3ViasUp','TopLayersTo4'):
    c = ly.cell(name)
    for l in ((30,0),(30,2),(30,25),(50,0),(126,0),(126,25),(50,25)):
        li = ly.find_layer(*l)
        if li is None: continue
        for s in c.shapes(li).each():
            print(name, l, s.dbox if s.is_box() else (s.dpolygon if not s.is_text() else (s.text_string, s.dtext.x, s.dtext.y)))
