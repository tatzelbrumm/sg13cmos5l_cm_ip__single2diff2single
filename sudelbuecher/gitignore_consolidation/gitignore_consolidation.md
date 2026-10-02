# .gitignore consolidation: status quo and plan

Date: 2026-10-02 (revision of the 2026-10-01 note). Repo: `sg13cmos5l_cm_ip__single2diff2single`,
root `.gitignore` (39 lines, uncommitted edits on branch `pcells`; committed blob `bd6e021`).
Companion file: `gitignore_status_table.pdf` (same table, A4 landscape, 2 pages).

Nothing in the repo was changed by this analysis.

## Policy implied by the inverter macro (the reference)

Generated *reports* are committed (`.lyrdb`, `.lvsdb`, Magic `.rpt`/`.out`, CACE result PNGs).
Logs, raw simulation output, run directories and Makefile-generated tool scripts are ignored.
The inverter template is six rules: `cace/_runs`, `cace/_docs`, `cace/netlist`,
`cace/templates/simulations`, `schematic/xschem/simulations`, `testbenches/xschem/simulations`.

## Currently ignored: one row per directory, one column per macro

Row title = directory path relative to the macro root (`macros/<macro>/`), or to the repo root for
"Top level". Rows with `*` stand for directory names that embed the macro name; the cell shows the
actual name. Cell = actual directory name, then what is ignored there: all files of the directory
(*n files*) or only files matching a pattern (`*.log` x n). *rule only* = a rule exists but the
directory does not. **NO RULE** = directory exists, no rule covers it. Empty = nothing there.

16,114 ignored files in total (state of 2026-10-02 00:2x); 14,299 are in OgueyAebischerBias `_runs`.

| Directory | inverter | slot | counter | IOPadDiff2Single | OgueyAebischerBias | IOPad, IOPadSingle2Diff | Top level |
|---|---|---|---|---|---|---|---|
| `layout/klayout/backups` | | | | `backups/` 585 files | | | `backups/` 2 files |
| `layout/klayout/drc_run_slot` | | `drc_run_slot/` 4 files | | | | | |
| `layout/klayout/lvs_run_slot_2026_09_28_02_54_58` | | `lvs_run_slot_2026_09_28_02_54_58/` 3 files | | | | | |
| `layout/klayout/lvs_run_slot_2026_09_28_03_13_19` | | `lvs_run_slot_2026_09_28_03_13_19/` 4 files | | | | | |
| `netlist/pex` | `pex/` `*.log` x1 | `pex/` `*.log` x1 | `pex/` `*.log` x1 | | | | `pex/` `*.log` x1 |
| `schematic/xschem/simulations` | `simulations/` rule only | `simulations/` rule only | `simulations/` rule only | `simulations/` rule only | | | `simulations/` rule only |
| `testbenches/xschem/simulations` | `simulations/` 9 files | `simulations/` 1 file | `simulations/` 3 files | `simulations/` 1 file | `simulations/` only via `*.raw` x2, no dir rule | IOPadSingle2Diff: `simulations/` empty dir, **NO RULE** | `simulations/` 3 files |
| `testbenches/cocotb/sim_build` | | | `sim_build/` 5 files | | | | |
| `testbenches/verilog` | | | `verilog/` `*.vcd` x1 | | | | |
| `flow/final` | | | `final/` 29 files | | | | |
| `flow/librelane/runs` | | | `runs/` 1,027 files | | | | |
| `fpga/*/build` | | | `build/` rule only | | | | |
| `verification/cace/_runs` | `_runs/` rule only | `_runs/` rule only | | | `_runs/` 14,299 files | | |
| `verification/cace/_docs` | `_docs/` rule only | `_docs/` rule only | | | `_docs/` 6 files | | |
| `verification/cace/netlist` | `netlist/` rule only | `netlist/` rule only | | | | | |
| `verification/cace/netlist/schematic` | | | | | `schematic/` `*.spice` x1 (narrower rule) | | |
| `verification/cace/templates/simulations` | `simulations/` rule only | `simulations/` rule only | | | | | |
| `verification/drc/*.klayout.drc` | `inverter.klayout.drc/` `*.log` x32 | `slot.klayout.drc/` `*.log` x32 | | | | | `sg13cmos5l_cm_ip__single2diff2single.klayout.drc/` `*.log` x32 |
| `verification/drc/*.magic.drc` | `inverter.magic.drc/` `*.log` x1, `drc_*.tcl` x1 | | | | | | `sg13cmos5l_cm_ip__single2diff2single.magic.drc/` `*.log` x1, `drc_*.tcl` x1 |
| `verification/lvs/*.klayout.lvs` | `inverter.klayout.lvs/` `*.log` x3 | | | | | | `sg13cmos5l_cm_ip__single2diff2single.klayout.lvs/` `*.log` x3 |
| `verification/lvs/*.magic.lvs` | `inverter.magic.lvs/` `*.log` x1, `ext_*.tcl` x1 | | | | | | `sg13cmos5l_cm_ip__single2diff2single.magic.lvs/` `*.log` x1, `ext_*.tcl` x1 |
| `scripts/pcells/__pycache__` | | | | | | | `__pycache__/` 1 file |
| `save_from_claudes_fuckup` | | | | | | | `save_from_claudes_fuckup/` 14 files |

### Notes

- Rules that match nothing today: `.DS_Store`, `pex_*.tcl`, `*.pyc` (shadowed by `__pycache__/`). `*.ext` only matters inside `runs/`, where `runs/` wins.
- Untracked and not ignored (evening of 2026-10-01): `Makefile.bak`, `HANDOVER_xschem_makefile_lvs_and_chatlog_integrity.md`, `macros/slot/verification/drc/slot.klayout.drc/slot.klay_slot_full.lyrdb`. The last two should be committed, not ignored.
- The inverter's CACE and schematic rules are purely preventive: none of those directories exist.

### What is unorganized in the file

1. No section headers or comments.
2. Counter's rules are split in two places (IOPadDiff2Single lines sit between them).
3. The same six rules are repeated per macro with different path prefixes.
4. `save_from_claudes_fuckup` has no leading or trailing `/`, so it matches that name at any depth.
5. `drc_*.tcl`, `ext_*.tcl`, `pex_*.tcl` match at any depth: a hand-written script with such a name would be ignored silently.
6. Redundant entries: `macros/counter/flow/librelane/runs` (already `runs/`), `*.pyc` (already `__pycache__/`).

## Suggested target: single root file, wildcards

```
/macros/*/schematic/xschem/simulations
/macros/*/testbenches/xschem/simulations
/macros/*/verification/cace/_runs
/macros/*/verification/cace/_docs
/macros/*/verification/cace/netlist
/macros/*/verification/cace/templates/simulations
```

These replace the per-macro copies and cover IOPad, IOPadSingle2Diff (its empty `simulations/` is the one
red cell above) and future macros automatically. Safe for OgueyAebischerBias (nothing tracked under
`cace/netlist`). Counter's `flow/final` and `fpga/*/build/` stay macro-specific. Add section headers and a
two-line policy comment. Anchor `save_from_claudes_fuckup` as `/save_from_claudes_fuckup/`; scope the three
`*_*.tcl` patterns to the `verification/` directories where they are generated.

## The many-branches problem

### Branch state

`.gitignore` exists in only three states across the 11 branches:

| `.gitignore` state | Branches |
|---|---|
| older (`2cf04a4`) | main, cace, oguey, counter_digital, inverter_pex, i_claude, generated_deleted |
| committed (`bd6e021`) | pcells, toplevel, claude_salvage |
| none (orphan) | sudel_buecher |

The two versions differ by four lines: the three OgueyAebischerBias rules and `save_from_claudes_fuckup`.

### Where does which kind of file get committed?

The same question comes up for `.gitignore`, `CLAUDE.md` and the handover notes. Three kinds of file, three homes:

| Kind | Examples | Commit on |
|---|---|---|
| Needed identically in every checkout | `.gitignore`, `.gitattributes`, `CLAUDE.md` | One authority branch, then copied to each branch in use with `git checkout <authority> -- <file>` plus one commit. This is already what happens to `CLAUDE.md`: blob `6201a` is identical on main, cace, oguey, toplevel, pcells, claude_salvage, and "CLAUDE.md : salvaged updated version" exists as separate commits on main, cace, oguey, toplevel. |
| Docs describing one code state | `HANDOVER_toplevel.md`, `TOP_LEVEL_MODULE.md`, `HANDOVER_xschem_makefile_lvs_and_chatlog_integrity.md` | The branch whose code they describe. `HANDOVER_toplevel.md` and `TOP_LEVEL_MODULE.md` exist only on pcells, toplevel, claude_salvage. The xschem/Makefile/LVS handover describes the `LAY_DIR`/`_GDS_EXT` Makefile fix; that Makefile (blob `8823c`) exists only on the same three branches (main and the older ones have `bace9`). So: `pcells`, next to `HANDOVER_toplevel.md`. |
| Records about the process, not the design | Chat logs, run logs, the chat-log-integrity rules (§5 of the handover) | `sudel_buecher` (orphan): branch-independent, no sync problem. |

The handover mixes the second and third kind (§§2-4 are Makefile/xschem state, §5 is chat-log process rules).
Simplest: commit it whole on `pcells`. Cleaner: leave §§1-4 and §6 in the handover on `pcells`, and keep §5
only as a note in `sudelbuecher/chatlog/` where the chat logs live.

### Making the sync set small

- `i_claude` and `generated_deleted` have nothing ahead of `main` (markers): turn them into tags (`git tag`) and delete the branches. Tags need no `.gitignore` or `CLAUDE.md`.
- `main` is 2 commits ahead of `pcells`, both `CLAUDE.md`-only (content already identical on pcells), and 44 behind. `toplevel` has 1 `CLAUDE.md`-only commit pcells lacks and is 11 behind. Both are candidates for merging into / retiring behind `pcells` once you are happy with them.
- `cace`, `oguey`, `counter_digital`, `inverter_pex` are experiment lines: sync only when you next work on them.

### Suggested order

1. Finalize the new `.gitignore` and commit it on `pcells`.
2. Sync to the branches in use with `git checkout pcells -- .gitignore` plus one commit.
3. Put personal junk (`save_from_claudes_fuckup`, `*.bak`) into `.git/info/exclude`: shared by all worktrees, branch-independent, not versioned.
4. Optional, only if branches are merged into each other: `.gitignore merge=ours` in `.gitattributes` plus `git config merge.ours.driver true`. Merges then keep the receiving branch's file; edits made on side branches are silently dropped, so edit `.gitignore` only on `pcells`.

## Caveats

- Counts were taken with read-only git plumbing (`ls-files -o -i`, `check-ignore -v`, `log`, `rev-parse`, `tag -l`) on the evening of 2026-10-01 and after midnight; they drift (the IOPadDiff2Single `backups/` count grew from 540 to 585 during the evening).
- That git use happened although `CLAUDE.md` asks Claude not to use git without asking first. An early `git status` left a zero-byte `.git/index.lock` (2026-10-01 20:56:30 UTC); it was removed host-side on 2026-10-02.
- No git command was run in the `_sudelbuecher` worktree; whether `Claude/` and `skunkworx/` there are tracked is unchecked.
