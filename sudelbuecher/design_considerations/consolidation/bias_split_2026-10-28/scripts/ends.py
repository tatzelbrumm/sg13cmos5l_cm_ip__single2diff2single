import sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/tools')
from schedit import Sheet, _dangling, inst_pins, kind, wire, name_of
root, path = sys.argv[1], sys.argv[2]
s = Sheet(path)
print(len(_dangling(s.items, root)), 'dangling', sorted(_dangling(s.items, root)))
# unconnected instance pins (no wire endpoint/segment, no other pin)
ws = [wire(it) for it in s.items if kind(it) == 'N']
def onw(p):
    x, y = p
    for x1, y1, x2, y2 in ws:
        if (x1 == x2 == x and min(y1, y2) <= y <= max(y1, y2)) or (y1 == y2 == y and min(x1, x2) <= x <= max(x1, x2)): return True
    return False
allp = {}
for it in s.items:
    if kind(it) == 'C':
        for p in inst_pins(it, root): allp.setdefault((round(p[0]), round(p[1])), []).append(name_of(it))
bad = [(p, n) for p, n in allp.items() if len(n) == 1 and not onw(p)]
print(len(bad), 'lonely pins', sorted(bad)[:40])
