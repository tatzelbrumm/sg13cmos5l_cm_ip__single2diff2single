# instantiate PDK PCells and print their bounding boxes and gate (GatPoly and Activ) area
import sys; sys.path[:0] = ["/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/python", "/foss/pdks/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/python/pycell4klayout-api/source/python", "/foss/pdks/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/python"]; import sg13cmos5l_pycell_lib
import pya
lib = [pya.Library.library_by_id(i) for i in pya.Library.library_ids() if pya.Library.library_by_id(i).name()=="SG13_dev"][0]; print(lib.technology)
print("lib", lib, [n for n in (lib.layout().pcell_names() if lib else [])])
ly = pya.Layout(); ly.dbu = 0.001; ly.technology_name = lib.technology
top = ly.create_cell("T")
def make(name, params):
    pcd = lib.layout().pcell_declaration(name)
    if pcd is None: print(name, "not registered"); return
    pc = ly.cell(ly.add_pcell_variant(lib, pcd.id(), params))
    if pc is None: print(name, "not available"); return
    bb = pc.dbbox()
    gp = pya.Region(pc.begin_shapes_rec(ly.layer(5,0)))
    ac = pya.Region(pc.begin_shapes_rec(ly.layer(1,0)))
    gate = (gp & ac).area()*ly.dbu**2
    print(name, params, "bbox %.3f x %.3f = %.1f um2, GatPoly*Activ %.2f um2" % (bb.width(), bb.height(), bb.width()*bb.height(), gate))
make("SVaricap", {"w":"3.74u","l":"0.3u","Nx":1})  # first call primes the callbacks (fails once)
make("SVaricap", {"w":"9.74u","l":"0.8u","Nx":10})
make("SVaricap", {"w":"3.74u","l":"0.3u","Nx":10})
make("pmosHV", {"w":"7.96u","l":"32.16u","ng":1})
make("SVaricap", {"w":"9.74u","l":"0.8u","Nx":1})
make("SVaricap", {"w":"9.74u","l":"0.8u","Nx":5})
make("cap_cmomf", {"w":"20u","l":"20u","mmin":1,"mmax":2})
make("cap_cmomi", {"w":"20u","l":"20u","mmin":1,"mmax":2})
make("moscap_p", {"w":"10u","l":"10u"})
