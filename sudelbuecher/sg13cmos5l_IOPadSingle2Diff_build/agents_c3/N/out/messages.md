<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Agent N to the lead (C3, 2026-11-03, Europe/Berlin)

Points where the brief left a choice. I decided each one myself and did not stop. All are reasoning, not tool
results.

1. **Where TPN / TNN live (21:00).** The brief lists `s2d_pd_n` as a cell of its own. Rule 6 says switches belong
   with the cell they serve, "not in a separate corner with their own taps". So `s2d_pd_n_c3` is the switch pair
   without a tap (as the library's and Christoph's compacted switch cells). The same geometry, drawn by the same
   function, also sits inside `s2d_cload_c3`, between the CLP and CLN gate columns. Their drains join voutp and
   voutn there directly, and the cload ring is their tap. Standalone, `s2d_pd_n_c3` shows LU.b (no tap) as its only
   DRC finding, by design. If you want it with its own tap, that is a small change, but rule 6 argues against it.
2. **Orientation of the sink blocks.** `sinks_6x6_s2d_c3` is N2's s2d cell, the block turned R90 (pins on the
   bottom edge). I kept that, because the brief says "start from N2's sinks_6x6_s2d_c2". `s2d_sinks_cmfb_c3` is
   turned the same way, so both blocks match. The unturned blocks are in the GDS as `*_c3_core`. F can use either.
3. **Dummy inner stripes to vss.** I used a 0.29 µm M1 lane between the end dummy and the gate column. This is the
   library sinks_6x6 solution that Christoph accepted ("your solution is good ... Keep it!", log 01:20). I did not
   strap across the dummy channel, because he reverted that one at 01:03. The exception is BN's twin T in the
   middle of the sinks: with the center columns gone, it can reach vss only through an M1 strap across its own
   channel (F2's fix). The lanes cost 0.31 µm per row end.
4. **casc_n is 1.03 × the library cell.** The library `s2d_casc_n` has no dummies, puts BNC at one end and has no
   ring. Mine has 4 dummies, BNC in the middle on both axes, and a closed ring. 5 band tracks and 3 source levels
   per side set its height. The vbnc track stays in the band (N2 / F2 style), so the BNC diode current runs in metal
   and not through gate poly. It crosses BNC's channel, as in N2's cell.
5. **cload is 1.09 × the library cell.** The library cell contacts each 12 µm gate through one narrowed poly neck and
   has one tie strip. Mine has full-height contact columns, a closed ring, and the output ties inside.
