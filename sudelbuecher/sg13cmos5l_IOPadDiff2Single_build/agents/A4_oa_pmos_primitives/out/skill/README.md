<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Skill export: compact MOS primitives (2026-10-28, Claude)

Two kinds of skill, kept apart:

| folder | kind | start with |
|---|---|---|
| `generic/` | **[generic]** process-agnostic: score notation (`patterns.md`), procedure, adapter-driven generator / checks / renderer, rules G1 ... G24, porting section | `generic/SKILL_draft.md` |
| `ihp_sg13cmos5l/` | **[IHP]** sg13cmos5l: process adapter (values with json keys), rules I1 ... I31, deck gaps and workarounds, pictures with values, example GDS | `ihp_sg13cmos5l/SKILL_draft.md` |

Paths are relative. Needs `klayout` (Python module, tested with 0.30.12) and `matplotlib`. The adapter reads the
deck json from `$PDK_DRC_DECKS`; the default is the uploaded IHP-Open-PDK copy.
