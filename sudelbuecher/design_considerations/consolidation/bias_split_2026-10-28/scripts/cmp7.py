import sys, os
sys.path.insert(0, os.path.dirname(__file__)); from flatten import parse, flat; from wl import compare
B, W, L = sys.argv[1], sys.argv[2], sys.argv[3]
nb = lambda f: f.replace('/', '_')[:-4] + '.spice'
for f in [l.strip() for l in open(L)]:
    sb, tb = parse([os.path.join(B, nb(f))]); sw, tw = parse([os.path.join(W, nb(f))]); db, dw = flat(sb, tb), flat(sw, tw)
    ob, ow = compare(db, dw, {})
    xb = len([d for d in db if '.xb.' in '.' + d[0] or d[0].startswith('xb.')]); xg = len([d for d in dw if d[0].startswith('xg.') or '.xg.' in d[0]])
    print('%s %-95s %4d %4d  (xb %d, xg+xt %d)' % ('SAME' if not ob and not ow else 'DIFF', f, len(db), len(dw), xb,
          len([d for d in dw if d[0].split('.')[0] in ('xg', 'xt') or '.xg.' in d[0] or '.xt.' in d[0]])))
    for d in ob[:6]: print('   -', d[0], d[1], ' '.join(d[2]), ' '.join(d[3]))
    for d in ow[:6]: print('   +', d[0], d[1], ' '.join(d[2]), ' '.join(d[3]))
