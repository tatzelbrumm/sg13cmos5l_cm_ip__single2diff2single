"""Small helpers to write xschem lines (agent BA)."""
def W(x1, y1, x2, y2, lab): return 'N %g %g %g %g {lab=%s}' % (x1, y1, x2, y2, lab)
def LP(x, y, n, lab, f=0): return 'C {devices/lab_pin.sym} %g %g 0 %d {name=%s sig_type=std_logic lab=%s}' % (x, y, f, n, lab)
def LW(x, y, n, lab, f=0): return 'C {devices/lab_wire.sym} %g %g 0 %d {name=%s sig_type=std_logic lab=%s}' % (x, y, f, n, lab)
def T(t, x, y, sz=0.25, lay=None): return 'T {%s} %g %g 0 0 %g %g {%s}' % (t, x, y, sz, sz, 'layer=%d' % lay if lay else '')
def BOX(x1, y1, x2, y2): return 'P 10 5 %g %g %g %g %g %g %g %g %g %g {dash=6}' % (x1, y1, x2, y1, x2, y2, x1, y2, x1, y1)
def MOS(kind, name, x, y, w, l, ng=1, flip=0):
    return ('C {sg13cmos5l_pr/sg13_hv_%s.sym} %g %g 0 %d {name=%s\nl=%s\nw=%s\nng=%d\nm=1\nmm_ok=1\nmodel=sg13_hv_%s\nspiceprefix=X}'
            % (kind, x, y, flip, name, l, w, ng, kind))
def RES(model, name, x, y, w, l, body, rot=0):
    return ('C {sg13cmos5l_pr/%s.sym} %g %g %d 0 {name=%s\nw=%s\nl=%s\nmodel=%s\nbody=%s\nspiceprefix=X\nb=0\nm=1\nmm_ok=1}'
            % (model, x, y, rot, name, w, l, model, body))
def DIO(model, name, x, y, w, l, rot=0):
    return 'C {sg13cmos5l_pr/%s.sym} %g %g %d 0 {name=%s\nmodel=%s\nl=%s\nw=%s\nspiceprefix=X}' % (model, x, y, rot, name, model, l, w)

def pmos_dummy(name, x, y, w, l, ng, gate, rail, k):
    """PMOS dummy, D = S = B = rail: tie at x+40 up to a rail label; gate stub to the left with its label."""
    return [MOS('pmos', name, x, y, w, l, ng),
            W(x + 20, y - 30, x + 40, y - 30, rail), W(x + 20, y, x + 40, y, rail), W(x + 20, y + 30, x + 40, y + 30, rail),
            W(x + 40, y + 30, x + 40, y - 60, rail), LP(x + 40, y - 60, 'ldm%d_r' % k, rail, 1),
            W(x - 20, y, x - 60, y, gate), LP(x - 60, y, 'ldm%d_g' % k, gate)]

def nmos_dummy(name, x, y, w, l, ng, net, bulk, k):
    """NMOS dummy, D = S = G = net (tie at x-40, label at its top-left stub), bulk to its own label."""
    return [MOS('nmos', name, x, y, w, l, ng),
            W(x - 20, y, x - 40, y, net), W(x + 20, y - 30, x + 20, y - 50, net), W(x + 20, y - 50, x - 40, y - 50, net),
            W(x + 20, y + 30, x + 20, y + 50, net), W(x + 20, y + 50, x - 40, y + 50, net), W(x - 40, y - 50, x - 40, y + 50, net),
            W(x - 40, y - 50, x - 80, y - 50, net), LP(x - 80, y - 50, 'ldm%d_g' % k, net),
            W(x + 20, y, x + 40, y, bulk), W(x + 40, y, x + 40, y + 70, bulk), LP(x + 40, y + 70, 'ldm%d_b' % k, bulk, 1)]

def nmos_dummy_rail(name, x, y, w, l, ng, gate, rail, k):
    """NMOS dummy as drawn in the s2d cells (C3 BA): D = S = B = rail, gate on its own net. Tie at x+40 down to a
    rail label; gate stub to the left with its label (the mirror of pmos_dummy)."""
    return [MOS('nmos', name, x, y, w, l, ng),
            W(x + 20, y - 30, x + 40, y - 30, rail), W(x + 20, y, x + 40, y, rail), W(x + 20, y + 30, x + 40, y + 30, rail),
            W(x + 40, y - 30, x + 40, y + 60, rail), LP(x + 40, y + 60, 'ldm%d_r' % k, rail, 1),
            W(x - 20, y, x - 60, y, gate), LP(x - 60, y, 'ldm%d_g' % k, gate)]
