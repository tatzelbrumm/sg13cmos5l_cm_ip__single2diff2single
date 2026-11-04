<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief F, stage B: routing and the pad candidate (C3, 2026-11-04)

You are resumed after Christoph's review of your stage A. `BRIEF.md` still applies (rules, inputs, checks); this
addendum gives his review, one change to the placement, and the stage B deliverables. New read-only inputs:
`$WS/inputs_B/` (listed at the end).

## Christoph's review of stage A (2026-11-04, verbatim)

> 1. Great choice to split the tails!
> 2. I'll go with your choice to omit the isolator ring.
> 3. I approve.
>
> Consider abutment of this pad with IHP sg13cmos5l_IOPad standard cells; if you can, leave some space at the long
> edges of the pads for placing guard/diffusion/well tap structures as they may become necessary.

Points 1–3 answer your three questions: `s2d_tails_hi_f` / `s2d_tails_lo_f` stay; no isolator; TPN / TNN stay inside
`s2d_cload_c3`.

## The edge reserve (the one change to your placement)

The long edges are x = 0 and x = 80 (180 µm). The template's own edge structures (legs, `edge_stubs`,
`edge_stubs_low`, the leg ties, the iovdd risers) occupy x 0–1.8 and 78.2–80, and they stay as they are.
- **Reserve:** keep a further 2.5 µm free on each side, x 1.8–4.3 and x 75.7–78.2, over the buffer's height (y ≥ 31.7).
  - No buffer device layers there: Activ, GatPoly, NWell, pSD, nSD, ThickGateOx, Cont, rhigh layers.
  - No buffer M1 there.
  - M2 may run through the reserve (for example the output trunk); prefer it along the edge, not across.
- **Purpose:** room for guard rings, diffusion and well taps that abutment with IHP's IO cells may later need.
- **What moves:** in stage A, `sinks` (x 1.8), `cload` (2.3), `sinks_cmfb` (to 78.2) and `tree_n` (to 78.11) touch the
  reserve, and so do channel C2 and the C7 tracks if they are in M1. Re-place what has to move (bottom-up, as in
  stage A). Christoph's "if you can" applies: if the full 2.5 µm doesn't fit somewhere, keep as much as you can, and
  report the reserve's actual width per y range.

## Stage B work

Route the block in M1 / M2 (M3 only at y 119–126 and 134–140), and connect it to the template:
- **vin:** from the template's `pad` pin (M2 x 20.40–21.02, top y 31.18) to the tubs' vin track. The secondary
  protection is left out for now.
- **Core-side pins** on Metal2 at the top edge (y 180): `outp outn vcm vref iref en_3v3 en_3v3_b`.
- **Supplies:** iovdd / iovss to the ring rails through Via2 / Via3 where M3 is the right rail, as in C2. The tail
  source bus and the sink source bus each tap the ring at one point (§6). Tie every well and tap; no floating rings.
- **The rest** of what you listed in your stage A note: the casc_n exits (`s2d_casc_n_f`, with sym_check), the NWell
  bridges from the tail rows to the dummy tubs, and the tail-row strap.
- **Port labels as C2 learned them** (`inputs_B/C2_report.md` §4.1 / §4.3):
  - texts on datatype 25 and pin shapes on datatype 2, for KLayout and magic;
  - **no** top-level `vss` text: the vss band's p+ and the iovss ties share the substrate, and a `vss` text names the
    joined net `iovss,vss`, which fails KLayout's port check;
  - ports `iovdd iovss vdd vss pad outp outn vcm vref iref en_3v3 en_3v3_b`; vdd / vss are ring ports without devices.

## Checks

Each check runs once, and once more after each fix; at most three rounds per item, then report it and leave it.
- **DRC:** IHP `run_drc.py --no_density` (grep for "exception") and `sg13cmos5l_maximal.drc -rd latchUpRules=true` on
  the pad candidate.
- **LVS, pad level:** `run_lvs.py --run_mode=deep --disable_tap_extraction` against `out/pad_candidate.cdl`. Compose
  that file from the primitives' CDLs and the protection: `inputs_B/s2d_pad_esd_xschem.spice` is the protection as
  drawn in the template, and it equals the template's extraction `inputs_B/template_extracted.cir`.
- **Circuit check:** every device of the extracted pad against the s2d circuit plus the protection, apart from the
  dummies.
- **row_check.py:** 25 of 25 bands / rails, 0 edge layers DIFFERENT.
- **Template part:** unchanged (XOR, as in stage A).
- **rhigh nodes:** count the capacitor-only nodes beside the rhigh segments in a PEX if F2's method in
  `inputs/C2_F2/` covers it; otherwise say it was not done.

## Deliverables (`out/`)

- `pad_candidate.gds` (top cell `sg13cmos5l_IOPadSingle2Diff`) and `pad_candidate.cdl`.
- `cells/` with every changed cell (`.gds` + `.cdl`) and its logs.
- Re-runnable `src/`, the check logs, and previews of the routed cell (whole cell plus close-ups), with the edge
  reserve marked.
- `netlist_changes.md`: every change the layout implies for the sheets and source netlists (`s2d_mpdda.sch`,
  `s2d_mpdda_pd.sch`, the pad sheet, `netlist/source/*.spice`, `bias_tree_noab_pd`), for the backannotation.
- `report_stageB.md` (under ~150 lines, a five-line summary first): the edge reserve as built, every change to the
  primitives and to stage A, the checks.
- Reply with a summary of at most 15 lines and the `out/` file list with sha256 (first 12 hex), then stop. The lead
  checks and integrates (phase 4).

## New inputs (`$WS/inputs_B/`)

- `s2d_pad_esd_xschem.spice`: the protection's netlist (xschem, from `s2d_pad_esd.sch`).
- `template_extracted.cir`: the template's IHP extraction; it equals the netlist above device for device.
- `C2_report.md`: C2's report, §4 for integration, port labels and the vss / iovss lesson.
- `macro/`: the s2d macro's current sheets, symbols and source netlists (read-only; the lead does the backannotation).
