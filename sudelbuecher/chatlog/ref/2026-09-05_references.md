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
  — appeared mid-session (see the transcript's "Companion activity" note),
  apparently from a parallel Opus session acting on turn 2's own
  suggestion. Neither the `.spi`'s claimed provenance (extraction "from the
  official IHP `libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spi`") nor the
  schematic's correctness has been checked by this session.
