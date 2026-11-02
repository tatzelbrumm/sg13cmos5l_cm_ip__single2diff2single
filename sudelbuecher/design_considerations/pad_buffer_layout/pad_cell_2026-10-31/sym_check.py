# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Device-layer symmetry and gate-poly check of a layout primitive (C2, after Christoph's rejection of 18:55).

python3 sym_check.py <gds> <cell> [--x <x_axis_um>] [--y <y_axis_um>] [--no-y]

Christoph's rules: rows mirror-symmetric about the line dividing them; dummies at both ends of every row, alike
(or none at all); never dummies at one end only; no narrowed poly feeding gate contacts.

Checks (merged shapes, cell flattened):
  X  Activ, GatPoly, ThickGateOx, pSD, NWell, Cont XOR their mirror image about the vertical line x = <x_axis>
     (default: the centre of the Activ bounding box). Catches one-sided dummies and lopsided rows.
  Y  the same about the horizontal line y = <y_axis> (default: the centre of the Activ bounding box): the rows'
     mirror symmetry about the line dividing them. --no-y for one-row cells.
  N  necked poly links to gate contacts: GatPoly beyond the endcap zone (Activ grown by 0.25 µm, past Gat.c's
     endcap), in pieces that carry a Cont, narrower than 0.30 µm (= Cnt.a 0.16 + 2 × Cnt.d 0.07,
     sg13cmos5l_tech_default.json). Each hit with its location.
A residual XOR area > 0 is printed per layer with its bounding box; it is a finding to explain, not automatically
an error (e.g. a diode connection, an odd device count). Device layers only: metal wiring may be asymmetric.
"""
import sys
import klayout.db as db

LAYERS = {'Activ': (1, 0), 'GatPoly': (5, 0), 'ThickGateOx': (44, 0), 'pSD': (14, 0), 'NWell': (31, 0), 'Cont': (6, 0)}


def region(ly, cell, ld):
    li = ly.find_layer(*ld)
    return db.Region(cell.begin_shapes_rec(li)).merged() if li is not None else db.Region()


def mirror_xor(r, trans):
    x = (r ^ r.transformed(trans)).merged()
    return x.area(), x.bbox()


if __name__ == '__main__':
    a = sys.argv[1:]
    gds, name = a[0], a[1]
    ly = db.Layout(); ly.read(gds); cell = ly.cell(name); u = ly.dbu
    act = region(ly, cell, LAYERS['Activ'])
    bb = act.bbox()
    xa = float(a[a.index('--x') + 1]) if '--x' in a else bb.center().x * u
    ya = float(a[a.index('--y') + 1]) if '--y' in a else bb.center().y * u
    tx = db.Trans(db.Trans.M90, int(round(2 * xa / u)), 0)     # x -> 2xa - x
    ty = db.Trans(db.Trans.M0, 0, int(round(2 * ya / u)))      # y -> 2ya - y
    print(f'{name}: Activ bbox {bb.to_dtype(u)}; axes x = {xa:g}, y = {ya:g} um')
    worst = 0.0
    for tag, t in (('X', tx), ('Y', ty)):
        if tag == 'Y' and '--no-y' in a:
            continue
        for ln, ld in LAYERS.items():
            area, box = mirror_xor(region(ly, cell, ld), t)
            area *= u * u
            worst = max(worst, area)
            if area > 0:
                print(f'  {tag} {ln:12s} XOR {area:9.4f} um2  in {box.to_dtype(u)}')
    gp = (region(ly, cell, LAYERS['GatPoly']) - act.sized(int(round(0.25 / u)))).interacting(region(ly, cell, LAYERS['Cont']))
    necks = gp.width_check(int(round(0.30 / u)))
    for e in necks.each():
        print(f'  N gate-contact poly narrower than 0.30 um at {e.first.to_dtype(u)}')
    print(f'  summary: max mirror XOR {worst:.4f} um2, {necks.count()} narrow-poly hits'
          f'{" -> SYMMETRIC" if worst == 0 and necks.count() == 0 else ""}')
