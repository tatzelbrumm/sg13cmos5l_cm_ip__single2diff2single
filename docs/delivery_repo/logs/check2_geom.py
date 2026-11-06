# Phase 2 checks 2 and 3: top cells, bboxes, pin texts (KLayout python), .subckt pins
import klayout.db as db, re, sys
R = "/home/user/sg13cmos5l_cm_slot7"
fail = 0
def say(ok, msg):
    global fail
    print(("OK   " if ok else "FAIL ") + msg); fail |= (not ok)
def load(p):
    ly = db.Layout(); ly.read(p); return ly
def texts(ly, top, layer, dt):
    li = ly.find_layer(layer, dt)
    out = []
    if li is None: return out
    it = top.begin_shapes_rec(li)
    while not it.at_end():
        s = it.shape()
        if s.is_text():
            t = s.text.transformed(it.trans())
            out.append((t.string, t.x*ly.dbu, t.y*ly.dbu))
        it.next()
    return out
# slot_7
ly = load(f"{R}/final/gds/slot_7.gds")
tops = [c.name for c in ly.top_cells()]
say(tops == ["slot_7"], f"slot_7.gds top cells = {tops}")
b = ly.top_cells()[0].dbbox()
say((round(b.left,3),round(b.bottom,3),round(b.right,3),round(b.top,3)) == (0,0,537.15,273), f"slot_7 bbox = {b}")
# pin table from slot7_pins.md
pins = {}
for line in open("/home/user/work/src/slot7_pins.md"):
    m = re.match(r"\|\s*(s7_an_\w+)\s*\|[^|]*\|[^|]*\|\s*metal3\s*\|[^|]*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|", line)
    if m: pins[m.group(1)] = tuple(float(m.group(i)) for i in range(2,6))
say(len(pins) == 13, f"slot7_pins.md rows = {len(pins)}")
top = ly.top_cells()[0]
alltxt = []
for li in ly.layer_indexes():
    info = ly.get_info(li)
    for (s,x,y) in texts(ly, top, info.layer, info.datatype):
        alltxt.append((s, info.layer, info.datatype, x, y))
s7 = [t for t in alltxt if t[0].startswith("s7_an_")]
names = sorted(set(t[0] for t in s7))
say(names == sorted(pins), f"slot_7 distinct s7_an_* texts = {len(names)}, equal to table: {names == sorted(pins)}")
for n,(x0,x1,y0,y1) in sorted(pins.items(), key=lambda kv: kv[1][2]):
    ts = [t for t in s7 if t[0] == n]
    m3 = [t for t in ts if (t[1],t[2]) == (30,25) and x0-1e-6 <= t[3] <= x1+1e-6 and y0-1e-6 <= t[4] <= y1+1e-6]
    other = [(l,d,round(x,3),round(y,3)) for (_,l,d,x,y) in ts if (l,d) != (30,25)]
    say(len(m3) == 1 and len([t for t in ts if (t[1],t[2])==(30,25)]) == 1, f"{n}: Metal3 text 30/25 at {[(round(t[3],3),round(t[4],3)) for t in m3]} within x {x0}..{x1} y {y0}..{y1}" + (f"; also on other layers (stand-in stub labels, info only): {other}" if other else ""))
    # metal3 shape (layer 30) covering the pin rect
    reg = db.Region(top.begin_shapes_rec(ly.find_layer(30,0))) if ly.find_layer(30,0) is not None else db.Region()
    pr = db.Region(db.Box(int(round(x0/ly.dbu)),int(round(y0/ly.dbu)),int(round(x1/ly.dbu)),int(round(y1/ly.dbu))))
    say((pr - reg).is_empty(), f"{n}: Metal3 30/0 covers the pin rectangle")
# pads
want = {}
for line in open(f"{R}/final/pads/pads.txt"):
    if line.startswith("#") or not line.strip(): continue
    f = line.split(); want[f[0]] = f[2:]
for cell, plist in want.items():
    ly = load(f"{R}/final/pads/{cell}.gds")
    tops = [c.name for c in ly.top_cells()]
    say(tops == [cell], f"{cell}.gds top cells = {tops}")
    top = ly.top_cells()[0]; b = top.dbbox()
    say((round(b.left,3),round(b.bottom,3),round(b.right,3),round(b.top,3)) == (-0.62,0,80.62,180), f"{cell} bbox = {b}")
    # texts on 10/25 in the top cell only (ports)
    li = ly.find_layer(10,25)
    tt = []
    for s in top.shapes(li).each():
        if s.is_text(): tt.append((s.text.string, s.text.x*ly.dbu, s.text.y*ly.dbu))
    for p in plist:
        hits = [t for t in tt if t[0] == p and 179.715-1e-6 <= t[2] <= 179.74+1e-6]
        say(len(hits) >= 1, f"{cell}: pin {p} on 10/25 at {[(round(x,3),round(y,3)) for (_,x,y) in hits]}")
    xs = [min(t[1] for t in tt if t[0]==p) for p in plist]
    print(f"     {cell}: x of pins in pads.txt order = {[round(x,3) for x in xs]} (monotonic: {xs==sorted(xs) or xs==sorted(xs,reverse=True)})")
    print(f"     {cell}: all top-cell texts on 10/25 = {sorted(set(t[0] for t in tt))}")
    # check 3
    sub = [l for l in open(f"{R}/final/pads/{cell}.spice") if l.startswith(f".subckt {cell} ")][0].split()[2:]
    exp = set(plist) | {"iovdd","iovss","vdd","vss","pad"}
    say(set(sub) == exp and len(sub) == len(exp), f"{cell}.spice .subckt pins {sub} == pads.txt + iovdd iovss vdd vss pad")
print("RESULT", "FAIL" if fail else "PASS"); sys.exit(fail)
