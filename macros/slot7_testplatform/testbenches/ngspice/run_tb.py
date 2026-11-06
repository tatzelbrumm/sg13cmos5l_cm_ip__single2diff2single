#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Stage-A testbenches of slot7_testplatform (ngspice, batch).

Usage (design repo root, after `export PDK_ROOT=/foss/pdks; source .designinit`):
    python3 macros/slot7_testplatform/testbenches/ngspice/run_tb.py [static|sweep|tran|leak|all] [--dut source|layout]

Writes CSV files and the generated netlists to macros/slot7_testplatform/testbenches/ngspice/results/.

Model of the harness around the slot:
  - bus switches: xgate driven by tp_en_ctrl (dig_in[2] / dig_in[3]).
  - SMU on analog_bus0 / analog_bus1: an ideal voltage source V_F (default 0.7 V); the current out of the slot into
    the SMU is i(Vbusk) (positive = sourced by the slot). The harness switch analog_switch_med and the pad are not
    modelled: they add series resistance (a few ohms at 5 uA: negligible) and leakage (measured separately on chip).
  - dig_in, enable: ideal 1.2 V sources (the harness drives them from its always-on rail, see PLAN.md section 1).
  - gated supply on: ideal source; gated supply off: the source removed, 1 Tohm to ground (power_stage* outputs float).
"""
import csv
import itertools
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAC = os.path.normpath(os.path.join(HERE, '..', '..'))
ROOT = os.path.normpath(os.path.join(MAC, '..', '..'))
PDK = os.path.join(os.environ.get('PDK_ROOT', '/foss/pdks'), os.environ.get('PDK', 'ihp-sg13cmos5l'))
OUT = os.path.join(HERE, 'results')
INCLUDES = [
    os.path.join(MAC, 'netlist', 'source', 'slot7_testplatform.spice'),
    os.path.join(ROOT, 'macros', 'bias_tree_pd', 'netlist', 'source', 'bias_ref_pd.spice'),
    os.path.join(ROOT, 'macros', 'ocd_analog_switches', 'netlist', 'source', 'ocd_analog_switches.spice'),
]
CORNERS = ['tt', 'ss', 'ff', 'sf', 'fs']
RES = {'tt': 'res_typ', 'ss': 'res_wcs', 'ff': 'res_bcs', 'sf': 'res_typ', 'fs': 'res_typ'}
TEMPS = [-40, 27, 125]
SUPPLIES = {'low': (3.0, 1.08), 'nom': (3.3, 1.2), 'high': (3.6, 1.32)}
# testbench node names (no brackets: ngspice reads v(a[0]) as a vector index); the DUT ports keep the pin names
PORTS = ('vdd_3v3 vss_3v3 vdd_1v2 vss_1v2 enable din0 din1 din2 din3 '
         + ' '.join(f'dout{k}' for k in range(12)) + ' analog_bus0 analog_bus1')
DUT = 'slot7_testplatform'


def header(corner, temp, extra=''):
    inc = '\n'.join(f'.include {p}' for p in INCLUDES)
    return f"""* slot7_testplatform testbench ({corner}, {temp} C)
.lib cornerMOShv.lib mos_{corner}
.lib cornerMOSlv.lib mos_{corner}
.lib cornerRES.lib {RES[corner]}
.lib cornerPNP.lib typ
.lib cornerCAP.lib cap_typ
.include diodes.lib
{inc}
.temp {temp}
.option gmin=1e-12 reltol=1e-4 abstol=1e-15
{extra}
"""


LAYOUT_NET = None          # set by --dut layout: magic's LVS extraction of slot_7.gds (devices only, no parasitics)


def dut_line():
    if LAYOUT_NET is None:
        return f'X1 {PORTS} {DUT}\n'
    # instance of the extracted subckt slot_7, ports connected by name; unused slot pins get 1 Tohm to ground
    head = re.search(r'^\.subckt slot_7 (.*?)$((?:\n\+.*$)*)', open(LAYOUT_NET).read(), re.M)
    ports = (head.group(1) + head.group(2).replace('\n+', ' ')).split()
    tb = dict(zip(['vdd_3v3', 'vss_3v3', 'vdd_1v2', 'vss_1v2', 'enable'] + [f'dig_in[{k}]' for k in range(4)]
                  + [f'dig_out[{k}]' for k in range(12)] + ['analog_bus0', 'analog_bus1'], PORTS.split()))
    nets, extra = [], ''
    for p in ports:
        if p in tb:
            nets.append(tb[p])
        else:
            n = 'nc_' + re.sub(r'\W', '_', p)
            nets.append(n)
            extra += f'R{n} {n} 0 1e12\n'
    return f'.include {LAYOUT_NET}\nX1 {" ".join(nets)} slot_7\n' + extra


def supplies(v3, v1, on3=True, on1=True, ileak=0.0):
    s = 'Vss3 vss_3v3 0 0\nVss1 vss_1v2 0 0\n'
    if not on1 and ileak:
        s += f'Ileak1 0 vdd_1v2 {ileak}\n'          # off-leakage of the harness power gate into the floating rail
    s += f'V3 vdd_3v3 0 {v3}\n' if on3 else 'R3off vdd_3v3 0 1e12\n'
    s += f'V1 vdd_1v2 0 {v1}\n' if on1 else 'R1off vdd_1v2 0 1e12\n'
    return s


def digital(v1, en, d):
    s = f'Ven enable 0 {v1 if en else 0}\n'
    for k in range(4):
        s += f'Vd{k} din{k} 0 {v1 if d[k] else 0}\n'
    s += ''.join(f'Rdo{k} dout{k} 0 1e12\n' for k in range(12))
    return s


RETRIED = []


def _ngspice(path):
    return subprocess.run(['ngspice', '-b', path], capture_output=True, text=True, timeout=900, cwd=OUT)


def run_raw(name, text):
    """Run a netlist; if ngspice fails (convergence: floating nodes of a disabled core), retry once with rshunt 1e14
    (100 Tohm from every node to ground) added. Retried names are kept in RETRIED.
    gmin is 1e-12 throughout: with 1e-15 a few static points (tt / fs at -40 C) settled on non-physical operating
    points of the disabled cores' floating nodes (0.03 .. 1 uA through an open switch; 2 pA at 1e-12; RUNLOG).
    Currents below ~10 pA are therefore at the simulation floor."""
    os.makedirs(os.path.join(OUT, 'netlists'), exist_ok=True)
    path = os.path.join(OUT, 'netlists', name + '.spice')
    with open(path, 'w') as f:
        f.write(text)
    p = _ngspice(path)
    if p.returncode != 0 or 'no simulations run' in p.stdout or 'aborted' in p.stdout:
        text = text.replace('.option gmin=1e-12', '.option gmin=1e-12 rshunt=1e14')
        with open(path, 'w') as f:
            f.write(text)
        p = _ngspice(path)
        RETRIED.append(name)
        if p.returncode != 0 or 'no simulations run' in p.stdout or 'aborted' in p.stdout:
            # second level (transients at -40 C: timestep too small in the bandgap's pnpMPA at the enable edge):
            # Gear integration and reltol 1e-3
            text = text.replace('reltol=1e-4 abstol=1e-15', 'reltol=1e-3 abstol=1e-15 method=gear')
            with open(path, 'w') as f:
                f.write(text)
            p = _ngspice(path)
            RETRIED.append(name + ':gear')
    return p, path


def run(name, text):
    p, path = run_raw(name, text)
    vals = {}
    for line in p.stdout.splitlines():
        m = re.match(r'^\s*(\S+)\s+=\s+(\S+)\s*$', line)
        if m:
            try:
                vals[m.group(1).lower()] = float(m.group(2))
            except ValueError:
                pass
    if p.returncode != 0 or not vals:
        sys.stderr.write(p.stdout[-3000:] + p.stderr[-3000:])
        raise SystemExit(f'ngspice failed on {path}')
    vals['retried'] = 1.0 if name in RETRIED else 0.0
    return vals, p.stdout


# --- static states -------------------------------------------------------------------------------------------
# (name, enable, dig_in[3:0] as d0..d3, vdd_3v3 on, vdd_1v2 on)
STATES = [
    ('all_off',        1, (0, 0, 0, 0), 1, 1),
    ('tg_on_cores_off', 1, (0, 0, 1, 1), 1, 1),
    ('oa_on',          1, (1, 0, 1, 0), 1, 1),
    ('bg_on',          1, (0, 1, 0, 1), 1, 1),
    ('both_on',        1, (1, 1, 1, 1), 1, 1),
    ('cores_on_tg_off', 1, (1, 1, 0, 0), 1, 1),
    ('enable_low',     0, (1, 1, 1, 1), 1, 1),
    ('vdd1v2_off',     1, (1, 1, 1, 1), 1, 0),
    ('vdd1v2_off_1uA',  1, (1, 1, 1, 1), 1, 0),
    ('vdd3v3_off',     1, (1, 1, 1, 1), 0, 1),
    ('both_supplies_off', 1, (1, 1, 1, 1), 0, 0),
]
PROBES = ['i(vbus0)', 'i(vbus1)', 'v(x1.en_oa)', 'v(x1.en_oa_b)', 'v(x1.en_bg)', 'v(x1.en_bg_b)',
          'v(x1.en_tg0)', 'v(x1.en_tg0_b)', 'v(x1.en_tg1)', 'v(x1.en_tg1_b)',
          'v(dout0)', 'v(dout1)', 'v(dout2)', 'v(dout3)', 'v(dout4)', 'v(dout11)', 'v(vdd_3v3)', 'v(vdd_1v2)',
          'v(x1.i_oa)', 'v(x1.i_bg)']


def static(vf=0.7):
    rows = []
    for corner, temp, (sname, (v3, v1)) in itertools.product(CORNERS, TEMPS, SUPPLIES.items()):
        for st, en, d, on3, on1 in STATES:
            t = header(corner, temp) + supplies(v3, v1, on3, on1, 1e-6 if st.endswith('_1uA') else 0.0) + digital(v1, en, d)
            t += f'Vbus0 analog_bus0 0 {vf}\nVbus1 analog_bus1 0 {vf}\n' + dut_line()
            probes = [p for p in PROBES if LAYOUT_NET is None or 'x1.' not in p]
            ilines = ' '.join(probes + ['i(v3)' if on3 else 'v(vdd_3v3)', 'i(v1)' if on1 else 'v(vdd_1v2)'])
            t += f'.control\nop\nprint {ilines}\n.endc\n.end\n'
            vals, _ = run(f'static_{corner}_{temp}_{sname}_{st}', t)
            row = dict(corner=corner, temp=temp, supply=sname, v3=v3, v1=v1, state=st, enable=en,
                       dig_in=''.join(map(str, d)), vdd_3v3_on=on3, vdd_1v2_on=on1)
            row.update({k: vals.get(k.lower(), '') for k in PROBES + ['i(v3)', 'i(v1)', 'retried']})
            rows.append(row)
            print(corner, temp, sname, st, 'I0=%.4g I1=%.4g' % (vals.get('i(vbus0)', 0), vals.get('i(vbus1)', 0)),
                  flush=True)
    write('static.csv', rows)
    return rows


def sweep():
    rows = []
    for corner, temp in itertools.product(CORNERS, TEMPS):
        t = header(corner, temp) + supplies(3.3, 1.2) + digital(1.2, 1, (1, 1, 1, 1))
        t += 'Vbus0 analog_bus0 0 0.7\nVbus1 analog_bus1 0 0.7\n' + dut_line()
        pts = [round(0.1 * k, 2) for k in range(0, 31)]
        t += '.control\n'
        for v in pts:
            t += f'alter Vbus0 dc={v}\nalter Vbus1 dc={v}\nop\nprint i(vbus0) i(vbus1)\n'
        t += '.endc\n.end\n'
        p, path = run_raw(f'sweep_{corner}_{temp}', t)
        i0 = [float(x) for x in re.findall(r'^i\(vbus0\)\s+=\s+(\S+)', p.stdout, re.M)]
        i1 = [float(x) for x in re.findall(r'^i\(vbus1\)\s+=\s+(\S+)', p.stdout, re.M)]
        if len(i0) != len(pts):
            sys.stderr.write(p.stdout[-2000:])
            raise SystemExit('sweep failed ' + path)
        for v, a, b in zip(pts, i0, i1):
            rows.append(dict(corner=corner, temp=temp, v_bus=v, i_oa=a, i_bg=b))
        print('sweep', corner, temp, 'I(0.7V) OA %.4g BG %.4g' % (i0[7], i1[7]), flush=True)
    write('sweep.csv', rows)


def tran():
    """dig_in[0]/[1] (core enables) ramp 0 -> 1.2 V in 100 ns at 1 us (a 10 ns edge stopped ngspice: timestep too small
    in the bandgap's pnpMPA) with the TGs already closed and the bus at 0.7 V;
    off again at 101 us. Settling: time until within 1 % of the final current."""
    rows = []
    for corner, temp in itertools.product(CORNERS, TEMPS):
        t = header(corner, temp) + supplies(3.3, 1.2)
        t += 'Ven enable 0 1.2\nVd2 din2 0 1.2\nVd3 din3 0 1.2\n'
        t += 'Vd0 din0 0 pwl(0 0 1u 0 1.1u 1.2 101u 1.2 101.1u 0)\n'
        t += 'Vd1 din1 0 pwl(0 0 1u 0 1.1u 1.2 101u 1.2 101.1u 0)\n'
        t += ''.join(f'Rdo{k} dout{k} 0 1e12\n' for k in range(12))
        t += 'Vbus0 analog_bus0 0 0.7\nVbus1 analog_bus1 0 0.7\n' + dut_line()
        t += """.control
tran 20n 200u
meas tran i0_on find i(vbus0) at=99u
meas tran i1_on find i(vbus1) at=99u
meas tran i0_off find i(vbus0) at=199u
meas tran i1_off find i(vbus1) at=199u
let lim0 = 0.99*i0_on
let lim1 = 0.99*i1_on
meas tran t0_on when i(vbus0)=lim0 rise=last from=1u to=100u
meas tran t1_on when i(vbus1)=lim1 rise=last from=1u to=100u
let l0 = 0.01*i0_on
let l1 = 0.01*i1_on
meas tran t0_off when i(vbus0)=l0 fall=last from=101u to=200u
meas tran t1_off when i(vbus1)=l1 fall=last from=101u to=200u
.endc
.end
"""
        vals, out = run(f'tran_{corner}_{temp}', t)
        row = dict(corner=corner, temp=temp)
        for k in ('i0_on', 'i1_on', 'i0_off', 'i1_off', 't0_on', 't1_on', 't0_off', 't1_off'):
            row[k] = vals.get(k, '')
        rows.append(row)
        print('tran', row, flush=True)
    write('tran.csv', rows)


def leak():
    """Open TGs (dig_in = 0, cores off, enable = 1): bus current vs. bus voltage 0..3.3 V and temperature."""
    rows = []
    for corner, temp in itertools.product(CORNERS, TEMPS):
        t = header(corner, temp) + supplies(3.3, 1.2) + digital(1.2, 1, (0, 0, 0, 0))
        t += 'Vbus0 analog_bus0 0 0\nVbus1 analog_bus1 0 0\n' + dut_line()
        pts = [0.0, 0.7, 1.65, 2.5, 3.3]
        t += '.control\n' + ''.join(f'alter Vbus0 dc={v}\nalter Vbus1 dc={v}\nop\nprint i(vbus0) i(vbus1)\n' for v in pts)
        t += '.endc\n.end\n'
        p, path = run_raw(f'leak_{corner}_{temp}', t)
        i0 = [float(x) for x in re.findall(r'^i\(vbus0\)\s+=\s+(\S+)', p.stdout, re.M)]
        i1 = [float(x) for x in re.findall(r'^i\(vbus1\)\s+=\s+(\S+)', p.stdout, re.M)]
        for v, a, b in zip(pts, i0, i1):
            rows.append(dict(corner=corner, temp=temp, v_bus=v, i_bus0=a, i_bus1=b))
        print('leak', corner, temp, ['%.3g' % x for x in i0], flush=True)
    write('leak.csv', rows)


def write(name, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print('wrote', os.path.join(OUT, name))


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if '--dut' in sys.argv and sys.argv[sys.argv.index('--dut') + 1] == 'layout':
        # extracted netlist of final/gds/slot_7.gds (magic, as in the LVS); internal nets have extraction names, so
        # probes of internal nodes (x1.en_oa ...) are empty: only the pin currents and voltages are compared
        LAYOUT_NET = os.path.join(MAC, 'netlist', 'layout', 'slot_7_magic.ext.spc')
        INCLUDES = []                    # the extraction is flat: cores, xgate and tp_en_ctrl devices are all in it
        OUT = os.path.join(HERE, 'results_layout')
    for w in (['static', 'sweep', 'tran', 'leak'] if what == 'all' else [what]):
        globals()[w]()
    print('retried (rshunt 1e14; :gear = also method=gear reltol=1e-3):', len(RETRIED), RETRIED)
