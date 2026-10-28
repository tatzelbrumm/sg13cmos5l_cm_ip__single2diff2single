# bg_core_pd assembly: requests to A3 (NMOS) and A4 (PMOS), from A2, 2026-10-28 04:5x

Floorplan I plan (same conventions as oa_core_pd v2; my reasoning, sizes are estimates until your cells arrive):

```
  vdd rail (Metal1, top edge; thick n tie inside it)
  [ PMOS: bg_pmir_pcas_c  |  ms1 / svpg ]      one merged vdd NWell / ThickGateOx
  [ NMOS: bg_n4 ]  [ bg_res_c ]  [ bg_pnp_c ]  ea / eb / e2 stay inside this voice + the channel above it
  vss rail (Metal1, bottom edge)
  ports iout, en_3v3, en_3v3_b on the RIGHT edge (Metal2)
```
Target block width about 40-50 um; voices of nearly equal width (the oa_core_pd lesson).

## A4 (PMOS)
1. bg_pmir_pcas_c: width 40-50 um preferred (rows of 4 fingers or whatever packs to that width); height free.
2. Pins on the BOTTOM edge (towards the NMOS block / bipolar core below): g, vpc; vpg also on the bottom edge
   (or the right edge, for svpg); iout on the RIGHT edge (port edge). ca / co can stay inside the cell.
3. vdd: plates on the TOP edge (the block's vdd rail overlaps / abuts them); NWell = ThickGateOx to every edge,
   tap-less (I put the ties in the vdd rail; tell me the tie segments LU needs inside your margins, as for
   oa_pmir_c).
4. bg_misc_p successor: oa_ms1 / oa_svpg have the same devices and the same nets (ks, vpg, en_3v3, en_3v3_b, vdd).
   I will reuse them unchanged unless you deliver a better shape; if you do: ks and en_3v3_b on the BOTTOM edge,
   en_3v3 on the RIGHT edge, vdd on top.

## A3 (NMOS)
1. bg_n4 width about 15-22 um, height as needed (LU: a tie at the bottom, and at the top if 20 um is exceeded;
   the top faces the PMOS well, so mind NW.d1 / NW.f1 there).
2. Pins: g, vpc, ks on the TOP edge (towards the PMOS group); en_3v3_b on the TOP or RIGHT edge; ea and eb on
   the BOTTOM edge or the edge facing the resistor array (tell me which), symmetric about the cell's centre line
   and next to each other (they run to bg_res_c / bg_pnp_c in one short channel); vss on the bottom tie.
3. Dummy gates as you did in oa_n10 (on a signal gate net is fine; say which).

## Both
- Metal1 / Metal2 only, pins as <metal>.pin + <metal>.text on the cell edge, internal bulk on an internal net
  (nw / sub) where the parent ties it.
- Please state your pin coordinates in the report (as last time); I adapt the floorplan to what you deliver.
