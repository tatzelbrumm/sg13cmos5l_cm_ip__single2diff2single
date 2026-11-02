# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""The lead's independent check of an agent's delivered cells (C2, phases 2-3).

python3 lead_check.py <delivered.gds> <rebuilt.gds> <ref.cdl> <outdir> <cell> [<cell> ...] [-- <run_lvs options>]

Per cell:
  1. XOR of the delivered cell against the same cell in a GDS the lead rebuilt with the agent's build script
     (all layers, merged; must be empty);
  2. IHP DRC: run_drc.py --no_density (main tables incl. latchup LU.b + maximal deck), exceptions counted;
  3. IHP LVS: run_lvs.py --disable_tap_extraction (+ options) against the agent's reference netlist;
  4. flat device table from the LVS-extracted netlist: model, L, W summed per (model, D, G, S, B, L), with counts,
     against the same table from the reference netlist.
Writes <outdir>/<cell>/... and prints one summary line per cell.
"""
import collections, glob, os, re, subprocess, sys
import klayout.db as db

PDK = '/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech'


def xor(a_gds, b_gds, cell):
    la, lb = db.Layout(), db.Layout()
    la.read(a_gds); lb.read(b_gds)
    ca, cb = la.cell(cell), lb.cell(cell)
    if ca is None or cb is None:
        return f'cell missing ({"delivered" if ca is None else "rebuilt"})'
    diffs = []
    keys = {(la.get_info(i).layer, la.get_info(i).datatype) for i in la.layer_indexes()} | \
           {(lb.get_info(i).layer, lb.get_info(i).datatype) for i in lb.layer_indexes()}
    for l, d in sorted(keys):
        ia, ib = la.find_layer(l, d), lb.find_layer(l, d)
        ra = db.Region(ca.begin_shapes_rec(ia)) if ia is not None else db.Region()
        rb = db.Region(cb.begin_shapes_rec(ib)) if ib is not None else db.Region()
        x = ra ^ rb
        if not x.is_empty():
            diffs.append(f'{l}/{d}:{x.area() * la.dbu ** 2:.3f}um2')
    return 'empty' if not diffs else 'DIFF ' + ' '.join(diffs)


def devices(netlist_text, cell):
    """(model, d, g, s, b, L) -> [count, sumW] from a flat SPICE / CDL subckt; ports renamed to themselves."""
    text = re.sub(r'\n\+', ' ', netlist_text)
    body, on = [], False
    for ln in text.splitlines():
        t = ln.split()
        if not t:
            continue
        if t[0].upper() == '.SUBCKT' and t[1] == cell:
            on = True
            continue
        if on and t[0].upper() == '.ENDS':
            break
        if on and t[0][0] in 'MmXxRr':
            body.append(t)
    table = collections.defaultdict(lambda: [0, 0.0])
    for t in body:
        params = dict(p.lower().split('=', 1) for p in t if '=' in p)
        pos = [p for p in t[1:] if '=' not in p]
        model, nets = pos[-1], pos[:-1]
        val = lambda k: float(re.sub(r'u$', 'e-6', params.get(k, '0')))
        m = float(params.get('m', '1'))
        key = (model.lower(), *(nets + [''] * (4 - len(nets)))[:4], round(val('l') * 1e6, 4))
        table[key][0] += int(m)
        table[key][1] += round(val('w') * 1e6 * m, 4)
    return table


def run(cmd, log):
    with open(log, 'w') as f:
        return subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT).returncode


if __name__ == '__main__':
    args = sys.argv[1:]
    extra = args[args.index('--') + 1:] if '--' in args else []
    args = args[:args.index('--')] if '--' in args else args
    gds, rebuilt, cdl, out, cells = args[0], args[1], args[2], args[3], args[4:]
    for cell in cells:
        d = os.path.join(out, cell)
        os.makedirs(d, exist_ok=True)
        x = xor(gds, rebuilt, cell)
        run(['python3', f'{PDK}/drc/run_drc.py', f'--path={gds}', f'--topcell={cell}', '--no_density', '--mp=4',
             f'--run_dir={d}/drc'], f'{d}/drc.log')
        drc = open(f'{d}/drc.log').read()
        exc = drc.count('generated an exception')
        viol = re.search(r"Violated rules are : (\{.*\})", drc)
        drc_s = ('clean' if 'Check Passed' in drc and not exc else (viol.group(1) if viol else 'see log')) + \
                (f' ({exc} table exceptions)' if exc else '')
        run(['python3', f'{PDK}/lvs/run_lvs.py', f'--layout={gds}', f'--netlist={cdl}', f'--topcell={cell}',
             f'--run_dir={d}/lvs', '--disable_tap_extraction'] + extra, f'{d}/lvs.log')
        lvs = open(f'{d}/lvs.log').read()
        lvs_s = 'match' if 'netlists match' in lvs else 'MISMATCH'
        ext = glob.glob(f'{d}/lvs/*_extracted.cir')
        lay = devices(open(ext[0]).read(), cell) if ext else {}
        ref = devices(open(cdl).read(), cell)
        with open(f'{d}/devices.md', 'w') as f:
            f.write(f'# {cell}: flat devices, extracted (layout) vs reference\n\n'
                    '| model | D | G | S | B | L µm | layout n / ΣW µm | reference n / ΣW µm |\n|---|---|---|---|---|---|---|---|\n')
            # nets of the extraction are named by labels; unlabelled internal nets differ in name, so compare by model + L too
            for k in sorted(set(lay) | set(ref)):
                a, b = lay.get(k, [0, 0]), ref.get(k, [0, 0])
                f.write(f'| {" | ".join(map(str, k))} | {a[0]} / {a[1]:g} | {b[0]} / {b[1]:g} |\n')
            by = lambda t: collections.Counter({(k[0], k[5]): v[1] for k, v in t.items()})
            sl, sr = collections.defaultdict(float), collections.defaultdict(float)
            for k, v in lay.items(): sl[(k[0], k[5])] += v[1]
            for k, v in ref.items(): sr[(k[0], k[5])] += v[1]
            f.write('\n| model | L µm | layout ΣW | reference ΣW |\n|---|---|---|---|\n')
            for k in sorted(set(sl) | set(sr)):
                f.write(f'| {k[0]} | {k[1]} | {sl.get(k, 0):g} | {sr.get(k, 0):g} |\n')
        wsum = all(abs(sl.get(k, 0) - sr.get(k, 0)) < 1e-3 for k in set(sl) | set(sr))
        bb = db.Layout(); bb.read(gds); c = bb.cell(cell)
        print(f'{cell}: {c.dbbox().width():.2f} x {c.dbbox().height():.2f} um | XOR {x} | DRC {drc_s} | LVS {lvs_s} | '
              f'W per (model, L) {"equal" if wsum else "DIFFERENT"}', flush=True)
