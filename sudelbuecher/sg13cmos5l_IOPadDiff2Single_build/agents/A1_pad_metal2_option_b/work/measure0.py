import sys; sys.path.insert(0, '.')
from common import *
load_lib()
import clamp_engine as E
ly = db.Layout(); ly.read(sys.argv[1]); t = ly.top_cell()
print('N columns', [round(v/1000,3) for v in E.columns(35, 1000, (80000-E.array_extent(35,1000,0)[1])//10*5)[0]][:3], '...')
x0N = (80000-E.array_extent(35,1000,0)[1])//10*5; x0P = (80000-E.array_extent(43,600,0)[1])//10*5
sN, dN = E.columns(35, 1000, x0N); sP, dP = E.columns(43, 600, x0P)
print('x0N', x0N, 'x0P', x0P)
print('N src', [v/1000 for v in sN]); print('N drn', [v/1000 for v in dN])
print('P src', [v/1000 for v in sP]); print('P drn', [v/1000 for v in dP])
gN = E.gate_lefts(35, 1000, x0N); gP = E.gate_lefts(43, 600, x0P)
print('N gate lefts 0,15,16,17,18,34', [gN[i]/1000 for i in (0,15,16,17,18,34)])
print('P gate lefts 0,19,20,21,22,42', [gP[i]/1000 for i in (0,19,20,21,22,42)])
tf = t.dup() if False else None
c = ly.cell(ly.add_cell('FLAT')); c.copy_tree(t); c.flatten(-1, True)
def R(l, d):
    li = ly.find_layer(l, d)
    return db.Region(c.shapes(li)).merged() if li is not None else db.Region()
def win(r, x0, y0, x1, y1):
    return [p.bbox().to_dtype(ly.dbu) for p in (r & db.Region(db.DBox(x0,y0,x1,y1).to_itype(ly.dbu))).each()]
NW = R(31,0); ACT = R(1,0); M1 = R(8,0); PSD = R(14,0); TGO = R(44,0); POLY = R(5,0); M2 = R(10,0)
print('NWell polygons:'); [print('  ', p.bbox().to_dtype(ly.dbu), 'holes', p.holes()) for p in NW.each()]
print('TGO polygons:'); [print('  ', p.bbox().to_dtype(ly.dbu)) for p in TGO.each()]
print('pSD polygons:'); [print('  ', p.bbox().to_dtype(ly.dbu), 'holes', p.holes()) for p in PSD.each()]
print('Activ in gap x 10..12 y 37..54:', win(ACT, 10, 37, 12, 54))
print('M1 in gap x 10..12 y 37..54:', win(M1, 10, 37, 12, 54))
print('NW in gap x 10..12 y 37..54:', win(NW, 10, 37, 12, 54))
print('pSD in gap x 10..12 y 37..54:', win(PSD, 10, 37, 12, 54))
print('Activ x 0..5 y 37..54:', win(ACT, 0, 37, 5, 54))
print('Activ x 75..80 y 37..54:', win(ACT, 75, 37, 80, 54))
print('M1 near P bus left x 0..10 y 80..85:', win(M1, 0, 80, 10, 85))
print('M1 near P bus right x 70..80 y 80..85:', win(M1, 70, 80, 80, 85))
print('M1 near lower N bus left x 0..8 y 12..15:', win(M1, 0, 12, 8, 15))
print('M1 near lower N bus right x 72..80 y 12..15:', win(M1, 72, 12, 80, 15))
print('M1 near upper N bus left x 0..8 y 21.5..24.5:', win(M1, 0, 21.5, 8, 24.5))
print('M1 near upper N bus right x 72..80 y 21.5..24.5:', win(M1, 72, 21.5, 80, 24.5))
print('M1 around RN1 x 36..42 y 17..24:', win(M1, 36, 17, 42, 24))
print('M1 around RP1 x 36..42 y 80..84.5:', win(M1, 36, 80, 42, 84.5))
print('M1 DCN x 0..8 y 25..40 :', win(M1, 0, 25, 8, 40))
print('M1 DCN x 72..80 y 25..40 :', win(M1, 72, 25, 80, 40))
print('M1 DCP x 0..9 y 50..66 :', win(M1, 0, 50, 9, 66))
print('M1 DCP x 71..80 y 50..66 :', win(M1, 71, 50, 80, 66))
print('M1 P frame low x 70..80 y 64..69:', win(M1, 70, 64, 80, 69))
print('M2 all:', [p.bbox().to_dtype(ly.dbu) for p in M2.each()])
print('Poly near P bus x 36..42 y 80..84:', win(POLY, 36, 80, 42, 84))
