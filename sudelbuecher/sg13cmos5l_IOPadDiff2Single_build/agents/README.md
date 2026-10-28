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

| agent | name in the task list | launched | asked for by Christoph | status (06:32) | results |
|---|---|---|---|---|---|
| A1 | Pad Metal2 rework (option B) | 00:50 | 00:41 "ok go" (the Metal2 option-B plan) | done 01:33; written 01:39 | `../m2_option_b_2026-10-28/` (report, build and check scripts); pad cell in `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/` |
| A2 | oa_core_pd layout from primitives | 01:34 | 01:30 "Tell an agent to create a layout from oa_core_pd.sch using the layout primitives, I think they're in IOPad layout."; 01:45 bg_core_pd next; 01:46 slot 7; 02:36 compactify; 03:40 may modify A3's / A4's cells; 04:25 bg_core_pd, primitives first | v1 done 02:23; compact v2 done 04:09, in the macro 05:05; bg_core_pd (`BRIEF_bg2.md`: bg_pnp / bg_res and the assembly; its pin requests to A3 / A4 in `requests_for_A3_A4.md`) done 06:19, GDS in the macro 06:26, sheet backannotation pending | v2: `macros/oa_core_pd/layout/gds/oa_core_pd.gds` (2355 µm²), backannotated sheet; everything in `design_considerations/pad_buffer_layout/oa_core_pd_v2_2026-10-28/`; `report.md`, `v1_vs_v2.png` here; v1 in `oa_core_pd_2026-10-28/`; bg: `macros/bg_core_pd/layout/gds/bg_core_pd.gds` (2380 µm²), everything in `design_considerations/pad_buffer_layout/bg_core_pd_2026-10-28/`; `report_bg.md`, `bg_core_pd.png`, `bg_primitives_before_after.png`, `bg_rule_savings.png` here |
| A3 | oa NMOS primitives compact | 02:39 | 02:36 (rotate oa_nmir / oa_misc_n / oa_mcs, one 10/1 array, no taps between rows, slim rings), 02:37 "other agents may be more experienced rotating transistors within layout primitives."; 04:28 "It might make sense for Agent 2 to recruit help from Agents 3 and 4." | oa cells done 03:24; bandgap NMOS block bg_n4 (`BRIEF_bg.md`) done 05:36, option 1 (dummies D = S = G = g) 05:56 | oa_n10, oa_mcs_c (in oa_core_pd v2); bg_n4 (in bg_core_pd); `report.md`, `before_after.png`, `report_bg.md`, `report_bg_option1.md`, `bg_n4*.png` |
| A4 | oa PMOS primitives compact | 02:39 | 02:36 (oa_misc_p compact, narrower dummies in oa_pmir), 02:37; 04:28 (as A3) | oa cells done 03:31; bandgap PMOS cells (`BRIEF_bg.md`) done 05:40 | oa_pmir_c, oa_ms1, oa_svpg (in oa_core_pd v2); bg_pmir_pcas_c, bg_ms1, bg_svpg (in bg_core_pd); `report.md`, `before_after.png`, `report_bg.md`, `before_after_bg.png`, `bg_pmir_pcas_c.png` |

Shared addendum: `SKILL_EXPORT.md` (02:50, sent to A2, A3 and A4). The user asked for transferable layout skills,
"not only in words, but very much in graphical (and musical) patterns". Each agent exports `out/skill/` in three forms:
- pattern notation in symbol / score form;
- pictures rendered from the GDS;
- a reusable generator;
plus `rules.md` with deck citations and a SKILL.md draft.

How A2, A3 and A4 depend on each other (the same pattern for both cores):
- A3 (NMOS) and A4 (PMOS) make the primitives in parallel, each in its own workspace (`scratchpad/primN`,
  `scratchpad/primP`).
- A2 prepares the floorplan and the parts that are neither (for the bandgap: the pnp and resistor arrays), and says
  what pins and shapes it needs. The session relays that to A3 / A4.
- The session checks A3's and A4's cells, passes them to A2, and A2 assembles them. It may change copies of them
  (03:40).
- The session checks the assembled block independently before it goes into the macro.

**What survives the session.** The agents themselves live only as long as this session's cloud container. An agent
from an earlier session can't be reached any more; the 2026-10-27 "sinks-style worker" and "cascode worker" are gone.
Their experience survives only as files:
- the log (`design_considerations/pad_buffer_layout/log.md`);
- the cells they drew;
- the briefs and reports kept here.

That's why each new agent's brief points at those log entries and cells.
