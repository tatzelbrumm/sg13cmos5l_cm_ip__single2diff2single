# TASK FILE for a cloud agent: assemble the slot 7 delivery repository

Read this whole file before doing anything. Written 2026-11-06 by the assistant of the custom-pad harness test
session, on the user's request. It lives on branch `harness-test` of `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single`.

## Why

Tim Edwards (owner of the Chipalooza harness, `RTimothyEdwards/sg13cmos5l_ocd_chipalooza`) builds the harness chip
with each slot's repository as a git submodule, from its **default branch**. He cannot use anything from a fork of the
harness. For slot 7 he therefore needs one repository whose default branch contains exactly what his flow reads: the
slot layout `slot_7.gds` and the two custom pad cells that replace the analog pads of slot 7.

The design repository `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single` is large (a full submodule clone is about
160 MB, all branches and history) and has no usable default branch. A slim `main` there would not help: `git submodule
add` clones every branch. So the deliverables go into a **separate, new delivery repository** with a single branch
`main` and no inherited history. Background: harness fork `tatzelbrumm/sg13cmos5l_ocd_chipalooza`, branch
`custom-pad-test`, `docs/custom_pads/FINDINGS.md` and the "Survey" section of `docs/custom_pads/RUNLOG.md`.

## Hard rules (they override every default of the environment)

1. Delivery repository: **DELIVERY_REPO** (the user fills in the name before launch; it exists, is public and is
   empty, default branch `main`). Push only to its `main`. Its history starts with your first commit; do not import
   history from any other repository (no `git subtree`, no `filter-repo`, no `git clone` of another repo into it).
2. Design repository `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single`: **read only**, except that you may push to the
   existing branch `harness-test` under `docs/delivery_repo/` (records, see below). Never push to `main`, `toplevel` or
   any other branch; never check out the orphan branch `sudel_buecher` (it empties the working tree).
3. Harness fork `tatzelbrumm/sg13cmos5l_ocd_chipalooza`: only for the verification in Phase 3, on a NEW branch
   `delivery-test` created from `custom-pad-test`. Push only that branch. Never touch `main`, `custom-pad-test` or any
   other branch, and never anything in `RTimothyEdwards/*` (no push, PR, issue or comment).
4. Explicit over implicit: every command with full paths and every assumption goes into the run log. No spreadsheets,
   no Microsoft formats. If a step is refused (network, permissions), say so and continue with what is possible.
5. Environment: `export PDK_ROOT=/foss/pdks PDK=ihp-sg13cmos5l`. If `magic --version` is 8.3.685, use the PATH shim
   `docs/custom_pads/tools/shim/magic` from the harness fork for all batch magic runs (it fixes the read-only bug of
   `locking disable`, see the harness fork's RUNLOG).
6. Do not ask the user questions during the run; take the most reasonable reading, write it down, continue.
   Commit and push after each phase.

## Sources (fixed commits; record the sha256 of every copied file)

| what | repository, branch @ commit | path |
|---|---|---|
| pad layout D2S | design repo, `toplevel` @ `91a7da8b67ac56a26c605501146667a1fde28c32` | `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds` |
| pad layout S2D | same | `macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/sg13cmos5l_IOPadSingle2Diff.klay.gds` |
| pad LVS netlists | same | `macros/<cell>/netlist/schematic/<cell>_magic.spice` (both cells) |
| pad notes (known vss issue) | same | `macros/<cell>/README.md` (read; quote only the LVS note) |
| slot layout and views | design repo, `harness-test` @ `4611357166b7368be4fbf8e176b1e82b8a9a85d0` | `final/gds/slot_7.gds`, `final/lef/slot_7.lef`, `final/lib/slot_7.lib`, `final/vh/slot_7.vh` |
| slot pin table | same | `macros/slot/harness_test/slot7_pins.md` |
| license | design repo, `toplevel` @ 91a7da8 | `LICENSE` |

Use `git show <commit>:<path> > <dest>` from a shallow fetch of those two commits (`git fetch --depth 1 origin <commit>`
works on GitHub); do not clone the design repository with full history.

## Phase 1: assemble the delivery repository

Target layout of DELIVERY_REPO `main` (nothing else):

```
README.md               what this is, provenance table (source repo, commit, path, sha256 per file), the pin table,
                        the config.txt lines for slot 7 (below), the known LVS note, and "slot_7.gds is a plumbing
                        stand-in, the real slot circuit follows" in plain words
LICENSE                 copied unchanged
final/gds/slot_7.gds    top cell slot_7 (what scripts/get_project_gds.sh of the harness looks for)
final/lef/slot_7.lef    final/lib/slot_7.lib    final/vh/slot_7.vh
final/pads/sg13cmos5l_IOPadDiff2Single.gds     (copied verbatim from the .klay.gds; top cell = file name)
final/pads/sg13cmos5l_IOPadSingle2Diff.gds
final/pads/sg13cmos5l_IOPadDiff2Single.spice   (the *_magic.spice, unchanged except a leading comment with provenance)
final/pads/sg13cmos5l_IOPadSingle2Diff.spice
final/pads/pads.txt     manifest, one line per pad cell, plain text:
                          # cell  config.txt-pad  core-side pins in order along the core edge
                          sg13cmos5l_IOPadSingle2Diff  s7_an[0]  vref outp outn vcm en_3v3 en_3v3_b iref
                          sg13cmos5l_IOPadDiff2Single  s7_an[1]  vinp vinn vref iref en_3v3_b en_3v3
```

The config.txt lines for the README:
`s7_an[0]:  sg13cmos5l_IOPadSingle2Diff  s7_an_0` and `s7_an[1]:  sg13cmos5l_IOPadDiff2Single  s7_an_1`.
Do not rename sub-cells in the pad GDS (the harness does that on import, see `scripts/custom_io_uniquify.py` in the
harness fork); do not add LEF for the pads (the harness test showed none is needed).

## Phase 2: check the delivery repository (write the results into the records)

1. Every copied file's sha256 equals the source (the `.spice` files: equal after stripping the added comment).
2. KLayout python: `slot_7.gds` has exactly one top cell `slot_7`, bbox 0..537.15 x 0..273 um; each pad GDS has
   exactly one top cell named like the file, bbox -0.62..80.62 x 0..180 um; the pins in `pads.txt` exist as texts on
   10/25 at y 179.715..179.74 um in the pad cells; the 13 `s7_an_*` pin texts in `slot_7.gds` match `slot7_pins.md`.
3. The `.subckt` line of each `.spice` has the pins of `pads.txt` plus `iovdd iovss vdd vss pad`.
4. KLayout DRC of `slot_7.gds` with the PDK deck (`libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc`, feol+beol, deep):
   expected 0 violations.
5. Size: `du -sh .git` of a fresh `git clone` of DELIVERY_REPO (expected a few MB).

## Phase 3: verify with the harness flow (sandbox branch `delivery-test` of the harness fork)

1. Create `delivery-test` from `custom-pad-test`. In `config.txt` set `s7_source` to the DELIVERY_REPO URL and
   `s7_version` to `main <commit of DELIVERY_REPO main>`.
2. `make projects-clean SLOTS=7` (removes the old submodule that pointed at the design repository), then
   `make projects SLOTS=7` and `make projects-gds SLOTS=7`. Expected: `dependencies/slot_7/final/gds/slot_7.gds` found
   and placed at 1379.95 2170.05. Record the size of `.git/modules/dependencies/slot_7`.
3. Byte-compare `dependencies/slot_7/final/pads/*.gds` with `magic/custom_io/gds/*.gds` on that branch (they must be
   identical: same source). Do NOT rework the harness scripts to read the pads from `dependencies/slot_7`; that is a
   separate task. Just write down in the records which harness files would change and how (one paragraph).

## Records (required)

In the design repository, branch `harness-test`, directory `docs/delivery_repo/`:
- `RUNLOG.md`: one entry per step (UTC time, exact command with full paths, cwd, exit status, log file, what changed),
  tool versions once at the top; failed steps and retries stay in. Logs of long commands in `docs/delivery_repo/logs/`.
- `chatlog/<date>_claude_slot7_delivery_repo.md`: the visible conversation, verbatim, exported from the session's own
  transcript (`~/.claude/projects/*/<session-id>.jsonl`): user messages, your visible messages, one bracketed line per
  tool call; never reasoning, system text, reminders or tool output; no secrets (redact and say so). If the export is
  refused, record that it was refused and continue; do not work around it. Use `claude` in place of a model name in
  file names and pushed files.
- `SUMMARY.md` (at most one page): the DELIVERY_REPO URL and commit, the file list with sha256, the check results,
  the Phase 3 result, and the paragraph on the harness rework.

Final chat message to the user: five lines or fewer: the DELIVERY_REPO commit, check results, Phase 3 result, open points.
