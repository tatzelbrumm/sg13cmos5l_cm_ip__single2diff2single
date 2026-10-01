# .gitignore consolidation: status quo and plan

Date: 2026-10-01. Repo: `sg13cmos5l_cm_ip__single2diff2single`, root `.gitignore`
(39 lines, with uncommitted edits on branch `pcells`; committed blob `bd6e021`).
Companion file: `gitignore_status_table.pdf` (same table, A4 landscape).

Nothing in the repo was changed. This is orientation plus suggestions only.

## Policy implied by the inverter macro (the reference)

Generated *reports* are committed (`.lyrdb`, `.lvsdb`, Magic `.rpt`/`.out`, CACE result PNGs).
Logs, raw simulation output, run directories and Makefile-generated tool scripts are ignored.
The inverter template is six rules: `cace/_runs`, `cace/_docs`, `cace/netlist`,
`cace/templates/simulations`, `schematic/xschem/simulations`, `testbenches/xschem/simulations`.

## Currently ignored, per macro

Numbers = files ignored on disk now. "rule only" = rule exists, matches nothing today.
"-" = no rule, nothing there.

| Category (rule) | inverter | slot | counter | IOPadDiff2Single | OgueyAebischerBias | IOPad, IOPadSingle2Diff | Top level |
|---|---|---|---|---|---|---|---|
| DRC/LVS tool logs (`*.log` under verification/) | 37 | 32 (DRC only) | - | - | - | - | 37 |
| PEX log (`*.log` in netlist/pex) | 1 | 1 | 1 | - | - | - | 1 |
| Magic scripts (`drc_*.tcl`, `ext_*.tcl`) | 2 | - | - | - | - | - | 2 |
| KLayout run dirs (`drc_run_*`, `lvs_run_*`) | - | 3 dirs, 11 files | - | - | - | - | - |
| testbenches/xschem/simulations | 9 (own rule) | 1 (own rule) | 3 (own rule) | 1 (own rule) | 2, only via `*.raw`, no dir rule | none, no rule (empty dir) | 3 (own rule) |
| schematic/xschem/simulations | rule only | rule only | rule only | rule only | - | - | rule only |
| CACE `_runs`, `_docs`, `netlist`, `templates/simulations` | 4 rules, rule only | 4 rules, rule only (no cace/ dir exists) | - | - | `_runs` 14,299; `_docs` 6; `netlist/schematic/*.spice` 1 (rule is narrower) | - | - |
| KLayout editor backups (`backups/`) | - | - | - | 540 | - | - | 2 |
| Digital flow | - | - | `runs/` 1,027; `flow/final` 29; `sim_build/` 5; `*.vcd` 1; `fpga/*/build/` rule only | - | - | - | - |
| Python cache (`__pycache__/`) | - | - | - | - | - | - | 1 (scripts/pcells/) |

Total ignored files on disk: 16,069 (14,299 of them OgueyAebischerBias `_runs`).

### Miscellaneous

- `save_from_claudes_fuckup/`: 14 files ignored, top level only. The only rule that is neither a macro rule nor a generated-file rule.
- Dormant rules (match nothing today): `.DS_Store`, `pex_*.tcl`, `*.pyc` (shadowed by `__pycache__/`). `*.ext` only matters inside `runs/`, where `runs/` wins.
- Untracked and not ignored: `Makefile.bak`, `HANDOVER_xschem_makefile_lvs_and_chatlog_integrity.md`, `macros/slot/verification/drc/slot.klayout.drc/slot.klay_slot_full.lyrdb`. The last two should be committed, not ignored.
- The inverter's CACE and schematic rules are purely preventive.

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

These replace the per-macro copies and cover IOPad, IOPadSingle2Diff and future macros automatically.
Safe for OgueyAebischerBias (nothing tracked under `cace/netlist`). Counter's `flow/final` and
`fpga/*/build/` stay macro-specific. Add section headers and a two-line policy comment.
Anchor `save_from_claudes_fuckup` as `/save_from_claudes_fuckup/`; scope the three `*_*.tcl`
patterns to the `verification/` directories where they are generated.

## The many-branches problem

Only three states of the file exist across the 11 branches:

| `.gitignore` state | Branches |
|---|---|
| older (`2cf04a4`) | main, cace, oguey, counter_digital, inverter_pex, i_claude, generated_deleted |
| committed (`bd6e021`) | pcells, toplevel, claude_salvage |
| none (orphan) | sudel_buecher |

The two versions differ by four lines: the three OgueyAebischerBias rules and `save_from_claudes_fuckup`.
So `main` and `oguey` currently lack the Oguey rules.

Suggestion:

1. Make `pcells` the source: commit the new file there. Copy it to branches you actually work on
   with `git checkout pcells -- .gitignore` plus one commit (whole-file replace, cannot conflict).
   Skip `i_claude` and `generated_deleted` (markers, nothing ahead of main). Update
   `counter_digital` and `inverter_pex` only when next touched.
2. Move personal junk (`save_from_claudes_fuckup`, `*.bak`) into `.git/info/exclude`: shared by all
   worktrees, branch-independent, but not versioned or shared with clones.
3. Optional, only if branches are merged into each other: `.gitignore merge=ours` in `.gitattributes`
   plus `git config merge.ours.driver true`. Merges then keep the receiving branch's `.gitignore`;
   edits made on side branches are silently dropped, so edit `.gitignore` only on `pcells`.

With wildcards the file should rarely change again, so the sync is a one-time cost.

## Caveats

- Counts were taken with read-only git plumbing (`ls-files -o -i`, `check-ignore -v`) on 2026-10-01 evening; they will drift.
- A stray zero-byte `.git/index.lock` in the main worktree (stamped 2026-10-01 20:56:30 UTC) came from an
  early `git status` run by Claude; it has to be removed host-side.
- No git command was run in the `_sudelbuecher` worktree; whether `Claude/` and `skunkworx/` there are tracked is unchecked.
