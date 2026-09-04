# Top-Level Module Description — `sg13cmos5l_cm_ip__single2diff2single`

Boundary-layer specification, written top-down, for the 2026-09-04 design
review with Tim Edwards. Companion to [`README.md`](README.md) (which
documents the build flow) and [`CLAUDE.md`](CLAUDE.md)/
[`HANDOVER_toplevel.md`](HANDOVER_toplevel.md) (which document repo state).
This file documents the *macro itself*: what crosses its boundary, in which
direction, in which voltage domain, bound to which internal block — and,
explicitly, what still cannot be pinned down because the harness it plugs
into is not yet a stable target. Modeled on the recursive-macro convention
of [`macros/inverter/README.md`](macros/inverter/README.md) (analog leaf)
and [`macros/counter/README.md`](macros/counter/README.md) (digital leaf),
scaled up to the level that actually matters for integration: the boundary,
not the build mechanics.

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
| `sg13cmos5l_cm_ip__single2diff2single` (top) | boundary, floorplan, integration | pins fixed by the floorplan template; internals still the inherited `inverter` placeholder |
| S2D input buffer | `vin` (single-ended pin) → internal differential pair, unity/negative-unity gain | not designed — no schematic |
| D2S output buffer | internal differential pair → `vout` (single-ended pin), class-AB | not designed — no schematic |
| V<sub>CM</sub> reference | internal common-mode reference, switchable analog-pin / internal / infrastructure | not designed — no schematic |
| g<sub>m</sub>C stage | differential filter, switchable to free-running/driven quadrature oscillator | not designed — no schematic |
| Digital scan chain | shift register + holding registers, absorbs mode-select/enable/trim bits | not designed — no schematic |
| [`macros/OgueyAebischerBias/`](macros/OgueyAebischerBias/) | on-chip PMOS/NMOS bias voltage generator | **schematic exists** (`OgueyAebischerBias.sch`/`.sym`, `ToBiasStartup.sch`/`.sym`); Makefile/layout/verification not yet set up; CACE characterization in progress on a separate branch |

Five of six blocks are still schematic-less. This document does not pretend
otherwise — its job is to fix the boundary each of those five will have to
meet, so that when they get drawn, drawing them against a moving target
isn't one more risk on top of everything else.

---

## 2. Boundary-layer pin table

The physical interface is fixed by the floorplan template (`floorplan/*.gds`)
and already exposed by `schematic/xschem/sg13cmos5l_cm_ip__single2diff2single.sym`
— **this is not negotiable at the macro level**, only what each pin is wired
to internally is. `analog-pins: 3` in `submission.yaml` is now a settled
fact, not the placeholder it was this morning.

| Pin | Dir | Domain | Internal signal | Bound to | Status |
| --- | --- | --- | --- | --- | --- |
| `VPWR` | inout, power | digital/core | digital core supply | scan chain, all digital logic | wired; **voltage TBD** (inherited testbench uses 1.5 V, see §4) |
| `VAPWR` | inout, power | analog | analog supply | S2D buf, D2S buf, V<sub>CM</sub> ref, gmC stage, `OgueyAebischerBias.vdd` | wired; **voltage TBD** |
| `VGND` | inout, power | — | common ground return | everything | wired |
| `analog_0` | inout, analog | `VAPWR` | `vin` | S2D input buffer, input | **settled this session** |
| `analog_1` | inout, analog | `VAPWR` | `vout` | D2S output buffer, output | **settled this session** |
| `analog_2` | inout, analog | `VAPWR` | `vcm` (external override/readback) | V<sub>CM</sub> reference | **settled this session** |
| `clk` | in, digital | `VPWR` | scan-chain clock, *or* reserved | scan chain (candidate) | **open** — see §5.1 |
| `ena` | in, digital | `VPWR` | `ena`, master enable | global enable tree | direct match |
| `rst_n` | in, digital | `VPWR` | `reset`, active-low | scan chain + global reset | direct match (polarity assumed, spec didn't specify) |
| `ui_in[7:0]` | in, digital ×8 | `VPWR` | `scanctrl[1:0]`, `scanin`, `scanclk` if not on `clk`, remainder spare | scan chain, input side | partial — ≤4 bits used, rest reserved |
| `uo_out[7:0]` | out, digital ×8 | `VPWR` | `scanout`, remainder spare | scan chain, output side | partial — 1 bit used, rest reserved |
| `uio_in/out/oe[7:0]` | inout, digital ×8×3 | `VPWR` | unassigned | — | fully spare, reserved for future trim/status |

**Deliberately not on this macro's own boundary** (resolved turns 2–5 of
today's design discussion, log below): `vdiffp`, `vdiffn`, `ibias`, `igmc`,
`vbias` from the original `s2d_d2s_pinbuffers.md` conceptual pinout. They
are not brought to a top-level pin:

- Bias is generated **on-die** by `OgueyAebischerBias` and distributed as
  an internal net, not received from outside — see §3. There is no
  `ibias`/`igmc` input pin because there is nothing external to drive it
  with at this level.
- `vdiffp`/`vdiffn` (direct access to the unbuffered internal differential
  node, per the original spec's standalone-bench test plan) are dropped.
  With only 3 analog pins and `vcm` now claiming one of them, there isn't
  a pin left for them, and — per this session's harness discussion —
  whatever "shared differential line" concept eventually exists lives at
  the harness/carrier integration layer, not as a dedicated pin this macro
  brings out itself. **Consequence**: test configurations 8 and 9 of the
  original 9-config test plan (shared analog pin shorted; differential
  output enabled standalone) are not executable as originally written
  against this macro's own pins. They become either chip-embedded-level
  tests (once a harness interconnect exists) or internal-node
  operating-point probes (`.save`/`annotate_op`) in simulation only, not
  bench-measurable pins. **This is a real scope reduction from the
  original proposal and should be said out loud to Tim, not discovered
  later.**

---

## 3. Bias generator boundary (`OgueyAebischerBias`)

Read directly from the committed symbol
(`macros/OgueyAebischerBias/schematic/xschem/OgueyAebischerBias.sym`):

| Pin | Dir | Meaning |
| --- | --- | --- |
| `vdd` | inout | supply |
| `vss` | inout | ground |
| `vbp` | inout | PMOS bias voltage (gate bias for PMOS current-mirror devices elsewhere on-die) |
| `vbn` | inout | NMOS bias voltage (gate bias for NMOS current-mirror devices elsewhere on-die) |
| `vbr` | inout | reference/startup node |

One correction to make explicit, because the original spec's language
invites the wrong mental model: this block does **not** output a current
(`ibias`) or a second control current (`igmc`) as a signal that gets routed
around the chip and re-mirrored generically. It outputs two **bias
voltages** (`vbp`, `vbn`) that every consuming block mirrors locally off
its own matched device. That's a layout-matching requirement (device
proximity, common-centroid where it matters), not a routing problem, and
it's the reason the original spec's "switch logic to select bias current
(infrastructure or internal)" framing needs revisiting: switching a
*voltage* bias between an internally-generated source and an
externally-supplied one is a mux on a high-impedance gate node, which is
exactly the kind of thing that's easy to get wrong (leakage, glitch
injection at the switch instant) and needs its own explicit sub-circuit,
not a one-line mention.

`ToBiasStartup.sch`/`.sym` exists alongside the main schematic — a
startup-kick circuit, standard practice for this self-biased topology
family (it has no natural startup point on its own load line without one).
Not yet characterized as part of this document; flagged for the CACE work
already underway on the `oguey` branch.

**Area**: not yet quantified. No layout exists for this macro yet, so
there is no committed number to cite, and inventing one would be worse
than saying so plainly. Qualitatively, the reason to expect it matters:
a sub-µA, low-noise, ultra-high-input-impedance self-biased reference
needs a large resistor (the defining element of the topology, and resistor
area scales with the inverse of the bias current it sets), large
filter/startup capacitance to keep noise and startup transients under
control, and several cascode devices for the high output impedance the
"ultra-high input impedance" claim in the paper title depends on. In a
`tiny` (200 µm × 200 µm = 40,000 µm²) slot, none of that is free. **This is
the argument for the peer-to-peer discussion, not a settled number**: the
harness needs to either budget real area for bias infrastructure per slot,
or accept that a properly-designed bias generator crowds out the signal
path it's supposed to support.

---

## 4. Power domain / level-shifting — the open risk

Every version of the harness interface examined today assumes a
dual-domain supply arrangement (`vdd3v3`/`vdd1v2` in the RTL and the PDF,
`vdd_3v3`/`vdd_1v2` in `user_project_wrapper_3a.v`). This macro's own
floorplan gives exactly two supply pins, `VPWR` and `VAPWR`, and the
*inherited, still-placeholder* testbench drives both at 1.5 V — a number
that came along with the `inverter` demo, not from any decision about the
real circuit.

If the real target ends up being a 3.3 V analog / 1.2 V digital split (as
every harness-side document assumes), then:

- `VAPWR` most likely carries 3.3 V (analog domain — matches `vdd3v3`),
  `VPWR` carries 1.2 V (digital/scan-chain domain — matches `vdd1v2`).
- Every digital signal crossing between the scan chain (1.2 V) and
  anything that needs to sit at the 3.3 V analog rail (mode-select bits
  gating analog switches, `vcmsel`, `vdiff_en`) needs a **level shifter**,
  and level shifters are exactly the "infrastructure" the user wants
  co-simulated with the harness, not assumed away.
- That's area and design effort *in addition to* the bias generator's
  footprint from §3 — both eating into the same `tiny`/`small` slot budget,
  and neither currently line-itemed anywhere.

This is not resolved here. It's flagged because it's the single largest
undetermined variable in this whole document, and because "co-simulation
of infrastructure like level shifters and bias circuits" was named
directly as the topic for the peer-to-peer discussion.

---

## 5. Proposed co-simulation methodology

### 5.1 What already works in this repo

The `counter` macro's `generate-xspice` flow (see
[`macros/counter/README.md`](macros/counter/README.md#generate-xspice-file))
is a proven pattern for exactly this class of problem: take a
LibreLane-hardened, standard-cell netlist, replace every cell with an
XSPICE primitive, reorder pins to a hand-maintained Xschem symbol via
`sim_pinname`, and co-simulate the result with real transistor-level analog
circuitry in one Xschem testbench. It's fast (event-driven digital,
full-analog only where it needs to be) and it's already verified working
end-to-end on this repo's own digital reference macro.

### 5.2 What it would take to apply this to the harness boundary

The missing piece isn't a new methodology — it's a **shared, versioned
XSPICE (or at minimum behavioral SPICE) stub of the harness boundary
itself**: the power-switch gating, the shared bias generator's output
impedance and noise, and — per §4 — any level-shifting infrastructure the
harness provides or expects the slot to provide. Right now every
contributor either has no such stub, or builds their own private guess at
one, which is the same "everyone designs against their own best guess"
problem this session already surfaced at the RTL/PDF/eFPGA-template
documentation level, just one layer further into simulation.

**The concrete proposal for Tim**: extend the pattern that already works
for a slot's own digital logic (`generate-xspice`) to the harness's own
shared infrastructure — a single canonical XSPICE/behavioral model of
`user_project_wrapper_Na.v`'s analog-facing boundary (power gates, shared
bias sources, whatever level-shifting the harness itself owns) that every
slot contributor `.include`s in their own testbench, kept in the harness
repository and versioned like any other interface artifact. That turns
"is my bias circuit compatible with the harness" from an integration-time
surprise into something every contributor can check today, on their own
schedule, against a moving but *shared* target instead of three
disagreeing documents.

---

## 6. Appendix: harness interface inconsistency, evidence

Three non-reconciled descriptions of the same harness interface, all
examined directly today:

| Source | Shared digital out | Shared analog bus | Dedicated analog pins/slot |
| --- | --- | --- | --- |
| `sg13cmos5l_ocd_chipalooza` RTL (`user_project_control.v`, `user_project_wrapper_3a.v`) | `dig_out[11:0]` (12-bit) | `analog_bus[3:0]` (4-wide) | variable 1–4, per `config.txt` |
| `sg13cmos5l_chipalooza_harness.pdf` ("Chipalooza #2 redesign") | `sN_do[7:0]` (8-bit) | `analog[2:0]` (3-wide) | uniform 2, all 16 slots |
| This repo's own submission template (HeiChips26/JKU "Austrian school" lineage) | `uo_out[7:0]` (8-bit, but a different bus concept entirely — fixed eFPGA GPIO, not a project-addressed shared bus) | none (no shared-analog-bus concept at this level) | 3 (`analog_0-2`, fixed) |

None of the three agree on bus width, and two of the three are Tim's own
documents. This is the primary evidence for the peer-to-peer reframe: the
gap isn't in any one contributor's diligence, it's structural.

---

## 7. Open items

1. `clk` vs. a spare `ui_in` bit for `scanclk` (§2).
2. Power domain split and its level-shifter consequence (§4) — the biggest
   open item in this document.
3. Bias-generator and level-shifter area budget vs. slot size (§3, §4) —
   currently unquantified for lack of a layout.
4. Scan-chain bit order / holding-register layout — not addressed here,
   still open from the pin-mapping discussion earlier today.
5. Whether tests 8/9 of the original 9-config test plan get formally
   dropped from this macro's own verification plan or deferred to a
   chip-embedded characterization step (§2).
6. The harness-boundary XSPICE stub proposed in §5.2 does not exist yet in
   any repository — this document proposes it, it does not assume it.
