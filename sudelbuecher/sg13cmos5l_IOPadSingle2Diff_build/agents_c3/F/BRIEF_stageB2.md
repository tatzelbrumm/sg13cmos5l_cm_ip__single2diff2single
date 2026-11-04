<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief F, stage B2: rerouting of the long nets (C3, 2026-11-04)

`BRIEF.md` and `BRIEF_stageB.md` still apply. The edge reserve stays as built, and the placement stays unless a change
below needs a small move (list every move). Christoph looked at the lead's marker render of the long nets
(`vbp_check.png`: vbp red, vbnc green, pad blue) and wrote (2026-11-04, verbatim):

> Looking at vpb_check.png, it seems to me that you could route the pad net down the center, maybe even with shield
> routes. Same seems to apply for the red net; the u shape on the left side seems avoidable. vbnc seems to take the
> long way unnecessarily, but when it's not parallel to the pad net, this doesn't seem to be critical.
> There are gaps in the metal3 buses. It is conceivable that you have short metal3 lines well clear of the standard pad
> bus lines.

## What to change

1. **pad (vin) down the center.**
   - Run it from the template's `pad` pin (M2 x 20.40–21.02, top y 31.18) up the middle of the cell to the inputs'
     vin track, not up the left reserve beside the output trunk.
   - Give it shield routes: a line on each side along its length, on a quiet supply of your choice. Say which supply
     and why. Tie each shield at one end only, or at both, and say why.
   - Nothing else runs parallel to it in the same or an adjacent metal over more than a few µm, apart from the
     shields; crossings are fine.
2. **vbp without the U on the left.**
   - Feed both tail rows from the bias tree on the right side: the tail rows have vbp stubs at both row ends.
   - No vbp metal on the left side of the cell.
3. **vbnc shorter where that comes easily.** It must not run parallel to the pad net anywhere.
4. **Metal3 in the gaps of the ring rails.** Short M3 segments are allowed inside the cell, where no M3 rail runs.
   - M3 rails, by y: iovss 7–32.5, 34.5–60, 126–134; iovdd 66–91.5, 93.5–119; vss 140–158; vdd 160–178.
   - The gaps are 32.5–34.5, 60–66, 91.5–93.5, 119–126, 134–140, 158–160 and 178–180.
   - **"Well clear":** keep every such M3 shape at least 0.5 µm from any M3 rail edge (Mn.b is 0.21; the extra
     margin is Christoph's "well clear"), and inside 0 < x < 80. Via2 / Via3 rules as in the decks.
   - Use them where they shorten a net or take it off a long parallel run (for example vbp or vbnc crossing the
     input group).
5. **Leave everything else as routed**, unless a change above needs room. The template, the protection and the edge
   reserve (no buffer device layers or M1 in x 1.8–4.3 / 75.7–78.2) stay as they are.

## Checks and deliverables

The same as stage B: DRC (run_drc.py, maximal with latch-up), deep LVS, circuit check, row check, template XOR,
reserve check, PEX capacitor-only nodes. In addition:
- **Lengths:** before / after per net (M1 / M2 / M3) for pad, vbp, vbnc, vbn, outp, outn.
- **Parallel runs:** the longest parallel run of any other net next to pad, at ≤ 1 µm spacing in the same or an
  adjacent metal, before and after.
- **Pictures:** `previews/` with pad, vbp and vbnc highlighted in color over the cell (as the lead's render), plus the
  usual ones.

Overwrite `pad_candidate.gds` / `.cdl` and keep the stage B versions as `out/stageB_v1/`. Report in
`report_stageB2.md` (under ~80 lines; if the harness refuses the file, put it in your reply), then reply with at
most 15 lines and the file list with sha256, and stop.
