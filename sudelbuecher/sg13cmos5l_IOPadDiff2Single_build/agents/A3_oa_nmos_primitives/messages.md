# A3 — oa NMOS primitives compact: everything the agent was told, verbatim

A subagent starts with no part of the conversation: it sees only the launch prompt, the brief file(s) it is
pointed to, the files in its own `inputs/` folder, and the later messages below. Times Europe/Berlin.

## 2026-10-28 02:39 — launch prompt

```text
You are the NMOS layout-primitive specialist for an analog IC block in IHP sg13cmos5l. Your complete brief is /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/BRIEF.md — read it first and follow it exactly, including its hard rules (cloud workspace only, no remote-devices tools, no git, inputs read-only, rule values only from the PDK decks with citations). Study how the earlier workers rotated sinks_6x6, d2s_casc_n, bg_nab and bias_tree_n (log entries named in the brief, cells in inputs/pad_buffer_cells.gds) before you draw. Deliverables go to /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/out/. When done, reply with the five-line summary, the report text, and the deliverable list with sha256 (first 12 hex). Report only what you checked.
```

## 2026-10-28 02:50 — message (“Add skill export deliverables (A3)”)

```text
Additional deliverable from the user (02:50): read /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/SKILL_EXPORT.md and deliver out/skill/ as described there (pattern notation in symbol/score form, pictures rendered from your GDS, a reusable generator, rules with deck citations, a SKILL.md draft), alongside your cells. The cells come first; the skill material documents how you made them, so build it from what you actually did.
```
