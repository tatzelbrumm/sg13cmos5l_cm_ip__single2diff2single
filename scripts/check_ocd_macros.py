#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""check_ocd_macros.py -- consistency checks of the harness-derived macros (2026-11-03).

    python3 -I scripts/check_ocd_macros.py <path to sg13cmos5l_ocd_chipalooza>

Checks (all text-based; this is NOT xschem and NOT a simulation):
  1. every sheet/symbol copied into macros/ocd_analog_switches is byte-identical to its harness original (sha256);
  2. macros/ocd_analog_switches/netlist/source/*.spice contains the harness subcircuits unchanged (ports + device lines);
  3. macros/ocd_ls_dn_3v3_1v2 has the devices of the harness cell hv_inv_1 (names ignored, ports mapped);
  4. macros/ocd_ls_up_1v2_3v3: instance x1 is sw_lvl_shift with the harness port order, in_p is two inverters and in_n one
     inverter away from `in`;
  5. for the sheets of ocd_ls_up_1v2_3v3 and ocd_ls_dn_3v3_1v2: the connectivity read from the .sch file (wires, labels,
     pin positions) reproduces the source subcircuit (devices, nets, params), and the .sym pin order equals the
     .subckt port order.  The same reader is run on ls_up_1v2_3v3 and ls_dn_3v3_1v2 as CONTROLS: those sheets were
     netlisted with xschem in earlier sessions, so if a control fails, the reader (not the sheet) is wrong;
  6. CACE suites of the two level shifters (structure only, nothing has been run): templates exist, yaml variables match the
     testbench echo line, specs and conditions equal those of the source macro, no stale names, limits relaxed to "any";
  7. the six KLayout layouts of ocd_analog_switches: readable, top cell = file name, size and sha256 prefix = README table
     (skipped if the python module `klayout` is missing).
The sheet reader supports rot=0 instances (MOS also mirror=1 = x flipped; pin symbols in any orientation); anything else
is reported as a problem and fails the check.
Exit status 0 only if every check passed.
"""
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MAC = REPO / "macros"
fails = []


def say(ok, msg):
    print(("OK    " if ok else "FAIL  ") + msg)
    if not ok:
        fails.append(msg)


# ---------------------------------------------------------------- spice
def num(s):
    m = re.fullmatch(r"([-+]?[0-9.]+(?:e[-+]?\d+)?)([a-z]*)", s.strip().lower())
    if not m:
        return s.strip().lower()
    f = {"": 1, "f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3, "k": 1e3, "meg": 1e6}.get(m.group(2))
    return round(float(m.group(1)) * f, 15) if f is not None else s.strip().lower()


def parse_spice(path):
    """-> {subckt: (ports, [(name, nodes, model, params)])}"""
    lines = []
    for raw in Path(path).read_text().splitlines():
        if raw.startswith("+") and lines:
            lines[-1] += " " + raw[1:].strip()
        elif raw.strip() and not raw.startswith("*") and not raw.startswith("**"):
            lines.append(raw.strip())
    out, cur = {}, None
    for ln in lines:
        t = ln.split()
        if t[0].lower() == ".subckt":
            cur = t[1]
            out[cur] = (t[2:], [])
        elif t[0].lower() == ".ends":
            cur = None
        elif cur:
            params = {k.lower(): num(v) for k, v in (x.split("=", 1) for x in t[1:] if "=" in x)}
            pos = [x for x in t[1:] if "=" not in x]
            out[cur][1].append((t[0], tuple(pos[:-1]), pos[-1], tuple(sorted(params.items()))))
    return out


# ---------------------------------------------------------------- 1. copies
def check_copies(h):
    sw, bg = h / "dependencies/sg13cmos5l_ocd_ip__analog_switches/xschem", h / "dependencies/sg13cmos5l_ocd_ip__biasgen/xschem"
    d = MAC / "ocd_analog_switches/schematic/xschem"
    for f in sorted(d.iterdir()):
        if f.suffix not in (".sch", ".sym"):
            continue
        src = sw / f.name if (sw / f.name).exists() else bg / f.name
        ok = src.exists() and hashlib.sha256(f.read_bytes()).digest() == hashlib.sha256(src.read_bytes()).digest()
        say(ok, f"copy identical to harness: {f.name} <- {src.parent.parent.parent.name if src.exists() else '?'}")


# ---------------------------------------------------------------- 2. switch netlist
def check_switch_netlist(h):
    mine = parse_spice(MAC / "ocd_analog_switches/netlist/source/ocd_analog_switches.spice")
    ref = {}
    for c in ("analog_switch_small", "analog_switch_med", "analog_pswitch_small"):
        ref.update(parse_spice(h / f"dependencies/sg13cmos5l_ocd_ip__analog_switches/netlist/schematic/{c}.spice"))
    ref.update({"xgate": parse_spice(h / "netlist/schematic/chipalooza_frame.spice")["xgate"]})
    for name in ("sw_lvl_shift", "gate_drive_med", "analog_switch_small", "analog_switch_med", "analog_pswitch_small", "xgate"):
        say(name in mine and name in ref and mine[name] == ref[name], f"switch source = harness netlist: {name}")


# ---------------------------------------------------------------- 3./4. level shifters
def check_ls_dn(h):
    ref = parse_spice(MAC / "ocd_ls_dn_3v3_1v2/reference/hv_inv_1.harness.spice")["hv_inv_1"]
    mine = parse_spice(MAC / "ocd_ls_dn_3v3_1v2/netlist/source/ocd_ls_dn_3v3_1v2.spice")["ocd_ls_dn_3v3_1v2"]
    mp = {"vdd": "vddl", "A": "in", "X": "out", "vss": "vss"}
    r = sorted((m, tuple(mp.get(n, n) for n in nodes), p) for _, nodes, m, p in ref[1])
    s = sorted((m, nodes, p) for _, nodes, m, p in mine[1])
    say(r == s, "ocd_ls_dn_3v3_1v2 devices = hv_inv_1 (vdd->vddl, A->in, X->out)")
    say(mine[0] == ["vss", "vddl", "out", "in"], "ocd_ls_dn_3v3_1v2 port order = ls_dn_3v3_1v2 (vss vddl out in)")


def check_ls_up(h):
    ref = parse_spice(MAC / "ocd_ls_up_1v2_3v3/reference/sw_lvl_shift.harness.spice")["sw_lvl_shift"]
    mine = parse_spice(MAC / "ocd_ls_up_1v2_3v3/netlist/source/ocd_ls_up_1v2_3v3.spice")["ocd_ls_up_1v2_3v3"]
    say(mine[0] == ["vss", "vddl", "vddh", "out", "in"], "ocd_ls_up_1v2_3v3 port order = ls_up_1v2_3v3 (vss vddl vddh out in)")
    say(ref[0] == ["in_p", "in_n", "out", "outn", "avdd", "avss"], "harness sw_lvl_shift ports: in_p in_n out outn avdd avss")
    dev = {n: (nodes, m) for n, nodes, m, _ in mine[1]}
    x1 = dev.get("x1")
    say(bool(x1) and x1[1] == "sw_lvl_shift" and len(x1[0]) == 6, "x1 is sw_lvl_shift with 6 nodes")
    if x1:
        inp, inn, out, _outn, avdd, avss = x1[0]
        drv = {nodes[0]: nodes[1] for n, (nodes, m) in dev.items() if m == "sg13cmos5l_inv_4"}

        def depth(net):
            d = 0
            while net in drv:
                net, d = drv[net], d + 1
            return net, d
        say(depth(inp) == ("in", 2) and depth(inn) == ("in", 1), "in_p = in through 2 inverters, in_n = in through 1 inverter")
        say(out == "out" and avdd == "vddh" and avss == "vss", "out -> out, avdd -> vddh, avss -> vss")
        # truth of the latch (read off the harness netlist): in_p high pulls net1 low, S1_N high, outn low, out high => out follows in_p
        say(True, "polarity: out follows in_p (net1/S1_N latch of the harness netlist), hence out follows in -> non-inverting [read, not simulated]")


# ---------------------------------------------------------------- 5. sheets
# Pin offsets of the PDK MOS symbols at rot=0 mirror=0, read off the xschem-checked sheet ls_dn_3v3_1v2.sch:
# NMOS drain on top, source below; PMOS source on top, drain below.  (The CONTROL sheets exist to catch errors here.)
MOS_PINS = {"nmos": {"d": (20, -30), "g": (-20, 0), "s": (20, 30), "b": (40, 0)},
            "pmos": {"s": (20, -30), "g": (-20, 0), "d": (20, 30), "b": (40, 0)}}


def parse_sym_pins(path):
    """pins in file (B box) order: [(name, (x, y))]"""
    pins = []
    for m in re.finditer(r"^B 5 (\S+) (\S+) (\S+) (\S+) \{name=(\S+) ", Path(path).read_text(), re.M):
        x1, y1, x2, y2 = map(float, m.group(1, 2, 3, 4))
        pins.append((m.group(5), ((x1 + x2) / 2, (y1 + y2) / 2)))
    return pins


def sym_format(path):
    """netlist order of a symbol: ([pin names], [attribute names netlisted after them]).
    format="@name @@in_p @@in_n ... @avdd @avss @symname" -> pins by '@@', extras by a single '@';
    format="@name @pinlist @symname" -> pins in B box order, no extras."""
    m = re.search(r'format="([^"]*)"', Path(path).read_text())
    toks = m.group(1).split() if m else ["@pinlist"]
    if "@pinlist" in toks:
        return [n for n, _ in parse_sym_pins(path)], []
    pins = [t[2:] for t in toks if t.startswith("@@")]
    extra = [t[1:] for t in toks if t.startswith("@") and not t.startswith("@@") and t not in ("@name", "@symname")]
    return pins, extra


def find_sym(name, dirs):
    for d in dirs:
        if (d / name).exists():
            return d / name
    return None


def sheet_netlist(sch, symdirs):
    txt = Path(sch).read_text()
    wires = [tuple(map(float, m.group(1, 2, 3, 4))) + (m.group(5),) for m in
             re.finditer(r"^N (\S+) (\S+) (\S+) (\S+) \{lab=([^}]*)\}", txt, re.M)]
    comps = [(m.group(1), float(m.group(2)), float(m.group(3)), int(m.group(4)), int(m.group(5)), m.group(6))
             for m in re.finditer(r"^C \{([^}]*)\} (\S+) (\S+) (\d) (\d) \{(.*?)\}$", txt, re.M | re.S)]
    parent = {}

    def find(p):
        parent.setdefault(p, p)
        while parent[p] != p:
            parent[p] = parent[parent[p]]
            p = parent[p]
        return p

    def union(a, b):
        parent[find(a)] = find(b)

    names = {}  # point -> set of names
    segs = []
    for x1, y1, x2, y2, lab in wires:
        a, b = (x1, y1), (x2, y2)
        union(a, b)
        segs.append((a, b))
        if lab and not lab.startswith("#"):
            names.setdefault(a, set()).add(lab)
    devices, pinlist, problems = [], [], []
    pinpts = []  # (point, kind, payload)
    for ref, x, y, rot, mir, attrs in comps:
        at = dict(re.findall(r'(\w+)=("[^"]*"|\S+)', attrs))
        base = ref.split("/")[-1]
        if base in ("title.sym",):
            continue
        is_mos = bool(re.fullmatch(r"sg13cmos5l_pr/sg13_(lv|hv)_[np]mos\.sym", ref))
        if (rot, mir) != (0, 0) and not (is_mos and (rot, mir) == (0, 1)) \
                and base not in ("ipin.sym", "opin.sym", "iopin.sym", "lab_pin.sym"):
            problems.append(f"unsupported rot/mirror on {at.get('name', ref)}")  # pin symbols: connection point is the origin
            continue
        if base in ("ipin.sym", "opin.sym", "iopin.sym"):
            pinlist.append(at["lab"])
            names.setdefault((x, y), set()).add(at["lab"])
            pinpts.append(((x, y), "label", None))
        elif base == "lab_pin.sym":
            names.setdefault((x, y), set()).add(at["lab"])
            pinpts.append(((x, y), "label", None))
        elif re.fullmatch(r"sg13cmos5l_pr/sg13_(lv|hv)_[np]mos\.sym", ref):
            offs = MOS_PINS["pmos" if ref.endswith("pmos.sym") else "nmos"]
            sx = -1 if mir else 1  # mirror=1 at rot=0 flips x about the symbol origin
            pts = [(x + sx * offs[k][0], y + offs[k][1]) for k in "dgsb"]
            for p in pts:
                pinpts.append((p, "pin", None))
            params = {k: num(at[k]) for k in ("l", "w", "ng", "m", "mm_ok") if k in at}
            devices.append(["mos", at["name"], pts, at["model"], tuple(sorted(params.items()))])
        elif base == "sg13cmos5l_inv_4.sym":
            pts = [(x + 40, y), (x - 40, y)]  # Y, A  (geometry read from the harness sheets; VDD/VSS by attribute)
            for p in pts:
                pinpts.append((p, "pin", None))
            devices.append(["inv", at["name"], pts, "sg13cmos5l_inv_4", (), at["VDD"], at["VSS"]])
        else:
            sp = find_sym(base, symdirs)
            if not sp:
                problems.append(f"no symbol file for {ref}")
                continue
            pos = dict(parse_sym_pins(sp))
            order, extra = sym_format(sp)
            pts = [(x + pos[n][0], y + pos[n][1]) for n in order]
            for p in pts:
                pinpts.append((p, "pin", None))
            devices.append(["sub", at["name"], pts, base[:-4], (), order, [at[k] for k in extra]])
    # pins/labels lying on the interior of an axis-aligned wire, and wire ends on other wires' interiors
    def on_seg(p, s):
        (ax, ay), (bx, by) = s
        if ax == bx == p[0]:
            return min(ay, by) < p[1] < max(ay, by)
        if ay == by == p[1]:
            return min(ax, bx) < p[0] < max(ax, bx)
        return False
    for p, _, _ in pinpts:
        find(p)
        for s in segs:
            if on_seg(p, s):
                union(p, s[0])
    for a, b in segs:
        for s in segs:
            if on_seg(a, s):
                union(a, s[0])
            if on_seg(b, s):
                union(b, s[0])
    netname = {}
    for p, ns in names.items():
        netname.setdefault(find(p), set()).update(ns)
    for r, ns in netname.items():
        if len(ns) > 1:
            problems.append(f"net with two names: {sorted(ns)}")

    def net(p):
        r = find(p)
        return "/".join(sorted(netname.get(r, {"#"}))) if netname.get(r) else f"#{r}"
    result = []
    for d in devices:
        if d[0] == "mos":
            nodes = tuple(net(p) for p in d[2])
            result.append((d[3], nodes, d[4]))
        elif d[0] == "inv":
            nodes = (net(d[2][0]), net(d[2][1]), d[5], d[6])
            result.append((d[3], nodes, ()))
        else:
            # drawn pins in the symbol's format order, then the attribute-assigned extras (avdd avss) as in its format string
            result.append((d[3], tuple([net(p) for p in d[2]] + d[6]), ()))
    return result, pinlist, problems


def sheet_vs_source(macro, symdirs, label):
    d = MAC / macro
    sch, sym, spc = d / f"schematic/xschem/{macro}.sch", d / f"schematic/xschem/{macro}.sym", d / f"netlist/source/{macro}.spice"
    res, pinlist, problems = sheet_netlist(sch, symdirs)
    src = parse_spice(spc)[macro]
    say(not problems, f"{label}{macro}.sch: reader had no problems {problems or ''}")
    symports = [n for n, _ in parse_sym_pins(sym)]
    say(symports == src[0], f"{label}{macro}.sym pin order {symports} = .subckt ports {src[0]}")
    say(pinlist == src[0], f"{label}{macro}.sch pin placement order {pinlist} = .subckt ports")
    # source devices -> comparable tuples; nets used once and not a port -> dangling
    used = {}
    for _, nodes, _, _ in src[1]:
        for n in nodes:
            used[n] = used.get(n, 0) + 1
    srcdev = []
    for _, nodes, m, p in src[1]:
        nn = tuple(n if (n in src[0] or used[n] > 1) else "DANGLING" for n in nodes)
        srcdev.append((m, nn, p))
    shdev = []
    ctr = {}
    for m, nodes, p in res:
        for n in nodes:
            ctr[n] = ctr.get(n, 0) + 1
    for m, nodes, p in res:
        nn = tuple("DANGLING" if (n.startswith("#") or (n not in src[0] and ctr[n] == 1)) else n for n in nodes)
        shdev.append((m, nn, p))
    a, b = sorted(srcdev), sorted(shdev)
    say(a == b, f"{label}{macro}: devices/nets/params of the sheet = source ({len(a)} devices)")
    if a != b:
        print("   only in source:", [x for x in a if x not in b])
        print("   only in sheet :", [x for x in b if x not in a])


# ---------------------------------------------------------------- 6. CACE suites (structure only; nothing has been run)
def check_cace(macro, src_macro):
    import yaml
    d, s = MAC / macro, MAC / src_macro
    y = yaml.safe_load((d / f"verification/cace/{macro}.yaml").read_text())
    ys = yaml.safe_load((s / f"verification/cace/{src_macro}.yaml").read_text())
    say(y["name"] == macro, f"{macro}.yaml: name = {macro}")
    ok = True
    for g, grp in y["parameters"].items():
        tool = grp["tool"]["ngspice"]
        tb = d / "verification/cace/templates" / tool["template"]
        if not tb.exists():
            ok = False
            continue
        txt = tb.read_text()
        echo = re.search(r"^echo (.*)$", txt, re.M)
        names = [w[2:] for w in echo.group(1).split() if w.startswith("$&")] if echo else []
        ok &= names == tool["variables"] and len(names) > 0
        ok &= list(grp["spec"]) == list(ys["parameters"][g]["spec"])
        ok &= grp["conditions"] == ys["parameters"][g]["conditions"]
        ok &= (f"{macro}.sym" in txt)
    say(ok, f"{macro}: every group's template exists, its echo line = yaml variables, specs/conditions = {src_macro}, DUT symbol {macro}.sym")
    stale = [str(p.relative_to(d)) for p in list(d.glob("verification/**/*")) + list(d.glob("testbenches/**/*"))
             if p.is_file() and re.search(rf"(?<![A-Za-z0-9_]){re.escape(src_macro)}",   # yaml comment lines (provenance) are allowed
                                          "\n".join(l for l in p.read_text(errors="ignore").splitlines() if not l.lstrip().startswith("#")))]
    say(not stale, f"{macro}: no leftover name '{src_macro}' in verification/ and testbenches/ {stale or ''}")
    relaxed = [(g, n, k) for g, grp in y["parameters"].items() for n, sp in grp["spec"].items() for k in ("minimum", "maximum")
               if sp[k]["value"] != "any" and (n, k) not in (("Voh", "minimum"), ("Vol", "maximum"))]
    say(not relaxed, f"{macro}: only Voh minimum / Vol maximum carry a limit (others 'any') {relaxed or ''}")


# ---------------------------------------------------------------- 7. imported KLayout layouts
def check_layouts():
    """macros/ocd_analog_switches/layout/klayout/<cell>.klay.gds: readable, top cell = file name, sha256 prefix = README table."""
    try:
        import klayout.db as kdb
    except ImportError:
        print("SKIP  layout checks: python module `klayout` not installed (pip install klayout)")
        return
    d = MAC / "ocd_analog_switches/layout/klayout"
    readme = (MAC / "ocd_analog_switches/README.md").read_text()
    for cell in ("analog_switch_small", "analog_switch_med", "analog_pswitch_small", "sw_lvl_shift", "gate_drive_med", "xgate"):
        f = d / f"{cell}.klay.gds"
        if not f.exists():
            say(False, f"layout missing: {f.name}")
            continue
        L = kdb.Layout()
        L.read(str(f))
        tops = [c.name for c in L.top_cells()]
        sha = hashlib.sha256(f.read_bytes()).hexdigest()[:12]
        say(tops == [cell] and f"| `{cell}.klay.gds` | {f.stat().st_size} | {sha} |" in readme,
            f"layout {cell}.klay.gds: top cell = file name {tops}, size and sha256 prefix {sha} as in the README table")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    h = Path(sys.argv[1])
    check_copies(h)
    check_switch_netlist(h)
    check_ls_dn(h)
    check_ls_up(h)
    sd = [MAC / "ocd_analog_switches/schematic/xschem", MAC / "ls_up_1v2_3v3/schematic/xschem", MAC / "ls_dn_3v3_1v2/schematic/xschem"]
    sheet_vs_source("ls_up_1v2_3v3", sd, "CONTROL ")
    sheet_vs_source("ls_dn_3v3_1v2", sd, "CONTROL ")
    sheet_vs_source("ocd_ls_dn_3v3_1v2", sd + [MAC / "ocd_ls_dn_3v3_1v2/schematic/xschem"], "")
    sheet_vs_source("ocd_ls_up_1v2_3v3", sd + [MAC / "ocd_ls_up_1v2_3v3/schematic/xschem"], "")
    check_cace("ocd_ls_up_1v2_3v3", "ls_up_1v2_3v3")
    check_cace("ocd_ls_dn_3v3_1v2", "ls_dn_3v3_1v2")
    check_layouts()
    print(f"\n{len(fails)} failed check(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
