# Sudelbuch — 2026-09-28 — verbatim chat log (Sonnet session: looked up the chatlog verbatim-log and README-index conventions, survived a mid-session device disconnect, then wrote both rules into the main `CLAUDE.md` so any future chat in this project picks them up automatically — "the log to log all logs")

- **Repo:** `sg13cmos5l_cm_ip__single2diff2single` (main worktree, linked computer,
  `~/EDA/sg13cmos5l_cm_ip__single2diff2single`) — read and write: edited `CLAUDE.md`
  §6 ("Where the record lives") — staged via `device_stage_files`, edited with `Edit`,
  committed back via `device_commit_files` — verified afterward by on-device `md5sum`
  against the container-side source (`f8ac5b45898c9a3e299be88ac985276a`, both sides).
  Otherwise read-only: `device_list_dir`, `device_bash` `cat`/`grep`/`sed`/`Read`.
- **Repo (write target for this file):** `sg13cmos5l_cm_ip__single2diff2single_sudelbuecher`
  (`_sudelbuecher` worktree) — this file, plus the `chatlog/README.md` index entry below.
- **Assistant:** Claude Sonnet 5 (Cowork), session `8092a469-edcc-5db6-924d-6f5c83ac024a`.
- **`ref/` and `pix/`:** no update needed — this session consulted no external source and
  produced no image.
- **Mid-session device disconnect:** between Turn 2 and Turn 3 the linked-computer bridge
  dropped (`device_bash` calls failed with "The device this session is bound to is not
  connected to the bridge," twice, including one retry per the tool's own guidance). No
  writes had happened yet at that point; the assistant stopped and reported status rather
  than continuing to guess. The user's Turn 3 also carries a harness-generated
  `<system-reminder>` ("Instruction files were re-read... Instructions no longer present:
  ...") from the reconnect — that is a system `attachment` record (`type: "instructions",
  reason: "session_start"`), not text the user typed, and is elided here as plumbing, same
  as a compaction marker or tool-list delta.
- **Every line below verified against this session's own raw transcript**
  (`/root/.claude/projects/-home-claude/8092a469-edcc-5db6-924d-6f5c83ac024a.jsonl`,
  extracted programmatically) before being written. Tool invocations are elided as
  bracketed italic summaries; every **User:**/**Assistant:** line is the real text,
  byte-for-byte as extracted.

---

## Turn 1

**User:**

> in the sudelbuecher/chatlog, what are the existing rules so far for unabridged, verbatim logs and the README.md summary?

**Assistant:**

*[Listed `sudelbuecher/` recursively (`device_list_dir`) to find `chatlog/`.  
Read `chatlog/README.md`, the `_sudelbuecher` worktree's own `CLAUDE.md`, and the main
worktree's `CLAUDE.md` (first 300 lines) via `device_bash cat`.  
Grepped `verbatim|unabridged|abridg` across `chatlog/README.md`, `chatlog/ref/README.md`,
`chatlog/pix/README.md`, and `2026-09-27_sonnet_chatlog_integrity_correction_and_
handover.md` — found the rule-bearing hits concentrated in the integrity file.  
Grepped that file for `README` mentions.  
Attempted a stray `Read` on a placeholder path (harmless tool error, no real file involved).  
Read that file's header (lines 1–40) and tail (lines 230–290, plus a line count) via `device_bash sed`/`wc`.  
Read `chatlog/ref/
README.md` and `chatlog/pix/README.md` in full.]*

Here's what's actually established as the current convention, drawn from `sudelbuecher/chatlog/README.md`, `ref/README.md`, `pix/README.md`, and the incident file `2026-09-27_sonnet_chatlog_integrity_correction_and_handover.md` (which is where most of the verbatim-log rules got hammered out the hard way).

## Verbatim / unabridged chat logs

**Core rule, stated by you directly and now binding:**
> "DO NOT REPEAT NOT LOG ABRIDGED CHAT LOGS, ESPECIALLY NOT WITHOUT BEING PROMPTED FOR A LOG."

Unpacked, that's two separate obligations:
1. **Never log unprompted.** A log entry only gets appended when you explicitly ask for one (the fabrication that triggered the whole incident was two paraphrased "turns" added *unprompted*).
2. **When logging, it's verbatim or nothing.** No paraphrasing, no third-person summarizing, no reconstruction "from memory" or from an earlier conversation summary.

**Working mechanics that follow from that, established in practice:**
- Every quoted `**User:**`/`**Assistant:**` line must be checked against the **raw session JSONL transcript** (`~/.claude/projects/.../*.jsonl`), line by line, before being written — not reconstructed from a prior summary or from context.
- Tool invocations are the one thing that *are* elided — as `*[bracketed italic summaries]*` — everything else is real text, verbatim.
- Turn labels are consistent per file (established as `**User:**` / `**Assistant:**`; a stray `**Claude:**` label was itself flagged as a fabrication marker).
- After writing/appending, verify the result — e.g. MD5-diff the container-side file against the device copy — rather than trusting the write tool's own success report.
- If a compaction or edit drops turns, the fix is to reconstruct the missing content from the raw transcript and correct it **in place**, with a dated note marking the correction (done for Turns 29–30 in the `toplevel_structure_and_chipalooza_magic_authoring` file).
- When a session is split into a new file at your request, the new file states exactly where it starts (e.g. "starts exactly where that summary stops") and is unabridged/verbatim from that point on; everything *before* the split point goes into a separate, explicitly **paraphrased** handover file instead (see `HANDOVER_xschem_makefile_lvs_and_chatlog_integrity.md`) — so paraphrase is allowed, just never inside a file that claims to be a verbatim log.
- Each file's own header states its scope/provenance (repo, worktree, session ID, what stretch it covers, and the verification method used) so a reader can check the claim without re-deriving it.

## `README.md` summary conventions

- **`chatlog/README.md`** — one entry per log file: `[filename](filename)` heading line + a one-sentence, third-person description of what that session covered. Updated whenever a file is added (new index entry) or a file's scope changes — and a `.bak` copy of the README is kept before editing it, same discipline as the logs themselves. A pure append to an existing file's *content* (not its scope) doesn't require touching the README entry.
- **`ref/README.md`** — explicit stated rule: **"index, do not copy"** — third-party sources are pointed to, never copied into the repo (SPDX/licensing reasons, since this is a Chipalooza submission). One reference file per session, named to match the transcript it supports.
- **`pix/README.md`** — one entry per image (or image pair), stating: what it shows, which chat-log file it belongs to, whether it's generated or hand-drawn, its source-of-truth build script, and any caveat about what the image does/doesn't prove (e.g. "DRC-clean" proves internal well-formedness, not fidelity to the real IHP cell). Explicitly *not* the place for design renders (those go in `render/img/` via `make render-gds`).

One thing worth flagging: `CLAUDE.md` §6 in the main worktree ("Where the record lives") predates this structure — it only mentions the single 2026-08-30 rename log and doesn't yet describe `chatlog/`, `ref/`, `pix/`, or the README-index convention. If you want, I can update that section to match what's actually in place now.

## Turn 2

**User:**

> Looking at the logs, I might have some formatting preferences ... some of your responses come across as wall of text. but let me take my time. For now, I'm just closing a chat, want it to produce a verbatim log at the end, and start a new chat. How can I point any chat in this project to read and follow the formatting conventions you just collected?

**Assistant:**

*[Located this session's own raw transcript on the container
(`/root/.claude/projects/-home-claude/8092a469-edcc-5db6-924d-6f5c83ac024a.jsonl`),
confirmed its record-type structure with a `python3` line-by-line dump, then extracted
and cross-checked the verbatim Turn-1 user message and final assistant text against it.  
Attempted `device_bash` to read the header of the two most recent chatlog files
(`2026-09-28_sonnet_slot_makefile_scaffold_and_klayout_lvs_debugging.md`,
`2026-09-28_sonnet_toplevel_verify_targets_and_check_boundary_gds_mismatch.md`) to
confirm the current header/turn convention before writing anything — the call failed:  
"The device this session is bound to is not connected to the bridge."  
Retried once, per the tool's own guidance; same failure.  
Stopped rather than keep retrying blind, since no file had been written yet.]*

I've hit a snag — the connection to your computer dropped mid-task. Let me flag this now rather than push further blind.

**Status so far:**
- I have this session's own raw JSONL transcript located (`/root/.claude/projects/-home-claude/8092a469-edcc-5db6-924d-6f5c83ac024a.jsonl`) and extracted the verbatim text for both turns of this chat, ready to write as a log entry.
- I have **not yet** written the log file, updated `chatlog/README.md`, or touched `CLAUDE.md` — the device connection dropped before I could get back to the file for the header-convention check, so nothing has been changed on disk.

**On your actual question — how to point any chat at these conventions:** the mechanism already exists and you just watched it work: this very turn opened with a full dump of both project `CLAUDE.md` files injected as "codebase and user instructions" — that's automatic, every session, no action needed from you per-chat.  
So the answer is simply: **write the conventions into `CLAUDE.md`**, and every future chat in this project gets them for free.  
The natural spot is §6 ("Where the record lives") in the main repo's `CLAUDE.md`, which I flagged last turn as already stale — it predates `chatlog/`, `ref/`, `pix/`, and the README-index convention entirely.

I'll hold off writing anything until your computer reconnects — I don't want to guess at the current file header convention and write something inconsistent with your existing logs. Want me to retry now, or say when you're back?

## Turn 3

**User:**

> ok computer is back ... lately, it has a habit of just freezing and crashing every now and then — so fast that no logs are left.
> This here chat is something of a meta-log "the log to log all logs" or some such.

**Assistant:**

*[Confirmed the device bridge was reachable again (`device_bash echo ok` + `ls "$HOME/
mnt/"`).  
Read the exact header/metadata/turn/footer convention from the two most recent
chatlog files in full (`...slot_makefile_scaffold_and_klayout_lvs_debugging.md`,
`...toplevel_verify_targets_and_check_boundary_gds_mismatch.md`) before writing
anything.  
Confirmed this is still the same session — same JSONL transcript file, now
grown to 166 lines — and extracted the full Turn-2/Turn-3 span programmatically,
including tracking down the harness's own "Instructions no longer present" notice as an
`attachment`-type `instructions` record (`reason: "session_start"`), confirming it was
never stored as user-authored text.  
Re-fetched `chatlog/README.md` and the main
`CLAUDE.md` fresh from the device to rule out any change during the disconnect (both
byte-identical to what had already been read this session).  
Staged the main `CLAUDE.md`
(`device_stage_files`), rewrote §6 ("Where the record lives") with `Edit` to reflect the
current `chatlog/`+`ref/`+`pix/`+README-index structure and to state the
verbatim-logging rule directly, with a pointer to this session's own referenced incident
file for the fuller mechanics rather than duplicating it, and committed it back to the
device via `device_commit_files` — verified by `md5sum` match between the container-side
edit and the device copy.  
Assembled this file from the full three-turn extraction, wrote
it to `/mnt/user-data/outputs/` in the cloud container, transferred it to
`sudelbuecher/chatlog/` via `device_commit_files`, updated `chatlog/README.md`'s index
the same way (`.bak` kept first), and verified both writes landed correctly on the
device via checksum rather than trusting the transfer tool's own success report.]*

Done — three things:

1. **`CLAUDE.md`** (main worktree, §6): rewritten to reflect the current `chatlog/`+`ref/`+`pix/`+README-index structure, plus the binding rule itself (verbatim-only, only when prompted, checked against the raw JSONL, tool calls elided, checksum-verified) — with a pointer to the incident file for full mechanics instead of duplicating it. That's the actual answer to "how do I point any chat at this": `CLAUDE.md` loads into every session in this project automatically — you watched it happen at the top of this very chat. Written and checksum-verified on the device; not committed to git, per the read-only-git rule — that's yours whenever you want it.
2. **This session's own verbatim log** — all three turns, including the disconnect — written to `sudelbuecher/chatlog/2026-09-28_sonnet_chatlog_convention_lookup_and_claude_md_pointer.md`, checksum-verified on the device.
3. **`chatlog/README.md`** — new index entry added, `.bak` kept.

Fitting: this chat is now filed as one of the logs whose own rules it went and looked up.

Everything's written and verified — go ahead and close it out.
