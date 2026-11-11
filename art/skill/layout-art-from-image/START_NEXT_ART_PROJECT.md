# How to start the next layout-art project (paste this into a new chat / Cowork session, attach the image)

```
Use the skill "layout-art-from-image" (upload layout-art-from-image-v1.zip first, or read art/skill/layout-art-from-image/ on branch
art/tughra-metal of tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single).

TASK: turn the attached image into layout art (GDS) for PDK <ihp-sg13cmos5l | sky130 | gf180mcu> in the empty space of the host layout <repo / file / top cell>.
Work unattended: do not wait for answers; where something is unclear pick the most reasonable option, record it in ART_NOTES.md, carry on.

Repos: host layout repo <name> = READ ONLY (no branch, commit, push, edit). Work repo <name>, new branch <art/...> from <base branch>.
Image: exclude <legend / caption area>; colours = <list or "the legend squares">.
Layers I allow: <e.g. metals + poly; not top metal; no active>. Layers I want merged: <e.g. red + orange> or "you propose".
Region: <whole free space | a given rectangle>; keep-outs: <host docs or none>.

Steps and evidence to give me: free rectangles per layer with margins and why; ART_LAYERS.md (commit before geometry); re-runnable script in art/;
art-only GDS and merged GDS; nofill markers; DRC on original vs merged (full deck, density, antenna), XOR (must be empty), LVS before/after,
filler test with control, previews side by side with the source; ART_NOTES.md with every assumption. Say what you did NOT verify.
```

Before sending, fill the angle brackets. Things worth deciding up front: which PDK(s); whether top metal is allowed; which colour goes on the least visible layer; whether the
host layout will be filled by a harness (then nofill markers are essential).
