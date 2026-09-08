# References — 2026-09-05 (Sonnet session: xschem explainer + IOPadInOut30mA sourcing)

Sources for
[`../2026-09-05_sonnet_xschem_explainer_and_iopad30ma_sourcing.md`](../2026-09-05_sonnet_xschem_explainer_and_iopad30ma_sourcing.md).

Rule, per [`README.md`](README.md): **index, do not copy.**

---

## 1. Web search (turn 2) — not fetched, results quoted inline only

- Krzysztof Herman (IHP), "IHP SG13G2 IO cells review" —
  <https://ieee-cas.org/files/ieeecass/2025-12/io-cells-sg13g2_0.pdf>.
  Source for the `sg13g2_IOPadInOut30mA` pin list quoted in the transcript
  (`c2p`, `c2p_en`, `p2c`, `pad`, `iovdd`/`iovss`/`vdd`/`vss`). **Not opened
  as a document** — the `WebSearch` tool returned a synthesized summary of
  it; the PDF itself was never fetched or read directly this session. The
  transcript says so explicitly ("I'm relaying a web search, not something
  I opened myself").
- IHP-Open-PDK-docs — <https://github.com/IHP-GmbH/IHP-Open-PDK-docs>.
  Named as the authoritative doc repo for the PDK this project forks from;
  not opened.
- IHP-Open-PDK — <https://github.com/IHP-GmbH/IHP-Open-PDK>. Named as the
  PDK source repo; not opened.

## 2. In-repo / connected-folder files read (turns 1–2)

All four connected folders, read-only, no `PDK_ROOT` access (the actual PDK
install lives inside the container, unreachable from the sandbox — see the
transcript's turn 2 for the `find`/`grep` commands handed to the user
instead):

- `sg13cmos5l_cm_ip__single2diff2single/schematic/xschem/*` (`.sch`, both
  `.sym` files, `xschemrc`) — turn 1, read in full.
- `sg13cmos5l_cm_ip__single2diff2single/CLAUDE.md` and
  `_sudelbuecher/CLAUDE.md` — project context.
- `sg13cmos5l_cm_ip__single2diff2single/README.md`,
  `chipalooza_cmos5L/s2d_d2s_pinbuffers.md`,
  `chipalooza_cmos5L/repo_consolidation_analog_project.md`,
  `chipalooza_cmos5L/sg13cmos5l_repository_comparison.md` — grepped for
  `iopad` context; only `README.md` had a relevant hit (the sibling
  `sg13cmos5l_IOPadAnalog` / padframe-slot discussion).
- `_sudelbuecher/sudelbuecher/chatlog/2026-09-04_ocd_reconciliation_and_ogueyaebischerbias_cace.md`
  — grepped for the same padframe context.
- `IIC-OSIC-TOOLS/_tests/{23,24,25}/` — listed; inverter DRC/LVS/PEX
  fixtures only, no io-cell library present.
- `chipalooza_cmos5L/` top-level listing and `krzysztof_explained/` —
  checked and set aside as unrelated (an ESD bootstrapped-switch simulation
  writeup, coincidentally the same author as the IO-cell review PDF above,
  not pad-cell source data).
- `git log` / `git diff` / `git status` on
  `schematic/xschem/sg13cmos5l_cm_ip__single2diff2single.sch` and `.sym`
  (main design worktree, `toplevel` branch) — turn 1, to explain the
  uncommitted template-teardown edits.

## 3. This directory's own format precedent

- [`2026-09-04_sonnet_oab_cace_unit_fixes_and_toplevel_handoff.md`](../2026-09-04_sonnet_oab_cace_unit_fixes_and_toplevel_handoff.md)
  — read in full as the header/elision/turn-numbering template for the
  transcript this file supports.
- [`ref/README.md`](README.md) and [`pix/README.md`](../pix/README.md) —
  read to determine that this session's material belongs in a new `ref/`
  file (external sources, none fetched) and *not* in `pix/` (see §4 — no
  image in this session is this session's own generated output).

## 4. Images mentioned in the transcript, found — not generated, not copied

Both belong to `sudelbuecher/sg13cmos5l_IOPadInOut30mA/`, a directory
dedicated to that one cell, not to this chatlog — so they are linked from
there rather than duplicated into `pix/`, per `pix/README.md`'s own scope
("images for the notes in `sudelbuecher/`", i.e. this session's own output;
neither of these is that):

- [`../../sg13cmos5l_IOPadInOut30mA/ChatGPT Image Sep 5, 2026, 09_32_59 PM.png`](<../../sg13cmos5l_IOPadInOut30mA/ChatGPT%20Image%20Sep%205%2C%202026%2C%2009_32_59%20PM.png>)
  — the user's colleague ChatGPT's own output, described (not opened
  pixel-by-pixel, not verified) in turn 2.
- [`../../sg13cmos5l_IOPadInOut30mA/sg13cmos5l_IOPadInOut30mA_verified_schematic_v3.png`](../../sg13cmos5l_IOPadInOut30mA/sg13cmos5l_IOPadInOut30mA_verified_schematic_v3.png)
  / [`.svg`](../../sg13cmos5l_IOPadInOut30mA/sg13cmos5l_IOPadInOut30mA_verified_schematic_v3.svg),
  plus the accompanying
  [`sg13cmos5l_IOPadInOut30mA_full_hierarchy.spi`](../../sg13cmos5l_IOPadInOut30mA/sg13cmos5l_IOPadInOut30mA_full_hierarchy.spi)
  — appeared mid-session (see the transcript's "Companion activity" note).
  Turn 12 corrected the provenance guess above: this was the user's
  colleague ChatGPT, not a parallel Opus session — see turn 12 and its
  correction of turn 3's misattribution. Neither the `.spi`'s claimed
  provenance (extraction "from the official IHP
  `libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spi`") nor the schematic's
  correctness had been checked as of turn 3; turn 13 (the `analog-schematic`
  build) and turn 24 (the real KLayout-exported GDS) are what actually
  checked parts of it — see §5 and §7.

## 5. `analog-schematic` skill build (turn 13)

- `anthropic-skills:analog-schematic`'s own `SKILL.md`,
  `scripts/sch_netlist.py`, `tests/golden.py` — read in full to learn the
  `Mosfet`/`TwoTerm`/`Port` primitives and the DRC-then-render workflow
  before writing any netlist code, per this session's own research-before-
  skill convention.
- Input netlist:
  `sudelbuecher/sg13cmos5l_IOPadInOut30mA/sg13cmos5l_IOPadInOut30mA_full_hierarchy.spi`
  (the ChatGPT-produced file above), read in full — every `.subckt`'s
  D/G/S/B node list transcribed by hand into the skill's Python primitives
  for the `GateDecode` N-path only (`io_inv_x1` → `io_nor2_x1` →
  `LevelUp`); the mirrored P-path and the ESD clamps/diodes were not
  rendered (no `Diode` primitive in the skill; device count too high for a
  legible figure). Output: `pix/2026-09-06_sonnet_gatedecode_npath_drc.png`
  / `.svg` (see `pix/README.md`) and
  `sudelbuecher/sg13cmos5l_IOPadInOut30mA/sg13cmos5l_GateDecode_npath_drc.py`
  (the build script, also copied there).
- `pip install cairosvg` — installed into the sandbox to rasterize the SVG
  for the mandatory visual-inspection step the skill requires.

## 6. Local build-script and meeting-chat research (turns 15–16)

All read directly, no web fetch:

- `IIC-OSIC-TOOLS/_build/images/open_pdks/scripts/install_ihp.sh` and
  `install_ihp_cmos5l.sh` — read for the real `libs.ref/<pdk>_io/` and
  `libs.tech/xschem/<pdk>_tests|tests/` path conventions and the
  `sg13g2_IOPad_tb.sch` testbench reference, before the user confirmed the
  real paths from inside the container in turn 14.
- `chipalooza_cmos5L/GMT20260827-140446_RecordingnewChat.txt` — the actual
  2026-08-27 Chipalooza review call chat log. Grepped for `klayout`/`magic`
  and for `Herman`/`Edwards`/`Dorrer`; quoted verbatim with timestamps in
  turn 16's answer (Simon Dorrer's KLayout productivity-suite link at
  00:46:48; Krzysztof Herman's and "tim"'s presence on the call at
  01:02:28/01:02:37).
- `chipalooza_cmos5L/repo_consolidation_analog_project.md` — read for the
  "Austrian School" (JKU/Dorrer/Pretl) vs. "Edwards School" (Tim Edwards)
  framing and its link to <https://opencircuitdesign.com/analog_flow/> as
  Edwards' own reference flow. Re-read in full, with its own byline read
  out, for turn 18's authorship question (Christoph Maier, revision 2,
  2026-08-28).
- `home/cmaier/EDA/sg13cmos5l_cm_ip__single2diff2single/README.md` §License
  — re-read for the SPDX-header question (turns 20–21).

## 7. Real KLayout-exported pad GDS (turn 24)

- `macros/IOPad/layout/gds/*.gds` (six files, user-exported from the real
  `$PDK_ROOT` inside the container via `pya`, per turns 19–21's discussion)
  — read with `gdstk` (`pip install gdstk`), not opened by hand: cell
  names, bounding boxes, polygon counts, per file. This is the first point
  in the whole `sg13cmos5l_IOPadInOut30mA` investigation where **real**
  IHP-sourced hierarchy data (not a ChatGPT transcription, not a web
  search) was directly inspected. Confirmed: `IOPadInOut30mA`'s real
  hierarchy has 13 cells and no `GuardRing_*` subcells anywhere — the
  ChatGPT `.spi`'s nine `GuardRing_*` subckts (§1 above / that transcript's
  turn 2) do not exist as named cells in the real layout.

## 8. Web search + failed fetch (turn 22, CC BY-NC question)

- `mcp__workspace__web_fetch` on
  <https://opencircuitdesign.com/chipalooza/challenge-2.html> — returned
  empty (likely JS-rendered); not used as a source, noted as a failed
  attempt in the transcript rather than silently dropped.
- `WebSearch`, query `Chipalooza challenge 2 open circuit design license
  requirements submission` — no Challenge-2-specific page found; used only
  for the general pattern ("recognized permissive open-source license"
  required by this class of program). Result links quoted to the user as a
  `Sources:` block in that turn; not reproduced again here since they were
  general-pattern evidence, not a specific rule for this repo.
