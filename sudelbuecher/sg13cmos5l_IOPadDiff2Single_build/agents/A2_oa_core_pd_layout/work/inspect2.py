import klayout.db as db, sys, collections
A="/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent"
ly=db.Layout(); ly.read(A+"/inputs/pad_buffer_cells.gds")
names=sys.argv[1:] or ["oa_pmir","oa_pcas","oa_nmir","oa_mcs","oa_misc_n","oa_misc_p"]
for n in names:
    c=ly.cell(n)
    print("=====",n,c.dbbox())
    for li in ly.layer_indexes():
        info=ly.get_info(li)
        it=c.begin_shapes_rec(li)
        txt=[]
        while not it.at_end():
            s=it.shape()
            if s.is_text():
                t=s.text.transformed(it.trans())
                txt.append("%s@(%.3f,%.3f)%s"%(t.string, t.x*ly.dbu, t.y*ly.dbu, "" if it.cell().name==n else "["+it.cell().name+"]"))
            it.next()
        if txt: print("  texts %d/%d (%d):"%(info.layer,info.datatype,len(txt)), " ".join(txt[:80]))
    # pin boxes on 8/2 and 10/2 at top level of the cell
    for L in [(8,2),(10,2)]:
        li=ly.find_layer(*L)
        if li is None: continue
        bx=[]
        for s in c.shapes(li).each():
            if s.is_box() or s.is_polygon(): bx.append(str(s.dbbox()))
        if bx: print("  pinboxes %s at cell level (%d):"%(L,len(bx))," ".join(bx[:40]))
