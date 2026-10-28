#!/bin/sh
# oa_core_pd v2: build and every check, from scratch (run in out/v2; 2026-10-28, Claude). Logs in logs/.
set -e
cd "$(dirname "$0")"
mkdir -p logs
python3 make_oa_pcas_c.py ../../inputs/pad_buffer_cells.gds oa_pcas_c.gds          > logs/oa_pcas_c_build.txt
python3 drc.py oa_pcas_c.gds oa_pcas_c logs/drc_oa_pcas_c.txt                         > /dev/null || true
python3 lvs.py oa_pcas_c.gds oa_pcas_c oa_pcas_c.cdl                                  > logs/lvs_oa_pcas_c.txt 2>&1
(cd configs && python3 ../generator.py oa_core_pd_v2.py ../oa_core_pd.gds)          > logs/build.txt 2>&1
python3 drc.py oa_core_pd.gds oa_core_pd logs/drc_oa_core_pd.txt                      > /dev/null
for c in oa_pmir_c oa_pcas_c oa_ms1 oa_svpg oa_n10 oa_mcs_c; do
  python3 drc.py oa_core_pd.gds $c logs/drc_cell_$c.txt > /dev/null || true
done
python3 lvs.py oa_core_pd.gds oa_core_pd oa_core_pd_ref.cdl - logs/oa_core_pd_ref.lvsdb > logs/lvs_vs_ref.txt 2>&1
sh logs/run_backannotation.sh                                                         > logs/backannotation.txt 2>&1
python3 lvs.py oa_core_pd.gds oa_core_pd backannotation/oa_core_pd_backannotated.cdl - logs/oa_core_pd_backannotated.lvsdb \
                                                                                      > logs/lvs_vs_backannotated.txt 2>&1
python3 area_audit.py process/ihp_sg13cmos5l.py ../oa_core_pd.gds oa_core_pd oa_core_pd.gds oa_core_pd > logs/area_audit.txt
python3 -c "
import sys; sys.path.insert(0, '.')
import generator as G, drc as D
G.selftest(G.load_process('process/ihp_sg13cmos5l.py'), 'logs/selftest.gds', drc=lambda ly, c: [(r[0], r[3]) for r in D.run(ly, c)])
"                                                                                      > logs/selftest_build.txt 2>&1
rm -f logs/selftest.gds.src.gds
python3 drc.py logs/selftest.gds selftest logs/drc_selftest.txt                      > /dev/null
for t in regress_v1cells regress_merged_well; do
  (cd configs && python3 ../generator.py $t.py ../logs/$t.gds)                        > logs/${t}_build.txt 2>&1
  python3 drc.py logs/$t.gds oa_core_pd logs/drc_$t.txt                              > /dev/null
  python3 lvs.py logs/$t.gds oa_core_pd ../oa_core_pd.cdl                            > logs/lvs_$t.txt 2>&1
done
python3 render_block.py process/ihp_sg13cmos5l.py oa_core_pd.png oa_core_pd.gds:oa_core_pd:"oa_core_pd v2 (compact)" --scale 8 > /dev/null
python3 render_block.py process/ihp_sg13cmos5l.py v1_vs_v2.png ../oa_core_pd.gds:oa_core_pd:"v1 (6 library primitives)" oa_core_pd.gds:oa_core_pd:"v2 compact" --scale 11 > /dev/null
python3 render_block.py process/ihp_sg13cmos5l.py rule_savings.png ../oa_core_pd.gds:oa_core_pd:"v1 where the area went" oa_core_pd.gds:oa_core_pd:"v2 what replaced it" --scale 11 --notes logs/savings_notes.json > /dev/null
grep -h "TOTAL" logs/drc_*.txt | sort | uniq -c
grep -h "LVS .* ->" logs/lvs_*.txt
grep -h "block\|UNROUTED\|latch-up" logs/build.txt
