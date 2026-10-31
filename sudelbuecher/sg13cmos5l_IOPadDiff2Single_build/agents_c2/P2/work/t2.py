import sys
sys.path += ['/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/python','/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/python/pycell4klayout-api/source/python']
import pya, sg13cmos5l_pycell_lib
ly=pya.Layout(); ly.technology_name="sg13cmos5l"
c=ly.create_cell("ntap1","SG13_dev",{"w":"3u","l":"0.3u"})
print(c.dbbox())
for li in ly.layer_indexes():
    r=pya.Region(c.begin_shapes_rec(li))
    t=[s.text_string for s in c.shapes(li).each() if s.is_text()]
    if not r.is_empty() or t: print(ly.get_info(li), [p.bbox().to_dtype(ly.dbu) for p in r.each()][:3], r.count(), t)
