# HANDOVER — seed context for a device-sizing / testbench session

Written 2026-09-04 by Claude Sonnet 5 (Cowork), at the end of a documentation
+ CACE-authoring session, for whoever picks up device sizing and testbench
verification next — likely a separate Opus 5 session, per the user's plan to
do topology by hand and bring in Opus specifically for sizing.

**Read [`CLAUDE.md`](CLAUDE.md) first.** This file does not repeat it — it
only adds what CLAUDE.md doesn't cover yet: the state of the
`OgueyAebischerBias` macro and the CACE work done today.

---

## 1. What changed today (2026-09-04)

Full verbatim transcript:
[`sudelbuecher/chatlog/2026-09-04_ocd_reconciliation_and_ogueyaebischerbias_cace.md`](../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/chatlog/2026-09-04_ocd_reconciliation_and_ogueyaebischerbias_cace.md)
in the `_sudelbuecher` worktree (branch `sudel_buecher`), with sources indexed in
that folder's `ref/2026-09-04_references.md`.

Short version:

- `README.md` and `submission.yaml` were rewritten to describe the actual
  single-ended↔differential design instead of the inherited `inverter`/
  `counter` template text, and to reconcile with the separate
  `sg13cmos5l_ocd_chipalooza` harness repo (a later, different integration
  step — see README's "Chip Integration" section).
- `macros/OgueyAebischerBias/schematic/xschem/reference.sch` and
  `reference.sym` were **ported** (not authored) from
  `~/EDA/TinyTapeout/designs/tt10-analog-tatzelreference` — the same author's
  earlier, sky130 version of this exact circuit. `reference` combines the two
  existing schematics, `OgueyAebischerBias.sch` (the Oguey-Aebischer
  resistor-free core + 4-leg long-channel cascode fan-out) and
  `ToBiasStartup.sch` (the start-up kick + `disable`), into one macro with
  pins `vdd`/`vss`/`vbp`/`vbn`/`vbr`/`disable`. This port is low-risk —
  it's a near-verbatim copy, only xschem version headers were adjusted.
- `macros/OgueyAebischerBias/verification/cace/reference.yaml` was written,
  following `macros/inverter/verification/cace/inverter.yaml`'s format.
  Two parameter groups (`dc_params`, `tran_startup_params`) are wired to
  real testbench templates; four more (`ac_psrr_params`, `noise_params`,
  `disable_params`, `mm_params`) are fully specified — targets adapted from
  `~/EDA/chipalooza2024/sky130_cm_ip__biasgen/README.md`'s spec table, same
  circuit family — but have **no testbench template yet** (marked `TODO` in
  the yaml).
- The two new testbenches,
  `macros/OgueyAebischerBias/verification/cace/templates/reference_tb_dc.sch`
  and `reference_tb_tran.sch`, were **authored, not ported**, using CACE's
  `CACE\{condition\}` templating syntax copied from
  `macros/inverter/verification/cace/templates/inverter_tb_ac.sch`. **They
  have not been opened in Xschem or simulated.** Treat every number they
  would produce as unverified until you've run them.
- A pre-existing gap in the top-level xschem library-path chain was found
  and fixed this session: `schematic/xschem/xschemrc` sourced
  `macros/inverter/.../xschemrc` and `macros/counter/.../xschemrc` but not
  `macros/OgueyAebischerBias/.../xschemrc`, so `reference.sym` (and the
  other two symbols) weren't resolvable from a top-level Xschem session.
  Fixed by adding the third `source` line, matching the existing two
  exactly; `README.md`'s Xschem Configuration table and chain diagram were
  updated to match. If you still get missing-symbol errors after pulling
  this, check whether you're opening files via `xschem --rcfile <path>` /
  `cd <folder> && xschem <file>` / `make open` (all pick up the right local
  `xschemrc`) rather than a bare `xschem <file>` from an arbitrary cwd,
  which falls back to `~/.xschem/xschemrc` and sees none of this — see
  README.md's "Which File Is Used" subsection.
- `macros/OgueyAebischerBias/verification/cace/OgueyAebischer.yaml` (note:
  missing the `Bias` suffix) is a **stray leftover** — an unfilled CACE
  scaffold that predates this session, superseded by `reference.yaml`.
  Left in place; wasn't deleted because files in this connected folder
  can't be removed without the user's explicit go-ahead.

## 2. Where sizing help is actually needed

**`OgueyAebischerBias.sch` and `ToBiasStartup.sch` are sized as a straight
port from the sky130 precedent — the L/W/multiplier numbers were never
re-derived for sg13cmos5l.** Specifically:

- Core loop: `M12`/`M13`/`M14` (PMOS, mirror ratio 1:4:2) and `M10`/`M11`
  (NMOS, ratio 4:1), all `L=1µm`, `W=1µm`, using `sg13_hv_pmos`/`sg13_hv_nmos`.
- Cascode fan-out: `M15`–`M22`, all `L=20µm`, `W=1µm`, single finger.
- Start-up kick (`ToBiasStartup.sch`): `M20`/`M26` at `L=2µm`/`W=8µm`,
  everything else `L=0.45µm`/`W=1µm`.

These ratios encode the topology's *intent* correctly (that part ported
fine — same device count, same connectivity, same mirror ratios as the
working sky130 version), but the *absolute* sizes assume sky130's
`nfet_01v8`/`pfet_01v8` device characteristics at a ~1.8V rail. This design
targets `sg13cmos5l`'s `sg13_hv_nmos`/`sg13_hv_pmos` at the proposal's
3.3V analog rail (see `sudelbuecher/description/s2d_d2s_pinbuffers.md`).
Whether `L=1µm`/`L=20µm` is still the right choice — for the target
`Ibias` range (100nA ballpark per the proposal, no firm spec yet), for
start-up reliability, for gm/Id-appropriate operation — has not been
checked. This is probably the single highest-value thing a sizing session
should look at first.

Secondary sizing questions once schematics for the other blocks exist (see
§3): the proposal's `ibias`/`igmc` targets are still "to be discussed" per
`s2d_d2s_pinbuffers.md` itself — nothing is committed yet.

## 3. What's still unbuilt

Per `README.md`'s state section and `CLAUDE.md` §7, only `OgueyAebischerBias`
has any schematic content among the design's real building blocks. Still
schematic-less: the single-ended↔differential input buffer, the
differential↔single-ended class-AB output buffer, the internal V_CM
reference, the g_mC filter/oscillator stage, and the digital scan chain.
`macros/inverter/` and `macros/counter/` are template placeholders, not part
of this design (see README's "Chip Integration" and "Recursive Macro
Structure" sections) — don't build on them, don't extend their CACE decks
for this project.

Once a new block gets a real schematic, `macros/inverter/verification/cace/inverter.yaml`
and `.../reference.yaml` (this session's) are the two format precedents to
follow; the six-group split used in `reference.yaml` (dc / start-up-or-
transient / ac-psrr / noise / disable-or-enable / mismatch) is a reasonable
default checklist for any bias- or reference-adjacent block, less so for a
signal-path block like the buffers, which will want gain/bandwidth/
distortion/offset groups instead — see this session's turn 6 in the
transcript for the reasoning, not just the template.

## 4. Precedents worth opening directly, not just reading about

- `~/EDA/TinyTapeout/designs/tt10-analog-tatzelreference/xschem/` — origin
  of `OgueyAebischerBias.sch`/`ToBiasStartup.sch`/`reference.sch`. Also has
  `test_OgueyAebischerBias.sch`, `test_reference.sch`, and unrelated other
  blocks (`dividerchain.sch`, `schmittinv.sch`, `BlinkenNeuron.sch`) not
  investigated this session.
- `~/EDA/chipalooza2024/sky130_cm_ip__biasgen/README.md` — the filled-in
  spec table this session's `ac_psrr_params`/`noise_params`/
  `disable_params`/`mm_params` targets came from. Its own CACE files
  (`cace/*.txt`, `.draft`) never got past boilerplate — don't treat those as
  a CACE-format precedent, only the README numbers are useful.
- `~/EDA/sg13cmos5l_ocd_chipalooza/` — the eventual chip harness (separate
  integration step, see README.md's "Chip Integration" section). Not
  touched this session by request; still no slot assigned.

## 5. Running Sonnet and Opus in parallel on this repo

If you do start a separate Opus session pointed at the same connected
folder: both sessions share the same files on disk, live-edited, with no
lock between them. That's fine for read-heavy work (sizing analysis,
reviewing a testbench) but a real risk the moment both sessions write to
the *same* file around the same time — last write wins, silently. Cheapest
mitigation: keep the division of labor by directory rather than by time —
e.g. Sonnet continues in `README.md`/`submission.yaml`/CACE `.yaml`
authoring, Opus works in the `schematic/xschem/*.sch` sizing and the
`verification/cace/templates/*.sch` testbenches — and avoid having both
sessions touch `reference.yaml` or the top-level `xschemrc` files in the
same window. If a sizing change in Opus means a CACE spec's target number
needs updating, that's a small enough diff to hand back to this session
afterward rather than have Opus edit the yaml directly.
