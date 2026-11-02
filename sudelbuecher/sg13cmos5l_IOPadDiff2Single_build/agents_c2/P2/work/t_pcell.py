import sys, os
sys.path += ['/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/python','/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/python/pycell4klayout-api/source/python']
import pya
import sg13cmos5l_pycell_lib
ly=pya.Layout()
print(pya.Library.library_names()); lib=pya.Library.library_by_name("SG13_dev"); print(lib, lib.layout().pcell_names() if lib else None); ly.technology_name="sg13cmos5l"; c=ly.create_cell("pmosHV","SG13_dev",{"w":"5u","l":"6u","ng":"1"})
print(c, c.name, c.dbbox())
