import sys
sys.path += ['/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/python','/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/python/pycell4klayout-api/source/python']
import pya, sg13cmos5l_pycell_lib
ly=pya.Layout(); ly.technology_name="sg13cmos5l"
for w,l,ng in [(5,6,1),(1,0.45,1),(20,1,2)]:
    c=ly.create_cell("pmosHV","SG13_dev",{"w":"%gu"%w,"l":"%gu"%l,"ng":str(ng)})
    print("==",w,l,ng,c.dbbox())
    for li in ly.layer_indexes():
        inf=ly.get_info(li)
        r=pya.Region(c.begin_shapes_rec(li)).merged()
        if r.is_empty():
            for s in c.shapes(li).each():
                if s.is_text(): print(inf, 'text', s.text_string, s.dtext.trans)
            continue
        bs=[p.bbox().to_dtype(ly.dbu) for p in r.each()]
        print(inf, len(bs), bs[:4])
    cc=pya.Region(c.begin_shapes_rec(ly.layer(6,0)))
    print('contacts', [b.to_dtype(ly.dbu) for b in [p.bbox() for p in cc.each()]][:6])
