#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Regenerate clamp_refdata.py from the IHP sg13cmos5l_io library.

    python3 extract_clamp_refdata.py <sg13cmos5l_io.gds> <sg13cmos5l_io.cdl> [-o clamp_refdata.py]

Needs the 'klayout' Python module (pip install klayout, or run inside KLayout).

For every reference cell the rule-generated finger array and gate bus
(clamp_engine.array_shapes / bus_shapes) are subtracted from the reference layout.
What is left is split into
  frame  - common to all reference cells of the same family and gate-tie variant
  tie    - the remainder, which must lie inside a window around the tie block
           (antenna diode + gate strap for 'D', rppd resistor for '0D')
  decor  - Metal1 pins and texts outside the tie window (ring labels)
The script aborts if the rules generate geometry the reference does not have, or
if anything is left over outside the tie window: both mean the rules are wrong.
"""

import argparse
import datetime
import hashlib
import os
import pprint
import re
import sys
import xml.dom.minidom

import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clamp_engine as E  # noqa: E402

REFS = {
    ('N', 'D'): [(2, 'sg13cmos5l_Clamp_N2N2D'), (8, 'sg13cmos5l_Clamp_N8N8D'), (15, 'sg13cmos5l_Clamp_N15N15D')],
    ('N', '0D'): [(20, 'sg13cmos5l_Clamp_N20N0D')],
    ('P', 'D'): [(2, 'sg13cmos5l_Clamp_P2N2D'), (8, 'sg13cmos5l_Clamp_P8N8D'), (15, 'sg13cmos5l_Clamp_P15N15D')],
    ('P', '0D'): [(20, 'sg13cmos5l_Clamp_P20N0D')],
}
D_WINDOW = 2000                 # tie block of a 'D' cell lies within xs +- 2 um
W0D = (63500, 69000)            # tie block of a '0D' cell (rppd) lies in this x range
DECOR_LAYERS = {('Metal1', 'pin')}

# GDS layer/datatype -> (layer, purpose); the subset the clamps use, from sg13cmos5l.lyp
LAYERS = {
    (1, 0): ('Activ', 'drawing'), (5, 0): ('GatPoly', 'drawing'), (6, 0): ('Cont', 'drawing'),
    (8, 0): ('Metal1', 'drawing'), (8, 2): ('Metal1', 'pin'), (8, 25): ('Metal1', 'text'),
    (10, 0): ('Metal2', 'drawing'), (10, 2): ('Metal2', 'pin'), (10, 25): ('Metal2', 'text'),
    (14, 0): ('pSD', 'drawing'), (19, 0): ('Via1', 'drawing'), (28, 0): ('SalBlock', 'drawing'),
    (29, 0): ('Via2', 'drawing'), (30, 0): ('Metal3', 'drawing'), (31, 0): ('NWell', 'drawing'),
    (40, 0): ('Substrate', 'drawing'), (44, 0): ('ThickGateOx', 'drawing'), (52, 0): ('HeatRes', 'drawing'),
    (63, 0): ('TEXT', 'drawing'), (99, 31): ('Recog', 'diode'), (111, 0): ('EXTBlock', 'drawing'),
    (128, 0): ('PolyRes', 'drawing'),
}
HALIGN = {db.HAlign.HAlignLeft: 'left', db.HAlign.HAlignCenter: 'center', db.HAlign.HAlignRight: 'right'}
VALIGN = {db.VAlign.VAlignBottom: 'bottom', db.VAlign.VAlignCenter: 'center', db.VAlign.VAlignTop: 'top'}


def shapes_to_regions(shapes):
    regs = {}
    for lay, pur, kind, d in shapes:
        r = regs.setdefault((lay, pur), db.Region())
        if kind == 'box':
            r.insert(db.Box(*d))
        else:
            r.insert(db.Polygon([db.Point(x, y) for x, y in d]))
    return {k: v.merged() for k, v in regs.items()}


def cell_regions(ly, cell):
    regs, texts = {}, []
    for li in ly.layer_indexes():
        info = ly.get_info(li)
        key = LAYERS.get((info.layer, info.datatype))
        shapes = cell.shapes(li)
        if shapes.size() == 0:
            continue
        if key is None:
            raise SystemExit('unmapped layer %d/%d in %s' % (info.layer, info.datatype, cell.name))
        r = db.Region()
        for s in shapes.each():
            if s.is_text():
                t = s.text
                texts.append((key[0], key[1], t.string, t.x, t.y, t.size,
                              HALIGN.get(t.halign), VALIGN.get(t.valign), 'R%d' % (t.trans.rot * 90)))
            else:
                r.insert(s.polygon)
        if not r.is_empty():
            regs[key] = r.merged()
    return regs, texts


def sub(a, b):
    out = {}
    for k, r in a.items():
        d = r - b[k] if k in b else r.dup()
        if not d.is_empty():
            out[k] = d
    return out


def encode(region):
    """Region -> list of items: arrays of equal small boxes, boxes, simple polygons."""
    items, small = [], []
    for p in region.each():
        if p.holes():
            p = p.to_simple_polygon()
        if p.is_box():
            b = p.bbox()
            if b.width() == b.height() and b.width() <= 200:
                small.append((b.left, b.bottom, b.width(), b.height()))
            else:
                items.append(('box', (b.left, b.bottom, b.right, b.top)))
        else:
            pts = [(q.x, q.y) for q in (p.to_simple_polygon() if hasattr(p, 'to_simple_polygon') else p).each_point()]
            items.append(('poly', tuple(pts)))
    # rows of equal-pitch small boxes
    rows = {}
    for x, y, w, h in sorted(small, key=lambda t: (t[2], t[3], t[1], t[0])):
        rows.setdefault((w, h, y), []).append(x)
    runs = []
    for (w, h, y), xs in rows.items():
        i = 0
        while i < len(xs):
            j = i + 1
            if j < len(xs):
                px = xs[j] - xs[i]
                while j + 1 < len(xs) and xs[j + 1] - xs[j] == px:
                    j += 1
                runs.append((w, h, y, xs[i], j - i + 1, px))
                i = j + 1
            else:
                runs.append((w, h, y, xs[i], 1, 0))
                i += 1
    # stack identical runs vertically
    cols = {}
    for w, h, y, x0, nx, px in runs:
        cols.setdefault((w, h, x0, nx, px), []).append(y)
    for (w, h, x0, nx, px), ys in sorted(cols.items()):
        ys.sort()
        i = 0
        while i < len(ys):
            j = i + 1
            if j < len(ys):
                py = ys[j] - ys[i]
                while j + 1 < len(ys) and ys[j + 1] - ys[j] == py:
                    j += 1
                items.append(('array', (x0, ys[i], w, h, nx, j - i + 1, px, py)))
                i = j + 1
            else:
                items.append(('array', (x0, ys[i], w, h, nx, 1, px, 0)))
                i += 1
    return items


def encode_regions(regs, dx=0):
    out = []
    for (lay, pur) in sorted(regs):
        r = regs[(lay, pur)].moved(-dx, 0) if dx else regs[(lay, pur)]
        for kind, d in encode(r):
            out.append((lay, pur, kind, d))
    return out


def parse_cdl(path):
    subckts, cur = {}, None
    for line in open(path):
        line = line.strip()
        if line.upper().startswith('.SUBCKT'):
            parts = line.split()
            cur = parts[1]
            subckts[cur] = {'pins': parts[2:], 'lines': []}
        elif line.upper().startswith('.ENDS'):
            cur = None
        elif cur and line and not line.startswith('*'):
            subckts[cur]['lines'].append(line)
    return subckts


def netlist_info(sc):
    info = {}
    for ln in sc['lines']:
        kv = dict(re.findall(r'(\w+)=(\S+)', ln))
        tok = ln.split()
        if ' ptap1 ' in ' %s ' % ln:
            info['ptap'] = {'A': kv['A'], 'P': kv['P']}
        elif tok[0].startswith('D'):
            info['diode'] = {'model': tok[3], 'w': kv['w'], 'l': kv['l'], 'a': kv['a'], 'p': kv['p']}
        elif tok[0].startswith('R') and '$[rppd]' in ln:
            info['rppd'] = {'value': tok[3], 'sub': re.search(r'\$SUB=(\S+)', ln).group(1),
                            'l': kv['l'], 'w': kv['w'], 'b': kv.get('b', '0')}
        elif tok[0].startswith('M'):
            info.setdefault('mos', []).append({'w': kv['w'], 'l': kv['l'], 'ng': kv['ng']})
    return info


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('gds')
    ap.add_argument('cdl')
    ap.add_argument('-o', '--output', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clamp_refdata.py'))
    a = ap.parse_args()

    ly = db.Layout()
    ly.read(a.gds)
    if abs(ly.dbu - 0.001) > 1e-12:
        raise SystemExit('expected dbu 0.001, got %g' % ly.dbu)
    cdl = parse_cdl(a.cdl)
    data = {}
    ok = True

    for (fam, tie), refs in REFS.items():
        H = E.FAMILY[fam]['height']
        rests, per = {}, {}
        for ng, name in refs:
            cell = ly.cell(name)
            if cell is None:
                raise SystemExit('cell %s not found' % name)
            regs, texts = cell_regions(ly, cell)
            decor_pins = {k: regs.pop(k) for k in list(regs) if k in DECOR_LAYERS}
            xs = None
            if tie == 'D':
                cand = [p.bbox() for p in regs[('Metal2', 'drawing')].each()
                        if p.bbox().width() == 200 and p.bbox().top == H and p.bbox().bottom > 0]
                if len(cand) != 1:
                    raise SystemExit('%s: cannot identify the M2 gate strap (%d candidates)' % (name, len(cand)))
                xs = cand[0].center().x
            gen = shapes_to_regions(E.array_shapes(fam, tie, ng) + E.bus_shapes(fam, tie, ng, xs))
            extra = sub(gen, regs)
            if extra:
                ok = False
                for k, r in extra.items():
                    print('ERROR %s: rules generate %d shapes on %s/%s not in the reference, bbox %s'
                          % (name, r.count(), k[0], k[1], r.bbox().to_dtype(0.001)))
            # An array shape that lies completely inside a larger reference shape on the same
            # layer (the P array NWell inside the frame NWell) is redundant there: subtracting
            # it would punch a hole into the frame. Detect that by the hole count and keep it.
            gen_sub = {}
            for k, g in gen.items():
                if k in regs:
                    holes_before = sum(p.holes() for p in regs[k].each())
                    holes_after = sum(p.holes() for p in (regs[k] - g).each())
                    if holes_after > holes_before:
                        print('  note %s: %s/%s array shapes are subsumed by the frame' % (name, k[0], k[1]))
                        continue
                gen_sub[k] = g
            rests[ng] = sub(regs, gen_sub)
            per[ng] = dict(name=name, xs=xs, texts=texts, pins=decor_pins, net=netlist_info(cdl[name]))

        # frame
        if tie == 'D':
            keys = set.intersection(*[set(r) for r in rests.values()])
            frame = {}
            for k in keys:
                acc = None
                for r in rests.values():
                    acc = r[k].dup() if acc is None else acc & r[k]
                if not acc.is_empty():
                    frame[k] = acc
        else:
            (only,) = rests.values()
            win = db.Region(db.Box(W0D[0], -10000, W0D[1], H + 10000))
            frame = {}
            for k, r in only.items():
                keep = db.Region([p for p in r.each() if not p.bbox().inside(win.bbox())])
                if not keep.is_empty():
                    frame[k] = keep

        refd = {}
        for ng, name in refs:
            pr = per[ng]
            tie_regs = sub(rests[ng], frame)
            xs = pr['xs']
            if tie == 'D':
                wx0, wx1 = xs - D_WINDOW, xs + D_WINDOW
            else:
                wx0, wx1 = W0D
            for k, r in tie_regs.items():
                b = r.bbox()
                if b.left < wx0 or b.right > wx1:
                    ok = False
                    print('ERROR %s: leftover on %s/%s outside the tie window: %s'
                          % (name, k[0], k[1], b.to_dtype(0.001)))
            # pins / texts: inside the tie window -> tie, else decor
            tie_pins, dec_pins = {}, {}
            for k, r in pr['pins'].items():
                for p in r.each():
                    tgt = tie_pins if wx0 <= p.bbox().left and p.bbox().right <= wx1 else dec_pins
                    tgt.setdefault(k, db.Region()).insert(p)
            tie_regs.update(tie_pins)
            tie_texts, dec_texts = [], []
            for t in pr['texts']:
                if t[0] == 'Metal2' and t[2] == 'pad':
                    continue                         # re-generated by rule
                if wx0 <= t[3] <= wx1:
                    tie_texts.append(t[:3] + ((t[3] - xs) if tie == 'D' else t[3],) + t[4:])
                else:
                    dec_texts.append(t)
            refd[ng] = {
                'cell': name,
                'xs': xs,
                'tie': encode_regions(tie_regs, xs if tie == 'D' else 0),
                'tie_texts': tie_texts,
                'decor': encode_regions(dec_pins),
                'decor_texts': dec_texts,
                'netlist': pr['net'],
            }
        data.setdefault(fam, {})[tie] = {'frame': encode_regions(frame), 'refs': refd}
        print('%s/%s: frame %d items; ' % (fam, tie, len(data[fam][tie]['frame']))
              + ', '.join('ng=%d tie %d items%s' % (ng, len(v['tie']), ' xs=%.3f' % (v['xs'] / 1e3) if v['xs'] else '')
                          for ng, v in refd.items()))

    if not ok:
        raise SystemExit('extraction failed: the array rules in clamp_engine.py do not match the references')

    sha = hashlib.sha256(open(a.gds, 'rb').read()).hexdigest()
    shc = hashlib.sha256(open(a.cdl, 'rb').read()).hexdigest()
    with open(a.output, 'w') as fh:
        fh.write('# SPDX-FileCopyrightText: 2024 IHP PDK Authors\n')
        fh.write('# SPDX-FileCopyrightText: 2026 Christoph Maier\n')
        fh.write('# SPDX-License-Identifier: Apache-2.0\n')
        fh.write('#\n# GENERATED by extract_clamp_refdata.py on %s -- do not edit by hand.\n'
                 % datetime.date.today().isoformat())
        fh.write('# Geometry extracted from the IHP sg13cmos5l_io library cells named in REFS:\n')
        fh.write('#   %s  sha256 %s\n' % (os.path.basename(a.gds), sha))
        fh.write('#   %s  sha256 %s\n' % (os.path.basename(a.cdl), shc))
        fh.write('# Units: nm. Item kinds: box (x1,y1,x2,y2), poly ((x,y),...), '
                 'array (x0,y0,w,h,nx,ny,px,py).\n')
        fh.write('# D refs: tie geometry and tie texts are stored relative to the M2 gate strap x (xs).\n\n')
        fh.write('SOURCE_GDS_SHA256 = %r\nSOURCE_CDL_SHA256 = %r\n\n' % (sha, shc))
        fh.write('REFDATA = ')
        fh.write(pprint.pformat(data, width=120, compact=True))
        fh.write('\n')
    print('wrote', a.output)


if __name__ == '__main__':
    main()
