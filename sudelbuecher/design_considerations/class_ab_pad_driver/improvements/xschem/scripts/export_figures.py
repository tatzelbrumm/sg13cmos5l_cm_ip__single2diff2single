#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Export xschem sheets as report figures: <sheet>.svg, <sheet>.pdf (vector) and <sheet>.png.

White background; wires, symbols and text black; block frames and legends (layer 10) in
#d55e00, which prints as about 47 % grey in monochrome. Left out: the title block, the
G/D/S/B pin letters (layer 7), the pin squares, m=1, ng=1, b=0, the rhigh R=... expression and
the MOS model names. Each figure is cropped to the drawing; the PNG has 2 px per xschem unit,
at most 6000 px wide.

    python3 export_figures.py                    all sheets of improvements/xschem -> improvements/figures
    python3 export_figures.py d2s_mpdda tb_units only these sheets
    options: --xschem DIR (sheets and xschemrc), --out DIR (figures)

Needs xschem on PATH, $PDK_ROOT, and the Python packages cairosvg and Pillow. The SVG names the
font "Liberation Sans" (falls back to Arial, Helvetica, sans-serif); the PDF and PNG use what
fontconfig finds for it.
"""
import argparse, os, re, subprocess, sys, tempfile
from io import BytesIO
import cairosvg
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ACCENT = '#d55e00'
# xschem layer colors: 0 background, 7 pin letters (hidden), 10 block frames, everything else black
COLORS = ['#ffffff', '#000000', '#808080', '#000000', '#000000', '#000000', '#000000', '#ffffff', '#000000',
          '#000000', ACCENT] + ['#000000'] * 11
DROP = re.compile(r'^(m=1|ng=1|b=0|R=.*|sg13_hv_[np]mos)$')
FONT = 'text {font-family: "Liberation Sans", Arial, Helvetica, sans-serif;}'


def area(text):
    """generous drawing area from the coordinates in the .sch (texts extend right and down)"""
    xs, ys = [], []
    for l in text.splitlines():
        t = l.split()
        if not t:
            continue
        if t[0] == 'N':
            xs += [float(t[1]), float(t[3])]; ys += [float(t[2]), float(t[4])]
        elif t[0] == 'C':
            m = re.match(r'C \{[^}]*\} (\S+) (\S+)', l)
            if m:
                xs.append(float(m.group(1))); ys.append(float(m.group(2)))
        elif t[0] == 'P':
            v = list(map(float, re.findall(r'-?[\d.]+', l.split('{')[0])[2:]))
            xs += v[0::2]; ys += v[1::2]
        elif t[0] == 'T':
            m = re.match(r'T \{(.*?)\} (\S+) (\S+) \S+ \S+ (\S+)', l)
            if m:
                x, y, sz = float(m.group(2)), float(m.group(3)), float(m.group(4))
                xs += [x, x + len(m.group(1)) * sz * 35]; ys += [y, y + sz * 60]
    code = re.search(r'code_shown\.sym\} (\S+) (\S+) .*?value="(.*?)"\}', text, re.S)
    if code:
        x, y = float(code.group(1)), float(code.group(2))
        lines = code.group(3).split('\n')
        xs.append(x + max(len(s) for s in lines) * 15); ys.append(y + len(lines) * 30 + 100)
    return min(xs) - 300, min(ys) - 300, max(xs) + 300, max(ys) + 300


def tiny_pin_box(m):
    v = list(map(float, re.findall(r'-?[\d.]+', m.group(1))))
    return '' if max(v[0::2]) - min(v[0::2]) <= 6 and max(v[1::2]) - min(v[1::2]) <= 6 else m.group(0)


def export(name, xsdir, figdir, tmp, rc):
    text = open(os.path.join(xsdir, name + '.sch')).read()
    text = '\n'.join(l for l in text.splitlines() if 'devices/title.sym' not in l) + '\n'
    sch = os.path.join(tmp, name + '.sch')
    open(sch, 'w').write(text)
    x1, y1, x2, y2 = (int(round(v / 10)) * 10 for v in area(text))
    raw, tcl = os.path.join(tmp, name + '.svg'), os.path.join(tmp, name + '.tcl')
    open(tcl, 'w').write(f'xschem load {sch}\nxschem print svg {raw} {x2 - x1} {y2 - y1} {x1} {y1} {x2} {y2}\n')
    r = subprocess.run(['xschem', '--rcfile', os.path.join(xsdir, 'xschemrc'), '--tcl', f'source {rc}', '-q', '-x',
                        '--script', tcl], cwd=xsdir, env=dict(os.environ, PWD=xsdir), capture_output=True, text=True)
    if not os.path.exists(raw):
        print(f'{name}: xschem wrote no SVG (status {r.returncode})')
        for l in (r.stdout + r.stderr).splitlines()[-10:]:
            print('   ', l)
        return False
    svg = open(raw).read()
    # declutter: hidden pin letters, default or repeated parameters, pin squares
    svg = re.sub(r'<text[^>]*fill="#ffffff"[^>]*>[^<]*</text>\n?', '', svg)
    svg = re.sub(r'<text[^>]*>([^<]*)</text>\n?', lambda m: '' if DROP.match(m.group(1).strip()) else m.group(0), svg)
    svg = re.sub(r'<path class="l5" d="(M[^"]*z)"/>\n?', tiny_pin_box, svg)
    svg = re.sub(r'stroke-width:\s*1\.2;', 'stroke-width: 2;', svg)
    svg = re.sub(r'text\s*\{\s*font-family:[^}]*\}', FONT, svg)
    # crop to the drawn content plus a margin, measured on a quarter-resolution render
    w, h = (int(float(v)) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', svg).groups())
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=w // 4, output_height=h // 4)
    bbox = ImageOps.invert(Image.open(BytesIO(png)).convert('L')).point(lambda v: 255 if v > 5 else 0).getbbox()
    m = 24
    cx1, cy1 = max(0, bbox[0] * 4 - m), max(0, bbox[1] * 4 - m)
    cx2, cy2 = min(w, bbox[2] * 4 + m), min(h, bbox[3] * 4 + m)
    cw, chh = cx2 - cx1, cy2 - cy1
    svg = re.sub(r'<svg ([^>]*?)width="[\d.]+" height="[\d.]+"',
                 rf'<svg \1width="{cw}" height="{chh}" viewBox="{cx1} {cy1} {cw} {chh}"', svg, count=1)
    out = os.path.join(figdir, name)
    open(out + '.svg', 'w').write(svg)
    scale = min(2.0, 6000 / cw)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=out + '.png', output_width=int(cw * scale),
                     output_height=int(chh * scale), background_color='white')
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=out + '.pdf')
    print(f'{name}: {cw} x {chh} units, png {int(cw * scale)} px wide')
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('sheets', nargs='*', help='sheet names without .sch (default: all)')
    ap.add_argument('--xschem', default=os.path.dirname(HERE), help='directory with the sheets and xschemrc')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(HERE), '..', 'figures'), help='figure directory')
    a = ap.parse_args()
    xsdir, figdir = os.path.abspath(a.xschem), os.path.abspath(a.out)
    os.makedirs(figdir, exist_ok=True)
    names = a.sheets or sorted(f[:-4] for f in os.listdir(xsdir) if f.endswith('.sch'))
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        rc = os.path.join(tmp, 'colors.tcl')
        open(rc, 'w').write('set dark_colorscheme 0\nset light_colors {' + ' '.join(f'"{c}"' for c in COLORS) + '}\n')
        for n in names:
            bad += not export(n, xsdir, figdir, tmp, rc)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
