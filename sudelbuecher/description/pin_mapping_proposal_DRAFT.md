# sg13cmos5l_cm_ip__single2diff2single — top-level pin mapping proposal

DRAFT for review, written by Claude Sonnet 5 (Cowork), 2026-09-04. Not yet
approved, not yet acted on. Purpose: settle how the conceptual pinout in
`s2d_d2s_pinbuffers.md` maps onto the fixed floorplan pins this repo
actually builds against, before writing any top-level testbench or CACE
`.yaml`. See `HANDOVER_toplevel.md` (main worktree) for the task this
feeds into.

## Two separate pin domains, plus the on-chip-interconnect point

The spec (`s2d_d2s_pinbuffers.md`) was written against neither of these
directly — it's a generic breakout/bench-test pinout, predating both. Two
real interfaces exist downstream of it:

1. **This repo's submission macro** — the floorplan templates in
   `floorplan/` fix the interface: `analog_0/1/2` (3 pins, Metal2),
   `ui_in[7:0]`, `uo_out[7:0]`, `uio_in/out/oe[7:0]` (eFPGA-connected,
   Metal3), `clk`, `ena`, `rst_n`, and `VPWR`/`VAPWR`/`VGND` power. This is
   what `sg13cmos5l_cm_ip__single2diff2single.sym` exposes today and what
   any testbench/CACE built here has to drive.
2. **`sg13cmos5l_ocd_chipalooza`** (separate repo, not started) — the
   eventual padframe slot: `sN_an[x]` dedicated analog pins plus the
   harness's shared bias, power-switch and housekeeping-SPI resources.
   README already flags this mapping as open/TBD.

Per your steer: `vdiffp`/`vdiffn`, several of the digital enable/mode
signals, and the power supplies are meant to come from the harness's
shared resources — and, per your follow-up, that harness is specifically
what carries the **on-chip interconnects between this macro and its
surroundings on silicon** (not an off-chip/bench concept). So this
macro's own pins at the standalone-submission level don't need to expose
those signals for external bench access at all — they're wired to the
harness once this macro is embedded, on-die. That resolves most of the
budget conflict below, but it also means this macro's *standalone*
testbench (the one buildable in this repo today, before
`sg13cmos5l_ocd_chipalooza` exists) has no real signal source/sink for
those nodes yet — they need internal defaults/stimuli inside the
testbench itself, not pin-level access.

## Analog pins (3 available: `analog_0/1/2`)

Spec lists 5 analog-ish signals (`vin`, `vout`, `vcm`, `vdiffp`,
`vdiffn`) for 3 physical pins. Proposal:

| Floorplan pin | Signal | Rationale |
| --- | --- | --- |
| `analog_0` | `vin` | dedicated, per spec |
| `analog_1` | `vout` | dedicated, per spec |
| `analog_2` | `vcm` | the one "shared analog" signal this macro still needs standalone (external V_CM override / readback, per `vcmsel[1:0]`) |
| *(none)* | `vdiffp`, `vdiffn` | dropped from this macro's own pins — these are on-die harness interconnects, not signals this standalone macro brings to an external pin itself |

This matches `analog-pins: 3` already committed in `submission.yaml` — so
that field turns out to need no change, just confirmation.

**Flags this raises**, not yet resolved:

- `submission.yaml`'s `long-description` currently says *"The two shared
  analog pins (vdiffp, vdiffn) carry the unbuffered internal differential
  signal..."* — that's the old (pre-clarification) reading and is now
  inconsistent with dropping `vdiffp`/`vdiffn` from this macro's pins. It
  needs rewriting once this mapping is confirmed.
- Without `vdiffp`/`vdiffn` externally accessible, tests 8 and 9 in the
  spec's 9-config test plan (`differential output enabled`, `shared
  analog pin shorted`) can't be run standalone as originally written —
  in the standalone macro's own testbench they'd need to become internal
  nodes probed via `.save`/operating-point annotation rather than driven
  from outside, or get dropped from this macro's own CACE skeleton and
  deferred to chip-embedded-level characterization instead. Worth
  confirming which.

## Bias (`ibias`, `igmc`, `vbias`)

Spec's architecture section already offers a choice: *"switch logic to
select bias current (infrastructure or internal)"*. Given the harness
doesn't exist yet and there's no spare analog pin left for an externally
injected bias, proposal: default this macro's standalone characterization
to the **internal** option — bias generated on-chip by
`OgueyAebischerBias` (already imported, not yet wired in) — rather than
add a 4th analog pin. The "from infrastructure" (harness-fed) option
stays available for the chip-embedded case later, no pin commitment
needed now.

## Power

Spec's table (`vdd3v3`, `vdd1v2`, `vss3v3`, `vss1v2`, `vssio`) assumes a
5-rail Caravel/openframe-style harness. This macro's actual floorplan
only has `VPWR`, `VAPWR`, `VGND` — 3 rails. The current (inherited,
placeholder) testbench drives both `VPWR` and `VAPWR` at 1.5 V. Not
proposing a specific rail assignment here since there's no confirmed
voltage plan for the real circuit yet — flagging as open rather than
guessing:

- Does the real circuit target a single ~1.5 V domain (matching the
  inherited testbench), or does it need the higher analog swing the spec
  text implies (3.3 V nominal)?
- If two domains are needed, `VPWR` vs `VAPWR` is the only split
  available at this macro's own pins (no separate digital/analog ground
  split at this level — just one `VGND`).

## Digital control

Per README's own design intent, most control is meant to be absorbed
into the on-chip scan chain rather than given dedicated pads. Proposal:

| Spec signal | Floorplan mapping | Notes |
| --- | --- | --- |
| `ena` | `ena` (existing dedicated pin) | direct match |
| `reset` | `rst_n` (existing dedicated pin) | active-low; spec didn't specify polarity |
| `scanclk` | a `ui_in[]` bit, **or** reuse `clk` | open — `clk` is presumably meant for eFPGA sync; using a spare `ui_in` bit avoids overloading it, but costs a pin. Your call. |
| `scanctrl[1:0]` | 2 bits of `ui_in[7:0]` | |
| `scanin` | 1 bit of `ui_in[7:0]` | |
| `scanout` | 1 bit of `uo_out[7:0]` | |
| `outbuf_en`, `inbuf_en`, `filter_en`, `vdiff_en[1:0]`, `vcmsel[1:0]` | **scan-chain holding-register bits**, not live pins | matches README's "most control pins... absorbed into a serial interface instead of dedicated pads" — these become write-once-per-config bits loaded serially, not wired to `ui_in`/`uio_*` directly |

This uses at most 4 of the 8 `ui_in` bits and 1 of the 8 `uo_out` bits,
leaving the rest (and all of `uio_*`) free. No pin-budget conflict here,
unlike the analog side.

## Net effect on the CACE/testbench skeleton (once this is confirmed)

- Real, working DC/connectivity checks are possible today only insofar
  as the top-level *schematic* is still the inherited inverter — the
  skeleton's DC group would need to be written against the eventual real
  pinout above but will only produce meaningful numbers once the macros
  in `CLAUDE.md` §7's teardown list actually exist.
- Placeholder parameter groups (gain, bandwidth, offset, PSRR) reference
  `vin`/`vout` directly — straightforward with the mapping above.
- The scan-chain bit assignment for the holding-register bits
  (`outbuf_en`, `inbuf_en`, `filter_en`, `vdiff_en[1:0]`, `vcmsel[1:0]`)
  needs an explicit shift-order convention before any testbench can drive
  it — not decided yet, and out of scope for this doc unless you want it
  folded in now.

## Open questions, summarized

1. Confirm dropping `vdiffp`/`vdiffn` from this macro's own external
   pins (on-die harness interconnects only), and which of the 9 spec
   test configs get dropped/deferred/turned into internal-node probes as
   a result.
2. `scanclk` — share `clk`, or spend a `ui_in` bit?
3. Power domain: single ~1.5 V rail (matches inherited testbench) or a
   real `VPWR`/`VAPWR` split at different voltages?
4. Should the scan-chain bit order/holding-register layout be decided in
   this same pass, or deferred?
