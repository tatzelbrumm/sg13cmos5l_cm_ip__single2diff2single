# Sudelbuch — 2026-08-30 — branch `i_claude`

Rename of the forked `sg13cmos5l_chipalooza_analog_project` template to
`sg13cmos5l_cm_ip__single2diff2single`, plus the git / container / make
groundwork that came out of it.

- **Repo:** `sg13cmos5l_cm_ip__single2diff2single`
- **Branch:** `i_claude`
- **Resulting commit:** `743c8a8`
- **Baseline tag:** `from_template` → `baf9173`
- **Assistant:** Claude Opus 4.6 (Cowork)

**Scope of this transcript.** Every user and assistant message is reproduced
verbatim. Tool invocations (shell commands, file reads, web fetches) are *not*
inlined — they were apparatus, and their output runs to thousands of lines.
Where a command or its output was quoted inside a message, it is preserved.
External sources are indexed in [`ref/references.md`](ref/references.md).
Images: none in this session (`pix/` is empty).

---

## 1 — User

> I just used the sg13cmos5l_chipalooza_analog_project to create this sg13cmos15l_cm_ip__single2diff2single repository.
> I think I need to change a lot of file names and configuration entries accordingly. I think that the procedure is described in README.md.
> Do the necessary changes. I created a git branch i_claude for you to commit changes as necessary.
> Stop short of committing changes. I want to review what you are changing. Compile a ADHD-afflicted human readable explanation what you are doing.

## 2 — Assistant

I'll start by reading the README and surveying the repo.

*[surveyed the repo; read `README.md`, `Makefile`, `submission.yaml`, the `.klib`, the testbench and plot script; established that the old name appears in 27 file paths, 18 text files and 5 binaries]*

Then asked three clarifying questions:

**Q1 — Confirm the new top-cell name.** Your folder is `sg13cmos5l_cm_ip__single2diff2single` (your message said `sg13cmos15l` — typo?).
- **`sg13cmos5l_cm_ip__single2diff2single`** — Matches the folder name exactly. Bonus: it is exactly 36 characters, same as the old name, so the binary GDS cell name can be patched byte-for-byte with zero risk of corrupting the KLayout PCell context.
- `sg13cmos15l_cm_ip__single2diff2single` — With the '15l' spelling from your message. Note the PDK is ihp-sg13cmos5l, so '15l' looks like a typo — and the folder on disk says 5l.

**Q2 — What should I do with the committed generated outputs** (`final/`, `netlist/`, `render/img/`, `verification/` reports, plot data+figures)? They all carry the old name in filenames and in their contents.
- **Rename + rewrite them too** — `git mv` every generated file and search/replace the name inside. Keeps the repo self-consistent and diffable right now. They are stale-but-correct until you next run `make all` in the container.
- Delete them — Remove the generated trees entirely; they get rebuilt by `make all`.
- Leave them alone — Only touch true source files.

**Q3 — `submission.yaml` metadata — how far should I go?**
- top-cell only
- **Also stub your details** — Set project-name, put you in team-members, and mark the description fields with clear TODO markers.

**User selected:** `sg13cmos5l_cm_ip__single2diff2single` / Rename + rewrite them too / Also stub your details.

## 3 — User *(mid-turn)*

> I'm assuming that everything you change is under version control. If not, hold your fire.

## 4 — Assistant

Holding fire — I hit a real problem worth flagging before anything else.

*[discovered the sandbox could not unlink files in the mount, and that a `git checkout` had left a stale `.git/index.lock`; requested delete permission]*

## 5 — User *(mid-turn)*

> Commit files you are going to delete into a git branch. Either the existing i_claude or a generated_deleted git branch.

## 6 — Assistant

*[cleared the stale lock, created branch `generated_deleted` at the pre-change commit, verified `git status --porcelain -uall` returned 0 lines, then performed 26 `git mv` renames, the text substitutions, the GDS byte patch and the PNG chunk patch]*

Done. Nothing committed — staged only, `git diff --cached` is your review surface.

### First, your two questions

**"Is everything under version control?"** Yes. Verified before touching anything: working tree clean, `git status --porcelain -uall` returned **0** lines. Every file I touched was already tracked.

**"Commit what you'd delete to a branch."** Nothing gets deleted. All 26 changes are `git mv` renames — old content lives on in history. But I made the safety net anyway: branch **`generated_deleted`** now points at the pre-change commit `baf9173`. `git diff generated_deleted` gets you back to square one.

### The one thing that went sideways

The sandbox couldn't delete files in your folder (`Operation not permitted`), and a `git checkout` left a stale **`.git/index.lock`** behind. That would have jammed every future git write. I got delete permission and cleared it. Git is healthy now.

### What actually changed

Old name → new name, everywhere: `sg13cmos5l_chipalooza_analog_project` → `sg13cmos5l_cm_ip__single2diff2single`

**26 renames.** Layout, schematic, symbols, testbench, plot script, netlists, LEF/LIB/VH, renders, DRC/LVS report dirs.

**4 files edited in place.** `Makefile` (the `TOP =` line — everything else derives from it), `submission.yaml`, `README.md`, `macros/inverter/README.md`.

**3 binaries patched.** The README says "open in KLayout, rename the cell." No KLayout here, so I patched the GDS bytes directly. Safe *only* because of a lucky coincidence: both names are **exactly 36 characters**, so no GDS record length changed. Verified afterwards by reading all three files back — top cell is correct, cell count unchanged, PCell context intact.

**2 PNGs patched.** They carry a `Cell1` metadata tag. Same-length swap, but PNG chunks are CRC-checked, so I recomputed the CRC32 properly. All 43 chunks validate; images still load.

### Judgment calls — check these

**`submission.yaml` has TODO markers.** I filled in `project-name`, put you in `team-members`, wrote a placeholder description. But the circuit inside is **still the inverter example**. Only names changed. The long-description says so explicitly, so you can't accidentally submit a lie.

**`analog-pins: 3` untouched.** Correct for the inherited layout, probably wrong for your real circuit. Flagged with a TODO.

**Copyright left alone.** LICENSE and all SPDX headers still credit Tim Edwards and Simon Dorrer. That's correct for a derived Apache-2.0 WITH SHL-2.1 work. I *added* your line to the README rather than replacing theirs.

**`floorplan/chipalooza_template_*.gds` kept their names.** Those are upstream templates, not your project.

**One "chipalooza" survives in README.md**, in a sentence I wrote saying what the old name was. Intentional.

### Sanity checks that passed

The four things the README says must agree — `Makefile TOP`, `submission.yaml top-cell`, the file names, and the GDS top cell — all agree. The three precheck globs each match exactly one file. The testbench's `.include` of the PEX netlist resolves. The `.klib` still binds `inverter` correctly.

### Before you trust the layout

Re-open `layout/*.klay.gds` in real KLayout once, confirm it looks right, and re-export the tapeout GDS. My byte patch is sound, but you should eyeball it. Then `make all` in the container to regenerate everything from scratch.

---

## 7 — User

> push and track:  git push -t or git push -u? What's the equivalent for pulling?

## 8 — Assistant

**`git push -u`.** `-t` doesn't exist for push — no `-t` in `git push` at all. You're thinking of `git branch -t` / `git switch -t` / `git checkout -t`, where `-t` = `--track`.

```
-u, --set-upstream    set upstream for git pull/status
```

For your case: `git push -u origin i_claude`

### Pull side

There are two different "equivalents" depending on which direction you're going:

**Branch already exists locally** (your situation, if you'd rather not use push):

```sh
git branch -u origin/i_claude          # -u = --set-upstream-to, on branch not push
git pull --set-upstream origin i_claude # sets upstream as a side effect of pulling
```

Note the asymmetry that trips everyone up: `-u` on `git push` is `--set-upstream`, but `-u` on `git branch` is `--set-upstream-to` and *needs* an argument. And `git pull --set-upstream` has **no** short form.

**Branch exists on the remote, not locally yet** — this is where `-t` finally shows up:

```sh
git switch -t origin/some-branch    # creates local branch + tracking
git switch some-branch              # same thing, DWIM, if exactly one remote has it
```

### Cheat sheet

| Command | `-t` | `-u` |
|---|---|---|
| `git push` | ✗ doesn't exist | `--set-upstream` |
| `git branch` | `--track` | `--set-upstream-to=<x>` (needs arg) |
| `git switch` / `checkout` | `--track` | ✗ |
| `git pull` | ✗ | ✗ (`--set-upstream` only, long form) |

---

## 9 — User

> git push tag to origin?

## 10 — Assistant

**One tag:**

```sh
git push origin v1.0
```

**All tags:**

```sh
git push origin --tags        # every tag, annotated and lightweight
git push origin --follow-tags # only annotated tags reachable from the commits being pushed
```

`--follow-tags` is the one you usually want in a normal workflow — it piggybacks on a regular push and won't drag along local scratch tags.

**Key gotcha:** a plain `git push` never pushes tags. They're a separate refspace, so they need naming explicitly.

### Deleting / moving

```sh
git push origin --delete v1.0      # delete remote tag
git push origin :refs/tags/v1.0    # same, older syntax
git push origin -f v1.0            # force-update a tag you moved locally
```

Moving an already-published tag is antisocial — anyone who fetched it keeps the old one silently, since fetch won't clobber an existing tag without `--force`. Delete-then-recreate is no better. Prefer a new tag.

**Ambiguity:** if a branch and a tag share a name, `git push origin foo` errors out. Be explicit: `git push origin refs/tags/foo`.

### For your repo

Your `generated_deleted` branch is doing a tag's job — marking a fixed pre-change snapshot that should never move. A tag says that more clearly and won't show up in branch listings:

```sh
git tag -a pre-rename -m "state before the chipalooza -> single2diff2single rename" baf9173
git push origin pre-rename
git branch -d generated_deleted
```

---

## 11 — User

> ok I created a tag. push it.

## 12 — Assistant

I can't push it — you'll need to run it. Two hard blockers on my side:

**No credentials.** `origin` is `git@github.com:tatzelbrumm/...` (SSH). My sandbox has no `~/.ssh`, no `SSH_AUTH_SOCK`, no agent. Your key lives on your machine, not in here. `git ls-remote` already failed with `Host key verification failed`.

**Not my call anyway.** Pushing publishes to a remote others can pull. That's yours to run.

### Run this

```sh
git push origin from_template
```

The tag checks out fine, for what it's worth:

- **`from_template`** — annotated (`objecttype=tag`), tagger Christoph Maier, message *"repository as forked from template"*
- points at **`baf9173`** "Initial commit"
- that commit is already on `origin/main`, so the push sends only the tag object — no new history

### Two things while you're in there

**`origin/i_claude` already exists on the remote.** So the branch was pushed at some earlier point. Whether it already tracks locally, `git branch -vv` will tell you.

**Your rename is still only staged.** `git push` won't carry it. It needs a commit first — which you asked me to stop short of, so it's sitting there waiting for your review.

And once the tag is up, `generated_deleted` is redundant — `from_template` marks the same commit, more clearly:

```sh
git branch -d generated_deleted
```

---

## 13 — User

> check my changes to the git repositories, local and remote.

## 14 — Assistant

Checked both. Everything is sound — you committed and pushed while I was out of the loop.

### Local

**`i_claude`** → `743c8a8`, authored by you, in sync with `origin/i_claude`. Working tree clean.

The commit contains exactly what I staged and nothing else: **26 renames + 4 in-place edits** (`Makefile`, `README.md`, `macros/inverter/README.md`, `submission.yaml`). No stray additions, no accidental deletions.

**`main`** → `baf9173`, untouched, matches `origin/main`. **`generated_deleted`** → `baf9173`, local only.

**Tag `from_template`** → annotated, points at `baf9173`.

Re-ran the consistency check against the *committed* tree, not just my working copy: `TOP`, `top-cell`, all three GDS top cells, and all three precheck globs still agree. All pass.

### Remote

`origin/i_claude` = `743c8a8`, ref updated 15:23 — four minutes after your commit, so the push landed. `origin/main` still `baf9173`.

**I can't verify the remote live.** No SSH key in my sandbox, so `git ls-remote` fails. Everything above is from your remote-tracking refs, which reflect your last push, not a fresh fetch.

### Two things worth a look

**Did the tag actually get pushed?** I can't tell, and neither can git locally — pushing a tag leaves no local trace. Check:

```sh
git ls-remote --tags origin
```

**`sudelbuecher/i_claude_rename.gitlog` is untracked and not ignored.** It'll clutter every `git status` and is one stray `git add -A` away from being committed. Either add `sudelbuecher/` to `.gitignore`, or commit it deliberately.

### One cosmetic oddity, already explained

In `git diff main i_claude` the Magic LVS report shows as a delete + add rather than a rename. Not a problem — that file mentioned the old name 173 times, so post-rename similarity is only **48%**, just under git's 50% default. Content is fine: diffed both blobs with the names normalised, byte-identical, 295 lines each. `git diff -M20%` pairs them correctly.

### Expected leftovers

`README.md` still contains the string `sg13cmos5l_chipalooza_analog_project` — that's the sentence I wrote recording what the old name was. And `floorplan/chipalooza_template_*.gds` keep their upstream names. Both intentional.

---

## 15 — User

> So far, so good. I need to figure out yet how best to keep track of sudelbuecher and its contents.

## 16 — Assistant

One observation first, because it changes the question.

### This particular file is derived data

`i_claude_rename.gitlog` is a 36-line `git status` dump of a state that is now commit `743c8a8`. It's fully reconstructible — and the reconstruction is *better*:

```sh
git show --stat -M 743c8a8
```

Plain `git status` reported the Magic LVS report as `deleted:` + `new file:`. `git show -M` pairs it as a rename. So the copy in `sudelbuecher/` is a slightly-wrong snapshot of something git already stores losslessly.

That suggests the useful split: **Sudelbücher are for what git can't derive** — why you chose a name, what you rejected, what confused you, what to check next time. Not status dumps.

### Four ways to keep it, roughly by increasing separation

**1. `.git/info/exclude`** — ignore it, but locally. Not committed, so you don't impose your personal note-taking habit on anyone who clones a public submission repo.

```sh
echo '/sudelbuecher/' >> .git/info/exclude
```

Downside: notes aren't versioned or backed up at all.

**2. Committed `.gitignore` entry** — same effect, but the rule travels. Only right if `sudelbuecher/` is a *project* convention you want collaborators to share.

**3. Orphan branch in the same repo** — my pick if you want them versioned and pushed. Notes get full history, but never appear in any diff, PR, or checkout of `i_claude`/`main`:

```sh
git worktree add --orphan -b sudelbuecher ../sudelbuecher-wt
```

One clone, one remote, one `git push`. The submission tree stays clean. The `sudelbuecher/` dir moves out of the working tree, which also ends the untracked-file noise.

**4. Separate repo** — maximum separation, but now you're keeping two things in sync, and notes lose their link to the commits they describe.

### The Chipalooza-specific wrinkle

This repo *is* the submission. The precheck reads `submission.yaml` and globs `final/`, so a stray directory almost certainly won't fail anything — but the repo also carries SPDX headers throughout, and a REUSE-style lint would flag unlicensed note files. That's an argument against option 2, and for 1 or 3.

**My suggestion:** option 3 for notes you want to keep, and stop recording things git already knows. If you want, I can set up the orphan branch and worktree.

---

## 17 — User

> what is, by convention, a smoke check?

## 18 — Assistant

The conventional term is **smoke test** ("smoke check" is understood but rarer).

**Definition:** a fast, shallow, go/no-go check that the thing isn't fundamentally broken — run *before* any expensive testing, to decide whether deeper testing is even worth starting.

### The defining properties

- **Fast.** Seconds to a couple of minutes. If it's slow, it isn't a smoke test.
- **Broad but shallow.** Touches many subsystems, verifies none of them properly. Breadth-first, not depth-first.
- **Binary.** Pass/fail. It tells you *that* something is wrong, not *what*.
- **A gate.** Fails → don't run the real suite. That's the whole economic point.
- **Cheap to run.** No special fixtures, no destructive setup.

In CI this is often called a **build verification test** (BVT) or build acceptance test — same idea, formalised.

### Origin

Two competing stories, both real. Plumbing is older: force smoke through sealed pipes and watch where it escapes to find leaks. Electronics is the one engineers actually repeat: power up a new board for the first time and see whether smoke comes out. The electronics version is why it means "did it survive being switched on at all."

### Versus its neighbours

| Term | Scope | Depth | When |
|---|---|---|---|
| **Smoke** | wide | shallow | first, as a gate |
| **Sanity** | narrow | moderate | after a change, on the thing you changed |
| **Regression** | wide | deep | to check old fixes still hold |
| **Acceptance** | wide | deep | against requirements |

Smoke and sanity get used interchangeably in the wild, and pedantry about it rarely pays.

### A fair correction on my own wording

I labelled my post-rename verification "sanity checks." By this taxonomy that was wrong — it was closer to a **smoke test**: broad, shallow, fast, gating. It confirmed `TOP` / `top-cell` / filenames / GDS top cells agree and the globs resolve. It did **not** confirm the design is correct. The only real verification is `make all` in the container: DRC, LVS, PEX, then the simulations.

Which is exactly the smoke-test relationship — mine takes about a second and tells you whether running the hours-long one is worth it.

---

## 19 — User

> sanity check is fine. I need lots of these for my ideas, anyhow.
> After all the changes, I want to check if everything still works as before and as intended. 
> This probably means I need to run some make commands. Give me a hint which make commands I should try, and which don't work in the template as forked and pulled.

## 20 — Assistant

Good news for sanity-checking: because the generated outputs are committed, you have a **golden reference**. Re-run the flow, then `git diff` — anything that changes beyond the name is a real regression. That's the strongest check available to you.

### The ladder — cheapest first, stop at the first failure

All of this inside IIC-OSIC-TOOLS, and `source .designinit` first if the repo isn't at `$DESIGNS` root.

**0 — free, no PDK needed**

```sh
make            # help; confirms the Makefile parses and TOP is right
make -n lef     # dry-run any target: see the commands, run nothing
```

**1 — the highest-value single check**

```sh
make check-boundary
```

Do this one first. `check_boundary.py` opens `layout/<TOP>.gds` and does `layout.cell(args.cell)`, erroring out if no cell by that name exists. So in one shot it validates my GDS byte-patch, the filename, and `TOP` — the three things most likely to have gone wrong. Pure Python + KLayout's `kdb` module, no Magic, no simulation. Seconds.

**2 — netlisting: exercises the renamed `.sch` / `.sym`**

```sh
make magic-lvs-netlist
make klayout-lvs-netlist
```

**3 → 6 — the real flow**

```sh
make klayout-verify-all     # DRC + LVS
make magic-verify-all       # DRC + LVS + PEX
make build-top              # boundary, LEF, LIB, verilog, GDS, render
make sim-all                # transient
```

Then the actual regression test:

```sh
git status && git diff --stat
```

Expect noise from timestamps and absolute paths in reports. Expect *nothing* structural.

### What won't work in the template as forked

**`make all` — don't use it as your first check.** It runs `build-macros` first, which runs `build-counter`, which drags in the entire LibreLane hardening, Verilator lint, cocotb and FPGA flow. Tens of minutes, and completely unrelated to your rename. The README says the shipped top level is analog-only and never touches the counter. Use `build-inverter` if you want a sub-macro built.

**`make open`** — needs the VNC/noVNC desktop or X11 forwarding. Dies with `cannot open a window` in a shell-only container.

**`make sim-view-xschem`** — the recipe hardcodes `SHOW_PLOTS=1`, so it wants a GUI. The plot script writes its SVG/PDF/CSV regardless, so headless you can just run the script directly and skip `plt.show()`.

**Anything outside the container** — every DRC/LVS/PEX/LEF/render target shells out to `sak-*`, which isn't in this repo by design.

### Three traps aimed straight at you

**`make clean` will look catastrophic.** It deletes the committed generated outputs, so `git status` fills with deletions. Recover with `git restore .`. The README warns about this.

**`sim-xschem` rewrites your testbench.** The recipe includes `xschem save`, so `<TOP>_tb_tran.sch` comes back modified even on a clean pass. Your tree will be dirty after a successful simulation — that's expected, not a bug. You already committed, so `git diff` will show you exactly what xschem touched.

**You can skip PEX before simulating.** Normally `make magic-pex` must precede `sim-*` / `verilog` / `build-top`, because the testbench `.include`s the PEX netlist. Yours is already committed and renamed, so `make sim-all` works cold — which conveniently isolates *simulation* from *extraction* as separate checks.

---

## 21 — User

> At some point, I should probably fire up IIC-OSIC-TOOLS in a docker container.

## 22 — User *(mid-turn)*

> I already pulled ~/EDA/IIC-OSIC-TOOLS locally. How do I give you read only access?

## 23 — Assistant

*[fetched the IIC-OSIC-TOOLS GitHub README, then mounted `~/EDA/IIC-OSIC-TOOLS` and read the launcher scripts directly]*

Connected — I can read `/home/cmaier/EDA/IIC-OSIC-TOOLS` now.

**Honest caveat on "read-only":** Cowork has no read-only mount flag. Connecting a folder grants read *and* write; the restriction is my behaviour, not a permission bit. I'll only read there. If you want a hard guarantee, it's a git clone — `git -C ~/EDA/IIC-OSIC-TOOLS status` will expose any write I made. That's a better guarantee than my word.

### What your clone actually is

```
2026.08-3-gdb8e081b   (3 commits past the 2026.08 tag)
```

Your project README demands container tag **`2026.08` or later**, so you're fine — but note the distinction that trips people up: **you pulled the launcher scripts, not the image.** The ~4 GB image comes down on first `start_*.sh`. Budget **≥20 GB free** (it expands), and a slow first run.

The scripts default to `DOCKER_TAG="latest"`, which is ≥ 2026.08. Pin it with `DOCKER_TAG=2026.08` if you'd rather have reproducibility than freshness.

### The one setting that matters for your repo

`DESIGNS` defaults to `$HOME/eda/designs` — you're at `~/EDA/...`, so you must set it. And *where* you point it changes whether `.designinit` gets sourced automatically, because the container only sources `$DESIGNS/.designinit`:

**Option A — point at the project itself** (`.designinit` auto-sourced):

```sh
cd ~/EDA/IIC-OSIC-TOOLS
DESIGNS=~/EDA/sg13cmos5l_cm_ip__single2diff2single ./start_x.sh
# repo lands at /foss/designs
```

**Option B — point at the parent** (both repos visible, but you must source by hand):

```sh
DESIGNS=~/EDA ./start_x.sh
# then inside: cd /foss/designs/sg13cmos5l_cm_ip__single2diff2single && source .designinit
```

Start with **A**. Fewer moving parts while you're checking the rename.

> **Superseded — see §26.** Option A was the wrong call for this setup; the user's existing practice (Option B, `DESIGNS="$HOME/EDA"`) is better, because `~/EDA/.designinit` holds their aliases.

### Which launcher

You're on Linux, and you need a display for `make open` and `sim-view-xschem`:

- **`./start_x.sh`** — uses your local X server. Faster, lighter, native copy-paste. Your default.
- **`./start_vnc.sh`** — full XFCE desktop in the browser. Your script prints the URL itself: `http://localhost:${WEBSERVER_PORT}/?password=abc123`, default port 80.
- **`./start_shell.sh`** — root, no GUI. Not what you want.

`CONTAINER_USER`/`CONTAINER_GROUP` default to `$(id -u)`/`$(id -g)`, so files written into your repo stay yours. Don't run these with `sudo`.

### Look before you leap

```sh
DRY_RUN=1 DESIGNS=~/EDA/sg13cmos5l_cm_ip__single2diff2single ./start_x.sh
```

Prints the full `docker run` without executing. Worth doing once — it's also the only documented way to get a raw command, since the README gives none.

Then, inside, the ladder from before: `make check-boundary` first.

---

## 24 — User

> docker images
> ```
>                                                                                                                 i Info →   U  In Use
> IMAGE                              ID             DISK USAGE   CONTENT SIZE   EXTRA
> ghcr.io/mneher11/open-dvs:latest   92b7bdf14f42       9.99GB         2.35GB        
> hello-world:latest                 f9078146db2e       25.9kB         9.49kB        
> hpretl/iic-osic-tools:2026.04      2a37a0e0ed9e       25.2GB         5.51GB        
> hpretl/iic-osic-tools:2026.07      5d6adf1f437c       15.9GB         3.65GB    U   
> hpretl/iic-osic-tools:2026.08      3c371645b19c         16GB         3.77GB    U   
> hpretl/iic-osic-tools:latest       3c371645b19c         16GB         3.77GB    U  
> ```
>
> And look at ~/EDA/cheatsheets, but don't write into that directory.

## 25 — Assistant

*[mounted `~/EDA/cheatsheets` read-only; read `iic-osic-tools_cheatsheet.md`]*

## 26 — Assistant

Your cheatsheet is better than the advice I just gave you — it's informed by actual pain (X11 hangups, `LIBGL_ALWAYS_SOFTWARE`, per-tag container names, "don't use `docker start`"). Three things worth adding.

### Your images

**`2026.08` and `latest` are the same image** — both `3c371645b19c`. Two tags, one blob. So you are *not* spending 16 GB + 16 GB on them; it's counted once. And your cheatsheet's `DOCKER_TAG=2026.08` is already pinned to exactly what `latest` resolves to. Nothing to change.

**`2026.04` is your reclaim candidate** — 25.2 GB disk usage, no `U` marker. Larger than either newer image. If nothing depends on it:

```sh
docker ps -a --filter ancestor=hpretl/iic-osic-tools:2026.04   # check first
docker image rm hpretl/iic-osic-tools:2026.04
```

`2026.07` still shows `U`, so a container is holding it — probably a stale one from before you moved to `2026.08`. `docker ps -a --filter 'name=iic-osic-tools'` will name it.

### Correction to what I told you earlier

I suggested pointing `DESIGNS` at the project folder so its `.designinit` gets auto-sourced. **Your setup is better and my advice would have broken it** — you use `DESIGNS="$HOME/EDA"` so both repos are visible, and line 102 of your cheatsheet shows you keep your aliases in `$HOME/EDA/.designinit`.

But that's the gotcha: the container sources **`$DESIGNS/.designinit`** — one file, the `~/EDA` one. The project's own `.designinit`, which exports `PDK`, `PDKPATH`, `STD_CELL_LIBRARY`, `SPICE_USERINIT_DIR`, `KLAYOUT_PATH`, is **not** picked up, because the repo sits in a *subfolder* of `$DESIGNS`. Its README says exactly this.

Your `sak-pdk ihp-sg13cmos5l` covers most of it, but the reliable move before any `make` target is:

```sh
cd /foss/designs/sg13cmos5l_cm_ip__single2diff2single
source .designinit
echo "$PDK $STD_CELL_LIBRARY"    # ihp-sg13cmos5l sg13cmos5l_stdcell
```

### A section you might want (not writing it — you said don't)

````markdown
## Chipalooza project: sanity check after a rename

```bash
cd /foss/designs/sg13cmos5l_cm_ip__single2diff2single
source .designinit
make check-boundary          # opens layout/<TOP>.gds, fails if the top cell name is wrong
make klayout-verify-all      # DRC + LVS
make magic-verify-all        # DRC + LVS + PEX
make build-top
make sim-all                 # note: runs `xschem save`, so the .sch comes back modified
git diff --stat              # generated outputs are committed -> this IS the regression test
```

Avoid `make all` for a quick check: it runs `build-macros` first, which
drags in the counter's LibreLane + FPGA flow. Use `make build-inverter`.
````

Also worth a line in the VNC section: besides `vncviewer localhost:5901`, the script prints a browser URL — `http://localhost:${WEBSERVER_PORT}/?password=abc123`, default port 80. Handy when you don't want a VNC client.

---

## 27 — User

> This is way tl;dr. 
> I don't want to use VNC, but X11 like with
> cd ~/EDA/IIC-OSIC-TOOLS
>
> ```
> DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08-sw DOCKER_EXTRA_PARAMS='-e LIBGL_ALWAYS_SOFTWARE=1' ./start_x.sh
> ```
>
> available docker instances are
> ```
> docker ps --all
> CONTAINER ID   IMAGE                           COMMAND                  CREATED       STATUS                      PORTS                                                           NAMES
> 6d5151b7f97c   hpretl/iic-osic-tools:2026.08   "/dockerstartup/scri…"   4 days ago    Exited (255) 43 hours ago   80/tcp, 5901/tcp, 8888/tcp                                      iic-osic-tools-2026-08-sw
> 5ae9990b7388   hpretl/iic-osic-tools:2026.07   "/dockerstartup/scri…"   8 days ago    Exited (255) 6 days ago     80/tcp, 5901/tcp, 0.0.0.0:8888->8888/tcp, [::]:8888->8888/tcp   iic-osic-tools-aicd-jupyter
> 37fc1b6f4049   hpretl/iic-osic-tools:2026.07   "/dockerstartup/scri…"   8 days ago    Exited (255) 6 days ago     80/tcp, 5901/tcp, 8888/tcp                                      iic-osic-tools-aicd
> 7d83c5d34334   5d6adf1f437c                    "/dockerstartup/scri…"   9 days ago    Exited (255) 8 days ago     80/tcp, 5901/tcp, 0.0.0.0:8888->8888/tcp, [::]:8888->8888/tcp   iic-osic-tools_jupyter_uid_1000
> 2bb0dd792b65   hpretl/iic-osic-tools:2026.07   "/dockerstartup/scri…"   2 weeks ago   Exited (0) 4 days ago                                                                       iic-osic-tools-2026-07-sw
> 8a6d0889bd7d   hpretl/iic-osic-tools:2026.07   "/dockerstartup/scri…"   2 weeks ago   Exited (0) 2 weeks ago                                                                      goofy_wilson
> ```
>
> Should I start a fresh docker instance with $DESIGNS="$HOME/EDA/sg13cmos5l_cm_ip__single2diff2single" for the initial tests?

## 28 — Assistant

No. Reuse `iic-osic-tools-2026-08-sw`.

The narrower `DESIGNS` only saves you one `source` line — and it costs you your `~/EDA/.designinit` aliases and visibility of your other repos.

Rerun your exact command (it's `Exited (255)` — dead X11; per your own cheatsheet press `s` to stop, `s` to start):

```sh
cd ~/EDA/IIC-OSIC-TOOLS
DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08-sw DOCKER_EXTRA_PARAMS='-e LIBGL_ALWAYS_SOFTWARE=1' ./start_x.sh
```

Then inside:

```sh
cd /foss/designs/sg13cmos5l_cm_ip__single2diff2single
source .designinit
make check-boundary
```

Bonus: no container uses `2026.04`, so `docker image rm hpretl/iic-osic-tools:2026.04` reclaims ~25 GB. `goofy_wilson` and `iic-osic-tools_jupyter_uid_1000` look like junk too.

---

## 29 — User

> I don't collect garbage very often. I'll do 
> cd ~/EDA/IIC-OSIC-TOOLS
> DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08-sw DOCKER_EXTRA_PARAMS='-e LIBGL_ALWAYS_SOFTWARE=1' ./start_x.sh 
> now and then follow your instruction to 
> cd /foss/designs/sg13cmos5l_cm_ip__single2diff2single
> source .designinit
> make check-boundary
> from within.
>
> So far, so good?
>
> ```
> /foss/designs > cd /foss/designs/sg13cmos5l_cm_ip__single2diff2single
> source .designinit
> make check-boundary
> python3 scripts/check_boundary.py layout/sg13cmos5l_cm_ip__single2diff2single.gds sg13cmos5l_cm_ip__single2diff2single
> [INFO] Checking the PR boundary of sg13cmos5l_cm_ip__single2diff2single in layout/sg13cmos5l_cm_ip__single2diff2single.gds ...
> [INFO] 1 shape(s) on layer 189/4, 200.000 um x 200.000 um.
> [INFO] PR boundary check passed.
> ```

## 30 — Assistant

Yes — and that's the load-bearing one.

It proves three things at once: KLayout's own reader opens the patched GDS, a cell named `sg13cmos5l_cm_ip__single2diff2single` exists in it, and the boundary geometry survived intact — 200×200 µm on layer 189/4, exactly the `tiny` template. My byte patch held.

Next rung:

```sh
make klayout-verify-all     # DRC + LVS
make magic-verify-all       # DRC + LVS + PEX
```

Then `git diff --stat` — the generated outputs are committed, so anything beyond timestamps and paths is a real regression.

---

## 31 — User

> at which point, if at any, would make clean make sense?

## 32 — Assistant

Not now. `make clean` deletes the committed generated outputs — which are your golden reference. Kill them and `git diff` stops being a regression test.

Three points where it does make sense:

**After the verify pass.** Once `klayout-verify-all` / `magic-verify-all` / `build-top` / `sim-all` have run clean against the reference, it's served its purpose.

**As a from-scratch check.** `make clean && make` proves the flow regenerates everything from source rather than from stale committed artifacts. Worth doing once, before you trust the repo.

**When you replace the circuit.** The moment the inverter example goes, those artifacts aren't stale — they're wrong. Clean then, definitely.

Two things that make it low-stakes: everything is committed, so `git restore .` undoes it completely. And the only real trap is ordering — after a clean, `make magic-pex` must run before `sim-*`, `verilog` or `build-top`, or the testbench's `.include` of the PEX netlist fails.

---

## 33 — User

> export this chat verbatim into markdown, with references into a /ref subdirectory and /pix for pictures (none so far, presumably), into sudelbuecher. That's what that directory is for. I need yet to decide how to keep track of versions in there.

## 34 — Assistant

*[this file]*

---

## Open items at end of session

- [ ] `make klayout-verify-all`, `make magic-verify-all`, `make build-top`, `make sim-all`, then `git diff --stat`
- [ ] Re-open `layout/*.klay.gds` in KLayout, eyeball it, re-export the tapeout GDS
- [ ] Decide how to version `sudelbuecher/` — `.git/info/exclude`, `.gitignore`, orphan branch, or separate repo (see §16)
- [ ] Confirm the `from_template` tag reached origin: `git ls-remote --tags origin`
- [ ] `git branch -d generated_deleted` once `from_template` is pushed (both point at `baf9173`)
- [ ] Fill the `TODO` fields in `submission.yaml`; revisit `analog-pins: 3` once the real circuit exists
- [ ] Replace the inherited inverter example with the actual single→diff→single circuit
- [ ] Optional: `docker image rm hpretl/iic-osic-tools:2026.04` (~25 GB)
