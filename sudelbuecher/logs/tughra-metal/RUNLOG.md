<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# RUNLOG: tughra art in slot_7 (branch `art/tughra-metal`, cloud session, 2026-11-08 / 2026-11-11)

What was run, in order, and what came out. Times are UTC and come from the tool output where it printed them (DRC / filler logs); the others are the order of the session.
Full tool logs were written to scratch directories of the cloud container and are gone; what is filed here are the files the repository holds (logs trimmed to their last 120 lines,
reports, statistics). Commit hashes are those after the rebase onto `toplevel` (2026-11-08 23:30).

| # | what | command / script | result |
|---|---|---|---|
| 1 | baseline DRC of the untouched slot7 `final/gds/slot_7.gds` (commit `454da6a` of the slot7 repo) | PDK `run_drc.py --path --topcell=slot_7 --mp=2` (22:48) | only global minimum-density rules violated: AFil.g, GFil.g, M1.j, M2.j, M3.j, M4.j, TM1.c |
| 2 | baseline LVS | PDK `run_lvs.py --run_mode=deep --disable_tap_extraction`, slot7 `netlist/slot_7.cdl` (22:48) | PASS, netlists match, 0 errors |
| 3 | free space per metal layer | `art/find_free_space.py` | per-layer free 88-98 %; largest common rectangle clear of the TopMetal1 straps 319 x 90 um |
| 4 | first geometry (45-degree outline, TopMetal1 green) merged and DRC-checked | `art/build_art.py` (old), `run_drc.py` (22:48) | 21 rules violated, 7 of them the baseline density rules; the other 14 (M1-4.a, M2-4.b, M3.i / M4.i / M2.i / M1.i, M4.d, TM1.a, TM1.b) came from the art |
| 5 | art cell alone, 45-degree outline with TopMetal1 / metal rules | `run_drc.py --no_density --no_feol` on `tughra_art.gds` (22:49) | 13 rules violated (tens of markers per layer) |
| 6 | staircase polygons, disc kernel | same (22:51) | 10 rules, 78-763 markers per rule (TM1.a 763, TM1.b 567), from stroke tips and round ends |
| 7 | staircase, chamfered-square kernel | same (22:52) | 2 rules left (M1.a 9, M4.a 24 markers) |
| 8 | + repair loop on the deck's width / space check | same (22:53) | **art cell passes the BEOL tables** |
| 9 | rev 2 (purple TopMetal1) full verify | `art/verify_art.py` | XOR 0; no rule newly violated; LVS identical |
| 10 | rev 3 (Metal1-4, red+orange+gold Metal1) full verify | `art/verify_art.py` (3 min) | XOR 0; no rule newly violated; LVS identical; densities M1 1.64 -> 2.20 % |
| 11 | poly feasibility test on a scratch copy: blue shapes as GatPoly (5/0) without and with Activ (1/0) under them | `run_drc.py --antenna`, `run_lvs.py` (23:14) | poly only: no rule beyond baseline, LVS PASS. Poly + Activ: Act.a, Act.b, Act.d, Gat.c, Gat.f, LU.b newly violated, LVS PASS |
| 12 | PDK filler script on the merged GDS, no seal ring | `klayout -n sg13cmos5l -zz -r filler.py` (23:26) | wrote no filler: the filler fills only inside layer 39/0 (seal ring) |
| 13 | filler with a synthetic seal ring, rev 3 (no markers) vs rev 4 (markers) | `art/fill_test.py` (committed result `art/fill_test.md`) | without markers 126-661 filler shapes touch the art box (Activ 6619, poly 3983, M1 5125, M2 6862, M3 5082, M4 5549, TM1 5823 um2 inside); with markers 0 um2 inside |
| 14 | rev 4 (GatPoly purple, Metal1 red+orange, Metal2 gold, Metal3 blue, Metal4 green; seven nofill markers) full verify | `art/verify_art.py` (3 min 16 s) -> `verify/*.log`, `verify_report.md/.json` | XOR 0 over 39 layer/datatypes; **no rule newly violated** (same 7 density rules, same marker counts); LVS PASS before and after, extracted netlists identical; density M1 1.64 -> 2.01, M2 0.76 -> 0.94, M3 2.14 -> 2.47, M4 0.65 -> 0.98, GatPoly 3.59 -> 3.64 % |
| 15 | rebase `art/tughra-metal` from `origin/main` (`60f270a`) onto `origin/toplevel` (`4223a63`) | `git rebase --onto origin/toplevel origin/main art/tughra-metal`; `git push --force-with-lease` | 10 commits, no conflicts, content of `art/` and the notes identical before and after; `main` and `toplevel` have unrelated histories (no merge base) |
| 16 | tag push (`art-rev2-topmetal1`, `art-rev3-m1-m4`) | `git push origin <tags>` x5 incl. backoff | refused by the remote ("unexpected disconnect"); tags exist locally only |
| 17 | skill folder `layout-art-from-image` and upload zip | files under `art/skill/` on `art/tughra-metal` (commit `c4e4d0d1`) | pushed; copy under `Claude/skills/` and `Claude/layout-art-from-image-v1.zip` on this branch |

## Files filed here

`drc_base.log`, `drc_merged.log`, `lvs_base.log`, `lvs_merged.log` (rev 4, last 120 lines), `verify_report.md/.json` (rev 4), `fill_test.md`, `build_stats.json`, `free_space.md`.
Not filed: the logs of runs 1-13 (their results are in the table), the rev 2 / rev 3 reports (their GDS are in the history of branch `art/tughra-metal`).

## Not run
Harness flow (projects-gds, gds-prefill, net check), PEX, a microscope look at poly, the other two PDKs.
