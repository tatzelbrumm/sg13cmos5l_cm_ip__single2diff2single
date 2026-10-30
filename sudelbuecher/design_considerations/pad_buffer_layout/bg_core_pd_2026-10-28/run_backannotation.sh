#!/bin/sh
# backannotation package of bg_core_pd (run from out_bg; 2026-10-28, Claude)
cd "$(dirname "$0")" && python3 backannotate.py bg_core_pd.gds bg_core_pd ../inputs_bg/bg_core_pd.sch xs/bg_core_pd_sheet_xschem.spice backannotation \
 --extractor tools/lvs.py --xschemrc xs/xschemrc --ports "vdd vss iout en_3v3 en_3v3_b" \
 --res-model rhigh --bjt-model pnpMPA --res-class RES --bjt-class PNPMPA \
 --ratio "PO : PA : PB (W, mirror; iout = 2 x branch):PO,PA,PB" --ratio "POC : PAC : PBC (W, cascodes):POC,PAC,PBC" \
 --ratio "NA : NB (W/L, matched pair):NA,NB" \
 --note "PMOS cells bg_pmir_pcas_c / bg_ms1 / bg_svpg tap-less in ONE merged vdd NWell; n ties: thick tie under the vdd rail, one 13.1 um segment in bg_pmir_pcas_c's bottom margin over bg_ms1" \
 --note "bg_n4 (NA, NB, MS2, MS3, SKS): own p+ ties at bottom and top; its dummies D = S = G = g (user's choice 2026-10-28 05:43)" \
 --note "bg_res_c: the library's rhigh segments (0.5 x 9.94 um, 0.68 um pitch, the library's interleave) without the p-tap ring; bg_pnp_c: the library's 3 x 3 pnpMPA array (Q1 centre) with its emitter / base wiring"
