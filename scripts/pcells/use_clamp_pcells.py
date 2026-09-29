#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Replace static copies of IHP clamp cells in a layout by the parametrized PCells.

Every cell named sg13cmos5l_Clamp_<F><ng>N<ng|0>D (F = N or P) that has no child
cells -- a static copy, or a by-reference proxy of the sg13cmos5l_io library as
placed through a .klib -- is swapped, in all its placements, for the PCell Clamp_<F>(ng, tie) from
library SG13_cm_clamps. The flattened top cell is then compared with the input,
layer by layer; the output is written only if all drawing and pin layers are
identical (--force overrides).

Inside the IIC-OSIC-TOOLS container, after 'source .designinit':
    klayout -b -r scripts/pcells/use_clamp_pcells.py -rd input=<in.gds> -rd output=<out.gds>
or, where the 'klayout' Python module is installed:
    python3 scripts/pcells/use_clamp_pcells.py <in.gds> <out.gds>

Interactive test (nothing written; one undo step), from KLayout's Macro Development
window (Python), in a KLayout started with -rm .../load_clamp_pcells.py:
    import runpy
    runpy.run_path('/foss/designs/sg13cmos5l_cm_ip__single2diff2single/scripts/pcells/use_clamp_pcells.py')['swap_in_view']()

Labels: the PCells carry one 'pad' label per drain strap; IHP's cells carry extra,
hand-placed 'pad' labels. Such label differences are listed but do not block.
"""

import os
import re
import runpy
import sys

try:
    import pya as db          # inside KLayout
except ImportError:
    import klayout.db as db

_HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else None
NAME = re.compile(r'^sg13cmos5l_Clamp_([NP])(\d+)N(\d+)D$')
TEXT_LAYERS = {(8, 25), (10, 25), (63, 0)}


def flat_regions(layout, top):
    """merged polygons per layer and the set of texts, flattened below top"""
    regs, texts = {}, set()
    for li in layout.layer_indexes():
        info = layout.get_info(li)
        key = (info.layer, info.datatype)
        r = db.Region()
        it = layout.begin_shapes(top, li)
        while not it.at_end():
            s = it.shape()
            if s.is_text():
                tt = s.text.transformed(it.trans())
                texts.add((key, tt.string, tt.x, tt.y))
            elif s.is_box() or s.is_polygon() or s.is_path() or s.is_simple_polygon():
                r.insert(s.polygon.transformed(it.trans()))
            it.next()
        if not r.is_empty():
            regs[key] = r.merged()
    return regs, texts


def swap_in_layout(ly, top=None):
    """Swap the clamp cells in an in-memory layout and compare. Returns (swapped, ok)."""
    if top is None:
        tops = ly.top_cells()
        if len(tops) != 1:
            raise SystemExit('expected exactly one top cell, found %s' % [c.name for c in tops])
        top = tops[0]
    before, tbefore = flat_regions(ly, top)

    swapped = []
    for c in list(ly.each_cell()):
        m = NAME.match(c.name)
        # static copies and by-reference proxies of the sg13cmos5l_io cells both qualify;
        # cells that already are PCell variants are left alone
        if not m or c.child_cells() > 0 or c.is_pcell_variant():
            continue
        fam, ng, drv = m.group(1), int(m.group(2)), int(m.group(3))
        tie = 'D' if drv == ng else '0D'
        pc = ly.create_cell('Clamp_' + fam, 'SG13_cm_clamps', {'ng': ng, 'tie': tie})
        if pc is None:
            raise SystemExit('library SG13_cm_clamps / Clamp_%s not available' % fam)
        n = 0
        for inst in list(c.each_parent_inst()):
            inst.child_inst().cell_index = pc.cell_index()   # the live Instance, not a copy
            n += 1
        swapped.append((c.name, 'Clamp_%s(ng=%d, tie=%s)' % (fam, ng, tie), pc.name, n))
        ly.delete_cell(c.cell_index())

    after, tafter = flat_regions(ly, top)
    ok = True
    for k in sorted(set(before) | set(after)):
        if k in TEXT_LAYERS:
            continue
        x = before.get(k, db.Region()) ^ after.get(k, db.Region())
        if not x.is_empty():
            ok = False
            print('XOR %d/%d: %d polygons, bbox %s' % (k[0], k[1], x.count(), x.bbox().to_dtype(ly.dbu)))
    for old, new, pname, n in swapped:
        print('swapped %-28s -> %-26s (%d placement%s, cell %s)' % (old, new, n, '' if n == 1 else 's', pname))
    lost, gained = sorted(tbefore - tafter), sorted(tafter - tbefore)
    if lost or gained:
        print('label differences (not blocking): %d removed, %d added' % (len(lost), len(gained)))
        for key, s, x, y in lost:
            print('   - %d/%d %-6s (%.3f, %.3f)' % (key[0], key[1], s, x * ly.dbu, y * ly.dbu))
        for key, s, x, y in gained:
            print('   + %d/%d %-6s (%.3f, %.3f)' % (key[0], key[1], s, x * ly.dbu, y * ly.dbu))
    if not swapped:
        print('no sg13cmos5l_Clamp_* cells to swap')
    else:
        print('geometry after swap:', 'IDENTICAL on all drawing/pin layers' if ok else 'DIFFERENT')
    return swapped, ok


def main(inp, out, force=False, script_dir=None):
    """Batch: read inp, swap, write out only if the geometry is unchanged."""
    runpy.run_path(os.path.join(script_dir, 'load_clamp_pcells.py'))
    ly = db.Layout()
    ly.read(inp)
    swapped, ok = swap_in_layout(ly)
    if not swapped:
        print('nothing written')
        return 1
    if ok or force:
        ly.write(out)
        print('wrote', out)
        return 0
    print('not written (use --force to write anyway)')
    return 2


def swap_in_view(view=None, script_dir=None):
    """Interactive: swap in the layout shown in the current KLayout window, as one undo step.
    Nothing is written to disk. Edit > Undo reverts it."""
    import pya
    runpy.run_path(os.path.join(script_dir or _HERE, 'load_clamp_pcells.py'))
    view = view or pya.LayoutView.current()
    cv = view.active_cellview()
    ly = cv.layout()
    top = cv.cell if cv.cell is not None and cv.cell.is_top() else None
    view.transaction('swap sg13cmos5l_Clamp_* for SG13_cm_clamps PCells')
    try:
        swapped, ok = swap_in_layout(ly, top)
    finally:
        view.commit()
    return swapped, ok


if __name__ == '__main__' and 'input' not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input')
    ap.add_argument('output')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    sys.exit(main(a.input, a.output, a.force, _HERE))
elif 'input' in globals():            # klayout -b -r ... -rd input=... -rd output=...
    _dir = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index('-r') + 1])) if '-r' in sys.argv else _HERE
    rc = main(input, output, globals().get('force', '') not in ('', '0', 'false'), _dir)  # noqa: F821
    if rc:
        raise SystemExit(rc)
