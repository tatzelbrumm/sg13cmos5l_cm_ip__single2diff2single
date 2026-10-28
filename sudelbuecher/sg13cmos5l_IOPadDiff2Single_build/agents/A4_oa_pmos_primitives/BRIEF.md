# Brief P: compact PMOS primitives for oa_core_pd (IHP sg13cmos5l), 2026-10-28

Workspace (yours only): `/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primP/`
(`inputs/` read-only, `work/` scratch, `out/` deliverables).

## Hard rules
- Cloud workspace only. No `mcp__remote-devices__*` tools, no git (not even read-only), do not touch `inputs/`.
- Rule values only from the PDK decks: `/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/`
  (`sg13cmos5l_tech_default.json` and the `.drc` files); cite key / file for every value. No invented numbers.
- Facts you measured vs. reasoning: say which is which. Times: `TZ=Europe/Berlin date`.
- The harness may block writing `.md` files for you: then put the report text in your final reply.

## The user's instruction (02:36, verbatim)
"oa_nmir, oa_mcs, oa_misc_n, oa_misc_p, need to be changed. in particular transistors in oa_nmir, oa_misc_n, oa_mcs
rotated, transistors of same size in oa_nmir and oa_misc_n combined into one array, NEVER use substrate tap between rows of
arrayed transistor, and completely revise the guard ring structures. They're too bulky as they are. There is WAY too much
empty space in the oa_core_pd layout. Compactify. Use narrower dummy transistors in oa_pmir. Let the layout drive the
design. backannotate if necessary. Hold off on the bandgap layout until there are lessons learned from compactifying
oa_core_pd."  And at 02:37: "other agents may be more experienced rotating transistors within layout primitives."

You are the PMOS specialist. A second agent does the NMOS cells (oa_nmir, oa_misc_n, oa_mcs); a third assembles oa_core_pd.

## Your cells
Library: `inputs/pad_buffer_cells.gds` (+ `.cdl`), cells `oa_pmir` (4 × 8 point-symmetric 2/8 PMOS mirror: PO 20,
P8 8, P2 2, P0 1, plus 9 dummies 2/8; rotated R270 by the "sinks-style worker", log 2026-10-27 04:01–04:14) and
`oa_misc_p` (MS1 = 0.5/100 drawn as 8 × 0.5/12.5 in series, gate en_3v3_b; SVPG 1/0.45, gate en_3v3; it is
`bg_misc_p` with its transistors turned, log 02:30–02:40, and still carries the user's note "NEEDS TO BE BROKEN UP" on
63/0; log 08:35–08:45: the split into `_ms1` / `_svpg` cells, the user's correction "NO. NO ntap rings." (tap-less cells,
bulk tied by the parent), then the hold). Circuit: `inputs/oa_core_pd.sch`, `inputs/oa_core_pd_xschem.spice`,
subckt `oa_core_pd` in `inputs/bias_ref_pd.spice`. The assembled v1 block (for context, what to beat):
`inputs/tools/oa_core_pd.gds`, `.png`, `oa_core_pd_v1_report.md`.

1. **oa_pmir with narrower dummies**: the 9 dummies are full 2/8 today. Make them narrow (keep L = 8 µm; W as small as
   the rules and the row pitch allow; the 2026-10-27 convention for end dummies was W = 2 µm, so here go below that,
   to the minimum that keeps the poly / diffusion environment of the real devices). Keep the point symmetry of the real
   devices (PO, P8, P2, P0) and the shared bands; revise its ring the same way as below. Report the size before / after
   (28.0 × 42.8 µm today).
2. **oa_misc_p compact**: MS1 chain (8 × 0.5/12.5, nodes ms1..ms7 between vdd and ks) and SVPG (vpg to vdd, gate
   en_3v3). Turned / arrayed as the earlier workers did (AREF rows, R270 for upright texts, merged gate strips where the
   gates share a net: all 8 MS1 gates are en_3v3_b). Minimum area; consider folding the chain into two rows.
3. **NEVER a well tap between rows of an arrayed block.** Taps only at the periphery; check the deck's latch-up rules
   (LU.*) with periphery taps; report the numbers if the block is too large for that instead of adding inner taps.
4. **Guard rings / ntap rings revised completely**: too bulky today. One contact row, minimum Activ / Metal1, shared with
   the neighbour where the well is the same net, no double rings, no ring where the deck doesn't need one; tap-less
   cells with bulk from the parent where that is what the user asked for (08:45).
5. Let the layout drive: if a different finger split, series split or dummy size is denser, do it and list the
   backannotation (every w / l / ng / series count change and its electrical effect).
6. Pins: `<metal>.pin` + `<metal>.text` as the library does, one per net, on the cell edge; Metal1 / Metal2 only.

## Checks and deliverables (`out/`)
- `oa_p_cells.gds` with the new cells (e.g. `oa_pmir_c`, `oa_misc_p_c` or split `oa_ms1` / `oa_svpg`),
  `oa_p_cells.cdl` (one `.subckt` per cell, devices as drawn incl. dummies), `build_oa_p.py` (re-runnable).
- DRC: `inputs/tools/oa_core_pd_drc.py <gds> <cell> [report]`, 0 per cell or a list of what remains and why. LVS:
  `inputs/tools/oa_core_pd_lvs.py <gds> <cell> <cdl> [subckt]`, match per cell. Renders, one PNG per cell.
- Report (under ~100 lines): sizes before / after (oa_misc_p 58.2 × 5.5 µm library, 12 × 17 µm as placed in v1),
  device map, tap / ring scheme with LU numbers, symmetry check of oa_pmir (XOR of the real devices' layers with their
  point image), backannotation list, pin list, and lessons for the bandgap's PMOS cells (bg_pmir_pcas, bg_misc_p).
- When done, reply with a five-line summary and the file list with sha256 (first 12 hex).
