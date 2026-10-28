# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""backannotate.py: layout-driven backannotation of a schematic (xschem) from the layout's extracted devices.
Written 2026-10-28 by Claude (Opus 5.5).

    python3 backannotate.py <layout.gds> <top cell> <sheet.sch> <sheet netlist.spice> <out dir>
                            [--subckt-name oa_core_pd] [--ports "vdd vss iout en_3v3 en_3v3_b"] [--no-dummies]
                            [--note "text"]... [--xschemrc rcfile]

Topology comes from the sheet, sizes from the layout:
  1. sheet devices from the sheet's netlist (X<name> d g s b model w= l= ng= m=);
  2. layout devices from a flat extraction (--extractor: a process-specific module with extract(); uncombined: one
     device per finger);
  3. every layout finger is assigned to a sheet device by its terminal nets (type, gate, {drain, source}, bulk):
     parallel fingers -> one sheet device (W summed, ng = finger count); fingers chained through nets that the
     sheet does not have -> a series split of one sheet device (e.g. MS1 = 8 x 0.5/12.5); fingers with drain =
     source -> dummies; anything else is an ERROR (topology differs from the sheet: fix the layout, not the sheet);
  4. writes <out>/<sheet>.sch (parameters edited in place; series splits replace their device by a chain drawn
     with net labels; dummies in a box of their own), <out>/<subckt>_subckt.spice (hand-netlist text),
     <out>/device_changes.txt (old -> new per device, the ratios that matter, notes);
  5. netlists the new sheet with xschem (if available) and checks it device by device against the subckt text.
LVS of the layout against the new sheet's netlist is then the closing check (run separately, lvs.py).
"""
import argparse
import collections
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def num(v):
    """'2u' -> 2.0 (um), '0.45u' -> 0.45, '1' -> 1."""
    v = v.strip().lower()
    mult = {"u": 1.0, "n": 1e-3, "m": 1e3, "p": 1e-6}
    if v and v[-1] in mult:
        return float(v[:-1]) * mult[v[-1]]
    return float(v)


def fmt(x):
    s = ("%.4f" % x).rstrip("0").rstrip(".")
    return s + "u"


def sheet_devices(netlist):
    devs = collections.OrderedDict()
    for line in open(netlist):
        t = line.split()
        if not t or not t[0].upper().startswith("X"):
            continue
        p = dict(a.split("=", 1) for a in t[6:] if "=" in a)
        devs[t[0][1:]] = dict(d=t[1].lower(), g=t[2].lower(), s=t[3].lower(), b=t[4].lower(), model=t[5],
                              w=num(p["w"]), l=num(p["l"]), ng=int(float(p.get("ng", 1))), m=int(float(p.get("m", 1))))
    return devs


def layout_devices(gds, cell, sheet_nets, extractor="lvs"):
    """extractor: a module (on sys.path, or a file path) with extract(gds, cell, labels, combine=False) returning
    (LayoutToNetlist-like object with netlist(), layout, n); process specific, e.g. ../ihp_sg13cmos5l/tools/lvs.py."""
    import importlib
    import importlib.util
    if extractor.endswith(".py"):
        spec = importlib.util.spec_from_file_location("extractor", extractor)
        LVS = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(LVS)
    else:
        LVS = importlib.import_module(extractor)
    lv, ly, _ = LVS.extract(gds, cell, "all", combine=False)
    c = lv.netlist().circuit_by_name(cell)
    out = []

    def nm(net):
        names = [x.lower() for x in (net.name or "").split(",") if x]
        for x in names:
            if x in sheet_nets:
                return x
        return names[0] if names else "$%d" % net.cluster_id
    for d in c.each_device():
        out.append(dict(model=d.device_class().name, d=nm(d.net_for_terminal("D")), g=nm(d.net_for_terminal("G")),
                        s=nm(d.net_for_terminal("S")), b=nm(d.net_for_terminal("B")), w=d.parameter("W"),
                        l=d.parameter("L")))
    return out


def assign(sheet, fingers, ties=None):
    """assign_once, plus: unlabelled layout nets ($N, e.g. a node internal to a primitive) are mapped to the sheet
    nets no layout label carries; every permutation is tried and only one without errors is accepted."""
    import itertools
    sheet_nets = set()
    for s in sheet.values():
        sheet_nets |= {s["d"], s["g"], s["s"], s["b"]}
    seen = set()
    for f in fingers:
        seen |= {f["d"], f["g"], f["s"], f["b"]}
    unnamed = sorted(n for n in seen if n.startswith("$"))
    missing = sorted(sheet_nets - seen - set((ties or {}).values()))
    best = assign_once(sheet, fingers, ties)
    if not best[2] or not unnamed or not missing or len(missing) > 4:
        return best
    for perm in itertools.permutations(unnamed, len(missing)):     # which unlabelled net is which missing one
        m = dict(zip(perm, missing))
        fs = [dict(f, **{t: m.get(f[t], f[t]) for t in "dgsb"}) for f in fingers]
        r = assign_once(sheet, fs, ties)
        if not r[2]:
            print("unlabelled layout nets mapped to sheet nets: %s" % m)
            return r
    return best


def assign_once(sheet, fingers, ties=None):
    """Returns (assignments {sheet device: dict}, dummies list, errors list)."""
    ties = ties or {}
    sheet_nets = set()
    for s in sheet.values():
        sheet_nets |= {s["d"], s["g"], s["s"], s["b"]}
    key = lambda m, d, g, s, b: (m, g, frozenset((d, s)), b)
    by_key = collections.defaultdict(list)
    for name, s in sheet.items():
        by_key[key(s["model"], s["d"], s["g"], s["s"], s["b"])].append(name)
    res = {n: dict(par=[], chain=None) for n in sheet}
    dummies, rest, errors = [], [], []
    for f in fingers:
        f = dict(f)
        f["b"] = ties.get(f["b"], f["b"])
        if f["d"] == f["s"]:
            dummies.append(f)
            continue
        k = key(f["model"], f["d"], f["g"], f["s"], f["b"])
        if k in by_key and len(by_key[k]) == 1:
            res[by_key[k][0]]["par"].append(f)
        elif k in by_key:
            errors.append("two sheet devices with the same terminals %s: %s" % (by_key[k], f))
        else:
            rest.append(f)
    # series chains through nets the sheet does not have
    internal = lambda n: n not in sheet_nets
    used = set()
    for name, s in sheet.items():
        if res[name]["par"]:
            continue
        cand = [f for i, f in enumerate(rest) if f["model"] == s["model"] and f["g"] == s["g"] and f["b"] == s["b"]]
        start = [f for f in cand if s["s"] in (f["d"], f["s"]) and (internal(f["d"]) or internal(f["s"]))]
        for st in start:
            chain, node = [st], (st["d"] if st["s"] == s["s"] else st["s"])
            while internal(node):
                nxt = [f for f in cand if f not in chain and node in (f["d"], f["s"])]
                if len(nxt) != 1:
                    break
                f = nxt[0]
                chain.append(f)
                node = f["s"] if f["d"] == node else f["d"]
            if node == s["d"]:
                res[name]["chain"] = chain
                used |= {id(f) for f in chain}
                break
    for f in rest:
        if id(f) not in used:
            errors.append("layout device not in the sheet: %s" % f)
    for name in sheet:
        if not res[name]["par"] and not res[name]["chain"]:
            errors.append("sheet device %s not found in the layout" % name)
    return res, dummies, errors


def new_params(s, r):
    if r["chain"]:
        ls = [f["l"] for f in r["chain"]]
        return dict(kind="series", n=len(ls), w=r["chain"][0]["w"], l_each=ls, l=sum(ls), ng=1)
    ws = [f["w"] for f in r["par"]]
    ls = {round(f["l"], 4) for f in r["par"]}
    return dict(kind="parallel", w=sum(ws), l=r["par"][0]["l"], ng=len(ws), w_finger=sorted(set(round(w, 4) for w in ws)),
                l_set=sorted(ls))


def group_dummies(dummies):
    g = collections.OrderedDict()
    for f in dummies:
        k = (f["model"], f["d"], f["g"], f["b"], round(f["l"], 4))
        g.setdefault(k, []).append(f)
    return [dict(model=k[0], d=k[1], s=k[1], g=k[2], b=k[3], l=k[4], w=sum(f["w"] for f in v), ng=len(v),
                 w_finger=sorted(set(round(f["w"], 4) for f in v))) for k, v in g.items()]


# ---- sheet editing (xschem .sch) ---------------------------------------------------------------------------
INST = re.compile(r"^C \{(?P<sym>[^}]+)\} (?P<x>-?[\d.]+) (?P<y>-?[\d.]+) (?P<rot>\d) (?P<flip>\d) \{(?P<attr>.*?)\}",
                  re.S | re.M)
PINS = {"pmos": {"d": (20, 30), "g": (-20, 0), "s": (20, -30), "b": (20, 0)},
        "nmos": {"d": (20, -30), "g": (-20, 0), "s": (20, 30), "b": (20, 0)}}


def set_attr(attr, k, v):
    if re.search(r"(^|\n)%s=" % k, attr):
        return re.sub(r"(^|\n)%s=[^\n]*" % k, lambda m: "%s%s=%s" % (m.group(1), k, v), attr)
    return attr + "\n%s=%s" % (k, v)


def inst_text(sym, x, y, attrs):
    return "C {%s} %d %d 0 0 {%s}" % (sym, x, y, "\n".join("%s=%s" % kv for kv in attrs))


def label(x, y, net, idx, rot=0):
    return "C {devices/lab_pin.sym} %d %d %d 0 {name=lba%d sig_type=std_logic lab=%s}" % (x, y, rot, idx, net)


def device_block(name, model, d, g, s, b, w, l, ng, x, y, lab0, sym):
    """sym: the sheet's own symbol of this model (taken from an existing instance); PINS assumes the usual 4-terminal
    MOS symbol (D / S at +-30 on the right, G at -20, B at +20); override PINS for another symbol library."""
    kind = "pmos" if "pmos" in model else "nmos"
    txt = [inst_text(sym, x, y, [("name", name), ("l", fmt(l)), ("w", fmt(w)), ("ng", ng), ("m", 1), ("mm_ok", 1),
                                 ("model", model), ("spiceprefix", "X")])]
    i = lab0
    for term, net in (("d", d), ("g", g), ("s", s), ("b", b)):
        dx, dy = PINS[kind][term]
        txt.append(label(x + dx, y + dy, net, i, 2 if term == "g" else 0))
        i += 1
    return txt, i


def edit_sheet(src, dst, sheet, res, dummies, notes, with_dummies=True):
    text = open(src).read()
    sym_of = {}
    for m in INST.finditer(text):
        mm = re.search(r"model=(\S+)", m.group("attr"))
        if mm:
            sym_of.setdefault(mm.group(1), m.group("sym"))
    out, pos = [], 0
    extra, lab = [], 1000
    x0, y0 = 1100, -1050
    col = 0
    for m in INST.finditer(text):
        attr = m.group("attr")
        nm_ = re.search(r"name=(\S+)", attr)
        name = nm_.group(1) if nm_ else None
        out.append(text[pos:m.start()])
        pos = m.end()
        if name in res and name in sheet:
            p = new_params(sheet[name], res[name])
            if p["kind"] == "parallel":
                a = set_attr(set_attr(set_attr(attr, "w", fmt(p["w"])), "l", fmt(p["l"])), "ng", str(p["ng"]))
                out.append("C {%s} %s %s %s %s {%s}" % (m.group("sym"), m.group("x"), m.group("y"), m.group("rot"),
                                                         m.group("flip"), a))
            else:   # series split: the device is replaced by a chain drawn with labels in the [B] box
                s = sheet[name]
                nodes = [s["s"]] + ["%s_%d" % (name.lower(), i + 1) for i in range(p["n"] - 1)] + [s["d"]]
                for i in range(p["n"]):
                    t, lab = device_block("%s_%d" % (name, i), s["model"], nodes[i + 1], s["g"], nodes[i], s["b"],
                                          p["w"], p["l_each"][i], 1, x0 + 140 * col, y0 + 100 * i, lab,
                                          sym_of[s["model"]])
                    extra += t
                col += 1
                out.append("T {%s: replaced by the %d-device series chain %s_0 ... %s_%d in the [B] box} %s %s 0 0 0.2 0.2 {}"
                           % (name, p["n"], name, name, p["n"] - 1, m.group("x"), m.group("y")))
        else:
            out.append(m.group(0))
    out.append(text[pos:])
    if with_dummies:
        for i, dm in enumerate(dummies):
            t, lab = device_block("MDUM%d" % i, dm["model"], dm["d"], dm["g"], dm["s"], dm["b"], dm["w"], dm["l"],
                                  dm["ng"], x0 + 140 * (col + i), y0, lab, sym_of[dm["model"]])
            extra += t
    if extra:
        extra.insert(0, "T {[B] layout-driven backannotation (series splits, dummies): see device_changes.txt} %d %d 0 0 0.3 0.3 {layer=10}"
                     % (x0 - 20, y0 - 90))
        for k, n in enumerate(notes):
            extra.append("T {%s} %d %d 0 0 0.25 0.25 {}" % (n.replace("{", "(").replace("}", ")"), x0 - 20, y0 - 60 + 22 * k))
    body = "".join(out).rstrip("\n") + "\n" + "\n".join(extra) + "\n"
    open(dst, "w").write(body)


# ---- text outputs --------------------------------------------------------------------------------------------
def subckt_text(name, ports, sheet, res, dummies, with_dummies=True):
    L = [".subckt %s %s" % (name, " ".join(ports))]
    for n, s in sheet.items():
        p = new_params(s, res[n])
        if p["kind"] == "parallel":
            L.append("X%s %s %s %s %s %s w=%s l=%s ng=%d" % (n, s["d"], s["g"], s["s"], s["b"], s["model"], fmt(p["w"]),
                                                          fmt(p["l"]), p["ng"]))
        else:
            nodes = [s["s"]] + ["%s_%d" % (n.lower(), i + 1) for i in range(p["n"] - 1)] + [s["d"]]
            for i in range(p["n"]):
                L.append("X%s_%d %s %s %s %s %s w=%s l=%s ng=1" % (n, i, nodes[i + 1], s["g"], nodes[i], s["b"], s["model"],
                                                                  fmt(p["w"]), fmt(p["l_each"][i])))
    if with_dummies:
        for i, dm in enumerate(dummies):
            L.append("XMDUM%d %s %s %s %s %s w=%s l=%s ng=%d" % (i, dm["d"], dm["g"], dm["s"], dm["b"], dm["model"],
                                                               fmt(dm["w"]), fmt(dm["l"]), dm["ng"]))
    L.append(".ends %s" % name)
    return "\n".join(L) + "\n"


def changes_text(sheet, res, dummies, notes, ratios=()):
    L = ["device changes, layout -> sheet (W, L in um; ng = fingers; series = devices in series)",
         "%-6s %-14s %-34s %-34s %s" % ("dev", "type", "sheet (old)", "layout (new)", "effect")]
    newp = {}
    for n, s in sheet.items():
        p = new_params(s, res[n])
        newp[n] = p
        old = "w=%s l=%s ng=%d m=%d" % (fmt(s["w"]), fmt(s["l"]), s["ng"], s["m"])
        if p["kind"] == "parallel":
            new = "w=%s l=%s ng=%d (%s/finger)" % (fmt(p["w"]), fmt(p["l"]), p["ng"], "+".join(fmt(w) for w in p["w_finger"]))
            same_wl = abs(p["w"] - s["w"] * s["m"]) < 1e-6 and abs(p["l"] - s["l"]) < 1e-6
            eff = "none (W, L as sheet)" + ("" if p["ng"] == s["ng"] else "; finger split only") if same_wl else \
                "W/L %.4g -> %.4g" % (s["w"] * s["m"] / s["l"], p["w"] / p["l"])
        else:
            new = "%d x w=%s l=%s in series" % (p["n"], fmt(p["w"]), "+".join(sorted(set(fmt(x) for x in p["l_each"]))))
            eff = "W/L %.4g as one %s/%s device (series of equal gates ~ one long device; internal nodes added)" % (
                p["w"] / p["l"], fmt(p["w"]), fmt(p["l"])) if abs(p["l"] - s["l"]) < 1e-6 and abs(p["w"] - s["w"]) < 1e-6 \
                else "W/L %.4g -> %.4g" % (s["w"] / s["l"], p["w"] / p["l"])
        L.append("%-6s %-14s %-34s %-34s %s" % (n, s["model"], old, new, eff))
    for i, dm in enumerate(dummies):
        L.append("%-6s %-14s %-34s %-34s %s" % ("MDUM%d" % i, dm["model"], "(not in the sheet)",
                                               "w=%s l=%s ng=%d (%s/finger)" % (fmt(dm["w"]), fmt(dm["l"]), dm["ng"],
                                                                                "+".join(fmt(w) for w in dm["w_finger"])),
                                               "dummy D=S=%s G=%s B=%s: gate load %.3g um2 on %s" % (
                                                   dm["d"], dm["g"], dm["b"], dm["w"] * dm["l"], dm["g"])))
    L.append("")
    L.append("ratios that set the circuit (sheet -> layout):")
    for title, names in ratios:
        if not all(n in sheet for n in names):
            continue
        so = [sheet[n]["w"] * sheet[n]["m"] / (sheet[n]["l"] if "W/L" in title else 1) for n in names]
        sn = [newp[n]["w"] / (newp[n]["l"] if "W/L" in title else 1) for n in names]
        r = lambda v: " : ".join("%.4g" % (x / v[-1]) for x in v)
        L.append("  %-50s %-24s %-24s %s" % (title, r(so), r(sn), "kept" if all(abs(a / so[-1] - b / sn[-1]) < 1e-6
                                                                                for a, b in zip(so, sn)) else "CHANGED"))
    if notes:
        L.append("")
        L.append("layout notes (no device change):")
        L += ["  - " + n for n in notes]
    return "\n".join(L) + "\n"


def compare_text(a, b):
    """device-by-device comparison of two netlist texts (X/M lines: name, nets, w, l)."""
    def parse(t):
        out = {}
        for line in t.splitlines():
            x = line.split()
            if not x or x[0][0].upper() not in "XM" or x[0].startswith("**"):
                continue
            p = dict(a.split("=", 1) for a in x[6:] if "=" in a)
            out[x[0][1:].upper()] = (tuple(n.lower() for n in x[1:5]), x[5], round(num(p.get("w", "0")), 4),
                                     round(num(p.get("l", "0")), 4), int(float(p.get("ng", 1))))
        return out
    pa, pb = parse(a), parse(b)
    diff = [k for k in set(pa) | set(pb) if pa.get(k) != pb.get(k)]
    return len(pa), len(pb), sorted(diff)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gds"); ap.add_argument("cell"); ap.add_argument("sch"); ap.add_argument("netlist"); ap.add_argument("out")
    ap.add_argument("--subckt-name", default=None)
    ap.add_argument("--ports", default=None, help="port order (default: the sheet netlist's .subckt line)")
    ap.add_argument("--ratio", action="append", default=[], help='"title:DEV1,DEV2,..." W ratio to report; "W/L" in the title: W/L ratio')
    ap.add_argument("--extractor", default="lvs", help="module name or .py path with extract()")
    ap.add_argument("--no-dummies", action="store_true")
    ap.add_argument("--note", action="append", default=[])
    ap.add_argument("--tie", action="append", default=[], help="layout net=sheet net (e.g. a cell-internal bulk)")
    ap.add_argument("--xschemrc", default=None)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    sheet = sheet_devices(a.netlist)
    nets = set()
    for s in sheet.values():
        nets |= {s["d"], s["g"], s["s"], s["b"]}
    fingers = layout_devices(a.gds, a.cell, nets, a.extractor)
    if a.ports is None:
        for line in open(a.netlist):
            t = line.lstrip("*").split()
            if t and t[0].lower() == ".subckt":
                a.ports = " ".join(t[2:])
                break
    ratios = [(r.rsplit(":", 1)[0], r.rsplit(":", 1)[1].split(",")) for r in a.ratio]
    ties = dict(t.split("=", 1) for t in a.tie)
    res, dummies, errors = assign(sheet, fingers, ties)
    if errors:
        print("TOPOLOGY ERRORS (sheet vs layout):\n  " + "\n  ".join(errors))
        sys.exit(2)
    dgroups = group_dummies(dummies)
    name = a.subckt_name or a.cell
    base = os.path.splitext(os.path.basename(a.sch))[0]
    edit_sheet(a.sch, os.path.join(a.out, base + ".sch"), sheet, res, dgroups, a.note, not a.no_dummies)
    sub = subckt_text(name, a.ports.split(), sheet, res, dgroups, not a.no_dummies)
    open(os.path.join(a.out, name + "_subckt.spice"), "w").write(sub)
    open(os.path.join(a.out, "device_changes.txt"), "w").write(changes_text(sheet, res, dgroups, a.note, ratios))
    # the same netlist as CDL (M devices, W / L) for LVS of the layout against the backannotated sheet
    cdl = [".SUBCKT %s %s" % (name, a.ports)]
    for line in sub.splitlines()[1:-1]:
        t = line.split()
        p = dict(x.split("=", 1) for x in t[6:] if "=" in x)
        cdl.append("M%s %s %s W=%s L=%s" % (t[0][1:], " ".join(t[1:6]), "", fmt(num(p["w"])), fmt(num(p["l"]))))
    cdl.append(".ENDS %s" % name)
    open(os.path.join(a.out, name + "_backannotated.cdl"), "w").write(
        "* LVS form of %s_subckt.spice (written by backannotate.py)\n" % name + "\n".join(cdl) + "\n")
    print("%d layout fingers -> %d sheet devices, %d dummy groups; wrote %s" % (len(fingers), len(sheet), len(dgroups), a.out))
    if a.xschemrc:
        net = os.path.join(a.out, base + "_xschem.spice")
        cmd = ["xschem", "--rcfile", a.xschemrc, "-n", "-s", "-q", "-x", "-o", a.out, "-N", os.path.basename(net),
               os.path.join(a.out, base + ".sch")]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        if os.path.exists(net):
            na, nb, diff = compare_text(open(net).read(), sub)
            print("xschem netlist of the new sheet: %d devices; subckt text: %d devices; differing: %s"
                  % (na, nb, diff or "none"))
        else:
            print("xschem netlist not produced")


if __name__ == "__main__":
    main()
