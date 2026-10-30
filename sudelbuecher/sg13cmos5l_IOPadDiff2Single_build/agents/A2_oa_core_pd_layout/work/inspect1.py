import klayout.db as db, sys
A="/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent"
ly=db.Layout(); ly.read(A+"/inputs/pad_buffer_cells.gds")
print("dbu",ly.dbu,"cells",ly.cells(),"tops",[c.name for c in ly.top_cells()])
names=["oa_pmir","oa_pcas","oa_nmir","oa_mcs","oa_misc_n","oa_misc_p","fit_bias_tree_oa_bg"]
def tree(c,ind=0,maxd=3):
    print("  "*ind+c.name, c.dbbox())
    if ind>=maxd: return
    seen={}
    for inst in c.each_inst():
        k=inst.cell.name; seen.setdefault(k,[]).append(inst)
    for k,v in seen.items():
        i=v[0]
        print("  "*(ind+1)+"%dx %s trans=%s arr=%s"%(len(v),k,[str(x.dcplx_trans) for x in v][:4], (i.na,i.nb) if i.is_regular_array() else ""))
        if ind+1<maxd: tree(i.cell,ind+2,maxd)
for n in names:
    c=ly.cell(n)
    if c is None: print("MISSING",n); continue
    tree(c,0,2)
    print()
