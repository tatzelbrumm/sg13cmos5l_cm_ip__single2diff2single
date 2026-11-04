<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Agent F to the lead (C3, stage A, 2026-11-03, Europe/Berlin)

Points where the brief was unclear or left a choice. I decided each one myself and did not stop. [M] = tool result,
[R] = reasoning.

1. **Row check, 26 / 26 (21:50).** The brief and the template README say 26 of 26 bands and rails. This
   `row_check.py` writes 25 table rows (6 bands, 7 + 7 M3 / M4 rails, 5 TM1 rails), also on the template alone. Both
   the template and `placement_A.gds` pass 25 of 25, and both have 0 edge layers DIFFERENT [M]. I report 25 / 25 and
   read the brief's number as the README's count. The `nets` column of three bands rises in the placement (for example,
   the p+ plate band 1 → 7), because the unrouted cells' own taps lie in those y ranges as separate nets. They become
   iovss / iovdd when routed [R].
2. **The tails split (21:45).** I changed one primitive: P's two-row `s2d_tails_c3` becomes two one-row cells,
   `s2d_tails_lo_f` below the tubs and `s2d_tails_hi_f` above them. Each tail drain then faces its own tub's source
   pin, so all 12 tail-to-tub links are short verticals of equal length (rule 2). This costs area: 2 × 413.9 against
   715.4 µm² (+112 µm²) [M].
   - It may also touch rule 4, "no taps between rows of arrayed transistors". The two tail rows now have the tubs and
     their own ring strips between them. I read the rule as applying within one array, and I flag it for Christoph's
     review.
   - Fallback: P's cell as delivered, M0, directly above the tubs. This puts the tails' far-side drains about 45 µm
     from their tubs [R].
3. **`s2d_pd_n_c3` is not placed.** Its two devices TPN / TNN are already inside `s2d_cload_c3`, and the cload ring
   is their tap (N's `messages.md`, point 1).
4. **The fit's keep-outs, refined.**
   - Off the pad pin strap, I keep 1.5 µm from CN's outer NWell ring (y 31.6), where the fit used y 32.68 everywhere.
     Around the strap itself (x 18.9–22.52) I keep the fit's y 32.68.
   - The riser margin is 0.25 µm (M2: Mn.b 0.21) instead of 0.5. Only casc_p (x 45.5) uses it.
   - DRC is clean with both [M].
5. **The fit used the C2 library cells** (`sinks_6x6_s2d_c2` and others). I placed P's and N's c3 cells, as the
   brief says.

# Stage B (2026-11-04, 13:08–14:10 CET)

6. **The router is read from outside `$WS`.** C2 F2's `route_block.py` uses the grid router `generator.py`, which is
   not in `inputs/`. I read it (read only) from the notes checkout
   (`/home/user/sudel/sudelbuecher/design_considerations/pad_buffer_layout/oa_core_pd_v2_2026-10-28/v2/generator.py`,
   sha256 cea21b865695) and copied it unchanged into `src/`. I wrote nothing outside `$WS`. The process adapter is
   C2 F2's `ihp_sg13cmos5l_f2.py`, unchanged, as `src/ihp_sg13cmos5l.py`.
7. **iovdd rail tie.** In this cell the two Metal3 iovdd rails (66–91.5 and 93.5–119) are not connected; IHP's cells
   rely on the IO ring. The front end taps the upper rail, the output stage and the protection the lower one, and
   deep LVS then found two iovdd nets [M]. I added one Metal2 / Via2 strap in the right edge reserve that joins
   them. This is Metal2 / Via2 / Metal3 only, which the reserve allows, and no template shape changes. If Christoph
   prefers, the front-end taps can move to the lower rail instead.
8. **LVS hierarchy.** `s2d_block` has no subckt in `pad_candidate.cdl`; its cells sit directly in the pad subckt.
   Inside the block, the supply groups meet only on the template's Metal3 rails, so a block subckt with one
   iovdd / iovss pin cannot match. The comparison flattens the layout's `s2d_block` [M: match].
9. **The harness refused `report_stageB.md`** ("subagents should return findings as text"). Its full text is in my
   final reply, for the lead to save.

# Stage B2 (2026-11-04, 16:52–17:55 CET)

10. **Shields.** Christoph's later word: "the shield lines around the pin line are optional". I had already drawn
    them. Every net still routes, and so does the order that routed everything with them, so they cost no other
    route. I kept them.
11. **vbnc.** Routing vbnc first (to shorten it) left 4 nets unroutable after 8 rounds [M]. It stays at 208 µm, on a
    different path from stage B. No part of it lies within 1 µm of the pad line [M], which was Christoph's condition.
12. **Keep-outs in the tubs' well gap.** Keep-outs there (to keep other nets 1 µm off the pad's Metal1 leg) left 7
    nets unroutable [M], so I did not use them. Every net that sits within 1 µm of that leg sits behind a shield.
13. **The tail rows lost their left vbp stubs** (stage-A cells changed: no vbp metal on the left). The stage-A /
    stage-B versions are in `stageB_v1/cells/`.

# Stage B3 (2026-11-04)

14. **Hand edit instead of a reroute.** With Metal1 kept out of x < 1.8 (stub clearance) and the reserve, the router
    could not place y again: an incremental reroute of y alone, and with up to 17 more nets ripped around it, left
    1 to 7 nets unrouted every time [M]. A full reroute would also have moved nets the brief keeps. So I redrew only
    y's left detour by hand (`src/patch_y.py`, applied to stage B2's routed block); every other shape is stage B2's
    [M: XOR differs only on Metal1 / Via1 / Metal2 inside x 0.66–2.07, y 117.92–149.46].
