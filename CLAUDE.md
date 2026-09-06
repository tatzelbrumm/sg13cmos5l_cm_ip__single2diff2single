# CLAUDE.md — `_sudelbuecher` worktree

This directory is the `sudel_buecher` orphan-branch worktree of
`sg13cmos5l_cm_ip__single2diff2single` — chat logs, run logs, provenance. No
project files live here; this branch shares the same `.git` object store as
the main design worktree at `~/EDA/sg13cmos5l_cm_ip__single2diff2single`,
whose `CLAUDE.md` (section 6, "Where the record lives") documents what's
filed where in here.

**Agent git access here: read-only, and even that isn't safe — treat it as fully
off-limits.** The sandbox can create/overwrite but not `unlink`/`rename` files in this
worktree's git metadata, so even a bare `status`/`log` can leave an unremovable
`index.lock` (confirmed 2026-09-05, no `add`/`commit` involved). Fix is host-side only.
No git commands without asking first; if one locks, name the exact file and stop — don't
retry.
