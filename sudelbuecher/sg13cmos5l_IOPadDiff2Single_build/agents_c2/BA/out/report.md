# BA: backannotation of sg13cmos5l_IOPadDiff2Single to the drawn pad cell (C2, 2026-11-03)

Agent BA. Edits only in `work/` (22 files, `out/changed_files.txt`; originals in `out/macro_before/`). Untouched
reference tree for the before/after checks: `out/old_root/` (`cp -a` of `work/{macros,schematic,testbenches}` before
any edit; 94 MB, delete when no longer needed). Tools: `out/tools/`, logs: `out/logs/`, renders: `out/renders/`
(`before/` = old sheets).

## What changed
1. **Pad sheet / symbol** (`sg13cmos5l_IOPadDiff2Single.sch/.sym`): ports `iovdd iovss vdd vss pad vinp vinn vref iref
   en_3v3 en_3v3_b` (iref, en_3v3, en_3v3_b take the symbol places of ibias, en_1v2, sel0_1v2; the other three old pins
   are gone; vdd / vss are n.c. inside). xc / xg removed; xt, xd, xfp, xfn, DP, DN kept. CMA `pa a pa pa`, CMB `b pb b b`,
   each behind a `d2s_sp2k` instance (XSPA, XSPB). Bias-tree layout dummies XMDBP (2u/6u, G vbp, rest iovdd) and XMDBN
   (2.4u/6u, D=S=G=ni, B iovss). Right half redrawn (a/b/dabp/dabn staircases, pad trunk, vfb as a `pad` label).
2. **New `d2s_sp2k.sch/.sym`** (ports `core iovdd iovss pad`): rppd 1u/7.435u pad->core (body iovss, 1.992 kOhm),
   dantenna 0.64u/3.1u (anode iovss), dpantenna 0.64u/4.98u (cathode iovdd). Its .subckt is in
   `netlist/source/sg13cmos5l_IOPadDiff2Single.spice`.
3. **`d2s_mpdda_pd.sch/.spice`**: SX/SY ng 4 -> 6; SA bulk vdd, SB bulk vss; block [DM] with all 27 dummies of the d2s
   cells as vector instances (MDT[3:0] tubs 20u/1u ng2, MDTL[2:0] 5u/6u G vbp, MDL[3:0] 1u/4u G l2, MDPC 1u/4u G vbpc,
   MDABP[1:0] 6.66u/0.6u, MDABN[1:0] 4.4u/1u all vss, MDCN[3:0] 2u/3u D=S=G=vbnc, MDSK[3:0] 2u/6u and MDBNT 6u/6u
   D=S=G=vbn, RD[1:0] rhigh 0.5u/12.65u vss-vss). PL/PR (ng 4) and PCL/PCR/CX/CY (ng 2) already were as drawn.
   BP/BN/BPC/BNC stay in bias_tree_pd (sheet unchanged).
4. **`unit_r2.sch` / `units.spice`**: R as vector instance `R[3:0]` (netlisted XR[3..0]), rhigh 0.5u/12.65u, sa n1 n2 n3
   sb, body vss. The sheet never parameterized rl (it had l=50.6u fixed), so it now has 12.65u fixed; in `units.spice`
   `rl` stays usable: each segment is `l={rl/4}`.
5. **Users**: 8 CACE templates, `slot.sch` (xd2s), top sheet (xoutbuf): the pad's six old pin labels removed, iref /
   en_3v3 / en_3v3_b labelled, and an `en_ctrl_3v3` + `bias_gen_pd` pair placed next to the pad with the nets the old pins
   had (xc: vddh = pad's iovdd net, vddl = pad's vdd net, vss = pad's iovss net; xg: vdd / vss likewise). Names: templates
   xc / xg and nets iref, en_3v3, ...; slot xd2s_c / xd2s_g, nets d2s_*; top xoutbuf_c / xoutbuf_g, nets outbuf_* (its
   pad pins were all unconnected before; the rail pins now carry outbuf_iovdd / _vdd / _iovss so xc / xg share them).
   tb_pd: `v(x1.en_3v3)` -> `v(en_3v3)` (the net left the cell). yaml `pins:` to the new ports (+ a comment); sources,
   conditions and measurements unchanged.
6. Also changed (not in the brief, needed to keep it working): `testbenches/spice/tb_pad_dc.spice` (instantiated the
   pad with the old ports: now Xc + Xg + X1, probe `v(en_3v3)`); `d2s_out.spice` comment on the CMA/CMB polarity.

## Checks (all measured)
| check | result | log |
|---|---|---|
| xschem netlist of every changed sheet, SPICE + LVS (PDK rc + all repo dirs) | 28/30 clean; top sheet: 2 missing symbols (IOPadAnalog, IOPadInOut16mA), same before | netlist_changed_sheets.log |
| same with each sheet's own xschemrc | templates, pad, d2s_mpdda_pd_sel, slot: 0 missing; top sheet writes no netlist with its own rc, same in old_root | netlist_own_rc.log |
| `make klayout-lvs-netlist` + `tools/cdl_compare.py` vs `pad_candidate.cdl` | MOS 53 keys, dummies 11, diodes 6, R 7: **0 differ, dummies included** | check_sheet_vs_cdl.log |
| same, source netlists vs CDL | 0 differ | check_source_vs_cdl.log |
| checker sanity (2 mutated dummy lines) | 4 keys differ, RESULT DIFFERENT | check_sanity_mutant.log |
| sheet vs source subckt (topology, w/l/ng): unit_r2, d2s_mpdda_pd, d2s_sp2k, pad | 4/4 equivalent, port order same | check_sheets_vs_source.log (+ _sanity) |
| `sheet_equiv.py old_root work` (20 sheets) | 20 DIFFERENT, as expected; lists only xc/xg moves, CMA/CMB, XSPA/B, dummies, SA/SB bulk, R chain | sheet_equiv_users.log |
| `tools/intended_equiv.py`: new flat netlist minus exactly the intended changes vs old | **20/20 equivalent** (slot, top, 8 templates, d2s_mpdda_pd, unit_r2, d2s_mpdda_pd_sel, loop template, 4 tb_pd, s2d_mpdda, IOPadSingle2Diff) | intended_equiv_users.log (+ _sanity_mutant: a swapped label is caught) |
| tb_pad_dc (ngspice, sel 0..3 + disabled) old vs new | runs; enabled: bias lines equal to 6 digits, v(pad) within 0.06 mV, iq +2.2 % (301.8 -> 308.4 uA at sel 0); disabled: iq 0.24 -> 0.25 nA, vbn (off) 0.196 -> 0.183 V | tb_pad_dc_{old,new}.log |
| make check-boundary | passed | check_boundary.log |

`inputs/circuit_vs_cdl.py` unchanged reports DIFFERENT on both sides (logs `*_unmodified_script.log`): it cannot read
xschem's CDL resistor lines, takes diode area only from `a=`, has no mapping for the DCN/DCP black boxes, and merges the
chain nodes n1..n3 of the four units by local name. `tools/cdl_compare.py` fixes exactly these (docstring) and also fails
on dummy differences.

The intended differences, one by one: (a) xc / xg moved out of the pad (no topological change, hierarchy is flattened);
(b) CMA S/D/B and CMB gate move from pad to pa / pb behind R0 of XSPA / XSPB, plus 2 x (rppd, 2 diodes); (c) 27 d2s
dummies + 2 bias-tree dummies; (d) SA / SB bulk vddo -> vdd, vsso -> vss (a topological change only where vddo != vdd,
i.e. in d2s_mpdda_pd_sel, the loop template and the tb_pd testbenches; identical nets in the pad); (e) SX / SY ng 6;
(f) each unit_r2 resistor -> 4 segments (this also changes sg13cmos5l_IOPadSingle2Diff, which shares unit_r2.sch /
units.spice: 6 units, no other change there).

## Findings for the lead
1. **XMDBN's `ni` is not the real ni.** ni is internal to bias_tree_pd (no port), and its sheet must stay unchanged, so on
   the pad sheet XMDBN's D=S=G sits on a separate local net named `ni`. The flat comparison by local names matches the
   CDL, but a real KLayout LVS of this sheet against the layout would see an extra floating net. Electrically harmless
   (Vgs = Vds = 0). Fix later: move that dummy into bias_tree_pd.sch, or give bias_tree_pd an `ni` port.
2. **iq +2.2 % from SX/SY ng 6** (finger width 9u -> 6u): the experiments with each change removed in turn show that the
   dummies, the stages and the R chains change nothing at 4 digits; SX/SY at ng 4 restores 301.8 uA. Real, as drawn;
   CACE limits on Iio may need a look.
3. The 15:50 entry of `decisions.md` mentions a wrapper sheet that keeps the old symbol; the brief asks for the port
   change and re-wired users, which is what I did. Flagging in case the wrapper was what was meant.
4. xschem 3.4.8RC LVS netlisting of vector MOS instances writes `M` only on the first element (`MDT[3]`, then `DT[2]`,
   read as a diode by a CDL reader). Hence all vector dummies are named `MD...` (`MMDT[3]`, `MDT[2]`, ...), and the
   source names follow (XMDT[3] ...). rhigh vectors (`RR[3]`, `R[2]`) are fine.
5. Not touched: macro README.md (still documents the old ports), testbenches/xschem/simulations netlists (gitignored,
   regenerated by my runs), CACE results. No CACE run was made.
