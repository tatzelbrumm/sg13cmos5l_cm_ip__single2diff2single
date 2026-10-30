<!-- Moved verbatim from CLAUDE.md (blob 6201ab3, commit 1903407). Read only when the task needs it. -->

# Record keeping: chat logs, run logs, provenance

## Tee every run (from section 4)

Generated outputs are **committed**, so re-running a target and then `git diff` is
the regression test. Tee everything:

```sh
make <target> > >(tee sudelbuecher/logs/<name>.out) 2> >(tee sudelbuecher/logs/<name>.err >&2)
```

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
