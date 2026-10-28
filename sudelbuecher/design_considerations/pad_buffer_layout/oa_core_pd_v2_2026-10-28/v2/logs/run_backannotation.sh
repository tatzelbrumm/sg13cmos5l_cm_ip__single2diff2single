#!/bin/sh
# backannotation package of oa_core_pd v2 (run from out/v2)
cd "$(dirname "$0")/.." && python3 backannotate.py oa_core_pd.gds oa_core_pd ../../inputs/oa_core_pd.sch ../../inputs/oa_core_pd_xschem.spice backannotation \
 --xschemrc ../../work_v2/xs/xschemrc --ports "vdd vss iout en_3v3 en_3v3_b" \
 --ratio "M10 : M11 (W; sets the OA current):M10,M11" --ratio "PO : P8 : P2 : P0 (W, mirror):PO,P8,P2,P0" \
 --ratio "POC : P8C : P2C : P0C (W, cascodes):POC,P8C,P2C,P0C" --ratio "MCS : MCL (W/L, matched):MCS,MCL" \
 --note "oa_pcas -> oa_pcas_c: own ntap ring removed, NWell to the cell edge; bulk through the merged vdd well (no device change)" \
 --note "PMOS cells oa_pmir_c / oa_ms1 / oa_svpg / oa_pcas_c tap-less in ONE merged vdd NWell; n ties: thick tie under the vdd rail, two 8.2 um segments in oa_pmir_c's margins" \
 --note "NMOS: oa_n10 (M10 / M11 / MC10 / MS2 / MS3 / SKS) and oa_mcs_c share one p+ tie; no ring"
