# HANDOVER_toplevel.md — seed context for the top-level testbench/CACE session

Written 2026-09-04 by Claude Sonnet 5 (Cowork), handing off to a fresh Sonnet
5 High session per the user's request — a deliberate context switch, not a
capability escalation like the `HANDOVER.md` → Opus hand-off was. That file
is about a different task (`OgueyAebischerBias` macro sizing/CACE, now largely
worked through) and a different branch (`cace`/`oguey`); you don't need it
for this task, though it's still worth skimming for the traps section.

**Read [`CLAUDE.md`](CLAUDE.md) first**, as always. This file adds the
current-branch state and the specific task, plus several fresh debugging
lessons that will very likely recur.

---

## 1. The task, in the user's own words (this session, turn 13)

> The testbench, though renamed, still works and refers to the analog on top
> demo project. This needs to be replaced by the top level for the
> single2diff2single circuit, a lot of which is non-existent. For starters,
> build a testbench and CACE skeleton based on the information in README.md,
> submission.yaml, and documentation in the sudelbuecher worktree.

Concretely, verified this session: `testbenches/xschem/
sg13cmos5l_cm_ip__single2diff2single_tb_tran.sch` instantiates
`sg13cmos5l_cm_ip__single2diff2single.sym` (`x1`) and its PEX counterpart
(`x3`) — the rename succeeded, the file runs, but the top-level *schematic*
those symbols point to is still the inherited template content (two
`inverter` placements — see `CLAUDE.md` §7's teardown list), not the real
single-ended↔differential↔single-ended circuit. There is currently **no**
top-level CACE deck at all (`ls macros/*/verification/cace/*.yaml` exists per
macro; nothing at the repo root does). Building one is the actual ask.

**Before writing anything**, read, in this order:
1. `README.md` — rewritten today (commit `7e1dccb`) from
   `sudelbuecher/description/*`; has the actual pinout/intent, "Chip
   Integration", "Recursive Macro Structure" sections.
2. `submission.yaml` — top-cell name (hard invariant, see `CLAUDE.md` §1),
   but note it still has two `TODO`s: `short-description` and `analog-pins:
   3` ("confirm once the real circuit is in... the inherited example wires
   all three"). Don't treat `analog-pins: 3` as settled.
3. `sudelbuecher/description/` in the `_sudelbuecher` worktree (see §4
   below for how to reach it) — in particular whatever file covers pin
   buffers (referenced elsewhere this session as
   `sudelbuecher/description/s2d_d2s_pinbuffers.md`; it's the closest thing
   to a spec, and per the `OgueyAebischerBias` HANDOVER.md it still has
   `ibias`/`igmc` targets marked "to be discussed" — nothing is committed).

Per `README.md`'s own "State" framing and `CLAUDE.md` §7, most of the design
is schematic-less: input S2D buffer, output D2S class-AB buffer, internal
V_CM reference, gmC filter/oscillator stage, digital scan chain. Whatever
CACE skeleton you build will mostly be scaffolding around parameters/blocks
that don't exist as circuits yet — that's expected, not a mistake to fix.

## 2. Branch state right now

`toplevel` is checked out and currently **identical to `main`** — same
commit, `7e1dccb`, no divergence:

```
main      7e1dccb  submission.yaml and README.md updated from sudelbuecher/description files
toplevel  7e1dccb  (same commit)
```

Only two commits have ever touched top-level `README.md`/`submission.yaml`
— the rename (`743c8a8`) and today's content rewrite (`7e1dccb`) — both
already in `toplevel`'s history, nothing stranded elsewhere.

Two loose ends in the working tree, not yet dealt with:
- Untracked `macros/OgueyAebischerBias/verification/cace/{_docs,_runs,netlist}/`
  — generated CACE run artifacts from this afternoon's debugging session on
  a different branch's worth of work; harmless, just not committed/ignored.
- Untracked `save_from_claudes_fuckup/` at the repo root — **not examined**
  this session. Arose from user frustration mid-session (see chatlog turn
  9); presumably a manual backup the user made. Don't interpret or touch it
  without asking first.

Also: `CLAUDE.md`'s branch table (§3) is stale — `oguey` and `cace` branches
now exist from today's parallel Sonnet/Opus work on the bias macro, not
listed there. Doesn't affect `toplevel`.

## 3. Fresh debugging lessons from today's CACE work (will very likely recur)

All discovered the hard way this session while fixing four testbenches Opus
authored for `OgueyAebischerBias`. Read the full blow-by-blow in
[`../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/chatlog/2026-09-04_sonnet_oab_cace_unit_fixes_and_toplevel_handoff.md`](../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/chatlog/2026-09-04_sonnet_oab_cace_unit_fixes_and_toplevel_handoff.md)
if you want the exact error text and how each was diagnosed. Summary, since
you'll be authoring new CACE `.yaml` and `.sch` files from scratch for this
task too:

- **CACE's `unit:` field is not a label, it's the scale.** The number you
  write under a spec's `minimum`/`typical`/`maximum` must already be
  expressed in the declared unit (e.g. `unit: nA`, `value: 200` means 200
  nanoamps). CACE's `spice_unit_convert`/`spice_unit_unconvert` (in
  `spiceunits.py`, verified by reading the `efabless/cace` source directly)
  scale by parsing a metric prefix out of the unit *string* — there's no
  auto-scaling of a raw-SI number into a nicer display unit on its own.
  Conversely, **every testbench must always echo the raw, unscaled SI value**
  (amps, volts, seconds, a plain fraction for `%`) — never pre-scale inside
  the `.sch`'s ngspice `.control` block to "match" the yaml's unit. Doing
  that double-converts in both directions (comparison *and* display) and is
  exactly the bug that took two rounds to find and fix in
  `reference_tb_noise.sch` (`1e9 *`) and `reference_tb_dc_mm.sch` (`100 *`)
  today.
- **Never put a literal ASCII `"` inside an xschem `value="..."` multi-line
  code block.** It terminates the string early and silently truncates
  everything after it from the generated netlist — no error pointing at the
  real cause, just a baffling downstream "incomplete or empty netlist... no
  simulations run!" that looks like it's about something else entirely. This
  bit me directly this session (added a comment quoting an error message
  verbatim, broke the netlist). The existing templates typeset their
  bibliographic citation with curly “ ” quotes specifically to dodge this —
  follow that convention in anything you write.
- **ngspice's `.noise` analysis needs `option sparse`, not `klu`** ("Noise
  simulation is not (yet) supported with 'option KLU'"), and **the
  designated noise-input source needs an explicit `ac <mag>` value**
  (`value="dc CACE\{vdd\} ac 1"`, not just a bare DC value) or ngspice aborts
  with "ac input not found" — even if you only read output-referred noise
  and don't care about the input-referred figure.
- **A CACE parameter group's `conditions:` block needs real `minimum`/
  `maximum`/`enumerate` entries to sweep anything.** Specifying only
  `typical:` for every condition legitimately produces exactly one
  simulation point, so Min/Typ/Max Value come out identical — not a bug,
  just no sweep defined. Decide up front, per group, whether you want a
  single nominal-corner check or an actual corner/temp sweep.
- **Verify CACE's own mechanism from its source rather than guess** when
  something about the yaml format is unclear — `cace/common/cace_write.py`
  (`markdown_summary`: the Limit columns are literal string interpolation,
  no math at all; only the Value columns call `spice_unit_unconvert`) and
  `cace/parameter/parameter.py` (`evaluate_result`) were both worth reading
  directly today; raw GitHub URLs work fine via `web_fetch`.

## 4. Reaching the `_sudelbuecher` worktree's notes

`sudelbuecher/description/`, `sudelbuecher/design_considerations/`, and the
chatlog referenced above all live in the **separate** `_sudelbuecher`
worktree (branch `sudel_buecher`, connected folder
`sg13cmos5l_cm_ip__single2diff2single_sudelbuecher`) — per `CLAUDE.md` §3,
never `git switch sudel_buecher` in this main worktree. `Read`/`Glob`/`Grep`
on that connected folder's path work completely normally.

**Plain `git` commands run from inside that worktree may not.** Discovered
this session: its `.git` file is a gitlink recording an absolute path
(`/home/cmaier/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/.git`)
that didn't resolve inside this session's sandbox (no `/home/cmaier` at all
in that mount namespace — confirmed by a permission-denied `mkdir`). If you
hit `fatal: not a git repository` there, this is why, and it's an
environment/mount quirk, not a repo problem — other sessions evidently *have*
had a working `/home/cmaier` and committed there directly (see the `oguey`/
`cace` branch tips). Workaround that reads/writes the worktree correctly
without touching any metadata:

```sh
export GIT_DIR=<main-repo-path>/.git/worktrees/chatlog_sg13cmos5l_cm_ip__single2diff2single
export GIT_WORK_TREE=<sudelbuecher-connected-folder-path>
git status   # etc.
```

One more wrinkle found via that workaround: a stale `index.lock` sits in that
worktree's git metadata (`.git/worktrees/chatlog_.../index.lock`), and this
sandbox's connected-folder bridge refuses to delete it (`rm`/`unlink` →
"Operation not permitted"; `lsattr` → "Operation not supported" — looks like
the FUSE bridge itself blocks the delete, not a real permission problem,
since ownership matches). `git status`/`git log` still work fine through it.
Whether `git add`/`git commit` do too was **not yet tested** when this file
was written — if you need to commit something in that worktree and hit
trouble, that lock is the likely reason, and removing it needs the user's
own terminal (or a session whose sandbox actually maps `/home/cmaier`), not
another attempt from in here.

**Concretely for this hand-off**: the chatlog and this file were written
with `Write` (which doesn't go through the sandbox's git-path issue at all),
so they exist on disk regardless. Whether they're committed on
`sudel_buecher` by the time you read this, check `git log --oneline -3` in
that worktree (via the workaround above if needed) rather than assume.

## 5. Background context, only relevant if the assembled chain ever needs characterizing

Not this task's direct concern, but came up in today's `OgueyAebischerBias`
deep-dive and may matter later if the top-level CACE deck ever needs to
characterize the bias generator feeding the rest of the chain: its PSRR
measures ~24 dB (well under a 50 dB target carried over from the sky130
precedent — the topology genuinely isn't designed for supply robustness, per
the user's own read), and its current mismatch spread is verified-real
(-76% to +148% across 200 Monte Carlo iterations, checked against
convergence logs, not an artifact) and unusually wide for the device sizing
as ported. Both trace back to `HANDOVER.md`'s original flag that this
macro's device sizes were never re-derived for sg13cmos5l. Not something to
fix from this branch — just don't be surprised if numbers coming out of that
macro look rough once something downstream depends on them.

## 6. Suggested first move

Read `README.md` + `submission.yaml` + the sudelbuecher description docs
(§1), form a concrete proposal for what a top-level CACE skeleton should
even characterize given how little of the circuit exists yet (probably: pin
connectivity/DC sanity checks on whatever *does* exist, plus placeholder
groups for gain/bandwidth/offset once the buffers land — HANDOVER.md §3 made
the same point about the six-group `dc`/`startup`/`ac-psrr`/`noise`/
`disable`/`mismatch` split being the wrong template for a signal-path
block), and check that proposal with the user before writing files — same
research-first order this project has used all along.
