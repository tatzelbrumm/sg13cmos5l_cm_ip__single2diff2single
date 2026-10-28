"""Checks for the Metal2 rework of sg13cmos5l_IOPadDiff2Single (2026-10-28, cloud workspace).

usage: python3 check_m2.py <start.klay.gds> <candidate.klay.gds> <outdir>

 1. cells: rail cells (Metal3ViasUp, TopLayersTo4) and every PCell variant byte-identical in geometry,
    flat Metal3 / Via3 / Metal4 / TopVia1 / TopMetal1 identical, the pad bar unchanged
 2. reopen with SG13_cm_clamps registered (subprocess): same PCell instances and parameters, live;
    regenerated geometry = stored geometry
 3. flat extraction (Activ, GatPoly, pSD, NWell, Cont, Metal1, Via1, Metal2, Via2, Metal3, labels 8/25,
    10/25, 30/25): devices, one net per name, label sets per net, probe points
 4. rules from the IHP deck (values: sg13cmos5l_tech_default.json, rule names: the .drc files), run on
    start and candidate; new violations listed
 5. review of the hand wiring: near-misses (space in [rule, 1.1 rule)), duplicates, stray shapes,
    labels, Via2 / Via3 / TopVia1 fields against the rails
 6. renders m2_full.png, m2_gap.png (Metal2 coloured by net over the device layers)
The stored geometry is read without the PCell library (what batch DRC / LVS see), except in step 2.
"""
import os, sys, json, subprocess, collections
sys.dont_write_bytecode = True
import klayout.db as db

W = '/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/pcw'
DECK = '/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks'
RV = json.load(open(DECK + '/sg13cmos5l_tech_default.json'))['drc_rules']
nm = lambda key: int(round(RV[key] * 1000))

# ---------------------------------------------------------------------------- reopen mode (subprocess)
if len(sys.argv) > 1 and sys.argv[1] == '--reopen':
    import runpy
    os.environ['PDKPATH'] = W + '/pdk/ihp-sg13cmos5l'
    sys.path.insert(0, W + '/new/pcells'); runpy.run_path(W + '/new/pcells/load_clamp_pcells.py')
    ly = db.Layout(); ly.read(sys.argv[2]); t = ly.top_cell()
    out = []
    for i in t.each_inst():
        c = i.cell
        p = c.pcell_parameters_by_name() if c.is_pcell_variant() else {}
        out.append(dict(cell=c.name, pcell=c.is_pcell_variant(), lib=c.library().name() if c.is_library_cell() else '',
                        at=str(i.dcplx_trans), params={k: str(v) for k, v in sorted(p.items())}))
    t.flatten(-1, True)
    o = db.SaveLayoutOptions(); o.format = 'GDS2'; o.write_context_info = False
    ly.write(sys.argv[3], o)
    print(json.dumps(out))
    sys.exit(0)

START, CAND, OUTD = sys.argv[1], sys.argv[2], sys.argv[3]
LOG = []


def say(*a):
    s = ' '.join(str(x) for x in a); print(s); LOG.append(s)


def read(path):
    ly = db.Layout(); ly.read(path); return ly


def flat(path):
    ly = read(path); t = ly.top_cell(); t.flatten(-1, True); return ly, t


def reg(ly, cell, l, d, merged=True):
    li = ly.find_layer(l, d)
    if li is None:
        return db.Region()
    r = db.Region(cell.begin_shapes_rec(li))
    return r.merged() if merged else r


def bb(x):
    return x.bbox().to_dtype(0.001)


S0, C0 = read(START), read(CAND)
say('# check_m2: start %s\n#           candidate %s' % (os.path.basename(START), os.path.basename(CAND)))

# =========================================================================== 1. cells unchanged
say('\n## 1. rails and PCells unchanged')


def cell_shapes(ly, cell):
    d = collections.defaultdict(list)
    for li in ly.layer_indexes():
        for s in cell.shapes(li).each():
            d[ly.get_info(li).to_s()].append(str(s))
    return {k: sorted(v) for k, v in d.items()}


for name in ('Metal3ViasUp', 'TopLayersTo4'):
    a, b = cell_shapes(S0, S0.cell(name)), cell_shapes(C0, C0.cell(name))
    say('%-14s shapes per layer %s ... identical: %s' % (name, {k: len(v) for k, v in a.items()}, a == b))
pc_s = {c.name: c for c in S0.each_cell() if c.name.startswith(('Clamp_', 'DCNDiode', 'DCPDiode'))}
for n, c in sorted(pc_s.items()):
    d = C0.cell(n)
    say('PCell variant %-22s stored geometry identical: %s' % (n, d is not None and cell_shapes(S0, c) == cell_shapes(C0, d)))
FS, FST = flat(START); FC, FCT = flat(CAND)
for l, d in ((30, 0), (49, 0), (50, 0), (125, 0), (126, 0), (30, 2), (50, 2), (126, 2)):
    x = reg(FS, FST, l, d) ^ reg(FC, FCT, l, d)
    say('flat %d/%d XOR start vs candidate: %s' % (l, d, 'empty' if x.is_empty() else bb(x)))
for name, l, d in (('pad bar Metal2', 10, 0), ('pad bar Via2', 29, 0)):
    a = db.Region(S0.top_cell().shapes(S0.find_layer(l, d)))
    b = db.Region(C0.top_cell().shapes(C0.find_layer(l, d)))
    say('top-level %s: start %d shapes, candidate %d, XOR %s' % (name, a.count(), b.count(), 'empty' if (a ^ b).is_empty() else bb(a ^ b)))
say('top-level instances: start %s' % sorted(i.cell.name for i in S0.top_cell().each_inst()))
say('                     cand  %s' % sorted(i.cell.name for i in C0.top_cell().each_inst()))
say('flat XOR start vs candidate per layer (what changed where):')
lds = sorted({(FS.get_info(i).layer, FS.get_info(i).datatype) for i in FS.layer_indexes()} |
             {(FC.get_info(i).layer, FC.get_info(i).datatype) for i in FC.layer_indexes()})
for l, d in lds:
    a, b = reg(FS, FST, l, d), reg(FC, FCT, l, d)
    if not (a ^ b).is_empty():
        say('   %3d/%-3d removed %s  added %s' % (l, d, bb(a - b) if not (a - b).is_empty() else '-', bb(b - a) if not (b - a).is_empty() else '-'))

# =========================================================================== 2. reopen with the library
say('\n## 2. reopen with SG13_cm_clamps registered (reopen.py logic, subprocess)')
res = {}
for tag, path in (('start', START), ('cand', CAND)):
    fl = os.path.join(OUTD, '_regen_%s.gds' % tag)
    r = subprocess.run([sys.executable, __file__, '--reopen', path, fl], capture_output=True, text=True)
    res[tag] = json.loads([l for l in r.stdout.splitlines() if l.startswith('[')][-1])
    res[tag + '_flat'] = fl
pcs = lambda L: sorted((x['cell'].split('$')[0], x['at'], json.dumps(x['params'], sort_keys=True), x['lib']) for x in L if x['pcell'])
for x in res['cand']:
    if x['pcell']:
        say('  %-20s live PCell lib=%s at %s %s' % (x['cell'], x['lib'], x['at'], x['params']))
say('PCell instances (cell, placement, parameters, library) identical to the start: %s (%d live)' % (pcs(res['start']) == pcs(res['cand']), len(pcs(res['cand']))))
rg = read(res['cand_flat']); rgt = rg.top_cell()
bad = []
for li in FC.layer_indexes():
    info = FC.get_info(li)
    if info.layer in (63, 189):
        continue
    if not (reg(FC, FCT, info.layer, info.datatype) ^ reg(rg, rgt, info.layer, info.datatype)).is_empty():
        bad.append(info.to_s())
say('regenerated (library) vs stored geometry, all layers: %s' % ('identical' if not bad else 'differs on ' + ', '.join(bad)))
for k in ('start_flat', 'cand_flat'):
    os.remove(res[k])

# =========================================================================== 3. extraction
say('\n## 3. flat extraction')
GROUPS = ('pad', 'iovss', 'iovdd', 'guard', 'a', 'b', 'dabp', 'dabn')
DIODE_TERM = {('DCNDiode', 'cathode'): 'pad', ('DCNDiode', 'anode'): 'iovss', ('DCNDiode', 'guard'): 'guard',
              ('DCPDiode', 'anode'): 'pad', ('DCPDiode', 'cathode'): 'iovdd', ('DCPDiode', 'guard'): 'iovss'}


def extract(path):
    ly = read(path); top = ly.top_cell()
    labels = []                                      # (text, source cell, layer, x, y) from the hierarchy
    for (l, d) in ((8, 25), (10, 25), (30, 25)):
        li = ly.find_layer(l, d)
        if li is None:
            continue
        it = top.begin_shapes_rec(li)
        while not it.at_end():
            s = it.shape()
            if s.is_text():
                t = s.text.transformed(it.trans())
                labels.append((t.string, it.cell().name.split('$')[0], (l, d), t.x / 1000, t.y / 1000))
            it.next()
    top.flatten(-1, True)
    li = lambda l, d: ly.find_layer(l, d) if ly.find_layer(l, d) is not None else ly.layer(l, d)
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, top, []))
    mk = lambda l, d: l2n.make_layer(li(l, d), 'L%d_%d' % (l, d))
    A, Pl, PS, NWl, C, M1, V1, M2, V2, M3 = (mk(1, 0), mk(5, 0), mk(14, 0), mk(31, 0), mk(6, 0), mk(8, 0), mk(19, 0),
                                            mk(10, 0), mk(29, 0), mk(30, 0))
    ng = (Pl & A) - PS; pg = (Pl & A) & PS; nsd = (A - PS) - Pl; psd = (A & PS) - Pl
    for r, n in ((ng, 'ng'), (pg, 'pg'), (nsd, 'nsd'), (psd, 'psd')):
        l2n.register(r, n)
    l2n.extract_devices(db.DeviceExtractorMOS3Transistor('NMOS'), {'SD': nsd, 'G': ng, 'P': Pl})
    l2n.extract_devices(db.DeviceExtractorMOS3Transistor('PMOS'), {'SD': psd, 'G': pg, 'P': Pl})
    for a in (nsd, psd, Pl, M1, M2, M3, NWl):
        l2n.connect(a)
    for a in (nsd, psd, Pl):
        l2n.connect(a, C)
    l2n.connect(NWl, nsd)                            # well ties: n+ inside an NWell
    l2n.connect(C, M1); l2n.connect(M1, V1); l2n.connect(V1, M2); l2n.connect(M2, V2); l2n.connect(V2, M3)
    for (l, d), m in (((8, 25), M1), ((10, 25), M2), ((30, 25), M3)):
        t = l2n.make_text_layer(li(l, d), 'T%d_%d' % (l, d)); l2n.connect(m, t)
    l2n.extract_netlist()
    nl = l2n.netlist(); nl.combine_devices()
    circ = nl.circuit_by_name(top.name)
    lay = {'M1': M1, 'M2': M2, 'M3': M3, 'NW': NWl, (8, 25): M1, (10, 25): M2, (30, 25): M3}
    return dict(ly=ly, top=top, l2n=l2n, nl=nl, circ=circ, labels=labels, lay=lay)


def probe(X, layer, x, y):
    n = X['l2n'].probe_net(X['lay'][layer], db.DPoint(x, y))
    return n.cluster_id if n is not None else None


def label_group(text, cell, y):
    if (cell, text) in DIODE_TERM:
        return DIODE_TERM[(cell, text)]
    if text in ('iovss', 'iovdd', 'vss', 'vdd') and cell == 'Metal3ViasUp' and y > 92:
        return 'rail %s y %.2f (no device in the cell; joined by the pad ring)' % (text, y)
    return text


def net_names(X):
    per_net = collections.defaultdict(set); group_nets = collections.defaultdict(set); misses = []
    for text, cell, ld, x, y in X['labels']:
        n = probe(X, ld, x, y)
        g = label_group(text, cell, y)
        if n is None:
            misses.append((text, cell, ld, x, y)); continue
        per_net[n].add(g); group_nets[g].add(n)
    return per_net, group_nets, misses


for tag, path in (('start', START), ('candidate', CAND)):
    X = extract(path)
    per_net, group_nets, misses = net_names(X)
    X['per_net'], X['group_nets'] = per_net, group_nets
    name = lambda n: ','.join(sorted(per_net[n])) if n in per_net else '#%d' % n
    say('\n### %s: %d nets, %d labels (%d not on their layer\'s metal: %s)' % (
        tag, sum(1 for _ in X['circ'].each_net()), len(X['labels']), len(misses), misses[:4]))
    for g in GROUPS:
        say('  %-6s labels on %d net(s)' % (g, len(group_nets.get(g, ()))))
    multi = [name(n) for n in per_net if len(per_net[n]) > 1]
    say('  nets carrying labels of more than one name: %s' % (multi or 'none'))
    agg = collections.defaultdict(float); cnt = collections.Counter()
    for d in X['circ'].each_device():
        sd = '/'.join(sorted({name(d.net_for_terminal('S').cluster_id), name(d.net_for_terminal('D').cluster_id)}))
        k = (d.device_class().name, round(d.parameter('L'), 3), name(d.net_for_terminal('G').cluster_id), sd)
        agg[k] += d.parameter('W'); cnt[k] += 1
    say('  devices (combined):')
    for k in sorted(agg):
        say('    %s L=%-6g G=%-6s S/D=%-14s W=%8.2f  (%d)' % (k[0], k[1], k[2], k[3], agg[k], cnt[k]))
    if tag == 'candidate':
        XC = X
    else:
        XS = X

say('\n### candidate: expected devices')
EXP = {('NMOS', 1.0, 'b', 'iovss/pad'): 299.2, ('NMOS', 1.0, 'dabn', 'dabn/iovss'): 8.8,
       ('PMOS', 0.6, 'a', 'iovdd/pad'): 546.12, ('PMOS', 0.6, 'dabp', 'dabp/iovdd'): 13.32,
       ('PMOS', 0.6, 'iovdd', 'dabp/iovdd'): 13.32, ('PMOS', 32.16, 'a', 'pad'): 7.96, ('PMOS', 32.16, 'pad', 'b'): 7.96}
nameC = lambda n: ','.join(sorted(XC['per_net'][n])) if n in XC['per_net'] else '#%d' % n
got = collections.defaultdict(float)
for d in XC['circ'].each_device():
    sd = '/'.join(sorted({nameC(d.net_for_terminal('S').cluster_id), nameC(d.net_for_terminal('D').cluster_id)}))
    got[(d.device_class().name, round(d.parameter('L'), 3), nameC(d.net_for_terminal('G').cluster_id), sd)] += d.parameter('W')
ok_dev = {k: abs(got.get(k, 0) - w) < 1e-6 for k, w in EXP.items()}
for k, w in EXP.items():
    say('  %-48s expected W %7.2f  got %7.2f  %s' % (str(k), w, got.get(k, 0), 'ok' if ok_dev[k] else 'MISMATCH'))
extra = [k for k in got if k not in EXP]
say('  devices not expected: %s' % (extra or 'none'))

say('\n### candidate: probe points (layer, x, y -> net)')
PROBES = [
    ('pad bar', 'M2', 40, 1.5, 'pad'), ('pad rail', 'M3', 40, 1.5, 'pad'),
    ('lower N frame drain k=0', 'M1', 8.485, 10.9, 'pad'), ('lower N frame drain x 39.045 (ON)', 'M1', 39.045, 10.9, 'pad'),
    ('upper N frame drain k=0', 'M1', 8.485, 20.5, 'pad'), ('upper N frame drain x 39.045 (RN1)', 'M1', 39.045, 20.5, 'dabn'),
    ('RN1 gate strip (gate 16)', 'M1', 37.955, 20.5, 'dabn'),
    ('P drain k=0', 'M1', 9.045, 70.0, 'pad'), ('P drain k=21 (end)', 'M1', 72.465, 70.0, 'pad'),
    ('P drain x 39.245 (RP1 + dummy)', 'M1', 39.245, 70.0, 'dabp'), ('RP1 gate strip (gate 21)', 'M1', 40.135, 70.0, 'dabp'),
    ('dummy gate strip (gate 20)', 'M1', 38.355, 70.0, 'iovdd'),
    ('DCN cathode stripe 1', 'M1', 20, 30.0, 'pad'), ('DCN cathode stripe 2 at x 39', 'M1', 39.0, 34.5, 'pad'),
    ('DCN anode bar', 'M1', 20, 27.75, 'iovss'), ('DCN left side bar', 'M1', 4.19, 32.25, 'iovss'),
    ('DCN right side bar', 'M1', 75.81, 32.25, 'iovss'), ('DCN guard ring top', 'M1', 20, 38.87, 'guard'),
    ('band column x 0.2', 'M1', 0.2, 50, 'guard'), ('N frame outer ring', 'M1', 20, 6.17, 'guard'),
    ('DCP anode stripe', 'M1', 20, 55.96, 'pad'), ('DCP cathode bar', 'M1', 20, 53.71, 'iovdd'),
    ('DCP left side bar', 'M1', 5.09, 58.2, 'iovdd'), ('DCP right side bar', 'M1', 74.91, 58.2, 'iovdd'),
    ('DCP guard ring bottom', 'M1', 20, 51.59, 'iovss'), ('P frame outer ring', 'M1', 20, 65.17, 'iovss'),
    ('N source k=0', 'M1', 6.575, 10.9, 'iovss'), ('N inner ring', 'M1', 20, 7.97, 'iovss'),
    ('P source k=0', 'M1', 7.535, 70.0, 'iovdd'), ('P source x 37.735', 'M1', 37.735, 70.0, 'iovdd'),
    ('P inner ring', 'M1', 20, 66.97, 'iovdd'),
    ('P bus left', 'M1', 20, 81.81, 'a'), ('P bus right', 'M1', 60, 81.81, 'a'), ('CMA gate head', 'M1', 20, 50.64, 'a'),
    ('a pin', 'M2', 36.5, 86.7, 'a'),
    ('lower N bus', 'M1', 20, 13.45, 'b'), ('upper N bus left', 'M1', 20, 23.01, 'b'), ('upper N bus right', 'M1', 60, 23.01, 'b'),
    ('CMB S/D + ntap frame', 'M1', 57, 41.675, 'b'), ('CMB well', 'NW', 57, 41.6, 'b'), ('b pin', 'M2', 41.5, 87.7, 'b'),
    ('CMA S/D + ntap frame', 'M1', 20, 40.5, 'pad'), ('CMA well', 'NW', 20, 41.6, 'pad'), ('CMB gate head', 'M1', 57, 50.64, 'pad'),
    ('junction left', 'M2', 20, 40.3, 'pad'), ('junction right', 'M2', 60, 40.3, 'pad'), ('P pad stub x 39.245', 'M2', 39.245, 58.0, 'pad'),
    ('dabn pin', 'M2', 38.3, 85.5, 'dabn'), ('dabn in the junction cut', 'M2', 38.3, 40.3, 'dabn'),
    ('dabp pin', 'M2', 39.245, 85.5, 'dabp'),
    ('iovss rail 7-32.5', 'M3', 40, 19.75, 'iovss'), ('iovss rail 34.5-60', 'M3', 40, 47.25, 'iovss'),
    ('iovdd rail 66-91.5', 'M3', 40, 78.75, 'iovdd'), ('DCN guard NWell', 'NW', 20, 39.5, 'guard'),
    ('DCP NWell', 'NW', 20, 52.6, 'iovdd'), ('P frame NWell', 'NW', 20, 75.0, 'iovdd'),
]
gnet = {g: next(iter(XC['group_nets'][g])) for g in GROUPS if len(XC['group_nets'].get(g, ())) == 1}
nprobe_ok = 0
for desc, lay, x, y, g in PROBES:
    n = probe(XC, lay, x, y)
    ok = n is not None and gnet.get(g) == n
    nprobe_ok += ok
    say('  %-36s %-2s (%6.3f, %6.3f) -> %-12s %s' % (desc, lay, x, y, nameC(n) if n is not None else 'nothing', 'ok' if ok else 'expected ' + g))
say('probe points: %d of %d on the expected net' % (nprobe_ok, len(PROBES)))
unl = [n for n in XC['circ'].each_net() if n.cluster_id not in XC['per_net']]
desc_unl = []
for n in unl:
    b = db.Box()
    for key in ('M1', 'M2', 'M3', 'NW'):
        b += XC['l2n'].shapes_of_net(n, XC['lay'][key], True).bbox()
    if not b.empty():
        desc_unl.append(str(b.to_dtype(0.001)))
say('unlabelled nets with metal or NWell: %d %s' % (len(desc_unl), desc_unl[:12]))

# =========================================================================== 4. rules
say('\n## 4. rules (values from sg13cmos5l_tech_default.json; names and implementation as in the .drc files)')


def layers(ly, t):
    g = lambda l, d: reg(ly, t, l, d)
    L = dict(act=g(1, 0), poly=g(5, 0), cont=reg(ly, t, 6, 0, False), m1=g(8, 0), m2=g(10, 0), psd=g(14, 0),
             v1=reg(ly, t, 19, 0, False), v2=reg(ly, t, 29, 0, False), m3=g(30, 0), nw=g(31, 0), tgo=g(44, 0),
             v3=reg(ly, t, 49, 0, False), m4=g(50, 0), tv1=reg(ly, t, 125, 0, False), tm1=g(126, 0), recog_diode=g(99, 31))
    for k in ('cont', 'v1', 'v2', 'v3', 'tv1'):
        L[k + '_m'] = L[k].merged()
    L['pact'] = L['act'] & L['psd']; L['nact'] = L['act'] - L['psd']
    L['gate'] = L['poly'] & L['act']; L['pgate'] = L['gate'] & L['psd']; L['ngate'] = L['gate'] - L['psd']
    return L


def endcap(vias, metal, ec):
    """deck: enclosed(metal, projection, whole_edges, one_side_allowed, two_opposite_sides_allowed) < ec, plus
    primary - secondary: a via side is short if the ec-wide strip along it is not all metal; an error unless the
    short sides are none, one, or two opposite ones."""
    sides = collections.defaultdict(set)
    vb = [v.bbox() for v in vias.merged().each()]
    for s_ in 'lrbt':
        ext, back = db.Region(), {}
        ext.merged_semantics = False
        for b in vb:
            e = {'l': db.Box(b.left - ec, b.bottom, b.left, b.top), 'r': db.Box(b.right, b.bottom, b.right + ec, b.top),
                 'b': db.Box(b.left, b.bottom - ec, b.right, b.bottom), 't': db.Box(b.left, b.top, b.right, b.top + ec)}[s_]
            ext.insert(e); back[str(e)] = str(b)
        for p in ext.overlapping(ext - metal).each():
            sides[back[str(p.bbox())]].add(s_)
    out = db.Region()
    for b in vb:
        ss = sides.get(str(b), set())
        if len(ss) > 1 and ss not in ({'l', 'r'}, {'b', 't'}):
            out.insert(b)
    return out + (vias.merged() - metal)


def b1(vias, sp, w, sz, n):
    """deck V1.b1 / V2.b1 / V3.b1 (array of more than n x n: spacing sp needed in one direction)."""
    x1 = vias.sized(int(sp / 2)).sized(-int(sp / 2))
    arr_d = int(((n + 1) * w + n * sz - 50) / 2)
    arr = x1.sized(-arr_d).sized(arr_d)
    vin = vias.inside(arr)
    big = vin.sized(143).sized(-143)
    e1 = big - vin
    e2 = e1 - e1.rectangles()
    return e2 + vin.interacting(e2)


def wide_sep(m, w, sp, cr):
    """deck Mn.e / Mn.f / M1.e: met.sep(wide, sp, projection_limits(cr + 1 dbu, nil)). In klayout.db 0.30.12 that
    two-layer form reports no pair where both lines are wide (tested), so wide.space with the same limits is added."""
    wide = m.sized(-w // 2).sized(w // 2)
    a = m.separation_check(wide, sp, False, db.Metrics.Euclidian, None, cr + 1, None)
    return a + wide.space_check(sp, False, db.Metrics.Euclidian, None, cr + 1, None)


def nw_nets(X, nwm):
    """NWell polygon -> net (probe a point inside each merged NWell polygon)."""
    out = {}
    for p in nwm.each():
        pt = None
        for tp in p.decompose_trapezoids():
            bx = tp.bbox()
            if bx.width() > 4 and bx.height() > 4:
                pt = bx.center(); break
        n = X['l2n'].probe_net(X['lay']['NW'], db.DPoint(pt.x / 1000, pt.y / 1000)) if pt else None
        out[p.bbox()] = n.cluster_id if n else None
    return out


def rules(L, X):
    R = {}
    act, poly, cont, m1, m2, m3, m4, psd, nw, tgo = (L[k] for k in ('act', 'poly', 'cont', 'm1', 'm2', 'm3', 'm4', 'psd', 'nw', 'tgo'))
    pact, nact, gate, pgate, ngate = L['pact'], L['nact'], L['gate'], L['pgate'], L['ngate']
    # --- NWell (feol/5_1_nwell.drc NW.b, NW.b1; sg13cmos5l_maximal.drc NW.a, NW.c..NW.f1)
    R['NW.a'] = nw.width_check(nm('NW_a'))
    netof = nw_nets(X, nw)
    pol = {p.bbox(): p for p in nw.each()}
    same, diff = db.EdgePairs(), db.EdgePairs()
    for ep in nw.space_check(nm('NW_b1')).each():
        ids = []
        for e in (ep.first, ep.second):
            c = e.bbox().center()
            hit = [k for k, p in pol.items() if p.bbox().enlarged(1, 1).contains(c) and
                   not (db.Region(p) & db.Region(e.bbox().enlarged(1, 1))).is_empty()]
            ids.append(netof.get(hit[0]) if len(hit) == 1 else ('?', tuple(hit)))
        if ids[0] == ids[1]:
            if ep.distance() < nm('NW_b'):
                same.insert(ep)
        else:
            diff.insert(ep)
    R['NW.b'] = same; R['NW.b1'] = diff
    pin = lambda r, inside: (r & tgo) if inside else (r - tgo)
    p_in_nw, n_in_nw = pact & nw, nact & nw
    R['NW.c'] = pin(p_in_nw, False).enclosed_check(nw, nm('NW_c'))
    R['NW.c1'] = pin(p_in_nw, True).enclosed_check(nw, nm('NW_c1'))
    R['NW.d'] = nw.separation_check(pin(nact - nw, False), nm('NW_d'))
    R['NW.d1'] = nw.separation_check(pin(nact - nw, True), nm('NW_d1'))
    R['NW.e'] = pin(n_in_nw, False).enclosed_check(nw, nm('NW_e'))
    R['NW.e1'] = pin(n_in_nw, True).enclosed_check(nw, nm('NW_e1'))
    R['NW.f'] = nw.separation_check(pin(pact - nw, False), nm('NW_f'))
    R['NW.f1'] = nw.separation_check(pin(pact - nw, True), nm('NW_f1'))
    # --- Activ (json Act_a, Act_b; maximal.drc Act.c, Act.d, Act.e)
    R['Act.a'] = act.width_check(nm('Act_a')); R['Act.b'] = act.space_check(nm('Act_b'))
    R['Act.c'] = poly.enclosed_check(act, nm('Act_c'), False, db.Metrics.Projection)
    R['Act.d'] = act.with_area(0, int(RV['Act_d'] * 1e6), False)
    R['Act.e'] = act.holes().with_area(0, int(RV['Act_e'] * 1e6), False)
    # --- GatPoly (json Gat_a, Gat_b, Gat_b1, Gat_c, Gat_d, Gat_e; maximal.drc Gat.a4, Gat.c, Gat.f)
    R['Gat.a'] = poly.width_check(nm('Gat_a')); R['Gat.b'] = poly.space_check(nm('Gat_b'))
    hvp = pgate & tgo
    sd = (act - hvp).interacting(hvp)
    R['Gat.a4'] = sd.space_check(nm('Gat_a4'), False, db.Metrics.Projection).polygons() & act
    R['Gat.b1'] = (gate & tgo).space_check(nm('Gat_b1'))
    R['Gat.c'] = act.enclosed_check(poly, nm('Gat_c')).polygons() + poly.inside(act)
    R['Gat.d'] = poly.separation_check(act, nm('Gat_d'))
    R['Gat.e'] = poly.with_area(0, int(RV['Gat_e'] * 1e6), False)
    R['Gat.f'] = gate.non_rectangles()
    # --- ThickGateOx (maximal.drc TGO.a .. TGO.e)
    R['TGO.a'] = act.interacting(tgo).enclosed_check(tgo, nm('TGO_a'))
    R['TGO.b'] = tgo.separation_check(act - tgo, nm('TGO_b'))
    R['TGO.c'] = (gate & tgo).enclosed_check(tgo, nm('TGO_c'))
    R['TGO.d'] = tgo.separation_check(gate - tgo, nm('TGO_d'))
    R['TGO.e'] = tgo.space_check(nm('TGO_e'))
    # --- pSD (maximal.drc pSD.a .. pSD.l, values json)
    R['pSD.a'] = psd.width_check(nm('pSD_a')); R['pSD.b'] = psd.space_check(nm('pSD_b'))
    R['pSD.c'] = (act & nw).inside(psd).enclosed_check(psd, nm('pSD_c'))
    R['pSD.d'] = psd.separation_check(nact - nw, nm('pSD_d'))
    R['pSD.d1'] = psd.separation_check(nact & nw, nm('pSD_d1'))
    R['pSD.i'] = (pgate - tgo).enclosed_check(psd, nm('pSD_i')); R['pSD.i1'] = (pgate & tgo).enclosed_check(psd, nm('pSD_i1'))
    R['pSD.j'] = psd.separation_check(ngate - tgo, nm('pSD_j')); R['pSD.j1'] = psd.separation_check(ngate & tgo, nm('pSD_j1'))
    R['pSD.k'] = psd.with_area(0, int(RV['pSD_k'] * 1e6), False)
    R['pSD.l'] = psd.holes().with_area(0, int(RV['pSD_l'] * 1e6), False)
    # --- Cont (feol/5_14_cont.drc Cnt.a .. Cnt.g2; maximal.drc Cnt.b1, Cnt.f, Cnt.g, Cnt.h, Cnt.j)
    cm = L['cont_m']
    R['Cnt.a'] = cm.non_squares() + cm.squares().with_bbox_width(160, 161, True)
    R['Cnt.b'] = cm.space_check(nm('Cnt_b'))
    x1 = cm.sized(100).sized(-100); arr = x1.sized(-669).sized(669); vin = cm.inside(arr)
    e = vin.sized(99).sized(-99) - vin
    R['Cnt.b1'] = e - e.rectangles()
    c_act, c_poly = cm.interacting(act), cm.interacting(poly).not_interacting(act)
    R['Cnt.c'] = c_act.enclosed_check(act, nm('Cnt_c')).polygons() + (c_act - act)
    R['Cnt.d'] = c_poly.enclosed_check(poly, nm('Cnt_d')).polygons() + (c_poly - poly)
    R['Cnt.e'] = c_poly.separation_check(act, nm('Cnt_e'))
    R['Cnt.f'] = c_act.separation_check(poly, nm('Cnt_f'))
    R['Cnt.g'] = cm - act - poly
    R['Cnt.g1'] = (cm & nact).separation_check(psd, nm('Cnt_g1'))
    R['Cnt.g2'] = (cm & pact).enclosed_check(psd, nm('Cnt_g2'))
    R['Cnt.h'] = cm - m1
    R['Cnt.j'] = cm & gate
    # --- Metal1 (json M1_a, M1_b, M1_e*; maximal.drc M1.c, M1.c1, M1.d)
    R['M1.a'] = m1.width_check(nm('M1_a')); R['M1.b'] = m1.space_check(nm('M1_b'))
    R['M1.e'] = wide_sep(m1, nm('M1_e_w'), nm('M1_e'), nm('M1_e_cr'))
    R['M1.d'] = m1.with_area(0, int(RV['M1_d'] * 1e6), False)
    R['M1.c1'] = endcap(L['cont'], m1, nm('M1_c1'))
    # --- Metal2..Metal4 (beol/5_17_metaln.drc Mn.a, Mn.b, Mn.e, Mn.f; maximal.drc Mn.c, Mn.c1, Mn.d)
    for n_, m, vb in ((2, m2, 'v1'), (3, m3, 'v2'), (4, m4, 'v3')):
        R['M%d.a' % n_] = m.width_check(nm('Mn_a')); R['M%d.b' % n_] = m.space_check(nm('Mn_b'))
        R['M%d.e' % n_] = wide_sep(m, nm('Mn_e_w'), nm('Mn_e'), nm('Mn_e_cr'))
        R['M%d.f' % n_] = wide_sep(m, nm('Mn_f_w'), nm('Mn_f'), nm('Mn_f_cr'))
        R['M%d.d' % n_] = m.with_area(0, int(RV['Mn_d'] * 1e6), False)
        R['M%d.c' % n_] = L[vb + '_m'].enclosed_check(m, nm('Mn_c')).polygons() + (L[vb + '_m'] - m)
        R['M%d.c1' % n_] = endcap(L[vb], m, 50)           # maximal.drc Mn.c1: 0.05 hard-coded
    # --- Via1 (beol/5_19_via1.drc V1.a, V1.b, V1.c; maximal.drc V1.b1, V1.c1), Via2/3 (beol/5_20_vian.drc, maximal.drc)
    for vn, vk, below, cval, c1val in (('V1', 'v1', m1, 'V1_c', 'V1_c1'), ('V2', 'v2', m2, 'Vn_c', 'Vn_c1'), ('V3', 'v3', m3, 'Vn_c', 'Vn_c1')):
        vm = L[vk + '_m']; a = 'V1_a' if vn == 'V1' else 'Vn_a'
        R[vn + '.a'] = vm.non_squares() + vm.squares().with_bbox_width(nm(a), nm(a) + 1, True)
        R[vn + '.b'] = vm.space_check(nm('V1_b' if vn == 'V1' else 'Vn_b'))
        R[vn + '.b1'] = b1(vm, nm('V1_b1' if vn == 'V1' else 'Vn_b1'), 190, 220, 3)
        R[vn + '.c'] = vm.enclosed_check(below, nm(cval)).polygons() + (vm - below)
        R[vn + '.c1'] = endcap(L[vk], below, nm(c1val))
    # --- TopVia1 / TopMetal1 (beol/5_21_topvia1.drc; json TM1_a, TM1_b)
    tv = L['tv1_m']
    R['TV1.a'] = tv.non_squares() + tv.squares().with_bbox_width(nm('TV1_a'), nm('TV1_a') + 1, True)
    R['TV1.b'] = tv.space_check(nm('TV1_b'))
    R['TV1.c'] = tv.enclosed_check(m4, nm('TV1_c')).polygons() + (tv - m4)
    R['TV1.d'] = tv.enclosed_check(L['tm1'], nm('TV1_d')).polygons() + (tv - L['tm1'])
    R['TM1.a'] = L['tm1'].width_check(nm('TM1_a')); R['TM1.b'] = L['tm1'].space_check(nm('TM1_b'))
    return R


def enlarge_inside(r, other, dist, step):
    """deck: ext_enlarge_inside (sg13cmos5l_maximal.drc line 1277): grow in steps, clipped to other each step."""
    n = int(dist / step + 0.5)
    for _ in range(n):
        r = r.sized(step) & other
    return r


def latchup(L):
    """maximal.drc LU.a, LU.d, LU.d1 ($latchUpRules), simplified layer derivations (no SalBlock, SVaricap,
    abutted ties or scr1 in this cell): all_ntie = n+ Activ in NWell; devExclud = Recog_diode."""
    R = {}
    nw, act, poly, cont = L['nw'], L['act'], L['poly'], L['cont_m']
    ntie = L['nact'] & nw
    x = enlarge_inside(ntie, nw, nm('LU_a'), 100)
    R['LU.a'] = ((L['pact'] & nw) - x) - L['recog_diode']
    act_conn = act - poly
    sz = enlarge_inside(cont, act_conn, nm('LU_d'), 210)
    tmp = ntie.not_interacting(act.interacting(poly))
    R['LU.d'] = (tmp - sz).interacting(sz)
    ptie = (L['pact'] - nw).not_interacting(act.interacting(poly))
    R['LU.d1'] = ((ptie - sz) - poly).interacting(sz)
    return R


def markers(x):
    if isinstance(x, db.EdgePairs):
        return [ep.bbox() for ep in x.each()]
    return [p.bbox() for p in x.each()]


LS, LC = layers(FS, FST), layers(FC, FCT)
RS, RC = rules(LS, XS), rules(LC, XC)
RS.update(latchup(LS)); RC.update(latchup(LC))
new_total, rows = 0, []
for k in RC:
    ms, mc = set(map(str, markers(RS[k]))), markers(RC[k])
    new = [b for b in mc if str(b) not in ms]
    new_total += len(new)
    rows.append((k, len(ms), len(mc), new))
say('%-8s %6s %6s %6s' % ('rule', 'start', 'cand', 'new'))
for k, ns, nc, new in rows:
    say('%-8s %6d %6d %6d %s' % (k, ns, nc, len(new), ' '.join(str(b.to_dtype(0.001)) for b in new[:6])))
say('rules run: %d; violations in the candidate: %d (start: %d); new: %d' % (
    len(rows), sum(r[2] for r in rows), sum(r[1] for r in rows), new_total))

# =========================================================================== 5. review of the hand wiring
say('\n## 5. hand wiring (everything that is not a PCell)')
say('(contact / via arrays are drawn at the rule pitch by convention -- IHP 0.34 / 0.41 -- and are not listed as near-misses)')
HW = read(CAND); hwt = HW.top_cell()
for i in list(hwt.each_inst()):
    if i.cell.name.startswith(('Clamp_', 'DCNDiode', 'DCPDiode')):
        i.delete()
hwt.flatten(-1, True)
hand = {k: reg(HW, hwt, *ld) for k, ld in (('m1', (8, 0)), ('m2', (10, 0)), ('m3', (30, 0)), ('act', (1, 0)), ('nw', (31, 0)),
                                          ('psd', (14, 0)), ('poly', (5, 0)), ('cont', (6, 0)), ('v1', (19, 0)), ('v2', (29, 0)),
                                          ('m4', (50, 0)), ('tgo', (44, 0)))}
NEAR = [('M1.b', 'm1', None, 'M1_b'), ('M1.e', 'm1', 'wide', 'M1_e'), ('M2.b', 'm2', None, 'Mn_b'), ('M2.e', 'm2', 'wide', 'Mn_e'),
        ('M3.b', 'm3', None, 'Mn_b'), ('Act.b', 'act', None, 'Act_b'), ('Gat.b', 'poly', None, 'Gat_b'),
        ('pSD.b', 'psd', None, 'pSD_b'), ('NW.b1', 'nw', None, 'NW_b1'),
        ('NW.f', 'nw', ('pact_out', 'NW_f'), None), ('NW.d', 'nw', ('nact_out', 'NW_d'), None),
        ('Cnt.f', 'cont_act', ('poly', 'Cnt_f'), None), ('Cnt.e', 'cont_poly', ('act', 'Cnt_e'), None),
        ('Gat.d', 'poly', ('act', 'Gat_d'), None), ('pSD.d1', 'psd', ('nact_nw', 'pSD_d1'), None),
        ('TGO.b', 'tgo', ('act_out_tgo', 'TGO_b'), None)]
LC['pact_out'] = (LC['pact'] - LC['nw']) - LC['tgo']; LC['nact_out'] = (LC['nact'] - LC['nw']) - LC['tgo']
LC['cont_act'] = LC['cont_m'].interacting(LC['act']); LC['cont_poly'] = LC['cont_m'].interacting(LC['poly']).not_interacting(LC['act'])
LC['nact_nw'] = LC['nact'] & LC['nw']; LC['act_out_tgo'] = LC['act'] - LC['tgo']
hand_any = db.Region()
for v in hand.values():
    hand_any += v
hand_edges = {k: v.edges() for k, v in hand.items()}
hand_edges['cont_m'] = hand_edges['cont']; hand_edges['v1_m'] = hand_edges['v1']; hand_edges['v2_m'] = hand_edges['v2']
hand_edges['cont_act'] = hand_edges['cont']; hand_edges['cont_poly'] = hand_edges['cont']
near_rows = []
for rname, lk, mode, key in NEAR:
    r = LC[lk]
    if mode is None:
        lo, hi = nm(key), int(round(nm(key) * 1.1))
        a, b = r.space_check(hi), r.space_check(lo)
    elif mode == 'wide':
        lo, hi = nm(key), int(round(nm(key) * 1.1))
        w = nm('M1_e_w' if rname.startswith('M1') else 'Mn_e_w'); cr = nm('M1_e_cr' if rname.startswith('M1') else 'Mn_e_cr')
        a, b = wide_sep(r, w, hi, cr), wide_sep(r, w, lo, cr)
    else:
        other, key = mode
        lo, hi = nm(key), int(round(nm(key) * 1.1))
        a, b = r.separation_check(LC[other], hi), r.separation_check(LC[other], lo)
    bad = set(str(ep.bbox()) for ep in b.each())
    ek = hand_edges.get(lk, db.Edges())
    eo = hand_edges.get(mode[0], db.Edges()) if isinstance(mode, tuple) else ek
    hits = []
    for ep in a.each():
        if str(ep.bbox()) in bad:
            continue
        mine = not (db.Edges(ep.first) & ek).is_empty() or not (db.Edges(ep.second) & eo).is_empty() or \
               not (db.Edges(ep.second) & ek).is_empty()
        if mine:
            hits.append((round(ep.distance() / 1000, 3), ep.bbox().to_dtype(0.001)))
    near_rows.append((rname, lo / 1000, hi / 1000, hits))
    say('near-miss %-6s [%.3f, %.3f): %3d %s' % (rname, lo / 1000, hi / 1000, len(hits),
                                                  ' '.join('%.3f@%s' % (d, str(bx)) for d, bx in hits[:5]) + (' ...' if len(hits) > 5 else '')))
# duplicates and stray shapes in the static cells
dups = []
for c in C0.each_cell():
    if c.is_pcell_variant() or c.name.startswith(('Clamp_', 'DCNDiode', 'DCPDiode')):
        continue
    for li in C0.layer_indexes():
        seen = collections.Counter(str(s) for s in c.shapes(li).each())
        dups += [(c.name, C0.get_info(li).to_s(), k, v) for k, v in seen.items() if v > 1]
say('duplicate shapes in static cells: %d %s' % (len(dups), dups[:5]))
bnd = db.Region(db.Box(0, 0, 80000, 180000))
outside = {k: bb(v - bnd) for k, v in hand.items() if not (v - bnd).is_empty()}
say('hand-wiring shapes beyond the 80 x 180 boundary: %s' % outside)
t63 = [s.dbbox() for s in C0.top_cell().shapes(C0.find_layer(63, 0)).each()]
say('TEXT 63/0 shapes in the top cell: %s' % t63)
# labels: on their layer's shapes, and M3 / M4 / TopMetal1 labels naming the same rails
def labels_of(ly, cell, ld):
    li = ly.find_layer(*ld)
    return [] if li is None else [(s.text_string, s.dtext.x, s.dtext.y) for s in cell.shapes(li).each() if s.is_text()]
for cname, pairs in (('Metal3ViasUp', ((30, 25), (30, 0))), ('TopLayersTo4', ((50, 25), (50, 0))), ('TopLayersTo4', ((126, 25), (126, 0)))):
    c = C0.cell(cname)
    shapes = db.Region(c.shapes(C0.find_layer(*pairs[1])))
    for txt, x, y in labels_of(C0, c, pairs[0]):
        hit = [p.bbox().to_dtype(0.001) for p in shapes.each() if p.bbox().contains(db.Point(int(x * 1000), int(y * 1000)))]
        say('label %-6s %-7s at (%5.1f, %6.2f) on %s' % (txt, '%d/%d' % pairs[0], x, y, hit[0] if hit else 'NOTHING'))
for txt, x, y in labels_of(C0, C0.top_cell(), (10, 25)):
    say('label %-6s 10/25   at (%5.1f, %6.2f) top cell, on Metal2 net %s' % (txt, x, y, nameC(probe(XC, 'M2', x, y))))
# via fields against the rails: every Via2 / Via3 / TopVia1 inside one rail band on both its metals
RAILS = [('pad', 0, 3), ('iovss', 7, 32.5), ('iovss', 34.5, 60), ('iovdd', 66, 91.5), ('iovdd', 93.5, 119),
         ('iovss', 126, 134), ('vss/vdd', 140, 178)]
for vname, vk, lowk, upk in (('Via2', 'v2_m', 'm2', 'm3'), ('Via3', 'v3_m', 'm3', 'm4'), ('TopVia1', 'tv1_m', 'm4', 'tm1')):
    v = LC[vk]
    per = []
    for rn, y0, y1 in RAILS:
        band = db.Region(db.Box(-1000, int(y0 * 1000), 81000, int(y1 * 1000)))
        per.append('%s %g-%g: %d' % (rn, y0, y1, v.inside(band).count()))
    say('%-7s %5d: %s; not inside a rail band: %d; not covered by %s: %d, by %s: %d' % (
        vname, v.count(), ', '.join(per), v.outside(db.Region([db.Box(-1000, int(a * 1000), 81000, int(b * 1000)) for _, a, b in RAILS])).count(),
        lowk, (v - LC[lowk]).count(), upk, (v - LC[upk]).count()))
# the 6-61 ring: Activ and Metal1 each continuous from cell edge to cell edge (side bars <-> DCN guard ring)
for nmL, k in (('Activ', 'act'), ('Metal1', 'm1'), ('NWell', 'nw')):
    r = LC[k]
    hit = r.interacting(db.Region(db.Box(0, 49900, 100, 50100)))          # left side bar at y 50
    rr = hit.interacting(db.Region(db.Box(79900, 49900, 80000, 50100)))   # same polygon reaches the right side bar
    top_y = max((p.bbox().top for p in (hit & db.Region(db.Box(2500, 38000, 77500, 45000))).each()), default=0)
    say('band %-6s: one polygon from x 0 to x 80 through the DCN guard ring: %s; its top between x 2.5 and 77.5: %.2f' % (
        nmL, not rr.is_empty(), top_y / 1000))
# Via2 by the net of its Metal2 and Metal3 (a via joining two different names would show up as a merged label set in 3.)
v2net = collections.Counter()
for p in LC['v2_m'].each():
    c = p.bbox().center()
    v2net[(nameC(probe(XC, 'M2', c.x / 1000, c.y / 1000)), nameC(probe(XC, 'M3', c.x / 1000, c.y / 1000)))] += 1
say('Via2 by (Metal2 net, Metal3 net): %s' % dict(v2net))

# =========================================================================== 6. renders
say('\n## 6. renders')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
BG, INK, INK2 = '#1a1a19', '#f0efec', '#c3c2b7'
NETC = {'pad': '#3987e5', 'iovss': '#d95926', 'iovdd': '#199e70', 'a': '#c98500', 'b': '#d55181', 'dabp': '#008300', 'dabn': '#9085e9'}
DEV = [((31, 0), '#268c6b', 0.18, True), ((14, 0), '#ccb899', 0.0, False), ((44, 0), '#ffffcc', 0.0, False),
       ((1, 0), '#00ff00', 0.22, True), ((5, 0), '#bf4026', 0.55, True), ((8, 0), '#39bfff', 0.16, True)]


def polys(r, win):
    out = []
    for p in (r & db.Region(win)).each():
        for tp in p.decompose_trapezoids():
            out.append([(q.x / 1000, q.y / 1000) for q in tp.each_point()])
    return out


def render(path, win, title, vias=False, netlabels=(), figsize=(14, 16), dpi=110):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    for (l, d), col, a, fill in DEV:
        P = polys(reg(FC, FCT, l, d), win)
        if P:
            ax.add_collection(PolyCollection(P, facecolors=col if fill else 'none', edgecolors=col,
                                             linewidths=0.4 if fill else 0.7, **({'alpha': a} if fill else {})))
    for rn, y0, y1 in RAILS:                              # Metal3 rails: dashed outlines at the cell edge
        if y1 > win.bottom / 1000 and y0 < win.top / 1000:
            ax.plot([-0.9, -0.9], [max(y0, win.bottom / 1000), min(y1, win.top / 1000)], color=INK2, lw=2.5, solid_capstyle='butt')
            ax.text(-1.1, (max(y0, win.bottom / 1000) + min(y1, win.top / 1000)) / 2, 'M3 ' + rn, color=INK2, fontsize=7,
                    rotation=90, ha='right', va='center')
    m2l = XC['lay']['M2']
    other = db.Region()
    for n in XC['circ'].each_net():
        r = XC['l2n'].shapes_of_net(n, m2l, True)
        if r.is_empty():
            continue
        g = nameC(n.cluster_id)
        g = g if g in NETC else None
        if g is None:
            other += r; continue
        ax.add_collection(PolyCollection(polys(r, win), facecolors=NETC[g], edgecolors=NETC[g], alpha=0.78, linewidths=0.3))
    if not other.is_empty():
        ax.add_collection(PolyCollection(polys(other, win), facecolors='#888', edgecolors='#888', alpha=0.8, linewidths=0.3))
    if vias:
        for ld, col in (((19, 0), '#f0efec'), ((29, 0), '#1a1a19')):
            P = polys(reg(FC, FCT, *ld), win)
            ax.add_collection(PolyCollection(P, facecolors=col, edgecolors=INK if col == BG else 'none', linewidths=0.3))
    for txt, x, y in netlabels:
        ax.text(x, y, txt, color=INK, fontsize=8, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', fc='#2b2b29', ec=NETC.get(txt, '#666'), lw=1.0))
    ax.set_xlim(win.left / 1000 - (1.6 if win.left == -1000 else 0), win.right / 1000); ax.set_ylim(win.bottom / 1000, win.top / 1000)
    ax.set_aspect('equal'); ax.set_title(title, color=INK, fontsize=10, loc='left')
    ax.tick_params(colors=INK2, labelsize=8)
    for s in ax.spines.values():
        s.set_color('#444')
    ax.set_xlabel('x (µm)', color=INK2, fontsize=8); ax.set_ylabel('y (µm)', color=INK2, fontsize=8)
    leg = [Patch(facecolor=c, edgecolor=c, label='Metal2 ' + k) for k, c in NETC.items()]
    leg += [Patch(facecolor='#268c6b', alpha=0.4, label='NWell'), Patch(facecolor='#00ff00', alpha=0.4, label='Activ'),
            Patch(facecolor='#bf4026', alpha=0.7, label='GatPoly'), Patch(facecolor='#39bfff', alpha=0.35, label='Metal1')]
    if vias:
        leg += [Patch(facecolor='#f0efec', label='Via1'), Patch(facecolor=BG, edgecolor=INK, label='Via2')]
    lg = ax.legend(handles=leg, loc='upper left', bbox_to_anchor=(1.01, 1.0), fontsize=8, frameon=False, labelcolor=INK)
    fig.savefig(path, facecolor=BG, bbox_inches='tight'); plt.close(fig)
    say('wrote %s' % path)


render(os.path.join(OUTD, 'm2_full.png'), db.Box(-1000, -1000, 81000, 92000),
       'sg13cmos5l_IOPadDiff2Single, y 0-92 um: Metal2 by net (option B), candidate',
       netlabels=[('pad', 40, 1.5), ('iovss', 6.575, 30.9), ('pad', 8.485, 18), ('dabn', 38.3, 31.5), ('pad', 9.045, 63.5),
                  ('iovdd', 7.535, 70), ('dabp', 39.245, 77), ('a', 3.45, 70), ('b', 0.75, 60), ('a', 30, 86.7), ('b', 50, 87.7),
                  ('pad', 20, 40.3), ('iovss', 13.575, 51.7), ('b', 79.25, 44), ('iovss', 75.3, 30), ('iovdd', 74.4, 62)])
render(os.path.join(OUTD, 'm2_gap.png'), db.Box(0, 36000, 80000, 55000),
       'gap between DCNDiode and DCPDiode (y 36-55 um): junction, CMA / CMB, iovss stubs, dabn; Via1 white, Via2 dark',
       vias=True, figsize=(22, 8), dpi=130,
       netlabels=[('pad', 20, 40.3), ('pad', 60, 40.3), ('dabn', 38.3, 45.5), ('a', 3.45, 53.5), ('b', 76.5, 45.95),
                  ('iovss', 13.575, 51.7), ('iovss', 37.5, 37.2), ('iovdd', 22.635, 54.4), ('b', 0.75, 47)])
open(os.path.join(OUTD, 'check_m2.log'), 'w').write('\n'.join(LOG) + '\n')
