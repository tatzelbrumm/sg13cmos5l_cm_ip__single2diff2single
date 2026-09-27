# SG13CMOS5L pad-cell internals: layout & schematic hierarchy notes

Compiled from IHP's actual PCell source (`bondpad_code.py`, both the SG13G2 and SG13CMOS5L copies) and the `sg13cmos5l_io.cdl` netlist, cross-checked against the local PDK checkout under `EDA/heichips26-analog-workshop/IHP-Open-PDK/ihp-sg13cmos5l/` and the project's own `ip/sg13cmos5l_ip__bondpad_70x70/` wrapper. Written for use in `sg13cmos5l_cm_ip__single2diff2single`.

## 1. The `bondpad` PCell (`SG13_dev` library, KLayout PyCell)

File: `libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/bondpad_code.py` (a **separate, hand-ported copy** of the SG13G2 file, not a symlink — the two can and do diverge; PR #1072 on IHP-Open-PDK had to fix the same bug in both files independently).

**Origin convention:** the cell is built symmetric about `(0,0)` — physical bbox is bbox-center, not lower-left like most other PDK PCells (confirmed both by reading the code and by IHP-Open-PDK issue #1109, "KLayout PyCells use inconsistent and undocumented cell-origin conventions," which audits 37 PCells and finds at least 4 incompatible origin conventions in this library, with `bondpad` and `via_stack` called out specifically as bbox-center while most active-device PCells are core-lower-left). The project's own `ip/sg13cmos5l_ip__bondpad_70x70/script/bondpad.py` already compensates for this correctly (it offsets by half the pad size when placing the PCell instance) — that offset is not optional boilerplate, it's required by this convention.

**Shape-dependent asymmetry:** for `shape='octagon'` (and `circle`), the code draws the top-metal polygon via `bondpadOctagonPoints(radx, rady+0.005, offset)` — a hardcoded +5 nm bump on the Y radius, repeated at several places in the octagon branch. The physical bounding box for a nominally symmetric octagonal pad is therefore **not exactly symmetric** (IHP's own PCell audit table lists the 80 µm bondpad's bbox as `(-40,-40.005)..(40,40.005)`). This does **not** affect the `square` branch (plain `Box(-radx,-rady,radx,rady)`, no offset) — so the project's default `SHAPE=square` bondpad is unaffected, but switching to `octagon` (e.g. for `FlipChip=yes`, which forces non-square) reintroduces the 5 nm Y offset. Worth knowing if you ever hand-align pads to a fine grid or build an array pitch calculation from the nominal diameter.

**`FlipChip` + `square` is a live bug, not just "unsupported":** the code path is
```python
if FlipChip and (shape == 'square'):
    print('Flip Chip requires octagon or circle shape')
    shape = octagon        # <-- bare name, not the string 'octagon'
```
`octagon` is never defined as a bare identifier anywhere in `geometry.py` or `utility_functions.py` (checked both files — no match). Unless `cni.dlo` happens to export a global of that name (unverified, but unlikely for a generic Cadence-compatibility shim), setting `FlipChip='yes'` together with `shape='square'` will raise a `NameError` inside KLayout batch mode rather than gracefully falling back to octagon as the print statement implies. If you ever need `FlipChip`, pass `shape='octagon'` or `'circle'` explicitly rather than relying on the auto-correct.

**Metal stack — already correctly narrowed for CMOS5L.** The SG13G2 version supports `topMetal` ∈ {`'TM1'`,`'TM2'`} mapping to a 6- or 7-layer stack. The CMOS5L port hardcodes `topMetal = 5` and restricts the `ChoiceConstraint` to `['TM1']` only, with `drawMetalList = ['Metal1','Metal2','Metal3','Metal4','TopMetal1']` — i.e. **CMOS5L has no Metal5 and no TopMetal2**; the pad surface is always TopMetal1. This matches your own `bondpad.py`'s comment ("There is no Metal5 and no TopMetal2 in this process"), so this one's already handled correctly in the project.

**The `TV1_a`/`TV1_d` fallback pattern — currently harmless, but worth watching.** Where SG13G2 pulls `TV1_size`/`TV1_dist` straight from `techparams['TV1_a']`/`['TV1_b']` (KeyError if missing), the CMOS5L port instead does:
```python
TV1_d = techparams.get('TV1_d', 0.42)  # TopMetal1 enclosure of TopVia1
TV1_a = techparams.get('TV1_a', 0.42)  # TopVia1 size
```
i.e. a **silent fallback to a hardcoded 0.42 µm** if the tech-params dict doesn't define these keys, used for the sizing of the actual M4→TopMetal1 via ring in the pad. I checked your local checkout: `sg13cmos5l_tech.json`, `sg13cmos5l_tech_mod.json`, and the KLayout DRC rule deck `sg13cmos5l_tech_default.json` all define `"TV1_a": 0.42` and `"TV1_d": 0.42` explicitly, so the fallback is currently a no-op — the value matches the authoritative rule deck. But the same `.get(..., 0.42)` pattern also appears in `sealring_code.py`, so it's a deliberate (if undocumented) IHP convention, not a one-off — if a future PDK release changes the TopVia1 design rule and the corresponding tech-params key gets renamed or dropped in one of these JSON files before the other, this PCell will keep generating pads with the *old* via size with no warning at all. Not an issue today; worth a quick re-check any time you update the PDK checkout.

**LVS/hierarchy black-box marking, undocumented even in IHP's own comment:**
```python
# Pad has 0 pins -> value must be one for unknown reason
dbReplaceProp(self, 'pin#', 1)
dbReplaceProp(self, 'ignore', 'TRUE')
```
IHP's own source admits it doesn't know why `pin#` has to be 1. The `ignore=TRUE` property is what matters for you: it marks the bondpad instance to be skipped/treated as a leaf by hierarchy-aware tools (extraction, LVS flattening), rather than recursed into. There's no `Pin()`/port shape created in `genLayout` at all — the `padPin` parameter (default `'PAD'`) is a **label only**, used on the schematic/CDF side for cross-probing; electrical connectivity from the layout side comes purely from whatever metal shape overlaps the pad polygon, not from a declared port object. If you're writing your own LVS setup or extraction script against a bondpad instance, don't expect it to expose a discoverable pin object the way a standard-cell PCell would.

## 2. `sg13cmos5l_io` cell library (the actual IO-ring cells — CDL: `libs.ref/sg13cmos5l_io/cdl/sg13cmos5l_io.cdl`)

Full cell list, naming convention identical to SG13G2's `sg13g2_io` (just prefix swap): `sg13cmos5l_IOPadIn`, `IOPadOut{4,16,30}mA`, `IOPadTriOut{4,16,30}mA`, `IOPadInOut{4,16,30}mA`, `IOPadAnalog`, `IOPadVdd`/`IOPadVss`/`IOPadIOVdd`/`IOPadIOVss`, `Corner`, `Filler{200,400,1000,2000,4000,10000}`. Below that sit the shared building blocks: `LevelDown`, `LevelUp`, `LevelUpInv`, `GateDecode`, `GateLevelUpInv`, `SecondaryProtection`, a family of ESD clamps `Clamp_{P|N}{2,8,15,20,43}...D[4R]`, `DCPDiode`/`DCNDiode`, `RCClampResistor`/`RCClampInverter`, and small digital cells (`io_inv_x1`, `io_nand2_x1`, `io_nor2_x1`, `io_tie`). (One curiosity: the file's built-in test/gallery subcircuit at the bottom is literally named `sg12g2_Gallery` — a leftover "12" typo from copy-pasting the SG13G2 file — so don't assume every cell in this file matches a clean `sg13cmos5l_*` prefix if you ever grep/script against it.)

### Two things directly relevant to an analog block like `single2diff2single`

**`IOPadAnalog`: `pad` and `padres` are not the same net — connect your circuit to `padres`.**
```
.SUBCKT sg13cmos5l_IOPadAnalog iovdd iovss pad padres vdd vss
  XI9 iovdd iovss pad / sg13cmos5l_Clamp_P20N0D
  XI3 iovss pad iovdd / sg13cmos5l_DCNDiode
  XI2 pad iovdd iovss / sg13cmos5l_DCPDiode
  XI6 padres iovss pad iovdd / sg13cmos5l_SecondaryProtection
  XI8 iovss pad / sg13cmos5l_Clamp_N20N0D
```
`SecondaryProtection` itself is:
```
.SUBCKT sg13cmos5l_SecondaryProtection core minus pad plus
  RR0 pad core 586.899 ... rppd ...      ' series resistor, pad -> core
  DD0 sub! core dantenna ...
  XR1 minus sub! / ptap1 ...
  DD1 core plus dpantenna ...
```
called as `XI6 padres iovss pad iovdd / sg13cmos5l_SecondaryProtection` — i.e. `padres` = the block's `core` terminal, sitting behind a **~587 Ω series resistor** from the actual bond pad, with its own secondary diode clamps to `iovdd`/`iovss`. `pad` is the primary-ESD/bond-wire node; `padres` is the RC-filtered, secondarily-clamped node your internal circuit should actually connect to. Tying your input to `pad` directly bypasses the secondary protection stage entirely; tying to `padres` puts ~587 Ω of series resistance in your signal path, which is probably non-negligible for a differential front-end's input impedance/noise budget and worth including explicitly in your hand calculations or extracted-parasitic sims, not just assumed away as "the pad." This exact same split exists in SG13G2's `IOPadAnalog` too, so it's an IHP-wide convention, not CMOS5L-specific.

**Pin order for `IOPadAnalog` differs between the two PDKs — a real trap for positional instantiation.**
- SG13G2: `.SUBCKT sg13g2_IOPadAnalog pad padres vdd vss iovdd iovss`
- SG13CMOS5L: `.SUBCKT sg13cmos5l_IOPadAnalog iovdd iovss pad padres vdd vss`

Same cell, same function, **different terminal order**. If any tooling, template, or hand-written testbench instantiates this by position (common in raw SPICE, easy to carry over by copy-paste from an SG13G2 example) rather than by name, switching between the two PDKs will silently cross-wire `vdd`/`vss` with `iovdd`/`iovss`/`pad`. Worth grep'ing your own `.spice`/`.cir` files for any positional (non-keyword) instantiation of `IOPadAnalog` before trusting a simulation that mixes reference material from both process variants.

**`LevelDown`'s two-stage structure — why you'll see HV devices biased off the core rails.**
```
.SUBCKT sg13cmos5l_LevelDown core iovdd iovss pad vdd vss
  MP0 net2 net4 vdd  vdd sg13_hv_pmos ...
  MN0 net2 net4 vss  sub! sg13_hv_nmos ...
  MN1 core net2 vss  sub! sg13_lv_nmos ...
  MP1 core net2 vdd  vdd sg13_lv_pmos ...
  XI0 net4 iovss pad iovdd / sg13cmos5l_SecondaryProtection
```
First stage is built from **thick-oxide (`sg13_hv_*`) devices** but powered from the **1.2 V core rails** (`vdd`/`vss`), not the 3.3 V IO rails — the HV device type is used purely for gate-oxide tolerance against the pad's high-swing input (via `net4`, the `SecondaryProtection`-filtered node), not because that stage runs at 3.3 V. The second stage is an ordinary `sg13_lv` inverter that squares up the level-shifted signal into `core`. If you're building your own custom receiver/level-shifter (rather than instantiating IHP's), this HV-device/LV-supply combination is the pattern to copy for reliability, and it's easy to misread the netlist and assume "hv device implies hv supply," which isn't the case here.

**`sub!` is used everywhere but never declared global in either CDL file — check your own testbench/xschemrc.** Every clamp, diode, and tap subcircuit in both `sg13g2_io.cdl` and `sg13cmos5l_io.cdl` references a bare node named `sub!` for substrate/bulk connections (e.g. `XR0 iovss sub! / ptap1 ...`), and it is never listed as a `.SUBCKT` port. The CMOS5L file even has a **commented-out** leftover `*.GLOBAL sub!` at the top (line 30) — SG13G2's file doesn't have the line at all, commented or not. Neither file actually declares it global. In a Cadence/Virtuoso flow `sub!`/`gnd!` are implicitly global by convention, but plain ngspice is not guaranteed to treat it that way unless a `.global sub!` (or equivalent tie) is declared somewhere in your own top-level deck or `xschemrc`. If it isn't, every instance of these subcircuits gets its own **local, disconnected** `sub!` node in simulation — the substrate-referenced ESD clamps and guard-ring taps silently stop doing anything electrically meaningful, with no error from ngspice. Worth explicitly checking whether your `testbenches/xschem/...tb_tran.spice` deck (or the PDK's own `xschemrc`) declares this, rather than assuming it's handled.

## Sources
- Local checkout: `EDA/heichips26-analog-workshop/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/bondpad_code.py`, `.../sealring_code.py`, `.../sg13cmos5l_tech.json`, `.../sg13cmos5l_tech_mod.json`, `libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_tech_default.json`
- `ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/cdl/sg13cmos5l_io.cdl` (via github.com/IHP-GmbH/ihp-sg13cmos5l)
- `ihp-sg13g2/libs.tech/klayout/python/sg13g2_pycell_lib/ihp/bondpad_code.py` and `ihp-sg13g2/libs.ref/sg13g2_io/cdl/sg13g2_io.cdl` (via github.com/IHP-GmbH/IHP-Open-PDK)
- github.com/IHP-GmbH/IHP-Open-PDK issue #1109 ("KLayout PyCells use inconsistent and undocumented cell-origin conventions") and PR #1072 ("KLayout PyCell bondpad: Fixed evaluation of parameter fill")
- Project files: `ip/sg13cmos5l_ip__bondpad_70x70/{README.md,script/bondpad.py}`, `macros/IOPad/schematic/xschem/*`
