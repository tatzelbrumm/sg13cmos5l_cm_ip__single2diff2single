# Brief, part 2 revised: compact `bg_core_pd`, primitives first (2026-10-28 04:25)

This replaces `BRIEF_bg.md` where the two differ; read that file for the inputs (`inputs_bg/`) and the goal.
The hard rules stay as before:
- cloud workspace only, no `mcp__remote-devices__*` tools, no git, inputs read-only;
- rule values only from the PDK decks, each with its file and rule name;
- facts kept apart from reasoning;
- `TZ=Europe/Berlin` times.

## The user, verbatim (04:25)

"okay, as long as you don't wait with it until Agent 2 has finished bg_core_pd, which is next in line. There should be
lessons learned from Oguey Aebischer for first modifying layout primitives for the bandgap reference, then compacting
the overall bandgap core."

("it" is putting your compact oa_core_pd into the macro. I do that now: your v2 passed my independent flat extraction,
which found every sheet device on its nets and the dummies as listed.)

All the user's layout instructions of 02:36–03:40 hold for the bandgap too:
- rotated transistors;
- same-size transistors combined into one array;
- never a tap between rows of an array;
- slim, optional and non-rectangular taps / rings, placed only where latch-up needs them;
- one merged NWell per rail, polygonal where the rules allow it;
- narrow dummies;
- the layout drives the design, with backannotation;
- skills split into generic and IHP.

## What changes against BRIEF_bg.md

`BRIEF_bg.md` said "primitives copied unchanged". That no longer holds. Work in two phases, as you, A3 and A4 did for
the OA core.

**Phase 1: revise the bandgap primitives.** Work on copies with new names (e.g. suffix `_c`), and keep the library
untouched. For each cell, apply what the OA work taught:
- `bg_pmir_pcas` (PB, PBC, PA, PAC, PO, POC):
  - no ring, NWell to the cell edge so it merges with the other vdd-well cells;
  - narrow dummies;
  - the common-centroid / point symmetry of the matched devices kept: XOR the device layers against their image, as
    A4 did for oa_pmir_c;
  - the cascodes placed like oa_pcas_c.
- `bg_nab` (NA / NB) together with `bg_misc_n` (MS2, MS3, SKS):
  - one rotated NMOS block like `oa_n10`, with interdigitated rows for NA / NB;
  - the small switches at the ends;
  - one periphery p+ tie and narrow end dummies, no tap between rows;
  - finger re-splits allowed, total W / L kept.
- `bg_misc_p` (MS1 chain, SVPG): like `oa_ms1` / `oa_svpg`, tap-less, NWell to the edge. Your v2 placement of them is
  the model.
- `bg_pnp` (Q1 + 8 × Q2, 3 × 3 with Q1 in the centre) and `bg_res` (R1A, R1B, R0, rhigh):
  - find out what "placed only" in `cell_tree.md` means;
  - add the internal wiring they lack;
  - keep the pnp array's common centroid and the resistor array's matching;
  - shrink the surrounding rings / spacing to what the deck requires: the pnp's own guard structures come from the
    device and are not yours to remove; anything added around them is.

Per changed cell: DRC 0 (or the listed LU.a that the parent resolves), LVS match, before / after size, and the
backannotation list.

**Phase 2: compact `bg_core_pd`** from the revised cells with your v2 generator:
- one vdd NWell;
- ties in the rails;
- the same rail / port conventions as `oa_core_pd` v2 (vdd top, vss bottom, ports on the right edge), so the two
  cores can stack or abut in `bias_gen_pd`;
- Metal1 / Metal2 only;
- `ea`, `eb`, `e2` short and symmetric, away from `iout` and the enables.

Report the area against the sum of the library primitives' areas, as you have no v1 block for the bandgap.

## Sources for the lessons

- Your own `out/skill/` (generic + IHP) and `out/v2/`.
- A3's `/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/out/` (REPORT_oa_n.md, skill/, build_oa_n.py).
- A4's `/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primP/out/` (oa_p_report.md, skill/, build_oa_p.py).

Read only; don't change their folders.

## Deliverables in `out_bg/`

- `bg_core_pd.gds` (the revised primitives inside) and the build script(s).
- `bg_core_pd.cdl`.
- DRC / LVS logs.
- Renders:
  - the block;
  - each revised primitive before / after at one scale;
  - one picture of the rule savings.
- The backannotation package, as for v2:
  - the sheet copy edited from `inputs_bg/bg_core_pd.sch`;
  - the subckt text;
  - `device_changes.txt`;
  - the xschem netlist of the new sheet;
  - the LVS against it.
- The skill export extended with the bandgap lessons (pnp array, resistor array, block with a bipolar core), keeping
  the generic / IHP split.
- The report: five-line summary first, under ~150 lines, file list with sha256 (first 12 hex). Put it in your final
  reply if `.md` writing is blocked.
