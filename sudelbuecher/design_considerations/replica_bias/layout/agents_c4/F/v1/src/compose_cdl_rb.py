# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): the flat LVS reference of pad_ref_rb from the circuit netlists (not from the rows' CDLs).
    python3 compose_cdl_rb.py <out.cdl> <pad_ref_rb.spice> <vcm_rb.spice> <vref_s2d_rb.spice> [<extra.spice>...]
pad_ref_rb is flattened: every X line whose model is sg13_hv_nmos / sg13_hv_pmos becomes one M line per m (m = {ncm}
/ {ncr} evaluated with the instance's parameters, default from the .subckt line), named by its hierarchy path; the
other X lines are subcircuit calls. The ports vdd / vss become vddh / vssh (pin names of the macro). Every dummy of
the circuit files is a device here. Extra files may redefine a subcircuit (later definitions win)."""
import re
import sys

OUT, FILES = sys.argv[1], sys.argv[2:]
MOS = ('sg13_hv_nmos', 'sg13_hv_pmos')
subs = {}
for f in FILES:
    cur, lines = None, []
    for raw in open(f):
        line = raw.split('$')[0].rstrip()
        if line.startswith('+') and lines:
            lines[-1] += ' ' + line[1:].strip()
        elif line.strip() and not line.startswith('*'):
            lines.append(line.strip())
    for line in lines:
        t = line.split()
        if t[0].lower() == '.subckt':
            ports = [x for x in t[2:] if '=' not in x]
            params = dict(x.split('=', 1) for x in t[2:] if '=' in x)
            cur = t[1]
            subs[cur] = (ports, params, [])
        elif t[0].lower() == '.ends':
            cur = None
        elif cur is not None:
            subs[cur][2].append(t)


def val(s, env):
    s = s.strip()
    m = re.fullmatch(r'\{(\w+)\}', s)
    return env[m.group(1)] if m else s


devs = []


def flat(name, conn, env, path):
    ports, params, body = subs[name]
    env = dict(params, **env)
    for t in body:
        if not t[0][0] in 'Xx':
            raise ValueError('unexpected line %s' % t)
        nodes = [x for x in t[1:] if '=' not in x]
        kw = dict(x.split('=', 1) for x in t[1:] if '=' in x)
        model, nodes = nodes[-1], nodes[:-1]
        nets = [conn.get(n, path + n) for n in nodes]
        inst = t[0][1:]
        if model in MOS:
            m = int(float(val(kw.get('m', '1'), env)))
            for i in range(m):
                devs.append(('M%s%s%s' % (path.replace('.', '_'), inst.replace('[', '').replace(']', ''),
                                          '_%d' % i if m > 1 else ''), nets, model, kw['w'], kw['l'], kw.get('ng', '1')))
        else:
            sub_env = {k: val(v, env) for k, v in kw.items()}
            flat(model, dict(zip(subs[model][0], nets)), sub_env, path + inst + '.')


top_ports = subs['pad_ref_rb'][0]
SUP = {'vdd': 'vddh', 'vss': 'vssh'}
flat('pad_ref_rb', {p: SUP.get(p, p) for p in top_ports}, {}, '')
with open(OUT, 'w') as o:
    o.write('* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n')
    o.write('* pad_ref_rb.cdl: flat LVS reference of pad_ref_rb, composed by compose_cdl_rb.py (Claude, agent F, C4)\n')
    o.write('* from: %s\n\n' % ' '.join(f.split('/')[-1] for f in FILES))
    o.write('.SUBCKT pad_ref_rb %s\n' % ' '.join(SUP.get(p, p) for p in top_ports))
    for n, nets, model, w, l, ng in devs:
        o.write('%s %s %s w=%s l=%s ng=%s m=1\n' % (n, ' '.join(n2.replace('.', '_') for n2 in nets), model, w, l, ng))
    o.write('.ENDS pad_ref_rb\n')
act = [d for d in devs if not re.search(r'MD|_MD', d[0]) and 'XMD' not in d[0]]
print('devices: %d (%d with names not starting MD after the path)' % (len(devs), len(act)))
by = {}
for n, nets, model, w, l, ng in devs:
    by[(model, w, l)] = by.get((model, w, l), 0) + 1
for k in sorted(by):
    print('  %-14s w=%-6s l=%-6s %3d' % (k[0], k[1], k[2], by[k]))
