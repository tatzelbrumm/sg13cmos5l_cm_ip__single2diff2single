# Claude, agent E (C4): copy of en_ctrl_3v3.gds without the three unconnected-port stubs (Metal2 and labels)
import sys
import klayout.db as db
ly = db.Layout(); ly.read(sys.argv[1])
c = ly.cell("en_ctrl_3v3")
names = ("vddl", "vdd1v2_sense", "vdd3v3_sense")
for ln in ((10, 0), (10, 2), (10, 25)):
    li = ly.find_layer(*ln)
    for s in list(c.shapes(li).each()):
        b = s.bbox()
        if (s.is_text() and s.text_string in names) or (not s.is_text() and b.right <= 400 and 12000 <= b.bottom <= 14400):
            c.shapes(li).erase(s)
ly.write(sys.argv[2])
