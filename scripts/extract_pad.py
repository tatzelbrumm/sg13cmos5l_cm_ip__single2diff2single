import pya
ly = pya.Layout()
ly.read("/foss/pdks/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds")
cell = ly.cell("sg13cmos5l_IOPadInOut30mA")
opt = pya.SaveLayoutOptions()
opt.select_cell(cell.cell_index())   # this cell + everything it references, nothing else
ly.write("sg13cmos5l_IOPadInOut30mA_only.gds", opt)
