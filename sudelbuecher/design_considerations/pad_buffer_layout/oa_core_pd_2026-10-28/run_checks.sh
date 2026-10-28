#!/bin/sh
# Rebuild oa_core_pd.gds and rerun every check; logs in logs/. Needs python3 with klayout (pip, >= 0.28) and matplotlib.
set -e
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
L=../inputs/pad_buffer_cells.gds
python3 oa_core_pd_build.py $L oa_core_pd.gds                                   > logs/build.txt
python3 selftest/check_inputs.py                                               > logs/inputs_check.txt
python3 oa_core_pd_verify.py oa_core_pd.gds $L                                 > logs/verify.txt
python3 oa_core_pd_drc.py oa_core_pd.gds oa_core_pd logs/drc_oa_core_pd.txt
python3 oa_core_pd_lvs.py oa_core_pd.gds oa_core_pd oa_core_pd.cdl - oa_core_pd.lvsdb > logs/lvs_oa_core_pd.txt
: > logs/drc_lib_cells.txt; : > logs/lvs_lib_cells.txt
for c in oa_pmir oa_pcas oa_misc_p oa_nmir oa_mcs oa_misc_n; do
  python3 oa_core_pd_drc.py $L $c logs/tmp.txt; cat logs/tmp.txt >> logs/drc_lib_cells.txt
  j=""; [ $c = oa_misc_n ] && j="--join"          # ks and vpc are split inside oa_misc_n; the parent joins them
  python3 oa_core_pd_lvs.py $L $c ../inputs/pad_buffer_cells.cdl $c logs/tmp.lvsdb $j >> logs/lvs_lib_cells.txt
done
rm -f logs/tmp.txt logs/tmp.lvsdb
python3 selftest/drc_selftest.py > logs/selftest_drc.txt
python3 selftest/lvs_selftest.py > logs/selftest_lvs.txt
python3 oa_core_pd_render.py oa_core_pd.gds oa_core_pd.cdl
sha256sum oa_core_pd.gds
