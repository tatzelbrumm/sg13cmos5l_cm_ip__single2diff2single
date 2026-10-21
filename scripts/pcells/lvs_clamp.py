#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Lightweight connectivity / device check for clamp layouts (klayout.db >= 0.28).

    python3 lvs_clamp.py <file.gds> [cell-regex]

This is NOT the PDK LVS deck (sg13cmos5l.lvs needs KLayout >= 0.30.2 and the
IIC-OSIC-TOOLS container; run that for sign-off). It extracts the clamp MOS
devices (parallel fingers combined), the rppd tie-off resistor, and the nets named
by the pad/gate/iovss/iovdd labels, then checks them against clamp_netlist's
device list for the (family, ng, tie) encoded in the cell name:

  N: one sg13_hv_nmos  D=pad G=gate|net2 S=iovss  W=4.4u*ng        L=0.6u
  P: sg13_hv_pmos      D=pad G=gate|net2 S=iovdd  W=2*6.66u*ng     L=0.6u
  D : the gate net contacts the antenna-diode active (Recog.diode)
  0D: an rppd connects the gate net to iovss (N) / iovdd (P)
  and pad, gate, iovss, iovdd are distinct nets (no shorts).
"""

import os
import re
import sys

import klayout.db as db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clamp_engine as E  # noqa: E402

L = dict(activ=(1, 0), poly=(5, 0), cont=(6, 0), m1=(8, 0), m1t=(8, 25), m2=(10, 0), m2t=(10, 25),
         psd=(14, 0), via1=(19, 0), via2=(29, 0), m3=(30, 0), nwell=(31, 0), tgo=(44, 0),
         diode=(99, 31), polyres=(128, 0))


def check(ly, cell):
    m = re.fullmatch(r'sg13cmos5l_Clamp_([NP])(\d+)N(\d+)D', cell.name)
    fam, ng, tie = m.group(1), int(m.group(2)), ('D' if m.group(3) != '0' else '0D')
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(ly, cell, []))
    r = {}
    for k, (a, b) in L.items():
        li = ly.find_layer(a, b)
        if li is None:
            li = ly.layer(a, b)
        r[k] = l2n.make_text_layer(li, k) if k in ('m1t', 'm2t') else l2n.make_polygon_layer(li, k)

    poly_c = r['poly'] - r['polyres']
    res = r['polyres']                  # rppd body: drawn on PolyRes, GatPoly only at the heads
    if fam == 'N':
        gate = (r['poly'] & r['activ']) - r['psd'] - r['nwell']
    else:
        gate = r['poly'] & r['activ'] & r['psd'] & r['nwell']
    sd = r['activ'] - r['poly']
    for name, reg in (('poly_c', poly_c), ('gate', gate), ('sd', sd)):
        l2n.register(reg, name)

    mos = db.DeviceExtractorMOS3Transistor('MOS')
    l2n.extract_devices(mos, {'SD': sd, 'G': gate, 'P': poly_c})
    rex = db.DeviceExtractorResistor('RPPD', 1.0)
    l2n.extract_devices(rex, {'R': res, 'C': poly_c})

    for x in (sd, poly_c, r['cont'], r['m1'], r['via1'], r['m2'], r['via2'], r['m3']):
        l2n.connect(x)
    l2n.connect(sd, r['cont'])
    l2n.connect(poly_c, r['cont'])
    l2n.connect(r['cont'], r['m1'])
    l2n.connect(r['m1'], r['via1'])
    l2n.connect(r['via1'], r['m2'])
    l2n.connect(r['m2'], r['via2'])
    l2n.connect(r['via2'], r['m3'])
    l2n.connect(r['m1'], r['m1t'])
    l2n.connect(r['m2'], r['m2t'])
    # the drain straps are joined only by the bond pad above the clamp
    l2n.join_net_names('pad')
    l2n.extract_netlist()
    nl = l2n.netlist()
    nl.combine_devices()
    circ = nl.circuit_by_name(cell.name)

    def netname(n):
        return n.name if n and n.name else ('<unnamed %d>' % n.cluster_id if n else None)

    errs = []
    named = {}
    for n in circ.each_net():
        if n.name:
            named.setdefault(n.name, []).append(n)
    for k, v in named.items():
        if len(v) > 1:
            errs.append("label '%s' on %d separate nets (open)" % (k, len(v)))
    expect_rail = 'iovss' if fam == 'N' else 'iovdd'
    for need in ['pad', expect_rail] + (['gate'] if tie == 'D' else []):
        if need not in named:
            errs.append("no net labelled '%s'" % need)
    mosd = [d for d in circ.each_device() if d.device_class().name == 'MOS']
    resd = [d for d in circ.each_device() if d.device_class().name == 'RPPD']
    w_exp = E.FAMILY[fam]['w_finger'] * E.FAMILY[fam]['n_dev'] * ng * 1e-3   # um
    if len(mosd) != 1:
        errs.append('%d MOS devices after combining, expected 1' % len(mosd))
        mosd = mosd[:1]
    for d in mosd:
        W, Lg = d.parameter('W'), d.parameter('L')
        s, g, dr = (netname(d.net_for_terminal(t)) for t in ('S', 'G', 'D'))
        if {s, dr} != {'pad', expect_rail}:
            errs.append('MOS S/D nets %s/%s, expected pad/%s' % (s, dr, expect_rail))
        if tie == 'D' and g != 'gate':
            errs.append("MOS gate on net %s, expected 'gate'" % g)
        if tie == '0D' and g in ('pad', 'iovss', 'iovdd', 'gate'):
            errs.append('MOS gate on net %s, expected the internal tie-off net' % g)
        if abs(W - w_exp) > 1e-3 or abs(Lg - 0.6) > 1e-3:
            errs.append('MOS W=%.3f L=%.3f, expected W=%.3f L=0.6' % (W, Lg, w_exp))
    if tie == '0D':
        if len(resd) != 1:
            errs.append('%d rppd devices, expected 1' % len(resd))
        for d in resd:
            a, b = netname(d.net_for_terminal('A')), netname(d.net_for_terminal('B'))
            gnet = netname(mosd[0].net_for_terminal('G')) if mosd else None
            if {a, b} != {gnet, expect_rail}:
                errs.append('rppd between %s and %s, expected gate(%s) and %s' % (a, b, gnet, expect_rail))
    else:
        if resd:
            errs.append('unexpected rppd in a D cell')
        gnet = circ.net_by_name('gate')
        if gnet is not None:
            dio = db.Region(db.RecursiveShapeIterator(ly, cell, ly.find_layer(*L['diode'])))
            shp = l2n.shapes_of_net(gnet, sd, True)
            if (shp & dio).is_empty():
                errs.append("gate net does not reach the antenna diode active")
    return dict(family=fam, ng=ng, tie=tie, mos=[(d.parameter('W'), d.parameter('L')) for d in mosd],
                nres=len(resd), errors=errs)


def main():
    ly = db.Layout()
    ly.read(sys.argv[1])
    pat = sys.argv[2] if len(sys.argv) > 2 else r'sg13cmos5l_Clamp_[NP]\d+N\d+D$'
    bad = 0
    n = 0
    for c in ly.each_cell():
        if re.search(pat, c.name) and re.fullmatch(r'sg13cmos5l_Clamp_[NP]\d+N\d+D', c.name):
            res = check(ly, c)
            n += 1
            if res['errors']:
                bad += 1
                print('%-28s FAIL %s' % (c.name, '; '.join(res['errors'])))
            else:
                print('%-28s ok   W=%.2fu L=%.2fu%s' % (c.name, res['mos'][0][0], res['mos'][0][1],
                                                       ' +rppd' if res['nres'] else ' +diode'))
    print('checked %d cells, %d failing' % (n, bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
