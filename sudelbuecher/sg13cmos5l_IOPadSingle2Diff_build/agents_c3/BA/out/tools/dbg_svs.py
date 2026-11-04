import sys, os, tempfile, collections
sys.argv = [sys.argv[0]] + sys.argv[1:]
root, cell, sheet, srcs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
sys.path.insert(0, os.path.join(root, 'scripts', 'xschem')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sheet_equiv as se
import importlib.util
spec = importlib.util.spec_from_file_location('svs', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sheet_vs_source.py'))
src = open(spec.origin).read().split("root, cell, sheet, srcs = sys.argv")[0]
exec(src)
with tempfile.TemporaryDirectory() as td:
    f = se.netlist(root, sheet, td); subs, top, miss = se.parse(f)
a = []; flat_sheet(subs, top, {p: 'PORT:' + p for p in subs[top][0]}, a)
s = parse_src(srcs); b = []
flat_src(s, cell, {p: 'PORT:' + p for p in s[cell][0]}, {k: val(v, {}) for k, v in s[cell][1].items()}, b)
ka = collections.Counter((d['model'], tuple(sorted(d['par'].items()))) for d in a)
kb = collections.Counter((d['model'], tuple(sorted(d['par'].items()))) for d in b)
print('sheet-only', ka - kb); print('source-only', kb - ka)
