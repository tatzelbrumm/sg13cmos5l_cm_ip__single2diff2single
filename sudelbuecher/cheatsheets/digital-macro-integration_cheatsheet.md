# Digital Macro → Analog Top Integration Cheatsheet

Project: `sg13cmos5l_cm_ip__single2diff2single`. Based on the `counter` macro,
which went through the full pipeline but is **not yet placed** in the analog
top (only `inverter` is). Use this as the checklist for wiring any RTL block
(your own, or `counter`) into the analog-on-top design.

## Mental model

```text
A macro is hardened OUTSIDE the top (its own LibreLane run, its own GDS/LEF/LIB).
The top only ever REFERENCES that macro: a schematic symbol + an XSPICE model
for simulation, and a GDS cell binding for layout. Hardening a macro and
placing it in the top are two separate, manual steps.
```

## Directory layout per macro

```text
macros/<name>/rtl/              SystemVerilog source — write your block here
macros/<name>/testbenches/      verilog / cocotb / xschem testbenches
macros/<name>/flow/librelane/   raw LibreLane run output
macros/<name>/final/            curated copy: gds, lef, lib (per corner), nl, vh, spef, pnl
macros/<name>/netlist/          spice, pnl, nl, xspice, pex
macros/<name>/schematic/xschem/ <name>_top.sym, <name>_top_pex.sym, xschemrc
```

## Pipeline, in Makefile order (run inside `macros/<name>/`)

```bash
# 1. RTL-level checks
make lint-verilog-all
make sim-rtl-verilog   [CELL=<cell>]
make sim-rtl-cocotb    [CELL=<cell>]

# 2. Harden with LibreLane (synth + APR + DRC/LVS)
make librelane                 # or librelane-nodrc / -magicdrc / -klayoutdrc
make copy-reports              # yosys, antenna, STA, power, IR-drop, DRC, LVS -> verification/
make copy-final                # gds, lef, lib, nl, pnl, spef, vh -> final/
make copy-netlist              # spice, pnl, nl -> netlist/

# 3. Gate-level checks against the hardened netlist
make sim-gl-cocotb     [CELL=<cell>]
make sim-gl-xschem     [CELL=<cell>] [TB=<testbench>]

# 4. Xschem symbol, scaffolded FROM the powered netlist ports
make symbol-gl   CELL=<cell>_top [FORCE=1]   # scripts/verilog2sym.py
make symbol-check CELL=<cell>_top            # re-validate .sym vs .pnl.v ports

# 5. XSPICE behavioral model (for ngspice/Xschem cosim, not transistor-level)
make generate-xspice            # runs symbol-check, then scripts/spi2xspice.py
                                 # + sak-pin-reorder.py to match the .sym

# 6. Render + all-in-one
make render-gds
make build-top                  # = librelane + copy-* + generate-xspice + render-gds

# 7. Parasitics + PEX symbol (once you have layout)
make symbol-pex   CELL=<cell>_top            # clones .sym -> _pex.sym, type=primitive
make magic-pex    CELL=<cell>_top [EXT_MODE=1|2|3]
make klayout-pex  CELL=<cell>_top [EXT_MODE=1|2|3]

# One-shot
make all                        # lint-verilog-all + build-fpga + build-top + magic-pex
```

`generate-xspice` params worth knowing (`spi2xspice.py`):
`-io_time=500p -time=50p -idelay=5p -odelay=50p -cload=250f` — tune these to
the real timing you need for the cosim, they don't come from the .lib alone.

## Wiring a hardened macro into the ANALOG TOP (manual, no single make target)

Nothing below happens automatically — this is the gap between "macro builds
clean" and "macro is in the chip". Mirror what's already done for `inverter`:

```text
1. schematic/xschem/xschemrc
   add: source .../macros/<name>/schematic/xschem/xschemrc
   (makes <name>_top.sym resolvable when the top .sch is opened)

2. schematic/xschem/<TOP>.sch
   add: C {<name>_top.sym} X Y 0 0 {name=xN}
   wire its pins to real analog net names

3. layout/<TOP>.klay.klib
   add a binding:
     { "lib_name": "<name>", "lib_path": "../macros/<name>/layout/<name>.gds" }
   (top Makefile/build-boundary reads this to pull the macro cell in)

4. layout/<TOP>.klay.gds
   place the macro cell in KLayout by hand, then re-export.
   NO Makefile target does this step.

5. Post-layout sim: swap the testbench DUT symbol
   <name>_top.sym  ->  <name>_top_pex.sym   at the SAME coordinates
   (do not touch x2/x3 spares' spice_ignore)

6. submission.yaml
   update pin counts / analog-pins / digital pin fields
```

## Traps specific to digital-in-analog

```text
- x2 / x3 in every testbench are UNWIRED SPARES. Leave spice_ignore alone.
- CACE falls back silently to schematic netlist if paths: has no layout: key.
  Always pass -s explicitly (schematic | best | pex).
- Icarus can't model IHP stdcell `ifnone` specify paths (68 warnings expected).
  Gate-level sim is functionally correct, NOT timing-accurate.
  Real timing comes from LibreLane STA, not Icarus.
- Mismatch Monte Carlo is vacuous on an EXTRACTED netlist (mm_ok=1 only on
  schematic devices; Magic splits ng=20 into 20 fingers). Run mismatch on
  -s schematic only; process MC (tt_stat) is fine on extracted.
- A digital block runs at its own logic/supply levels — level shifters
  between it and the analog domain are a separate, still-open task, not
  something this flow builds for you.
- `#` inside a `\`-continued make recipe line is a shell comment and eats
  the rest of the && chain. Only safe at column 0, no preceding backslash.
```

## Quick reference: what each generated file actually is

```text
<cell>_top.pnl.v      powered netlist -> source of truth for .sym pin list
<cell>_top.spice      LibreLane-extracted transistor/gate netlist
<cell>_top.xspice     behavioral digital model for ngspice cosim
<cell>_top.sym        Xschem symbol, type=subcircuit, generated not hand-drawn
<cell>_top_pex.sym    same symbol, type=primitive, points at extracted netlist
```
