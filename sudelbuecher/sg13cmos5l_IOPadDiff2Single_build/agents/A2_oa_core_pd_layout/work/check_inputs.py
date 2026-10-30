"""Input checks: (1) sheet netlist vs hand netlist, (2) XOR of standalone exports vs library cells."""
import re, sys, klayout.db as db
A = "/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent/inputs/"

def devs(text, sub):
    m = re.search(r"\.subckt\s+%s\s+([^\n]*)\n(.*?)\.ends" % sub, text, re.S | re.I)
    ports = m.group(1).split()
    out = {}
    for line in m.group(2).splitlines():
        line = line.strip()
        if not line or line[0] in "*.":
            continue
        t = line.split()
        name = t[0].upper().lstrip("X")
        par = dict(kv.split("=") for kv in t[6:] if "=" in kv)
        out[name] = (tuple(t[1:5]), t[5], par.get("w"), par.get("l"), par.get("ng"))
    return ports, out

ps, s = devs(open(A + "oa_core_pd_xschem.spice").read().replace("**.subckt", ".subckt").replace("**.ends", ".ends"), "oa_core_pd")
ph, h = devs(open(A + "bias_ref_pd.spice").read(), "oa_core_pd")
print("sheet ports:", ps, " hand ports:", ph)
print("devices sheet %d, hand %d" % (len(s), len(h)))
diff = 0
for k in sorted(set(s) | set(h)):
    if s.get(k) != h.get(k):
        diff += 1
        print("  DIFF", k, s.get(k), h.get(k))
print("device differences:", diff)

# XOR standalone exports vs library cells
lib = db.Layout(); lib.read(A + "pad_buffer_cells.gds")
for f, cname in (("oa_pmir.gds", "oa_pmir"), ("oa_pcas.gds", "oa_pcas"), ("oa_misc_p.gds", "oa_misc_p")):
    ex = db.Layout(); ex.read(A + f)
    tops = [c.name for c in ex.top_cells()]
    c1, c2 = lib.cell(cname), ex.cell(cname)
    layers = set((i.layer, i.datatype) for i in lib.layer_infos()) | set((i.layer, i.datatype) for i in ex.layer_infos())
    nd = 0
    for L in sorted(layers):
        l1, l2 = lib.find_layer(*L), ex.find_layer(*L)
        r1 = db.Region(c1.begin_shapes_rec(l1)) if l1 is not None else db.Region()
        r2 = db.Region(c2.begin_shapes_rec(l2)) if l2 is not None else db.Region()
        x = r1 ^ r2
        if not x.is_empty():
            nd += 1; print("   XOR", f, L, x.area() * 1e-6)
        # texts
        def tx(c, li, ly):
            out = []
            if li is None: return out
            it = c.begin_shapes_rec(li)
            while not it.at_end():
                sh = it.shape()
                if sh.is_text():
                    t = sh.text.transformed(it.trans()); out.append((t.string, t.x, t.y))
                it.next()
            return sorted(out)
        if tx(c1, l1, lib) != tx(c2, l2, ex):
            nd += 1; print("   TEXT diff", f, L)
    # sub-cell names
    n1 = sorted(lib.cell(i).name for i in c1.called_cells()); n2 = sorted(ex.cell(i).name for i in c2.called_cells())
    print("%-14s top cells %s; XOR layers differing: %d; subcell names equal: %s" % (f, tops, nd, n1 == n2))
