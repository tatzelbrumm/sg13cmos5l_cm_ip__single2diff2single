# Top-Level Module Description — `sg13cmos5l_cm_ip__single2diff2single`

Boundary-layer specification, written top-down, for the 2026-09-04 design
review with Tim Edwards. Companion to [`README.md`](README.md) (which
documents the build flow) and [`CLAUDE.md`](CLAUDE.md)/
[`HANDOVER_toplevel.md`](HANDOVER_toplevel.md) (which document repo state).
This file documents the *macro itself*: what crosses its boundary, in which
direction, in which voltage domain, bound to which internal block.

**Rebuilt from a first pass** that designed against this repo's own
inherited eFPGA-style template pins (`analog_0-2`/`ui_in`/`uo_out`/`uio_*`)
instead of the actual harness slot interface. Per the user's explicit
direction — every pin of this macro connects to the
`sg13cmos5l_ocd_chipalooza` harness, and its RTL is the most real interface
definition available even while it remains a moving target — **this
version designs against `verilog/rtl/user_project_wrapper_3a.v` and
`user_project_control.v` directly**, read from the connected
`sg13cmos5l_ocd_chipalooza` folder. The first pass's error is kept visible
in the chat log rather than quietly erased.

`OgueyAebischerBias` was designed bottom-up — device by device, from the
Oguey & Aebischer topology (M. Oguey, B. Aebischer, "Simple bias circuits
for ultra-high input impedance low-noise operational amplifiers,"
[document 6122459, IEEE](https://ieeexplore.ieee.org/document/6122459)),
sized and Monte-Carlo-characterized independently of what it plugs into.
This document goes the other way: start from the boundary every block has
to honor, and let that constrain the blocks, not the reverse.

---

## 1. Recursive macro structure — current vs. target

| Block | Role | Status |
| --- | --- | --- |
| `sg13cmos5l_cm_ip__single2diff2single` (top) | boundary, integration | internals still the inherited `inverter` placeholder; this document fixes what the boundary should be once that's torn out |
| S2D input buffer | `vin` → internal differential pair, unity/negative-unity gain | not designed — no schematic |
| D2S output buffer | internal differential pair → `vout`, class-AB | not designed — no schematic |
| V<sub>CM</sub> reference | internal common-mode reference, switchable pin / internal / infrastructure | not designed — no schematic |
| g<sub>m</sub>C stage | differential filter, switchable to free-running/driven quadrature oscillator | not designed — no schematic |
| Digital scan chain | shift register + holding registers | **dropped, see §2.3** — redundant with the harness's own `dig_in`/`dig_out`, and removing it is itself a hedge against further harness churn |
| [`macros/OgueyAebischerBias/`](macros/OgueyAebischerBias/) | on-chip PMOS/NMOS bias voltage generator | **schematic exists**; layout/verification not yet set up |

---

## 2. Boundary-layer pin table — against `user_project_wrapper_3a.v`

Source: `sg13cmos5l_ocd_chipalooza/verilog/rtl/user_project_wrapper_3a.v`
(the 3-dedicated-analog-pin wrapper variant, matching this design) and
`user_project_control.v` (how the shared resources are addressed/gated).
This macro is instantiated as `openframe_user_project` inside that wrapper
— per the harness README, the user project's own pin *names* don't need to
match the wrapper's, but the **signals and their behavior** do, since the
wrapper is where this macro gets wired to the harness pin-for-pin.

| Wrapper port | Dir | Domain | Proposed internal signal | Bound to | Gating |
| --- | --- | --- | --- | --- | --- |
| `vdd_3v3` | inout, gated power | 3.3 V analog | analog supply | S2D buf, D2S buf, V<sub>CM</sub> ref, gmC stage, `OgueyAebischerBias.vdd` | per-slot pMOS power switch, `power_3v3_ena` |
| `vdd_1v2` | inout, gated power | 1.2 V (or up to 1.5 V, PDF note) digital | digital/control supply | scan-chain logic if any survives §2.3, control decode | per-slot pMOS power switch, `power_1v2_ena`; **also powers the harness's own SPI/sequencer** — not a fully isolated domain |
| `vss_3v3` | inout | analog ground return | — | pairs with `vdd_3v3` | |
| `vss_1v2` | inout | digital ground return | — | pairs with `vdd_1v2` | |
| `vssio` | inout | global substrate/ESD ground | substrate tie | ESD structures, analog switches | independent of `vss_3v3`/`vss_1v2`, tied at the padframe |
| `enable` | in, digital | 1.2 V | project master enable | global enable tree | **dedicated to this slot**, not addressed/shared |
| `clk` | in, digital | 1.2 V | candidate: internal control-logic clock | whatever survives of §2.3 | gated to `proj_clk = select & clk` only while this slot is addressed — **not continuously available**, a real constraint an always-running block (e.g. a free-running oscillator test mode) has to account for |
| `dig_in[23:0]` | in, digital ×24 | 1.2 V | see §2.3 | control inputs | **entire 24-bit bus is this slot's own** while addressed + `dig_ena` latched — not a slice shared bit-by-bit with other slots |
| `dig_out[11:0]` | out, digital ×12 | 1.2 V | see §2.3 | status/readback outputs | same latching/addressing as above |
| `analog_pin[2:0]` | inout, analog ×3 | 3.3 V (assumed = `vdd_3v3`) | `vin`, `vout`, `vcm` | S2D input buffer / D2S output buffer / V<sub>CM</sub> ref | dedicated to this slot, not time-shared |
| `ibias[1:0]` | in, analog ×2 | shared bias domain | **infrastructure bias option**, alternative to `OgueyAebischerBias` | bias mux at every consuming block | individually enabled per slot, `ibias_ena[1:0]` |
| `vbias` | in, analog | shared bias domain | candidate infrastructure feed for V<sub>CM</sub> reference | V<sub>CM</sub> mux input | individually enabled, `vbias_ena` |
| `analog_bus[3:0]` | inout, analog ×4 | shared analog domain | **candidate route for `vdiffp`/`vdiffn`** (2 of 4 lines), 2 spare | gmC stage differential nodes, optional bring-out | individually enabled per line, `analog_ena[3:0]` — reopens tests 8/9 of the original 9-config plan as harness-level, not fully dropped |

**No dedicated `reset` pin exists at this level.** `reset` is chip-global,
generated by the housekeeping SPI (`0x04` "Reset digital" command in
`sg13cmos5l_chipalooza_harness.pdf`'s register map) and applied uniformly,
not passed to `user_project_wrapper_3a.v` as a per-slot port. Any
block-local reset behavior has to be derived internally — from a
power-on/enable transition, not a received signal — unless the housekeeping
reset is confirmed to also reach the project area some other way not shown
in this wrapper.

### 2.1 Correction from the first pass

`analog_0`/`analog_1`/`analog_2` → `analog_pin[0]`/`analog_pin[1]`/
`analog_pin[2]` is a rename, not a re-decision — `vin`/`vout`/`vcm` stays.
Everything else changes:

- `ui_in[7:0]`/`uo_out[7:0]`/`uio_*[7:0]` (this repo's own submission
  template pins) do not exist on this interface at all. They're replaced
  by `dig_in[23:0]`/`dig_out[11:0]` — 3x the input width, exactly 1x the
  output width, and *not* individually spare/reserved the way the eFPGA
  pins were, because the whole bus belongs to this slot only while it's
  addressed and latched.
- `VPWR`/`VAPWR`/`VGND` (2 supply pins + 1 ground) becomes 5 pins:
  `vdd_3v3`/`vdd_1v2`/`vss_3v3`/`vss_1v2`/`vssio`, each independently
  gated. This is a real domain split, not a renaming — see §3.
- `ibias[1:0]`/`vbias` exist as real pins on this interface. The first pass
  said "there is nothing external to drive it with at this level" —
  that was wrong; there is, and it's a legitimate alternative to
  `OgueyAebischerBias` that needs an actual decision, not an absence.
- `analog_bus[3:0]` exists. The first pass dropped `vdiffp`/`vdiffn`
  outright for lack of a pin. There's a real candidate pin for them now,
  shared and enable-gated rather than dedicated, which is a different
  (and more honest) constraint than "doesn't exist here."

### 2.2 What's still not resolved

- **Level shifting** — see §3. `dig_in`/`dig_out`/`enable`/`clk` are on the
  1.2 V domain, `analog_pin`/`ibias`/`vbias`/`analog_bus` are presumably on
  the 3.3 V domain (not stated explicitly in the wrapper; inferred from
  power pin naming). Any digital control signal that has to gate or select
  something in the analog domain crosses that boundary.
- **`clk` is not always available.** `user_project_control.v` gates it as
  `proj_clk = select & clk` — only while the housekeeping sequencer has
  this slot addressed. A gmC stage running as a free-running oscillator, or
  any block needing a continuous timing reference independent of whether
  the harness happens to be addressing this slot, cannot rely on it.
- **`dig_ena`'s own latching behavior is unfinished in the harness RTL
  itself** — `user_project_control.v` line 96 says outright: `/* TO BE
  DONE: dig_ena should act as a latch---Use latches (or can the synthesis
  tools infer a latch? */`. Designing this macro's control scheme around
  a mechanism the harness's own source admits isn't finished yet is a risk
  worth naming to Tim directly, not quietly assuming away.

### 2.3 No on-die scan chain — decided

The original spec called for an on-die shift register + holding registers
specifically to avoid spending dedicated pads on `outbuf_en`, `inbuf_en`,
`filter_en`, `vdiff_en[1:0]`, `vcmsel[1:0]`, and similar control bits. That
reasoning made sense against a padframe with a handful of raw digital pins.
It doesn't hold here: `dig_in[23:0]`/`dig_out[11:0]`, addressed and latched
by the harness's own housekeeping SPI, **is already a generic, per-slot
serial-loadable control mechanism** — functionally the same thing the
original scan chain was proposed to build, just implemented once in the
harness instead of once per slot.

**Decision: dropped.** `outbuf_en`, `inbuf_en`, `filter_en`,
`vdiff_en[1:0]`, `vcmsel[1:0]`, and headroom for more, wire directly to
individual `dig_in[i]` bits — no on-die shift register, no holding
registers, one fewer schematic block to design, lay out and verify.
`dig_out[11:0]` is free for direct status/readback (oscillator lock,
V<sub>CM</sub> settled, etc.), no serial read-back protocol needed.

The reasoning is two-fold, not just "avoid redundant logic": with the
harness interface itself a demonstrated moving target (§6 — three
disagreeing definitions already), minimizing this macro's own digital
footprint and its dependency on any *specific* harness control mechanism
is itself the hedge. A hand-built scan chain wired to today's `dig_in`
layout is one more thing that breaks the next time the harness interface
changes; direct wiring to whichever bits the harness hands this slot is
the smallest possible surface exposed to that churn. The remaining risk
is the `dig_ena` latch behavior the harness's own RTL admits is
unfinished (§2.2) — that risk exists either way, on-die scan chain or not,
so it isn't a reason to keep one.

---

## 3. Bias generator boundary — two real options now

Read directly from the committed symbol
(`macros/OgueyAebischerBias/schematic/xschem/OgueyAebischerBias.sym`):

| Pin | Dir | Meaning |
| --- | --- | --- |
| `vdd` | inout | supply |
| `vss` | inout | ground |
| `vbp` | inout | PMOS bias voltage, mirrored locally by every consuming block |
| `vbn` | inout | NMOS bias voltage, mirrored locally by every consuming block |
| `vbr` | inout | reference/startup node |

This block outputs **bias voltages**, mirrored by each consumer off its own
matched device — a layout-matching requirement, not a routed current. That
was true regardless of which harness interface this document targets, and
stays true here.

What changes with the correct interface: `ibias[1:0]`/`vbias` on
`user_project_wrapper_3a.v` are a genuine **infrastructure** bias
alternative — exactly the "switch logic to select bias current
(infrastructure or internal)" the original spec called for, now with a
real pin to switch to instead of an aspiration. The actual decision this
macro's schematic needs to make explicit:

1. Use `OgueyAebischerBias` exclusively (on-die, no dependency on the
   harness's shared bias generator or its `ibias_ena`/`vbias_ena` gating).
2. Use the harness's `ibias[1:0]`/`vbias` exclusively (smaller area, but
   dependent on a shared resource with unknown noise/output-impedance
   specs — nothing in `user_project_wrapper_3a.v` or the PDF states these).
3. Build the switch the original spec asked for — a mux between the two,
   selected via one of the `dig_in` bits from §2.3. This is real analog
   switch design on a high-impedance gate node (leakage, glitch injection
   at the switch instant), not a one-line schematic addition, and is
   itself an instance of the "level shifter"/"infrastructure" class of
   circuit the user named as the actual topic for the peer-to-peer
   discussion.

**Area**: still not quantified — no layout exists for this macro yet.
Unchanged from the first pass's honest gap. What's new: if option 3 is
chosen, the mux/switch circuit itself is additional area on top of
`OgueyAebischerBias`'s own footprint, not a substitute for it.

---

## 4. Power domain / level-shifting — now concrete, not hypothetical

`user_project_wrapper_3a.v` states the domain split explicitly:
`vdd_3v3`/`vss_3v3` and `vdd_1v2`/`vss_1v2`, independently gated. The PDF's
supporting text adds two details worth carrying forward even though its
bus widths don't match the RTL: `vdd_3v3` "can be set to any value the
user project requires" (independent of `vddio`, the padframe's own I/O
supply), and `vdd_1v2` "can also run the digital at 1.5V" but **also
powers the SPI and sequencer** — meaning this project's own 1.2 V domain
is not electrically isolated from the harness's own control logic power.

Consequences for the boundary this macro presents:

- Every signal crossing from `dig_in`/`dig_out`/`enable`/`clk` (1.2 V
  domain) into anything gating or selecting in the analog domain
  (`analog_pin`, `analog_bus`, the bias mux from §3, `vcmsel`) needs a
  level shifter. This is no longer speculative — it's a direct consequence
  of the wrapper's own port domains.
- Whatever level shifters this design needs are themselves infrastructure
  co-simulated against the harness boundary, per §5, and are area on top
  of everything in §3 — same `tiny`/`small` slot budget, still not
  line-itemed anywhere by either side.

---

## 5. Proposed co-simulation methodology

Unchanged in substance from the first pass, retargeted to the real ports:

**What already works in this repo**: the `counter` macro's
`generate-xspice` flow (see
[`macros/counter/README.md`](macros/counter/README.md#generate-xspice-file))
— LibreLane-hardened netlist → XSPICE primitives → co-simulated with real
transistor-level analog in one Xschem testbench. Proven end-to-end here
already.

**The concrete proposal for Tim**: a single canonical XSPICE/behavioral
model of `user_project_wrapper_3a.v`'s analog-facing boundary — the power
switches (`power_3v3_ena`/`power_1v2_ena` behavior, not just an ideal
switch), the `ibias[1:0]`/`vbias` sources' actual output impedance and
noise, and the `dig_ena` latch behavior flagged as unfinished in §2.2 —
kept in the harness repository, versioned, and `.include`d by every slot
contributor's own testbench. That turns "is my bias circuit and my level
shifters compatible with the harness" from an integration-time surprise
into something checkable today, against one shared artifact instead of
three disagreeing documents (§6).

---

## 6. Appendix: harness interface inconsistency, evidence

Kept for context — this document now designs against the RTL row only, per
the user's explicit direction, but the other two remain evidence for the
peer-to-peer reframe:

| Source | Shared digital out | Shared analog bus | Dedicated analog pins/slot |
| --- | --- | --- | --- |
| **`sg13cmos5l_ocd_chipalooza` RTL — design target of this document** (`user_project_control.v`, `user_project_wrapper_3a.v`) | `dig_out[11:0]` (12-bit) | `analog_bus[3:0]` (4-wide) | variable 1–4, per `config.txt` |
| `sg13cmos5l_chipalooza_harness.pdf` ("Chipalooza #2 redesign") | `sN_do[7:0]` (8-bit) | `analog[2:0]` (3-wide) | uniform 2, all 16 slots |
| This repo's own submission template (HeiChips26/JKU lineage) — **the first pass's mistaken target** | `uo_out[7:0]` (8-bit, different bus concept entirely) | none | 3 (`analog_0-2`, fixed) |

---

## 7. Open items

1. Level shifter design between the 1.2 V control domain and the 3.3 V
   analog domain (§4) — now the concrete, unavoidable consequence of the
   real interface, not a hypothetical.
2. ~~On-die scan chain~~ — **decided, dropped** (§2.3): redundant with
   `dig_in`/`dig_out`, and minimizing this macro's dependency surface on
   the harness's exact digital-control mechanism hedges against further
   interface churn. Residual risk (the harness's own unfinished `dig_ena`
   latch, §2.2) exists regardless and isn't scan-chain-specific.
3. Bias source: `OgueyAebischerBias` only, harness `ibias`/`vbias` only, or
   a switched combination (§3) — and if switched, that switch is itself
   more infrastructure to design and co-simulate.
4. `clk`'s gated availability (§2.2) — a problem for any block needing a
   continuous timing reference, most notably the gmC free-running
   oscillator mode.
5. `vdiffp`/`vdiffn` on `analog_bus[3:0]` (§2) — candidate, not committed;
   depends on understanding the `ana_route_sel`/analog-switch mechanism
   the PDF shows but the RTL doesn't fully document.
6. Area budget for bias generator + level shifters + (if built) the bias
   mux — still entirely unquantified (§3).
7. The harness-boundary XSPICE stub proposed in §5 does not exist in any
   repository yet — this document proposes it, it does not assume it.
