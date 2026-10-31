import os, sys
pdk = "/foss/pdks/ihp-sg13cmos5l"
sys.path += [pdk + "/libs.tech/klayout/python", pdk + "/libs.tech/klayout/python/pycell4klayout-api/source/python"]
import pya
import sg13cmos5l_pycell_lib
ly = pya.Layout(); ly.dbu = 0.001; ly.technology_name = "sg13cmos5l"
for kind, par in [("nmosHV", dict(w="6u", l="6u", ng="1")), ("nmosHV", dict(w="15u", l="3u", ng="1")), ("nmosHV", dict(w="4.4u", l="1u", ng="1")),("nmosHV", dict(w="1u", l="0.45u", ng="1")),("nmosHV", dict(w="1u", l="8u", ng="1")),("nmosHV", dict(w="2u", l="6u", ng="1")),("ptap1", dict(w="10u", l="0.78u")), ("rhigh", dict(w="0.5u", l="12.65u", b="0"))]:
    c = ly.create_cell(kind, "SG13_dev", par)
    print(kind, par, c.name, c.dbbox())
    for li in ly.layer_indexes():
        r = pya.Region(c.begin_shapes_rec(li)).merged()
        if r.is_empty() and c.shapes(li).is_empty(): continue
        info = ly.get_info(li)
        polys = [p.bbox().to_dtype(0.001) for p in r.each()]
        txt = [s.text_string for s in c.shapes(li).each() if s.is_text()]
        print("  ", info, len(polys), polys[:4], txt[:4])
