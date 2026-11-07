# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Label-style xschem sheet + symbol from a source subckt of hv MOS devices (as bias_dist_pd's sheet: one lab_pin on every
device pin), and a check that xschem's netlist of the sheet equals the source subckt device by device.

usage: python3 -I gen_sheet.py <source.spice> <subckt> <out dir> [columns]      (writes <subckt>.sch / .sym)
       python3 -I gen_sheet.py --check <source.spice> <subckt> <xschem netlist>
Device lines: X<name> d g s b sg13_hv_{n,p}mos w= l= ng= [m=] mm_ok=1; comment lines '* --- <group>' become box titles.
"""
import re
import sys
from pathlib import Path

DEV = re.compile(r"^X(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(sg13_hv_[np]mos)\s+(.*)$", re.I)


def parse(src, sub):
    lines, inside, ports, devs, group, notes = open(src).read().splitlines(), False, [], [], "", []
    for l in lines:
        if l.lower().startswith(f".subckt {sub.lower()} "):
            inside, ports = True, l.split()[2:]
            continue
        if not inside:
            if l.startswith("*") and not l.startswith("* SPDX"):
                notes.append(l[1:].strip())
            continue
        if l.lower().startswith(".ends"):
            break
        if l.startswith("* ---"):
            group = l[5:].strip()
            continue
        m = DEV.match(l)
        if m:
            p = dict(kv.split("=") for kv in m.group(7).split())
            devs.append(dict(name=m.group(1), d=m.group(2), g=m.group(3), s=m.group(4), b=m.group(5),
                             model=m.group(6).lower(), p=p, group=group))
    return ports, devs, notes


def gen(src, sub, out, cols=6):
    ports, devs, notes = parse(src, sub)
    o = ["v {xschem version=3.4.8RC file_version=1.3}", "G {}", "K {}", "V {}", "S {}", "F {}", "E {}"]
    y = -1400
    o.append(f"T {{{sub}: generated label-style sheet from netlist/source/{Path(src).name} (gen_sheet.py)}} 60 {y} 0 0 0.4 0.4 {{}}")
    for i, n in enumerate([n for n in notes if n][:14]):
        o.append(f"T {{{n.replace('{', '(').replace('}', ')')}}} 60 {y + 40 + 22 * i} 0 0 0.2 0.2 {{}}")
    for i, p in enumerate(ports):
        kind = "iopin" if p in ("vdd", "vss") else ("opin" if p in ("vcm", "vref") else "ipin")
        o.append(f"C {{devices/{kind}.sym}} 100 {-960 + 40 * i} 0 {1 if kind != 'ipin' else 0} {{name=p{i} lab={p}}}")
    groups, gx = [], {}
    for d in devs:
        if d["group"] not in gx:
            gx[d["group"]] = len(groups)
            groups.append(d["group"])
    k, lk = 0, 0
    per = {}
    for d in devs:
        per.setdefault(d["group"], []).append(d)
    gy = -960
    for gi, g in enumerate(groups):
        o.append(f"T {{[{gi + 1}] {g}}} 300 {gy - 60} 0 0 0.3 0.3 {{layer=10}}")
        for j, d in enumerate(per[g]):
            x, yy = 400 + 220 * (j % cols), gy + 140 * (j // cols)
            p = d["p"]
            o.append(f"C {{sg13cmos5l_pr/{d['model']}.sym}} {x} {yy} 0 0 {{name={d['name']}")
            o += [f"l={p['l']}", f"w={p['w']}", f"ng={p.get('ng', 1)}", f"m={p.get('m', 1)}",
                  f"mm_ok={p.get('mm_ok', 1)}", f"model={d['model']}", "spiceprefix=X", "}"]
            top, bot = (d["d"], d["s"]) if d["model"].endswith("nmos") else (d["s"], d["d"])
            for (dx, dy, fl, net) in ((20, -30, 1, top), (20, 30, 1, bot), (20, 0, 1, d["b"]), (-20, 0, 0, d["g"])):
                lk += 1
                o.append(f"C {{devices/lab_pin.sym}} {x + dx} {yy + dy} 0 {fl} {{name=l{lk} sig_type=std_logic lab={net}}}")
            k += 1
        gy += 140 * ((len(per[g]) - 1) // cols + 1) + 120
    Path(out, f"{sub}.sch").write_text("\n".join(o) + "\n")
    # symbol: power on top / bottom, inputs left, outputs right
    left = [p for p in ports if p not in ("vdd", "vss", "vcm", "vref")]
    right = [p for p in ports if p in ("vcm", "vref")]
    h = 20 * max(len(left), 2) + 40
    s = ["v {xschem version=3.4.8RC file_version=1.3}", "G {}",
         f'K {{type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\ndescription="{sub}: replica bias"\n}}',
         "V {}", "S {}", "F {}", "E {}"]
    geo = {"vdd": (f"L 4 0 {-h // 2 - 20} 0 {-h // 2} {{}}", f"B 5 -2.5 {-h // 2 - 22.5} 2.5 {-h // 2 - 17.5} {{name=vdd dir=inout}}", ""),
           "vss": (f"L 4 0 {h // 2} 0 {h // 2 + 20} {{}}", f"B 5 -2.5 {h // 2 + 17.5} 2.5 {h // 2 + 22.5} {{name=vss dir=inout}}", "")}
    for i, p in enumerate(left):
        yy = -h // 2 + 20 + 20 * i
        geo[p] = (f"L 4 -100 {yy} -80 {yy} {{}}", f"B 5 -102.5 {yy - 2.5} -97.5 {yy + 2.5} {{name={p} dir=in}}",
                  f"T {{{p}}} -76 {yy - 7} 0 0 0.2 0.2 {{}}")
    for i, p in enumerate(right):
        yy = -10 + 20 * i
        geo[p] = (f"L 4 80 {yy} 100 {yy} {{}}", f"B 5 97.5 {yy - 2.5} 102.5 {yy + 2.5} {{name={p} dir=out}}",
                  f"T {{{p}}} 76 {yy - 7} 0 1 0.2 0.2 {{}}")
    s += [geo[p][0] for p in ports] + [geo[p][1] for p in ports] + [geo[p][2] for p in ports if geo[p][2]]
    s += [f"P 4 5 -80 {-h // 2} 80 {-h // 2} 80 {h // 2} -80 {h // 2} -80 {-h // 2} {{}}",
          f"T {{@symname}} -60 {h // 2 - 30} 0 0 0.25 0.25 {{}}", f"T {{@name}} 60 {-h // 2 - 20} 0 0 0.2 0.2 {{}}",
          f"T {{vdd}} 4 {-h // 2 + 2} 0 0 0.2 0.2 {{}}", f"T {{vss}} 4 {h // 2 - 22} 0 0 0.2 0.2 {{}}"]
    Path(out, f"{sub}.sym").write_text("\n".join(s) + "\n")
    print(f"{sub}: {len(devs)} devices, {len(ports)} ports -> {out}")


def instances(text, sub):
    """subcircuit instance lines (X<name> <nets ...> <cell>, no '=' parameters) inside .subckt <sub>."""
    out, inside = {}, False
    for l in text.splitlines():
        l = l[2:] if l.startswith("**.") else l
        if l.lower().startswith(f".subckt {sub.lower()} "):
            inside = True
            continue
        if inside and l.lower().startswith(".ends"):
            break
        t = l.split()
        if inside and t and t[0][:1] in "Xx" and not DEV.match(l) and not any("=" in x for x in t):
            out[t[0].upper()] = tuple(t[1:])
    return out


def check(src, sub, net):
    """Compares the sheet's xschem netlist with the source subckt: ports, every hv MOS device (nets, model, w, l, ng, m)
    and every subcircuit instance (nets, cell)."""
    ports, devs, _ = parse(src, sub)
    want = {d["name"].upper(): (d["d"], d["g"], d["s"], d["b"], d["model"], d["p"]["w"], d["p"]["l"],
                                str(d["p"].get("ng", 1)), str(d["p"].get("m", 1))) for d in devs}
    got, gports, inside = {}, None, False
    text = open(net).read().replace("\n+", " ").replace("\n*+", " ")  # xschem wraps long (commented) header lines
    for l in text.splitlines():
        l = l[2:] if l.startswith("**.") else l
        if l.lower().startswith(f".subckt {sub.lower()} "):
            inside, gports = True, l.split()[2:]
            continue
        if inside and l.lower().startswith(".ends"):
            break
        m = DEV.match(l) if inside else None
        if m:
            p = dict(kv.split("=") for kv in m.group(7).split() if "=" in kv)
            got[m.group(1).upper()] = (m.group(2), m.group(3), m.group(4), m.group(5), m.group(6).lower(), p["w"],
                                       p["l"], p.get("ng", "1"), p.get("m", "1"))
    bad = [n for n in want if want[n] != got.get(n)] + [n for n in got if n not in want]
    wi, gi = instances(open(src).read(), sub), instances(text, sub)
    badi = [n for n in wi if wi[n] != gi.get(n)] + [n for n in gi if n not in wi]
    inst = f"; instances source {len(wi)}, sheet {len(gi)}, mismatches {len(badi)} {badi[:5]}" if (wi or gi) else ""
    print(f"{sub}: ports {'equal' if gports == ports else f'DIFFER {gports} vs {ports}'}; devices source {len(want)}, "
          f"sheet {len(got)}, mismatches {len(bad)} {bad[:5]}{inst}")
    return 0 if (not bad and not badi and gports == ports) else 1


if __name__ == "__main__":
    if sys.argv[1] == "--check":
        sys.exit(check(*sys.argv[2:5]))
    gen(sys.argv[1], sys.argv[2], sys.argv[3], *(int(x) for x in sys.argv[4:5]))
