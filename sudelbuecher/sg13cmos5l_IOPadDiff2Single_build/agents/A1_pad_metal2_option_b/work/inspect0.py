import klayout.db as db, sys
ly = db.Layout(); ly.read(sys.argv[1]); t = ly.top_cell()
print('top', t.name, 'dbu', ly.dbu, 'bbox', t.dbbox())
for c in ly.each_cell():
    print('cell %-28s pcellvar=%s lib=%s ninst=%d parents=%d bbox=%s' % (c.name, c.is_pcell_variant(), c.is_library_cell(), c.child_instances(), c.parent_cells(), c.dbbox()))
print('--- top-level shapes per layer')
for li in ly.layer_indexes():
    sh = t.shapes(li)
    if sh.size():
        info = ly.get_info(li)
        n = sh.size(); bb = db.Region(sh).bbox().to_dtype(ly.dbu)
        texts = [s.text_string for s in sh.each() if s.is_text()]
        print('%-8s n=%5d bbox=%s texts=%s' % (info.to_s(), n, bb, texts[:20]))
for name in ('contacts','Metal3ViasUp','TopLayersTo4'):
    c = ly.cell(name)
    print('--- cell', name)
    for li in ly.layer_indexes():
        sh = c.shapes(li)
        if sh.size():
            print('   %-8s n=%5d bbox=%s' % (ly.get_info(li).to_s(), sh.size(), db.Region(sh).bbox().to_dtype(ly.dbu)))
