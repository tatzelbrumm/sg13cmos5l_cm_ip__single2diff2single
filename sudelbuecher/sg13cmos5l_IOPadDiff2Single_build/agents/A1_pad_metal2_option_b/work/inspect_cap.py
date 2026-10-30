import klayout.db as db, sys
ly = db.Layout(); ly.read(sys.argv[1])
for name in ('d2s_cma','d2s_cmb'):
    c = ly.cell(name)
    print('=== ', name, c.dbbox(), 'children', [ly.cell(i.cell_index).name for i in c.each_inst()])
    cf = ly.cell(ly.add_cell(name+'_flat')); cf.copy_tree(c); cf.flatten(-1, True)
    for li in ly.layer_indexes():
        sh = cf.shapes(li)
        if sh.size() == 0: continue
        info = ly.get_info(li)
        items = []
        for s in sh.each():
            if s.is_text(): items.append(('T', s.text_string, round(s.dtext.x,3), round(s.dtext.y,3)))
            else:
                items.append(s.dbbox() if s.is_box() else ('poly', s.dpolygon.to_s()))
        if len(items) > 12:
            r = db.Region(sh).merged()
            print('  %-7s n=%d merged=%d bbox=%s' % (info.to_s(), len(items), r.count(), r.bbox().to_dtype(ly.dbu)))
            for p in list(r.each())[:6]: print('       ', p.to_dtype(ly.dbu))
        else:
            print('  %-7s' % info.to_s(), items)
