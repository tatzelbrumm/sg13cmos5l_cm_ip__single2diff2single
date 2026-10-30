#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# bg_core_pd (compact): build and every check from scratch (run in out_bg; 2026-10-28, Claude). Logs in logs/.
# Inputs read: ../inputs/pad_buffer_cells.gds (library), ../inputs_bg/bg_core_pd.sch, A3's ../../primN/out_bg and
# A4's ../../primP/out_bg cells (read only).
set -e
cd "$(dirname "$0")"
mkdir -p logs
LIB=../inputs/pad_buffer_cells.gds
# 1. A2's revised primitives: rhigh array and pnp array, DRC, LVS, devices vs the library
python3 build_bg_res_c.py $LIB bg_res_c.gds bg_res_c.cdl                              > logs/build_bg_res_c.txt
python3 build_bg_pnp_c.py $LIB bg_pnp_c.gds bg_pnp_c.cdl                              > logs/build_bg_pnp_c.txt
for c in bg_res_c bg_pnp_c; do
  python3 tools/drc.py $c.gds $c logs/drc_$c.txt                                       > /dev/null
  python3 tools/lvs.py $c.gds $c $c.cdl - logs/$c.lvsdb                                > logs/lvs_$c.txt 2>&1
done
python3 verify_bg_cells.py $LIB bg_pnp_c.gds bg_res_c.gds                             > logs/verify_bg_cells.txt
# 2. the block: generator, reference netlist from the primitives' netlists, DRC (block and each cell), LVS
(cd configs && python3 ../generator.py bg_core_pd.py ../bg_core_pd.gds)              > logs/build.txt 2>&1
python3 make_bg_core_pd_ref.py configs/bg_core_pd.py bg_core_pd.cdl                   > logs/make_ref.txt
python3 tools/drc.py bg_core_pd.gds bg_core_pd logs/drc_bg_core_pd.txt               > /dev/null
for c in bg_pmir_pcas_c bg_ms1 bg_svpg bg_n4 bg_res_c bg_pnp_c; do
  python3 tools/drc.py bg_core_pd.gds $c logs/drc_cell_$c.txt                          > /dev/null || true
done
python3 tools/lvs.py bg_core_pd.gds bg_core_pd bg_core_pd.cdl - logs/bg_core_pd.lvsdb > logs/lvs_vs_ref.txt 2>&1
# 3. backannotation: sheet netlist (xschem, PDK rc + the pnp format helpers), edited sheet, subckt text, changes,
#    xschem netlist of the new sheet, LVS of the layout against it
xschem --rcfile xs/xschemrc -n -s -q -x -o xs -N bg_core_pd_sheet_xschem.spice ../inputs_bg/bg_core_pd.sch > /dev/null 2>&1
sh run_backannotation.sh                                                              > logs/backannotation.txt 2>&1
python3 tools/lvs.py bg_core_pd.gds bg_core_pd backannotation/bg_core_pd_backannotated.cdl - \
  logs/bg_core_pd_backannotated.lvsdb                                                 > logs/lvs_vs_backannotated.txt 2>&1
# 4. area audit (library primitives side by side vs the block), pictures
python3 make_bg_library_set.py $LIB logs/bg_library_set.gds                           > logs/library_set.txt
python3 area_audit.py process/ihp_sg13cmos5l.py logs/bg_library_set.gds bg_library_set bg_core_pd.gds bg_core_pd \
                                                                                      > logs/area_audit.txt
python3 render_block.py process/ihp_sg13cmos5l.py bg_core_pd.png bg_core_pd.gds:bg_core_pd:"bg_core_pd (compact)" \
  --scale 7 > /dev/null
P=../../primP/out_bg/bg_p_cells.gds; N=../../primN/out_bg/bg_n_cells.gds
python3 render_block.py process/ihp_sg13cmos5l.py primitives_before_after.png \
  $LIB:bg_pmir_pcas:"library bg_pmir_pcas" $P:bg_pmir_pcas_c:"A4 bg_pmir_pcas_c" // \
  $LIB:bg_nab:"library bg_nab" $LIB:bg_misc_n:"library bg_misc_n" $N:bg_n4:"A3 bg_n4" // \
  $LIB:bg_misc_p:"library bg_misc_p" $P:bg_ms1:"A4 bg_ms1" $P:bg_svpg:"A4 bg_svpg" // \
  $LIB:bg_res:"library bg_res" bg_res_c.gds:bg_res_c:"A2 bg_res_c" // \
  $LIB:bg_pnp:"library bg_pnp" bg_pnp_c.gds:bg_pnp_c:"A2 bg_pnp_c" --scale 9 > /dev/null
python3 render_block.py process/ihp_sg13cmos5l.py rule_savings.png \
  logs/bg_library_set.gds:bg_library_set:"library primitives side by side (not a layout; sum 2673 um2)" \
  bg_core_pd.gds:bg_core_pd:"bg_core_pd compact" --scale 9 --notes logs/savings_notes.json > /dev/null
grep -h "TOTAL" logs/drc_*.txt | sort | uniq -c
grep -h "LVS .* ->" logs/lvs_*.txt
grep -h "RESULT" logs/verify_bg_cells.txt
grep -h "^block\|UNROUTED\|latch-up" logs/build.txt
grep -h "xschem netlist\|TOPOLOGY" logs/backannotation.txt
