# BA: backannotation of sg13cmos5l_IOPadSingle2Diff to the drawn pad cell (C3, 2026-11-04)

Agent BA. Edits only in `work/` (25 files, `out/changed_files.txt`; originals in `out/macro_before/`). Untouched
reference tree: `out/old_root/` (`cp -a` of `work/{macros,schematic,testbenches}` before any edit). Tools:
`out/tools/` (C2's, adapted; `run_checks.sh` reruns every check below), logs: `out/logs/`, renders: `out/renders/`
(`before/` = old sheets, `after/`). The GDS was not touched.

## What changed
1. **Pad sheet / symbol** (`sg13cmos5l_IOPadSingle2Diff.sch/.sym`): ports `iovdd iovss vdd vss pad outp outn vcm vref
   iref en_3v3 en_3v3_b` (iref, en_3v3, en_3v3_b take the symbol places of ibias, en_1v2, sel0_1v2; the other three
   old pins are gone). xc / xg removed; xt, xa kept. XSP (SecondaryProtection) gone, `padres` -> `pad`: xa's vin is
   the pad. Rsub 1 Ohm vss - iovss, `lvs_ignore=open`, with C2's note. Sheet redrawn (labels, no long crossings added).
2. **Primary protection: `xp` = an instance of `s2d_pad_esd.sym`**, not drawn on the pad sheet. Why: that sheet already
   holds exactly these 8 devices (checked equal to the template's extraction by the lead); one copy stays the only
   copy, and the pad sheet stays readable. Its diodes are scalar (DP1, DP2, DN1, DN2). `s2d_pad_esd.sch` changed:
   rppd `body=sub!` -> `body=iovss` (RP, RN) and its text. `.subckt s2d_pad_esd` added to
   `netlist/source/sg13cmos5l_IOPadSingle2Diff.spice`.
3. **Dummies (29 s2d + 2 tree), where each went** (names / nets from the CDL; NMOS dummies here are D = S = B = vss
   with the gate on the bias line, unlike C2's d2s D = S = G):
   - `s2d_mpdda_pd.sch` block [DM] (all nets are ports there): MDT[3:0] tubs 20u/1u ng2 all vdd; MDTL[2:0] 5u/6u G vbp
     (tails_hi D7, tails_lo D0 / D7); MDPC[2:0] 1u/4u G vbpc; MDSK[3:0] 2u/6u + MDBNT 6u/6u G vbn (sinks); MDSC[3:0]
     2u/6u G vbn (sinks_cmfb); MDCN[3:0] 2u/3u G vbnc; RD[1:0] rhigh 0.5u/12.65u vss-vss.
   - `s2d_mpdda.sch` (Christoph's sheet): only MDL[3:0] 1u/4u, G vcmfb, D = S = B = vdd (s2d_loads_f). vcmfb is internal
     to s2d_mpdda, so this is the only place they can sit without a fake local net (C2 finding 1).
   - `bias_tree_noab_pd.sch`: MDBP 2u/6u D = S = B = vdd, G vbp; MDBN 2.4u/6u D = S = B = vss, G ni (CDL `Mdummy_3 vss ni
     vss vss`; C2's MDBN in bias_tree_pd is D = S = G = ni, so only the names / style follow C2).
   - Sources follow: `s2d_pd.spice`, `s2d_mpdda.spice`, `bias_tree_noab_pd.spice` (same names, header comments).
4. **Finger counts: no change needed.** All s2d devices already had the drawn finger count and width (SX / SY 36u ng6,
   SXC / SYC 24u ng4, LP / LN / D 24u ng4, the cascodes 30u ng2); the CDL's separate ng=1 PCells sum to the same, and
   the finger check below compares count x width per key. BP / BN / BPC / BNC stay in bias_diodes / the tree sheet.
5. **unit_r2** not edited: C2's 4 x rhigh 0.5u/12.65u, body vss, equals each drawn `s2d_rhigh_c3` unit (4 segments,
   same w / l / body; 24 segments + 2 dummies on both sides).
6. **Users**: 7 CACE templates (xc + xg next to x1, nets as the old pins; tb_pd `v(x1.en_3v3)` -> `v(en_3v3)`; noise /
   tran texts no longer claim the 587 Ohm stage); slot.sch `xs2d_c` / `xs2d_g` (nets `s2d_*`); top sheet `xinbuf_c` /
   `xinbuf_g` (its pad pins were unconnected; rails now `inbuf_iovdd / _vdd / _iovss`); the yaml `pins:` (+ comment
   and two comments on the secondary protection); `s2d_mpdda_pd_sel.yaml` vin description; `tb_pad_dc.spice` (Xc + Xg
   + X1, probe `v(en_3v3)`). Rewiring script `out/tools/users_s2d.py` (C2's users_ba.py for the s2d symbol).
7. README.md (structure, sheets, sources, ports) and FILL_IN.md items 8, 9: only statements the change made false.
8. Added (generated): `netlist/schematic/sg13cmos5l_IOPadSingle2Diff_klayout.cdl` (as d2s has its own).

## Checks (all measured)
| check | result | log |
|---|---|---|
| xschem netlist of 17 sheets, SPICE + LVS (PDK rc + all repo dirs) | 32/34 with 0 missing; top sheet: 2 missing (IOPadAnalog, IOPadInOut16mA), same in old_root. Exit 10 on templates / slot / top / loop, same in old_root, netlists complete | netlist_changed_sheets.log |
| same with each sheet's own xschemrc | 15/16 written, 0 missing; top sheet writes none, same in old_root | netlist_own_rc.log |
| `make klayout-lvs-netlist` + `cdl_compare.py` vs `pad_candidate.cdl` | MOS 56 keys, dummies 9, diodes 2, fingers 65, R 9 (series-reduced): **0 differ, dummies included** | check_sheet_vs_cdl.log |
| same, source netlists vs CDL | 0 differ | check_source_vs_cdl.log |
| checker sanity: 3 mutated CDL copies (dummy gate, SX ng 6->4, one diode removed) | all RESULT DIFFERENT | check_sanity_mutant.log |
| sheet vs source subckt (topology, w/l/ng, port order): pad, s2d_mpdda_pd, s2d_mpdda, s2d_pad_esd, bias_tree_noab_pd, unit_r2 | 6/6 equivalent; mutant (one dummy gate label) DIFFERENT | check_sheets_vs_source*.log |
| `intended_equiv_s2d.py old_root work` (16 sheets) | **15/16 equivalent**: slot, top, 7 templates, s2d_mpdda_pd_sel, loop template, s2d_mpdda_pd, s2d_mpdda, bias_tree_noab_pd, bias_sel_noab_pd. The pad sheet alone differs by its port list (xc / xg moved out), as intended; its users carry the function | intended_equiv_users.log (+ _sanity_mutant: a swapped ibias label in slot is caught) |
| tb_pad_dc (ngspice, sel 0..3 + disabled) old vs new | runs; iq, vd, vc and all bias lines equal to 6 digits; pad current i(vin) -276 -> -183 pA (secondary diodes gone) | tb_pad_dc_{old,new,table}.log |
| make check-boundary | passed | check_boundary.log |

Per selection (new): iq 115.5 / 123.3 / 124.7 / 246.3 uA (sel 0..3); vbp 1.972 / 1.973 / 1.976 / 1.694 V, vbn 0.914 /
0.913 / 0.912 / 1.049 V, vbpc 1.913 / 1.914 / 1.917 / 1.608 V, vbnc 1.208 / 1.207 / 1.205 / 1.444 V; vd 199.9 mV,
vc +10.4 mV (sel 3: 199.87 mV, +12.1 mV). Disabled: iq 0.314 nA (old 0.322 nA), vbp 3.04 V, vbn 0.196 V.
The old tree already had C2's 4-segment unit_r2, so no other change shows in DC.

intended_equiv_s2d reverts exactly: dummies XMD* / XRD[*] (s2d_mpdda_pd), XMDL[*] (s2d_mpdda), XMDBP / XMDBN, Rsub,
and xp's 8 devices; it puts IHP's XCP / XCN / XDN / XDP / XSP back (old pin order) with a new padres net on xa's side.

## Findings for the lead
1. `Rsub` in the source is written `Rsub iovss vss 1` (xschem's terminal order), because `sheet_vs_source.py` keys a
   plain R's terminals by position; with `vss iovss` it reported DIFFERENT on an identical circuit.
2. A mutant on a dummy is (by design) invisible to intended_equiv, since it removes dummies; cdl_compare and
   sheet_vs_source catch it (logs above).
3. `s2d_pad_esd.sch` now has body iovss on RP / RN (the brief); its template documentation mentioned sub!. If the
   template sheet must stay as extracted, the pad would need its own copy.
4. Not run: KLayout / magic LVS of the GDS against the new CDL, CACE. `tb_s2d_noise.spice` still mentions the 587 Ohm
   SecondaryProtection of the harness IOPadAnalog (it does not instantiate this pad; left alone).
5. The top sheet's pre-existing layout overlaps (pad symbols over the port column) are unchanged; only the new
   instances were placed clear of them.
