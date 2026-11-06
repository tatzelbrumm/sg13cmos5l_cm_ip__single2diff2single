#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Merge LEF PIN blocks of the same name into one PIN with all their PORTs (in place).

magic writes two `PIN vss_1v2` blocks for slot_7: the frame's Metal2 strip at the right edge (relabelled vss_1v2 by
the harness, not connected inside the slot) and the TopMetal1 stub at the left edge (connected to the platform).
The delivery LEF before had one PIN with two PORTs; this restores that form.  Usage: lef_merge_pins.py <file.lef>
"""
import re
import sys

text = open(sys.argv[1]).read()
blocks = list(re.finditer(r'^  PIN (\S+)\n(.*?)^  END \1\n', text, re.M | re.S))
seen, out, pos = {}, [], 0
for m in blocks:
    out.append(text[pos:m.start()])
    pos = m.end()
    name, body = m.group(1), m.group(2)
    if name in seen:
        ports = re.findall(r'^    PORT\n.*?^    END\n', body, re.M | re.S)
        i = seen[name]
        out[i] = out[i].replace(f'  END {name}\n', ''.join(ports) + f'  END {name}\n')
    else:
        seen[name] = len(out)
        out.append(m.group(0))
out.append(text[pos:])
open(sys.argv[1], 'w').write(''.join(out))
print(f'{sys.argv[1]}: {len(blocks)} PIN blocks -> {len(seen)} pins')
