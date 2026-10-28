# Background agents of the 2026-10-27/28 IOPadDiff2Single session: briefs, messages, contexts

Each agent has a folder here with three files:
- `BRIEF.md`: the brief file it was pointed to (A2 also has `BRIEF_bg.md`, its part 2).
- `messages.md`: its launch prompt and every later message, verbatim, with times.
- `inputs.md`: the files it was given, with sha256.

**What an agent knows.** A background agent starts with no part of this conversation. Its whole context is:
- the launch prompt;
- the brief file(s);
- the files in its own read-only `inputs/` folder in the cloud workspace;
- the later messages listed in `messages.md`.

It works only in its cloud workspace: it cannot use the computer or git, and it doesn't change `inputs/`. Its results
come back to the session, which checks them before anything is written to the computer.

| agent | name in the task list | launched | asked for by Christoph | status (02:41) | results |
|---|---|---|---|---|---|
| A1 | Pad Metal2 rework (option B) | 00:50 | 00:41 "ok go" (the Metal2 option-B plan) | done 01:33; written 01:39 | `../m2_option_b_2026-10-28/` (report, build and check scripts); pad cell in `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/` |
| A2 | oa_core_pd layout from primitives | 01:34 | 01:30 "Tell an agent to create a layout from oa_core_pd.sch using the layout primitives, I think they're in IOPad layout."; 01:45 bg_core_pd next; 01:46 slot 7; 02:36 compactify | v1 done 02:23 (written 02:25); bg_core_pd part 2 started 02:24, stopped 02:37; since 02:38 the assembler of the compact oa_core_pd (waits for A3 / A4) | v1: `macros/oa_core_pd/layout/gds/oa_core_pd.gds`; report, scripts, logs in `design_considerations/pad_buffer_layout/oa_core_pd_2026-10-28/` |
| A3 | oa NMOS primitives compact | 02:39 | 02:36 (rotate oa_nmir / oa_misc_n / oa_mcs, one 10/1 array, no taps between rows, slim rings) and 02:37 "other agents may be more experienced rotating transistors within layout primitives." | running | to come |
| A4 | oa PMOS primitives compact | 02:39 | 02:36 (oa_misc_p compact, narrower dummies in oa_pmir) and 02:37 | running | to come |

Shared addendum: `SKILL_EXPORT.md` (02:50, sent to A2, A3 and A4). The user asked for transferable layout skills,
"not only in words, but very much in graphical (and musical) patterns". Each agent exports `out/skill/` in three forms:
- pattern notation in symbol / score form;
- pictures rendered from the GDS;
- a reusable generator;
plus `rules.md` with deck citations and a SKILL.md draft.

How A2, A3 and A4 depend on each other:
- A3 and A4 make the new primitives in parallel, each in its own workspace (`scratchpad/primN`, `scratchpad/primP`).
- A2 prepares the compact floorplan and the back-annotation of the sheet, then stops.
- The session resumes A2 with A3's and A4's cells, and A2 assembles them.
- bg_core_pd is on hold until oa_core_pd's lessons are in (02:36).

**What survives the session.** The agents themselves live only as long as this session's cloud container. An agent
from an earlier session can't be reached any more; the 2026-10-27 "sinks-style worker" and "cascode worker" are gone.
Their experience survives only as files:
- the log (`design_considerations/pad_buffer_layout/log.md`);
- the cells they drew;
- the briefs and reports kept here.

That's why each new agent's brief points at those log entries and cells.
