# Brief N: compact NMOS primitives for oa_core_pd (IHP sg13cmos5l), 2026-10-28

Workspace (yours only): `/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/`
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

You are the NMOS specialist. A second agent does oa_misc_p and oa_pmir; a third assembles oa_core_pd from your cells.

## Your cells
Library: `inputs/pad_buffer_cells.gds` (+ `.cdl`), cells `oa_nmir` (M10 / M11), `oa_misc_n` (MC10, MS2, MS3, SKS),
`oa_mcs` (MCS / MCL). Circuit: `inputs/oa_core_pd.sch`, `inputs/oa_core_pd_xschem.spice`, subckt `oa_core_pd` in
`inputs/bias_ref_pd.spice`:
`XM11 vnc vnc vss vss 90/1 ng4`, `XM10 d10 vnc vres vss 180/1 ng8`, `XMC10 vpc vbr d10 vss 10/1`, `XMS2 ks vbr vss vss 10/1`,
`XMS3 vpc ks vss vss 0.5/2`, `XSKS ks en_3v3_b vss vss 1/0.45`, `XMCS vbr vbr vss vss 3.4/30`, `XMCL vres vbr vss vss 3.4/30`
(all sg13_hv_nmos; bulk = substrate = vss).

1. **One 10/1 array** for M10, M11, MC10, MS2 (all 10 µm × 1 µm fingers today: M10 18, M11 9, MC10 1, MS2 1), rotated
   as the earlier workers rotated sinks_6x6, d2s_casc_n, bg_nab, bias_tree_n (read their log entries: 01:22–02:50 and
   03:32–03:45 on 2026-10-27 in `inputs/pad_buffer_layout_log.md`, and look at those cells in the library: unmodified
   SG13_dev device cells, R270 so texts stay upright, rows as AREFs at the Gat.b1 pitch, shared drain / source stripes,
   drain tabs with up to 3 Via1, tracks on Metal2). M10 : M11 = 2 : 1 must stay matched (common centroid or
   interdigitated, as oa_pmir does for its mirror); MC10 and MS2 sit at the ends or wherever they cost least. You may
   re-split fingers (e.g. 10/1 → 5/1 or 20/1 fingers) if the array gets more compact, keeping total W and L; then report
   the backannotation (new ng / w per device).
2. **Dummies** at the array ends only, narrow (the 2026-10-27 convention: W = 2 µm, same L), gates tied off.
3. **NEVER a substrate tap between rows of the array.** Taps only around the periphery. Check the latch-up distance
   rules of the deck (LU.*) with periphery taps only; if the array is too big for that, report the numbers instead of
   adding an inner tap.
4. **Guard rings revised completely**: the old ones are too bulky. One contact row, minimum Activ / Metal1, shared
   with the neighbour where it is the same well / substrate type, no double rings; no ring where the deck doesn't need
   one. (2026-10-27 08:45, the user on small split cells: "NO. NO ntap rings." — tap-less cells, bulk tied by the parent.)
5. **MS3 (0.5/2) and SKS (1/0.45)**: small; either tap-less cells to be placed by the assembler (bulk = vss by the
   parent, like `d2s_pd_n`), or appended to the 10/1 array's end if that is denser. Your call, with the reason.
6. **oa_mcs rotated**: MCS / MCL (3.4/30 each, matched pair, gates on vbr). Rotate so the 30 µm gates run in the
   direction that packs best next to the 10/1 array; minimal ring / periphery taps.
7. Pins: Metal1 / Metal2 pin boxes + texts as the library does (`<metal>.pin` + `<metal>.text`), one per net, on the
   cell edge where the assembler can reach them; tracks on Metal2; nothing on Via2 / Metal3 or above.

## Checks and deliverables (`out/`)
- `oa_n_cells.gds` with your new cells (names e.g. `oa_n10` for the 10/1 array, `oa_mcs_c`, `oa_ms3_sks`), each also
  standalone-checkable; `oa_n_cells.cdl` with one `.subckt` per cell (devices as drawn, dummies included);
  `build_oa_n.py` (re-runnable, reads `inputs/pad_buffer_cells.gds` for the device cells).
- DRC: reuse `inputs/tools/oa_core_pd_drc.py` (`python3 oa_core_pd_drc.py <gds> <cell> [report]`), 0 violations per cell
  or a list of what remains and why. LVS: `inputs/tools/oa_core_pd_lvs.py <gds> <cell> <cdl> [subckt]`, match per cell.
- Renders (`inputs/tools/oa_core_pd_render.py` as a start), one PNG per cell.
- Report (under ~100 lines): per cell the size before / after (old cells: `oa_nmir` 34.1 × 24.4, `oa_misc_n` 9.5 × 12.6,
  `oa_mcs` 62.5 × 6.0 µm), device-to-finger map, tap / ring scheme with the LU numbers, the backannotation list (every
  ng / w change), pin list with coordinates, and lessons for the bandgap's NMOS cells (bg_nab, bg_misc_n).
- When done, reply with a five-line summary and the file list with sha256 (first 12 hex).
