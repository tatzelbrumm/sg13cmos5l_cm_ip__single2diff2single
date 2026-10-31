<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C2, rejected first attempt (P, N on Sonnet; F on Opus): kept for the record

Christoph, 2026-10-31 about 18:55 CET, verbatim:

> d2s_loads have asymmetric dummies. Best: symmetric rows along the line dividing the rows, symmetric dummies. Worse:
> symmetric rows along the line dividing the rows, no dummies
> ABSOLUTELY, UNACCEPTABLY WORST: dummies on only one (mismatching) side of each row.
> Applies also to sinks_6x6. d2s_tails, d2s_casc_n, d2s_casc_p look horrible, too. The input differential pairs have
> the kind of narrowed poly contacts already eliminated in other cells. Based on this, the entire layout is f$cked up
> from the bottom up. Upgrade the model of the layout agents, throw away their shit, rebuild, and wait for manual
> review of the layout primitives. Keep the horror show of failed layouts for archival purposes.

What is here: the briefs, messages, reports, `out/` and `work/` of P, N and F as they were at 18:55 (F's stage 3 pad
candidate in `F/stage3/`; F's `work/repo` copy, caches, GDS and lvsdb files of its run folders dropped). All of it
passed the lead's checks (XOR against a rebuild, IHP DRC incl. latch-up, IHP LVS, device tables against the circuit):
those checks verified correctness, not layout quality (symmetry, dummies, gate contacts), which is what failed.
Not to be reused; see the rebuild in `../P/`, `../N/` (Opus) and the lead's report.
