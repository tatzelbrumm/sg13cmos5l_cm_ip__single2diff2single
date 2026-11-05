#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Add a port that the layout extraction cannot see to a PEX netlist, tied to another net by a resistor.

Usage: pex_add_port.py <pex.spice> <subckt> <port> <net> <ohm>

Written for the pad cells (cloud session C3, 2026-11-05). Their vss ring rail joins iovss through the p-substrate (the
vss band's p+ tie and the iovss ties). Magic puts every p+ tie on one substrate node, and the top cell has no vss text,
so the extracted subckt has no vss port: 11 ports instead of the symbol's 12, and sak-pin-reorder.py stops. The sheet
models the same path as Rsub (1 Ohm vss - iovss, simulation only). This script does the same for the PEX netlist:
it appends <port> to the .subckt line and adds "Rport_<port> <port> <net> <ohm>" before .ends. A netlist that already
has <port> is left unchanged. The file is rewritten in place.
"""
import sys


def main(argv):
    if len(argv) != 5:
        sys.exit(__doc__)
    path, subckt, port, net, ohm = argv
    lines = open(path).read().split('\n')
    # the .subckt statement with its continuation lines
    start = next(i for i, l in enumerate(lines)
                 if l.lower().startswith('.subckt') and l.split()[1] == subckt)
    end = start
    while end + 1 < len(lines) and lines[end + 1].startswith('+'):
        end += 1
    ports = ' '.join([lines[start]] + [l[1:] for l in lines[start + 1:end + 1]]).split()[2:]
    if port in ports:
        print(f'{path}: {subckt} already has port {port}, unchanged')
        return
    if net not in ports:
        sys.exit(f'{path}: {subckt} has no port {net} to tie {port} to')
    lines[end] += f' {port}'
    stop = next(i for i in range(end + 1, len(lines)) if lines[i].lower().startswith('.ends'))
    lines.insert(stop, f'Rport_{port} {port} {net} {ohm}')
    open(path, 'w').write('\n'.join(lines))
    print(f'{path}: {subckt}: port {port} added, tied to {net} by {ohm} Ohm')


if __name__ == '__main__':
    main(sys.argv[1:])
