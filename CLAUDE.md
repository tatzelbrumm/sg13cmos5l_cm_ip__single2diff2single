# CLAUDE.md — project context

Analog-on-top IC project for **Chipalooza 2026**, PDK **ihp-sg13cmos5l**, forked from
the *Chipalooza Analog Project* template (`from_template` tag → `baf9173`).

Target circuit: a **single-ended → differential → single-ended converter**.
As of this file, the repo still contains the *template's* example circuits; the
next task is replacing them.

---

## 1. Hard invariant: the top-cell name

All of these must read `sg13cmos5l_cm_ip__single2diff2single` and must agree:

| Where | What |
|---|---|
| `Makefile` | `TOP =` (line 7) — every target derives from it |
| `submission.yaml` | `top-cell:` — read by the Chipalooza precheck |
| `layout/`, `schematic/xschem/`, `testbenches/xschem/` | file names |
| **inside `layout/*.gds` and `layout/*.klay.gds`** | the **GDS cell name** |

The DRC/LVS/PEX targets pass the *file name* as the *cell name*. If they diverge,
tools fail confusingly or silently. `make check-boundary` is the cheapest validator:
it opens `layout/<TOP>.gds` and errors if no cell of that name exists.

Renaming the top cell inside a GDS normally needs KLayout. It was once done as a
byte patch because the old and new names were both exactly 36 characters; a
later real KLayout re-export proved the patch byte-exact.

---

## 2. Working environment

Everything runs inside the IIC-OSIC-TOOLS container (tag `2026.08` or later).
Host clone of the launcher scripts: `~/EDA/IIC-OSIC-TOOLS`.

```sh
cd ~/EDA/IIC-OSIC-TOOLS
DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08-sw \
  DOCKER_EXTRA_PARAMS='-e LIBGL_ALWAYS_SOFTWARE=1' ./start_x.sh
```

X11, not VNC. Restart by rerunning that same command (not `docker start`).
More recipes in `sudelbuecher/cheatsheets/iic-osic-tools_cheatsheet.md`.

**Inside the container, before any `make`:**

```sh
cd /foss/designs/sg13cmos5l_cm_ip__single2diff2single
source .designinit
```

Required because `DESIGNS="$HOME/EDA"` means the container auto-sources
`~/EDA/.designinit`, **not** this project's. Without it `PDK`, `PDKPATH`,
`STD_CELL_LIBRARY` and `KLAYOUT_PATH` are unset or wrong.

---

## 3. Repository layout — TWO worktrees

```
~/EDA/sg13cmos5l_cm_ip__single2diff2single             ← the design. main / project branches
~/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher ← notes. branch `sudel_buecher`
```

**Never `git switch sudel_buecher` in the main directory.** It is an orphan branch
containing no project files, so the switch empties the working tree of everything
tracked, `.gitignore` disappears, and ~2900 generated files suddenly show as
untracked. Work on notes in the `_sudelbuecher` directory instead.

Branches:

| Branch | Purpose |
|---|---|
| `main` | the renamed, fully verified template — the working base |
| `i_claude` | marker: renamed + verified, no design work yet |
| `counter_digital` | the counter digital-flow verification run |
| `inverter_pex` | inverter post-layout / CACE `-s pex` experiments |
| `sudel_buecher` | **orphan** — chat logs, run logs, provenance |

The branch is named `sudel_buecher` with an underscore deliberately: a branch named
`sudelbuecher` collides with the tracked directory `sudelbuecher/` and makes
`git log sudelbuecher` ambiguous.

---

## 4. Make targets

Top level and each macro (`macros/inverter`, `macros/counter`) have the same target
names. `make -C <dir> <target>` runs one from the repo root.

```sh
make                      # help
make check-boundary       # cheapest sanity check after any rename
make klayout-verify-all   # DRC + LVS
make magic-verify-all     # DRC + LVS + PEX
make build-top            # boundary, LEF, LIB, verilog stub, GDS, render
make sim-all              # transient
```

**Avoid `make all`** unless you mean it — it runs `build-macros`, which drags in the
counter's LibreLane + FPGA flow.

Generated outputs are **committed**, so re-running a target and then `git diff` is
the regression test. Tee everything:

```sh
make <target> > >(tee sudelbuecher/logs/<name>.out) 2> >(tee sudelbuecher/logs/<name>.err >&2)
```

---

## 5. Traps that have already cost hours

**Full-RC PEX is not reproducible.** Identical geometry, three runs: devices 90/90/90,
C 82/82/82, **R 574 / 833 / 376**. Magic's `extresist` reduction is threshold-driven and
unstable. Never read a PEX diff as a regression; judge by element counts. Use
`EXT_MODE=2` when you need a repeatable number. The digital flow *is* deterministic —
LibreLane reproduced a GDS bit-for-bit across machines.

**Mismatch Monte Carlo is vacuous on an extracted netlist.** `mm_ok=1` appears on the
schematic devices and on none of the extracted ones, and Magic splits `ng=20` into
twenty separate fingers. Symptom: min = typ = max in the CACE summary, which *looks*
like a pass. Run mismatch on `-s schematic`; process MC (`tt_stat`) survives extraction.

**CACE silently falls back to the schematic netlist** when `paths:` in the `.yaml` has
no `layout:` key — the default `-s best` tries extracted, fails to find a layout, and
says nothing. Always pass `-s` explicitly.

**`#` inside a `\`-continued make recipe is a *shell* comment** and eats the rest of the
`&&` chain → `Syntax error: end of file unexpected`. Comments are only safe at column 0
with no preceding backslash.

**KLayout: launch from the file's own directory** (`cd layout && klayout -e <file>`) —
that is what `sak-open.py` does, and the `.klib`'s relative `lib_path` depends on it.
Do **not** pass `-nn <techfile>` when `KLAYOUT_PATH` is set: it registers a duplicate
technology `<name>[1]` and the PDK machinery fails.

**`x2` / `x3` in every testbench are unwired spares.** To go post-layout, change `x1`'s
symbol to `<CELL>_pex.sym` at the same coordinates. Do not clear their `spice_ignore`.

**The template's `adm_db` is not a gain** — it divides absolute peaks including the DC
offset. Real small-signal gain is `vout_pp / vin_pp`.

**`sim-xschem` runs `xschem save`** and can leave the testbench `.sch` modified even on
a clean pass.

**Icarus cannot model IHP stdcell `ifnone` `specify` paths** (68 warnings). Gate-level
sim is functionally accurate, not timing-accurate. Timing comes from LibreLane STA.

**A cosmetic CACE error to ignore:** `Unable to open … sg13g2.lyp`. CACE hardcodes a
fallback filename for the sibling PDK; this one ships `sg13cmos5l.lyp`. It only breaks
the datasheet's layout thumbnail, after all numbers are computed.

**Agent git access here: read-only, and even that isn't safe — treat it as fully
off-limits.** The sandbox can't `unlink`/`rename` in a connected folder's `.git/`, and a
bare `status`/`log`, not just `add`/`commit`, can leave an unremovable `index.lock`
(confirmed 2026-09-05). No git commands without asking first; if one locks, name the
exact file and stop — don't retry.

---

## 6. Where the record lives

On the **`sudel_buecher`** branch, in the `_sudelbuecher` worktree:

- `sudelbuecher/chatlog/` — one file per session (or per split-off stretch of a
  long one), named `<date>_<model>_<topic>.md`. Indexed in
  `sudelbuecher/chatlog/README.md`: one `[file](file)` + one-sentence entry per
  log, kept current (`.bak` copy first) whenever a file is added or its scope
  changes — a pure content append doesn't need a new entry.
  - `sudelbuecher/chatlog/ref/` — pointers to external sources a session used,
    one file per session, named to match. Rule: **index, do not copy** — this
    is a Chipalooza submission with SPDX headers throughout, so no unlicensed
    copies of other people's docs. See `ref/README.md`.
  - `sudelbuecher/chatlog/pix/` — images belonging to a session's notes: what
    it shows, which log file it belongs to, generated-vs-hand-drawn, source
    script, and what it does/doesn't prove. Not for design renders — those are
    `render/img/`, via `make render-gds`. See `pix/README.md`.
- `sudelbuecher/logs/<branch>/` — tee'd `.out`/`.err` of every run, filed by the branch
  that produced it.
- `sudelbuecher/MANIFEST.tsv` — original mtimes, sizes, commands, originating commits.
  Git stores no mtimes, so this is the only record of when each run happened.
- `sudelbuecher/recovered/` — earlier chat-log versions.

**Chat-log rule:** never create or append to a `chatlog/*.md` file unless the
user explicitly asks for one — and when asked, it is **verbatim, never
paraphrased**. Check every quoted `**User:**`/`**Assistant:**` line against
this session's own raw transcript
(`~/.claude/projects/-home-claude/<session-id>.jsonl`) before writing it;
don't reconstruct from memory or an earlier summary. Tool calls are the one
thing that get elided, as `*[bracketed italic summaries]*`.
How to ask for and build such a log without tripping the `[reasoning_extraction]`
stop: `sudelbuecher/verbatim_chatlog_recovery/verbatim-chatlog-export.md`.

For the **`.md` file itself**, checksum it against the container-side source
after transferring — cheap, and it has caught a real `device_commit_files`
silent-no-op bug more than once. **Do not extend this to any attached image.**
A checksum comparison on an image is a dead end on this account: something in
the write path stamps a several-KB C2PA/Content-Credentials (JUMBF) manifest
into image files, so file-level hashes will never match no matter how many
times you retry — the picture is fine, only invisible provenance metadata
differs. If an image's own correctness needs checking, compare the payload
(PNG `IHDR`+`IDAT`+`IEND`, JPEG SOI…EOI minus `APPn` segments), not the whole
file — and only bother if there's an actual reason to doubt it arrived
correctly, not as a default step. This was learned the hard way — see
`sudelbuecher/chatlog/2026-09-27_sonnet_chatlog_integrity_correction_and_handover.md`
for the incident (an unprompted, paraphrased "turn" fabricated into a log) and
the fuller mechanics (in-place correction with a dated note if turns are ever
found missing, splitting a file at the user's request, etc.).

**Don't round-trip files that don't need it.** If a file already lives on the
user's computer and you don't need to change it, don't stage it into the cloud
and commit it back — that's a wasted transfer, and for an image it also means
paying the C2PA-stamp tax above for nothing. Stage a file in only when you
actually need to read it here; commit a file out only when it actually
changed. Don't push a cloud-generated image to the device by default either —
hand it over some other way, or say up front that a stamp will land if the
user specifically wants a copy placed in a folder.

**Building a log fast:** the real cost is never the transfer, it's
regenerating text. Appending to an existing log is an `Edit`/insert after the
last turn — never a full `Write` of the whole file, which forces you to
re-emit every past turn's text just to add one more. On a continuation,
extract only the transcript delta since the last export, not the whole
session, and don't re-derive the header/turn format by opening old log files
"to check the convention" — it's fully specified above; follow it directly.

---

## 7. State and next task

**Verified working, all on the current `main`:**

- rename complete and consistent
- tapeout GDS re-exported from `.klay.gds`, geometry verified unchanged
- Magic DRC clean, KLayout DRC clean, Magic+Netgen LVS "Circuits match uniquely"
- full-RC PEX, all ports connected
- top-level transient simulated
- inverter: three testbenches + CACE characterization
- counter: lint → Icarus → cocotb → LibreLane (all eight checkers clear) → PEX →
  gate-level cocotb → XSPICE co-simulation in Xschem

**Next: replace the template example modules with the real design.** The teardown
touches more than `macros/`:

- `macros/inverter/`, `macros/counter/`
- top `Makefile` — `build-inverter`, `build-counter`, `build-macros`, `clean-*`
- `schematic/xschem/xschemrc` — sources both macro `xschemrc` files
- `layout/<TOP>.klay.klib` — binds library `inverter` → `../macros/inverter/layout/inverter.gds`
- `schematic/xschem/<TOP>.sch` — 2 × `inverter.sym`
- `layout/<TOP>.klay.gds` — 2 × `inverter` placements, **needs KLayout**, then re-export
- `testbenches/xschem/<TOP>_tb_tran.sch` — DUT and stimulus
- `submission.yaml` (still has `TODO` fields, and `analog-pins: 3` is inherited)
- `README.md`

Re-run the full sign-off after any layout change; the committed outputs are the
reference to diff against.

**Also still open:** the mixed-signal path for the I/O-limited design will need digital
logic and level shifters. The mechanism is `generate-xspice` — LibreLane hardens the
block, `magic-pex` extracts it, and the XSPICE model drops into an Xschem testbench
beside the analog. Verified working with the counter.
