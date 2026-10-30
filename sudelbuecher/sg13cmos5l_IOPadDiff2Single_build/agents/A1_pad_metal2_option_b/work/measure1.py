import sys, collections; sys.path.insert(0, '.')
import klayout.db as db
ly = db.Layout(); ly.read(sys.argv[1]); t = ly.top_cell()
cc = ly.cell('contacts'); CONT = ly.find_layer(6, 0)
boxes = [s.dbbox() for s in cc.shapes(CONT).each()]
cnt = collections.Counter((round(b.left,3), round(b.bottom,3), round(b.right,3), round(b.top,3)) for b in boxes)
print('contacts:', len(boxes), 'distinct', len(cnt), 'dups', [(k, v) for k, v in cnt.items() if v > 1])
print('sizes', collections.Counter((round(b.width(),3), round(b.height(),3)) for b in boxes))
# where are they
ys = collections.Counter(round(b.bottom,3) for b in boxes)
xs = collections.Counter(round(b.left,3) for b in boxes)
inbar = [b for b in boxes if b.bottom > 38.9 and b.top < 42.7]
print('in crossbar y 38.9-42.7:', len(inbar), 'x range', min(b.left for b in inbar), max(b.right for b in inbar), 'y', sorted(set(round(b.bottom,3) for b in inbar)))
col = [b for b in boxes if b.left < 2.0]
print('left column contacts x lefts', sorted(set(round(b.left,3) for b in col)), 'y range', min(b.bottom for b in col), max(b.top for b in col))
colr = [b for b in boxes if b.right > 78.0]
print('right column contacts x lefts', sorted(set(round(b.left,3) for b in colr)), 'y range', min(b.bottom for b in colr), max(b.top for b in colr))
# contacts in left column near y 37-43
print('left near 37-43:', sorted(set((round(b.left,3), round(b.bottom,3)) for b in boxes if b.left < 2.3 and 36.5 < b.bottom < 43.5)))
# overlap with PCell contacts (flatten)
c = ly.cell(ly.add_cell('F')); c.copy_tree(t); c.flatten(-1, True)
allc = db.Region(c.shapes(CONT))
m = allc.merged()
bad = [p.bbox().to_dtype(ly.dbu) for p in m.each() if not (p.is_box() and p.bbox().width() == 160 and p.bbox().height() == 160)]
print('merged Cont not 0.16 squares:', len(bad), bad[:10])
print('raw Cont count flat', allc.count(), 'merged', m.count())
