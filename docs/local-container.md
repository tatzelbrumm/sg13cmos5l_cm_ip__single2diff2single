<!-- Moved verbatim from CLAUDE.md (blob 6201ab3, commit 1903407). Read only when the task needs it. -->

# Local container (IIC-OSIC-TOOLS) and worktrees — local use only

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
