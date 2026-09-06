"""
sg13cmos5l_IOPadInOut30mA -- GateDecode N-path (EN inverter -> NOR2 -> LevelUp -> ngate)

Transcribed from sudelbuecher/sg13cmos5l_IOPadInOut30mA/sg13cmos5l_IOPadInOut30mA_full_hierarchy.spi
(the file ChatGPT produced, claiming extraction from the real
libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spi). Renders the fully-MOSFET
sub-tree relevant to "how are enable/bias signals wired to the pad driver":
  sg13cmos5l_io_inv_x1   (c2p_en -> en_n)
  sg13cmos5l_io_nor2_x1  (c2p, en_n -> ngate_core)
  sg13cmos5l_LevelUp     (ngate_core -> ngate, 1.2V core domain -> 3.3V IO domain)
The mirrored P-path (io_nand2_x1 + a second identical LevelUp -> pgate) is not
re-rendered: it is this circuit's structural mirror (NAND instead of NOR),
and drawing it too would double the figure without adding new information.

Every pin below is placed by reading the .spi's own D/G/S/B node list for each
device (not by guessing a "reasonable" CMOS topology) -- including one detail
worth flagging because a fabricated netlist would be unlikely to get it right:
NOR_P1 (the series PMOS closest to the output) has its bulk tied directly to
`vdd`, NOT to the source it shares with NOR_P0 -- a real n-well bulk tie is
independent of stack position, and the .spi has that exactly right.

NOT rendered anywhere in this cell, and not representable by this skill at
all: the ESD clamps (Clamp_N15N15D / Clamp_P15N15D, ~15-30 parallel HV
devices each) and the two DC diodes (DCNDiode / DCPDiode) -- sch_netlist.py
has no Diode primitive, and the clamps' device count would not fit a
legible "concept figure" per the skill's own stated scope.

DRC proves THIS transcription is internally well-formed (no floating pin,
every bulk tied). It does not prove the transcription is a faithful copy of
the real IHP cell -- nobody in this chain has opened the real
$PDK_ROOT/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spi
directly; that check is still open.
"""
import sys
sys.path.insert(0, '.')
from sch_netlist import Circuit, Mosfet, Port, save_png

c = Circuit(1080, 480)

# ---- rails ---------------------------------------------------------------
VDD   = c.add(Port('VDD',   (60, 55), 'VDD',   kind='rail'))
IOVDD = c.add(Port('IOVDD', (760, 55), 'IOVDD', kind='rail'))
GND1  = c.add(Port('GND1', (150, 440), '', kind='gnd'))
GND2  = c.add(Port('GND2', (405, 440), '', kind='gnd'))
GND3  = c.add(Port('GND3', (660, 440), '', kind='gnd'))
GND4  = c.add(Port('GND4', (960, 440), '', kind='gnd'))
EN    = c.add(Port('EN',   (72, 245), 'c2p_en'))
CORE  = c.add(Port('CORE', (280, 275), 'c2p'))
NGATE = c.add(Port('NGATE', (1040, 75), 'ngate'))

# ---- stage 1: sg13cmos5l_io_inv_x1  (en=c2p_en -> en_n) -------------------
INV_P = c.add(Mosfet('INV_P', 'p', (150, 120), gate='L', label='INV_P'))
INV_N = c.add(Mosfet('INV_N', 'n', (150, 320), gate='L', label='INV_N'))

c.net('en',   [EN.P('p'), INV_P.P('G'), INV_N.P('G')])

# ---- stage 2: sg13cmos5l_io_nor2_x1  (c2p, en_n -> ngate_core) -----------
# pull-up: vdd -[core]- net0 -[en_n]- ngate_core (series PMOS)
# pull-down: ngate_core -[core]- vss , ngate_core -[en_n]- vss (parallel NMOS)
NOR_P0 = c.add(Mosfet('NOR_P0', 'p', (405, 100), gate='L', label='NOR_P0'))
NOR_P1 = c.add(Mosfet('NOR_P1', 'p', (405, 190), gate='L', label='NOR_P1'))
NOR_N0 = c.add(Mosfet('NOR_N0', 'n', (355, 320), gate='L', label='NOR_N0'))
NOR_N1 = c.add(Mosfet('NOR_N1', 'n', (465, 320), gate='L', label='NOR_N1'))

c.net('core',       [CORE.P('p'), NOR_P0.P('G'), NOR_N0.P('G')], trunk=('v', 280))
c.net('net0',       [NOR_P0.P('S'), NOR_P1.P('D')], trunk=('v', 405))
c.net('en_n',   [INV_P.P('D'), INV_N.P('D'), NOR_P1.P('G'), NOR_N1.P('G')], trunk=('h', 190))

# ---- stage 3: sg13cmos5l_LevelUp  (ngate_core, 1.2V -> ngate, 3.3V) ------
LU_IP = c.add(Mosfet('LU_IP', 'p', (620, 120), gate='L', source_up=True, label='LU_IP'))
LU_IN = c.add(Mosfet('LU_IN', 'n', (620, 220), gate='L', label='LU_IN'))
LU_NA = c.add(Mosfet('LU_NA', 'n', (700, 320), gate='L', source_up=True, label='LU_NA'))
LU_NB = c.add(Mosfet('LU_NB', 'n', (820, 320), gate='L', source_up=True, label='LU_NB'))
LU_PA = c.add(Mosfet('LU_PA', 'p', (700, 190), gate='L', label='LU_PA'))
LU_PB = c.add(Mosfet('LU_PB', 'p', (820, 190), gate='L', source_up=True, label='LU_PB'))
LU_OP = c.add(Mosfet('LU_OP', 'p', (960, 100), gate='L', label='LU_OP'))
LU_ON = c.add(Mosfet('LU_ON', 'n', (960, 320), gate='L', source_up=True, label='LU_ON'))

# the NOR2 output (ngate_core) fans out to three LevelUp gates -- this IS the
# 1.2V-domain "i" input to the level shifter
c.net('ngate_core', [NOR_P1.P('S'), NOR_N0.P('D'), NOR_N1.P('D'),
                      LU_IP.P('G'), LU_IN.P('G'), LU_NA.P('G')], trunk=('h', 320))

c.net('i_n',    [LU_IP.P('D'), LU_IN.P('D'), LU_NB.P('G')], trunk=('h', 220))
c.net('lvld_n', [LU_NA.P('S'), LU_PA.P('S'), LU_PB.P('G'), LU_OP.P('G'), LU_ON.P('G')], trunk=('v', 700))
c.net('lvld',   [LU_NB.P('D'), LU_PB.P('D'), LU_PA.P('G')], trunk=('v', 820))
c.net('ngate',  [LU_OP.P('S'), LU_ON.P('S'), NGATE.P('p')], trunk=('v', 1040))

# ---- rails, consolidated: one net per rail, every pin exactly once -------
c.net('vdd', [VDD.P('p'),
              INV_P.P('S'), INV_P.P('B'),
              NOR_P0.P('D'), NOR_P0.P('B'),
              NOR_P1.P('B'),                      # bulk-only tie: real n-well, not the D/S stack node
              LU_IP.P('S'), LU_IP.P('B')],
       trunk=('h', 55))

c.net('iovdd', [IOVDD.P('p'),
                LU_PA.P('D'), LU_PA.P('B'),
                LU_PB.P('S'), LU_PB.P('B'),
                LU_OP.P('D'), LU_OP.P('B')],
       trunk=('h', 55))

c.net('gnd_inv', [INV_N.P('S'), INV_N.P('B'), GND1.P('p')])
c.net('gnd_nor', [NOR_N0.P('S'), NOR_N0.P('B'), NOR_N1.P('S'), NOR_N1.P('B'), GND2.P('p')], trunk=('h', 320))
c.net('gnd_lu_in', [LU_IN.P('S'), LU_IN.P('B'),
                     LU_NA.P('D'), LU_NA.P('B'),
                     LU_NB.P('S'), LU_NB.P('B'), GND3.P('p')], trunk=('h', 320))
c.net('gnd_lu_out', [LU_ON.P('D'), LU_ON.P('B'), GND4.P('p')])

if __name__ == '__main__':
    v = c.drc()
    if v:
        print('[FAIL] DRC violations:')
        for x in v:
            print('   ', x)
        sys.exit(1)
    c.render('gatedecode_npath.svg')
    save_png('gatedecode_npath.svg', 'gatedecode_npath.png', width=1300)
    print('[PASS] DRC clean -> gatedecode_npath.svg / .png')
