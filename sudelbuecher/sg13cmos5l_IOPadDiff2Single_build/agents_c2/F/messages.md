<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# F: messages

Agent F of session C2 (floorplan and assembly). Model Opus, effort high. Started by the lead on 2026-10-31 at 16:39
CET. Workspace `/home/user/c2/F/`; inputs: `inputs/repo/` (`git archive` of `toplevel` 8a72dd8) and `inputs/notes/`
(phase 1 report, `layout_primitives.md`, `log.md`, the library folder, oa_core_pd v2 and bg_core_pd folders with the
router, A1's Metal2 report, the replica prototype, A2's briefs / reports, A3's / A4's reports and skills, the ESD notes,
the PDK PDFs as text, `row_check.py`, `path_widths.py`, `pex_for_sim.py` from `claude/c1-core-pex-verif`).

## 16:39, launch prompt (verbatim)

> You are agent F, the floorplan and assembly agent for an analog IC layout on IHP sg13cmos5l. Your whole task is in the brief file `/home/user/c2/F/BRIEF.md` — read it first and follow it exactly, including its rules (work only in `/home/user/c2/F/`, `inputs/` read-only, no git, no web searches, no mcp tools). Do only **stage 1** now: the floorplan (at most two variants) of the pad cell's amplifier block in y 84–178 and your pin / aspect / edge requests for the primitive agents P (PMOS cells: d2s_inputs / tub_p20x1, d2s_tails, d2s_loads, d2s_casc_p, d2s_ab_p, d2s_pd_p) and N (NMOS cells: sinks_6x6, d2s_casc_n, d2s_ab_n, d2s_pd_n), written to `out/requests_for_P_N.md` and `out/floorplan_stage1.md` with a picture. Then reply with a summary of no more than 15 lines and stop; the lead will resume you for stage 2.

## 16:58, F's stage 1 reply

Floorplan in two variants (variant 1 recommended: PMOS column left, NMOS column right, input stage centre; 4534 of
6668 µm² planned, ≈ 1160 µm² spare at the top as CMB reserve); requests to P / N (`requests_for_P_N.md`, relayed
verbatim into their briefs); question: draw `bias_tree_pd` without its four diodes (they sit in the tails, sinks and
cascodes), LVS the pad flat, check the tree against "sheet minus diodes" as a proposal. Files: `stage1/` here.

## 17:01, from the lead (verbatim)

> From the lead, 17:01 CET. Stage 1 accepted; go on with **stage 2** (your own cells) on **variant 1**.
>
> 1. Your requests went to P and N verbatim at 17:00; both are working. I pass their cells to you after my checks.
> 2. **bias_tree_pd's diodes (your question):** accepted as you propose. Draw the tree without BP / BN / BPC / BNC (they sit in the tails, sinks and cascodes). The pad's LVS runs flat against the present sheets (the devices and their connections are the same). Check the tree cell alone against "sheet minus diodes", and write the sheet change only as a proposal in your report (rule 4: the sheet of `bias_tree_pd` stays unchanged in this task).
> 3. **Christoph, about 16:50:** the 63/0 box in the pad's top cell (x 36.355–45.815, y 147.73–180.62) is TEXT.drawing only and goes; I delete it at integration, so ignore it and don't draw anything that relies on it. The PCells' own 63/0 texts stay. **CMB stays as in the sheet** (gate on the pad) for now; Christoph will discuss capacitor options when K reports. So lay CMA / CMB out as hv PMOS units as in the sheet, each in its own region, so a later change of type stays local; keep the top spare (CMB reserve) free.
> 4. K has not reported a stage yet; I relay when it does.
> 5. Add **previews**: whenever you have an intermediate layout picture worth looking at (a drawn cell, a partial assembly), put a PNG in `out/previews/` with a name that says what it is. Christoph looks at them and may suggest corrections.
>
> Reply at the end of stage 2 with a summary of no more than 15 lines (cells drawn, sizes, DRC / LVS, the rhigh capacitor-only node count if you already have it), then wait for stage 3.

## 17:45, from the lead (summary; verbatim text in the session)

N's cells passed the lead's check, read-only copy in `/home/user/c2/F/inputs_N/` (sizes, check results, the decision on
SB's bulk = vss, to go into F's `netlist_changes.md`; XSA's bulk likewise vdd if P draws SA in the shared iovdd NWell);
CMB: Christoph is deciding between keeping it and turning it around; keep it local to its own region.

## about 17:50, F's stage 2 reply (summary)

d2s_rhigh 13.92 × 15.41 (18 capacitor-only nodes in a magic PEX, mode 2), bias_tree_pd 52.36 × 11.82 (without its diodes,
moved to the top band), d2s_cma / d2s_cmb one hv PMOS unit each, CMA's p+ guard ring closed (CMA's junction vias moved to M2
tabs), `guard` tied to iovdd, NWell isolator, edge stubs; `pad_stage2.gds` DRC 0, row check passes. Files: `stage2/`.

## 17:57, from the lead (summary; verbatim text in the session)

Stage 3 go. Christoph's two messages of about 17:55, verbatim; bottom-up floorplan from the drawn cells in the pad context,
nothing back to P / N, a placement preview before routing; P's cells passed the check (`/home/user/c2/F/inputs_P/`, sizes
and P's notes); the lead's check of stage 2 (passed; `row_check.py` label bug fixed); CMB still undecided.

## about 18:00, from the lead (verbatim)

> From the lead, about 18:00 CET. One more from Christoph, verbatim: "F can tweak the layout primitives ex post facto and build the floorplan from there."
>
> So you may change your copies of P's and N's cells (pin positions, outlines, tie strips, aspect, column pitch of the tails to match the tubs, etc.) and then build the floorplan from the tweaked cells. Keep each tweaked cell DRC clean and LVS-matched on its own, name it distinctly (e.g. `<cell>_f`), and list every change in your report. No reply needed.

## about 18:00, from the lead (verbatim)

> From the lead, correction to my 17:57 message. Christoph rejects sharing a well between CMA and CMB (my suggestion; withdrawn). CMA and CMB stay separate devices, each with its own well, its own region and its own guard ring, whatever is decided for CMB's orientation. Do not merge or abut their wells, and keep CMB as in the sheet until told otherwise. No reply needed.

## about 18:15, from the lead (summary; verbatim text in the session)

Christoph: "yes, have F reserve a spot for the CMB stage". Reserve a spot for IHP's secondary stage in front of CMB's gate
(2 kΩ case: rppd 1 × 7.435 µm, dantenna 0.64 × 3.1 to the substrate, dpantenna 0.64 × 4.98 to iovdd), with a short wide
pad-side connection and a short line to CMB's gate; in the ESD zone if it fits, else above y 88; keep CMB's gate feed as it is
but cuttable at one place; mark the reserve in the previews and the report; don't draw the stage yet.
