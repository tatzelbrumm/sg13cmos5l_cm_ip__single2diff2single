#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Intrinsic DC/small-signal characterization of the IHP sg13cmos5l ESD-clamp
frames reused as class-AB output devices (sg13_hv_nmos / sg13_hv_pmos, L=0.6um).

One full frame per polarity, as the Clamp_N / Clamp_P PCells allow:
  N: ng=42, 4.4 um fingers, 1 row         -> W = 184.8 um
  P: ng=41, 6.66 um fingers, 2 stacked rows -> 82 fingers, W = 546.12 um
Pre-layout models only: no strap/via resistance, no ESD structures.

Usage (IIC-OSIC-TOOLS, after `source .designinit`):
    python3 output_driver_char.py > results.txt
Models: $MODELDIR, else $PDK_ROOT/$PDK/libs.tech/ngspice/models.
OSDI:   if $OSDI_DIR is set, psp103{,_nqs}.osdi are loaded from there;
        otherwise ngspice's own .spiceinit (the container's) must load them.
"""
import os, subprocess, tempfile
import numpy as np

MODELDIR = os.environ.get('MODELDIR') or os.path.join(
    os.environ.get('PDK_ROOT', '/foss/pdks'), os.environ.get('PDK', 'ihp-sg13cmos5l'),
    'libs.tech', 'ngspice', 'models')
OSDI_DIR = os.environ.get('OSDI_DIR')
VDD = 3.3
DEV = {'n': dict(w=4.4 * 42, nf=42, ngmax=42, model='sg13_hv_nmos'),
       'p': dict(w=6.66 * 82, nf=82, ngmax=41, model='sg13_hv_pmos')}
OPVARS = ['ids', 'gm', 'gds', 'cgg', 'cgdol', 'cjd']
WORK = tempfile.mkdtemp(prefix='odc_')
if OSDI_DIR:
    with open(os.path.join(WORK, '.spiceinit'), 'w') as f:
        f.write('set ngbehavior=hsa\n')
        for m in ('psp103.osdi', 'psp103_nqs.osdi'):
            f.write(f"osdi {os.path.join(OSDI_DIR, m)}\n")


def sweep(dev, corner, temp, swept, fixval, start, stop, step, L=0.6, nf=None):
    """|V| magnitudes throughout: PMOS source sits at VDD, nodes = VDD - |V|.
    swept = 'd' (fixval = |Vgs|) or 'g' (fixval = |Vds|)."""
    d = dict(DEV[dev])
    if nf is not None:
        d['w'] = d['w'] / d['nf'] * nf
        d['nf'] = nf
    inst = f"n.x1.n{d['model']}"
    vd, vg = (0, fixval) if swept == 'd' else (fixval, 0)
    if dev == 'n':
        body = f"Vd d 0 {vd}\nVg g 0 {vg}\nX1 d g 0 0 {d['model']} w={d['w']}u l={L}u ng={d['nf']}\n"
    else:
        body = (f"Vd d 0 {vd}\nVg g 0 {vg}\nVs s 0 {VDD}\nEd s dd d 0 1\nEg s gg g 0 1\n"
                f"X1 dd gg s s {d['model']} w={d['w']}u l={L}u ng={d['nf']}\n")
    saves = ' '.join(f'@{inst}[{v}]' for v in OPVARS)
    net = (f"* output driver char\n.lib {MODELDIR}/cornerMOShv.lib {corner}\n.temp {temp}\n{body}"
           f".save {saves}\n.control\ndc V{swept} {start} {stop} {step}\n"
           f"wrdata out.txt {saves}\n.endc\n.end\n")
    with open(os.path.join(WORK, 'tb.cir'), 'w') as f:
        f.write(net)
    r = subprocess.run(['ngspice', '-b', 'tb.cir'], cwd=WORK, capture_output=True, text=True)
    try:
        a = np.loadtxt(os.path.join(WORK, 'out.txt'))
    except OSError:
        raise SystemExit(r.stdout + r.stderr)
    return a[:, 0], {v: np.abs(a[:, 2 * i + 1]) for i, v in enumerate(OPVARS)}


def full_drive():
    print(f"== Full gate drive |Vgs|={VDD} V, one full frame each")
    pts = [0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 1.65, 3.3]
    for dev in 'np':
        for corner, T in [('mos_tt', 27), ('mos_ss', 27), ('mos_ff', 27), ('mos_ss', 125)]:
            x, r = sweep(dev, corner, T, 'd', VDD, 0, VDD, 0.01)
            I = np.interp(pts, x, r['ids'])
            print(f"{dev} {corner} {T:3d}C Ron(50mV)={0.05 / I[0]:5.1f} ohm " +
                  " ".join(f"I({p})={i * 1e3:5.1f}mA" for p, i in zip(pts[1:], I[1:])))


def fingers_for(itarget=10e-3):
    print(f"\n== Fingers of one frame needed for {itarget * 1e3:g} mA, mos_ss 125C (hd = |Vds| headroom)")
    for dev in 'np':
        for vg in [2.0, 2.5, 3.0, 3.3]:
            x, r = sweep(dev, 'mos_ss', 125, 'd', vg, 0, VDD, 0.01)
            cells = []
            for hd in [0.2, 0.3, 0.5]:
                I = np.interp(hd, x, r['ids'])
                cells.append(f"hd={hd}V {I * 1e3:5.1f}mA/frame ng={itarget / I * DEV[dev]['ngmax']:5.1f}")
            print(f"{dev} |Vgs|={vg}  " + "  ".join(cells))


def small_signal(vds=1.65):
    print(f"\n== Small signal vs quiescent current, |Vds|={vds} V, mos_tt 27C, one full frame")
    for dev in 'np':
        x, r = sweep(dev, 'mos_tt', 27, 'g', vds, 0.2, VDD, 0.005)
        for IQ in [10e-6, 30e-6, 100e-6, 300e-6, 1e-3, 3e-3, 10e-3]:
            vg = np.interp(np.log(IQ), np.log(r['ids'] + 1e-15), x)
            g = {k: np.interp(vg, x, r[k]) for k in OPVARS}
            print(f"{dev} IQ={IQ * 1e6:6.0f}uA |Vgs|={vg:5.3f} gm={g['gm'] * 1e3:6.3f}mS "
                  f"gm/Id={g['gm'] / IQ:5.1f}/V gds={g['gds'] * 1e6:6.2f}uS Cgg={g['cgg'] * 1e15:5.0f}fF "
                  f"Cjd={g['cjd'] * 1e15:3.0f}fF Cgdov={g['cgdol'] * 1e15:3.0f}fF "
                  f"fT={g['gm'] / (2 * np.pi * g['cgg']) / 1e6:6.0f}MHz")


def length_comparison(itarget=10e-3):
    """Same 80 um frame at longer L. Finger pitch = L + 0.91 um (drain 1.18 / source 0.64
    kept), so fingers per frame = (63.7 - 0.3) / (L + 0.91). Frames needed for itarget at
    0.3 V headroom, |Vgs| = 2.5 V, mos_ss 125C. Idle current: |Vgs| fixed for 100 uA at
    |Vds| = 1.65 V (tt 27C), then |Vds| moved to 0.5 / 2.8 V."""
    print(f"\n== Length comparison, one 80 um frame (P: 2 rows), {itarget * 1e3:g} mA target")
    for dev, rows in [('n', 1), ('p', 2)]:
        for L in [0.6, 1.0, 2.0]:
            nf_frame = int((63.7 - 0.3) / (L + 0.91))
            nf = nf_frame * rows
            x, r = sweep(dev, 'mos_ss', 125, 'd', 2.5, 0, VDD, 0.01, L, nf)
            frames = itarget / np.interp(0.3, x, r['ids'])
            x, r = sweep(dev, 'mos_tt', 27, 'g', 1.65, 0.2, 2.0, 0.001, L, nf)
            vg = np.interp(np.log(1e-4), np.log(r['ids'] + 1e-15), x)
            g = {k: np.interp(vg, x, r[k]) for k in OPVARS}
            x2, r2 = sweep(dev, 'mos_tt', 27, 'd', vg, 0.3, 3.0, 0.01, L, nf)
            I = np.interp([0.5, 1.65, 2.8], x2, r2['ids'])
            print(f"{dev} L={L} ng/frame={nf_frame:2d} W/frame={DEV[dev]['w'] / DEV[dev]['nf'] * nf:6.1f}um "
                  f"frames={frames:4.2f} | IQ=100uA: gm/gds={g['gm'] / g['gds']:5.0f} VA={1e-4 / g['gds']:5.1f}V "
                  f"Cgg={g['cgg'] * 1e15:5.0f}fF Cgdov={g['cgdol'] * 1e15:3.0f}fF "
                  f"Id(Vds=0.5/1.65/2.8)={I[0] * 1e6:3.0f}/{I[1] * 1e6:3.0f}/{I[2] * 1e6:3.0f}uA")


if __name__ == '__main__':
    print(f"# models: {MODELDIR}\n# osdi: {OSDI_DIR or '(from .spiceinit)'}")
    full_drive()
    fingers_for()
    small_signal()
    length_comparison()
