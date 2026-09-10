"""
sg13cmos5l_IOPadAnalog -- Clamp_N20N0D unit cell (self-biased passive NMOS ESD clamp)

Sourced directly from the real IHP sg13cmos5l_io.spi (not a ChatGPT
transcription -- see sudelbuecher/sg13cmos5l_IOPadAnalog/
sg13cmos5l_IOPadAnalog_real_hierarchy.spi for the excerpt with source line
numbers). sg13cmos5l_Clamp_N20N0D has 20 parallel sg13_hv_nmos fingers, all
gated by one internal node "off" that is biased toward iovss by a single
resistor (XRoff). This script draws 3 representative fingers (g0, g1, g2)
plus that resistor -- the electrical unit that repeats 20 times, not the
full array. The 17 elided fingers are identical in structure and net
membership to the ones shown (alternating D/S orientation between "pad"
and "iovss", same W/L, same gate and bulk connections) -- see the real
.spi for the other 17 instance lines verbatim.

This is the one piece of sg13cmos5l_IOPadAnalog that is cleanly
Mosfet+TwoTerm-renderable by this skill. Everything else in the cell is
either more of this same clamp array (17 more N fingers, 40 P fingers in
the P-side mirror Clamp_P20N0D -- not re-rendered, would only repeat this
same picture) or a diode-primitive block (DCNDiode, DCPDiode,
SecondaryProtection's two diodes) that sch_netlist.py has no primitive
for at all.

D/G/S/B per finger, read directly off the real .spi (device line order is
D G S B):
    Xclamp_g0  iovss off pad  iovss   -> D=iovss S=pad   B=iovss
    Xclamp_g1  pad  off iovss iovss   -> D=pad   S=iovss B=iovss
    Xclamp_g2  iovss off pad  iovss   -> D=iovss S=pad   B=iovss   (repeats g0)
    XRoff      iovss off sub! rppd    -> resistor, iovss to "off"
                                          ("sub!" third terminal, a
                                          substrate/guard tie on the
                                          resistor body, is not modeled --
                                          TwoTerm is 2-terminal only; noted
                                          as a simplification, not an
                                          omission of an electrical path)

Every bulk (B) ties to iovss, same as every D or S that happens to land on
iovss -- this is the real device's own bulk connection, not a schematic
simplification.
"""
import sys
sys.path.insert(0, '.')
from sch_netlist import Circuit, Mosfet, TwoTerm, Port, save_png

c = Circuit(620, 380)

IOVSS = c.add(Port('IOVSS', (310, 50), 'IOVSS', kind='rail'))
PAD   = c.add(Port('PAD',   (310, 330), 'PAD',   kind='rail'))

G0 = c.add(Mosfet('G0', 'n', (150, 190), gate='L', label='g0'))
G1 = c.add(Mosfet('G1', 'n', (310, 190), gate='L', label='g1'))
G2 = c.add(Mosfet('G2', 'n', (470, 190), gate='L', label='g2'))

ROFF = c.add(TwoTerm('XRoff', 'R', (560, 90), (560, 190), label='Roff'))

# net "off": every finger's gate, plus the resistor's far terminal from iovss
c.net('off', [G0.P('G'), G1.P('G'), G2.P('G'), ROFF.P('2')], trunk=('v', 560))

# net "iovss": rail, D of g0, S of g1, D of g2, every bulk, resistor's near terminal
c.net('iovss', [IOVSS.P('p'),
                 G0.P('D'), G0.P('B'),
                 G1.P('S'), G1.P('B'),
                 G2.P('D'), G2.P('B'),
                 ROFF.P('1')],
      trunk=('h', 50))

# net "pad": rail, S of g0, D of g1, S of g2
c.net('pad', [PAD.P('p'), G0.P('S'), G1.P('D'), G2.P('S')], trunk=('h', 330))

if __name__ == '__main__':
    v = c.drc()
    if v:
        print('[FAIL] DRC violations:')
        for x in v:
            print('   ', x)
        sys.exit(1)
    c.render('clamp_n20n0d_unitcell.svg')
    save_png('clamp_n20n0d_unitcell.svg', 'clamp_n20n0d_unitcell.png', width=900)
    print('[PASS] DRC clean -> clamp_n20n0d_unitcell.svg / .png')
