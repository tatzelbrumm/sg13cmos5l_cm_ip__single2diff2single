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
