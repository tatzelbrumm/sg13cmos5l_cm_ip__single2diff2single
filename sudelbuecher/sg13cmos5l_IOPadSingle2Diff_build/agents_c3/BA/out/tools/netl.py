#!/usr/bin/env python3
"""netl.py ROOT SHEET OUTDIR [--lvs]: netlist an xschem sheet of ROOT with the PDK rc plus every macro's
schematic / testbench folder (as scripts/xschem/sheet_equiv.py does); prints xschem's messages and the result path."""
import glob, os, subprocess, sys
root, sheet, out = os.path.abspath(sys.argv[1]), sys.argv[2], os.path.abspath(sys.argv[3])
lvs = '--lvs' in sys.argv
os.makedirs(out, exist_ok=True)
dirs = sorted(glob.glob(os.path.join(root, 'macros', '*', 'schematic', 'xschem'))) + \
    sorted(glob.glob(os.path.join(root, 'macros', '*', 'testbenches', 'xschem'))) + \
    [os.path.join(root, 'schematic', 'xschem'), os.path.join(root, 'testbenches', 'xschem')]
rc = os.path.join(out, 'xschemrc_netl')
with open(rc, 'w') as f:
    f.write('source $env(PDK_ROOT)/$env(PDK)/libs.tech/xschem/xschemrc\n')
    for d in dirs:
        if os.path.isdir(d): f.write('append XSCHEM_LIBRARY_PATH :%s\n' % d)
cell = os.path.splitext(os.path.basename(sheet))[0]
name = cell + ('_lvs.cdl' if lvs else '.spice')
path = os.path.join(out, name)
if os.path.exists(path): os.remove(path)
cmd = ['xschem', '-n', '-s', '-q', '-x', '--no_x', '--rcfile', rc, '-o', out, '-N', name]
if lvs:
    cmd += ['--tcl', 'set lvs_netlist 1; set spiceprefix 1; set top_is_subckt 1; set lvs_ignore 1']
cmd.append(os.path.join(root, sheet))
r = subprocess.run(cmd, cwd=out, env=dict(os.environ, PWD=out), capture_output=True, text=True, timeout=300)
msg = (r.stdout + r.stderr).strip()
print('xschem exit %d %s' % (r.returncode, sheet))
if msg: print(msg)
if not os.path.exists(path): print('NO NETLIST'); sys.exit(2)
miss = sum('IS MISSING' in l.upper() for l in open(path))
print('netlist %s, %d missing symbol line(s)' % (path, miss))
sys.exit(1 if miss else 0)
