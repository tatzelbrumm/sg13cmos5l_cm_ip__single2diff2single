#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Stage-B testbenches of slot7_testplatform_ab (ngspice, batch); reuses run_tb.py (models, retries).

Usage (design repo root, after `export PDK_ROOT=/foss/pdks; source .designinit`):
    python3 macros/slot7_testplatform/testbenches/ngspice/run_tb_b.py [ref|ib1|failsafe|all] [--dut layout]
Writes results_b/*.csv (results_b_layout/ with --dut layout).

Harness model (see run_tb.py for the rest):
  - analog_bus2: SMU as a voltmeter, 1 Gohm; analog_bus0 / 1 / 3: SMU forcing 0.7 V (current = i(Vbusk));
  - ibias0 / ibias1: the harness bias current, present only where the harness bias switch of slot 7 would be on
    (ibias0 as tree reference; ibias1 in its own test): an ideal 5 uA source with a clamp diode to a node 0.7 V below
    the 3.3 V rail, so the pin cannot rise above the rail (the harness source is a PMOS current source on the same
    supply). Otherwise the pin floats (1 Tohm). (First version, 2026-11-06: a clamp 0.6 V ABOVE the rail forward-biased
    the xgate PMOS junctions and fed current into iref / analog_bus3 through switches that were off; see RUNLOG.)
Cases:
  ref:      reference = OA core (dig_in[0], dig_in[4]), BG core (dig_in[1], dig_in[5]) or ibias0 (dig_in[6]); tree on
            (dig_in[7]); each of vbp / vbn / vbpc / vbnc in turn onto analog_bus2 (dig_in[8..11]); stage-A bus switches
            off. Then the tree off (dig_in[7] = 0) with vbp still selected. Also the tree input current (TG TGN drain).
  ib1:      dig_in[12] on / off, analog_bus3 at 0.7 V: current of ibias1 through the slot.
  failsafe: every dig_in = 1, enable = 1, the slot's vdd_1v2 gated off (+1 uA injected): nothing on bus2 / bus3.
"""
import csv
import itertools
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_tb as A                          # noqa: E402

MAC = A.MAC
INCLUDES_B = [os.path.join(MAC, 'netlist', 'source', 'slot7_stage_b.spice'),
              os.path.join(A.ROOT, 'macros', 'bias_tree_noab_pd', 'netlist', 'source', 'bias_tree_noab_pd.spice')]
A.INCLUDES = A.INCLUDES + INCLUDES_B
A.OUT = os.path.join(HERE, 'results_b')
LAYOUT_NET = None
PORTS_AB = (['vdd_3v3', 'vss_3v3', 'vdd_1v2', 'vss_1v2', 'enable'] + [f'din{k}' for k in range(13)]
            + [f'dout{k}' for k in range(12)] + ['analog_bus0', 'analog_bus1', 'analog_bus2', 'analog_bus3',
                                                 'ibias0', 'ibias1'])
PIN_AB = (['vdd_3v3', 'vss_3v3', 'vdd_1v2', 'vss_1v2', 'enable'] + [f'dig_in[{k}]' for k in range(13)]
          + [f'dig_out[{k}]' for k in range(12)] + ['analog_bus0', 'analog_bus1', 'analog_bus2', 'analog_bus3',
                                                   'ibias0', 'ibias1'])
MUX = ['vbp', 'vbn', 'vbpc', 'vbnc']


def dut():
    if LAYOUT_NET is None:
        return 'X1 ' + ' '.join(PORTS_AB) + ' slot7_testplatform_ab\n'
    head = re.search(r'^\.subckt slot_7 (.*?)$((?:\n\+.*$)*)', open(LAYOUT_NET).read(), re.M)
    ports = (head.group(1) + head.group(2).replace('\n+', ' ')).split()
    tb = dict(zip(PIN_AB, PORTS_AB))
    nets, extra = [], ''
    for p in ports:
        if p in tb:
            nets.append(tb[p])
        else:
            n = 'nc_' + re.sub(r'\W', '_', p)
            nets.append(n)
            extra += f'R{n} {n} 0 1e12\n'
    return f'.include {LAYOUT_NET}\nX1 {" ".join(nets)} slot_7\n' + extra


def bench(corner, temp, v3, v1, dig, en=1, on1=True, ileak=0.0, ib0=False, ib1=False):
    """dig: dict k -> 0/1 for dig_in[k]; ib0 / ib1: harness bias source connected."""
    t = A.header(corner, temp, '.include diodes.lib\n.model dclamp d is=1e-14\n')
    t += A.supplies(v3, v1, True, on1, ileak)
    t += f'Ven enable 0 {v1 if en else 0}\n'
    for k in range(13):
        t += f'Vd{k} din{k} 0 {v1 if dig.get(k) else 0}\n'
    t += ''.join(f'Rdo{k} dout{k} 0 1e12\n' for k in range(12))
    t += 'Vbus0 analog_bus0 0 0.7\nVbus1 analog_bus1 0 0.7\nRbus2 analog_bus2 0 1e9\nVbus3 analog_bus3 0 0.7\n'
    t += f'Vhb vhb 0 {v3 - 0.7}\nVhs vhs 0 {v3}\n'
    for n, on in (('ibias0', ib0), ('ibias1', ib1)):
        t += (f'I{n} vhs {n} 5u\nD{n} {n} vhb dclamp\n' if on else f'R{n} {n} 0 1e12\n')
    t += dut()
    return t


def write(name, rows):
    os.makedirs(A.OUT, exist_ok=True)
    with open(os.path.join(A.OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print('wrote', os.path.join(A.OUT, name))


def ref():
    rows = []
    REFS = {'oa': {0: 1, 4: 1}, 'bg': {1: 1, 5: 1}, 'ib0': {6: 1}}
    for corner, temp, (sname, (v3, v1)) in itertools.product(A.CORNERS, A.TEMPS, A.SUPPLIES.items()):
        for rname, bits in REFS.items():
            dig = dict(bits)
            dig[7] = 1
            dig[8] = 1
            t = bench(corner, temp, v3, v1, dig, ib0=(rname == 'ib0'))
            t += '.control\n'
            for m, k in enumerate(range(8, 12)):
                t += ''.join(f'alter Vd{j} dc={v1 if j == k else 0}\n' for j in range(8, 12))
                t += f'op\nprint v(analog_bus2) i(vbus0) i(vbus1) i(vbus3)\n'
            t += 'alter Vd8 dc=' + str(v1) + '\nalter Vd11 dc=0\nalter Vd7 dc=0\nop\nprint v(analog_bus2) i(vbus0) i(vbus1) i(vbus3)\n'
            t += '.endc\n.end\n'
            p, path = A.run_raw(f'b_ref_{corner}_{temp}_{sname}_{rname}', t)
            v = [float(x) for x in re.findall(r'^v\(analog_bus2\)\s+=\s+(\S+)', p.stdout, re.M)]
            ihb = [float(x) for x in re.findall(r'^i\(vhb\)\s+=\s+(\S+)', p.stdout, re.M)]
            if len(v) != 5:
                sys.stderr.write(p.stdout[-2000:])
                raise SystemExit('failed ' + path)
            row = dict(corner=corner, temp=temp, supply=sname, ref=rname)
            row.update({m: v[i] for i, m in enumerate(MUX)})
            row['bus2_tree_off'] = v[4]
            row['retried'] = 1 if any(n.startswith(f'b_ref_{corner}_{temp}_{sname}_{rname}') for n in A.RETRIED) else 0
            rows.append(row)
            print('ref', corner, temp, sname, rname, ' '.join('%s=%.4f' % (m, row[m]) for m in MUX),
                  'off=%.3g' % v[4], flush=True)
    write('ref.csv', rows)


def ib1():
    rows = []
    for corner, temp, (sname, (v3, v1)) in itertools.product(A.CORNERS, A.TEMPS, A.SUPPLIES.items()):
        t = bench(corner, temp, v3, v1, {12: 1}, ib1=True)
        t += '.control\nop\nprint i(vbus3)\nalter Vd12 dc=0\nop\nprint i(vbus3)\n.endc\n.end\n'
        p, path = A.run_raw(f'b_ib1_{corner}_{temp}_{sname}', t)
        i = [float(x) for x in re.findall(r'^i\(vbus3\)\s+=\s+(\S+)', p.stdout, re.M)]
        if len(i) != 2:
            sys.stderr.write(p.stdout[-2000:])
            raise SystemExit('failed ' + path)
        rows.append(dict(corner=corner, temp=temp, supply=sname, i_bus3_on=i[0], i_bus3_off=i[1]))
        print('ib1', corner, temp, sname, i, flush=True)
    write('ib1.csv', rows)


def failsafe():
    rows = []
    for corner, temp, (sname, (v3, v1)) in itertools.product(A.CORNERS, A.TEMPS, A.SUPPLIES.items()):
        for case, on1, il in (('vdd1v2_off', False, 0.0), ('vdd1v2_off_1uA', False, 1e-6), ('enable_low', True, 0.0)):
            dig = {k: 1 for k in range(13)}
            t = bench(corner, temp, v3, v1, dig, en=0 if case == 'enable_low' else 1, on1=on1, ileak=il, ib0=True, ib1=True)
            t += '.control\nop\nprint v(analog_bus2) i(vbus0) i(vbus1) i(vbus3)\n.endc\n.end\n'
            vals, _ = A.run(f'b_fs_{corner}_{temp}_{sname}_{case}', t)
            rows.append(dict(corner=corner, temp=temp, supply=sname, case=case, v_bus2=vals.get('v(analog_bus2)'),
                             i_bus0=vals.get('i(vbus0)'), i_bus1=vals.get('i(vbus1)'), i_bus3=vals.get('i(vbus3)')))
            print('failsafe', corner, temp, sname, case, rows[-1]['v_bus2'], rows[-1]['i_bus3'], flush=True)
    write('failsafe.csv', rows)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if '--dut' in sys.argv and sys.argv[sys.argv.index('--dut') + 1] == 'layout':
        LAYOUT_NET = os.path.join(MAC, 'netlist', 'layout', 'slot_7_magic.ext.spc')
        A.INCLUDES = []
        A.OUT = os.path.join(HERE, 'results_b_layout')
    for w in (['ref', 'ib1', 'failsafe'] if what == 'all' else [what]):
        globals()[w]()
    print('retried (rshunt 1e14; :gear = also method=gear reltol=1e-3):', len(A.RETRIED), A.RETRIED)
