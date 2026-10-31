#!/bin/bash
# usage: check.sh <round> [cells...]  -- DRC, LVS, sym_check of out/d2s_p2_cells.gds, logs to work/r<round>/
R=$1; shift
cd /home/user/c2/P2
GDS=out/d2s_p2_cells.gds; CDL=out/d2s_p2_cells.cdl
D=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech
mkdir -p work/r$R
for c in "$@"; do
  python3 $D/drc/run_drc.py --path=$GDS --topcell=$c --no_density --mp=4 --run_dir=work/r$R/drc_$c > work/r$R/drc_$c.txt 2>&1
  python3 $D/lvs/run_lvs.py --layout=$GDS --netlist=$CDL --topcell=$c --run_dir=work/r$R/lvs_$c --disable_tap_extraction $([ $c = d2s_inputs_c2 ] && echo --run_mode=deep) > work/r$R/lvs_$c.txt 2>&1
  ny=""; case $c in d2s_ab_p_c2|d2s_pd_p_c2|bias_tree_p_c2|tub_p20x1_c2) ny="--no-y";; esac
  python3 inputs/sym_check.py $GDS $c $ny > work/r$R/sym_$c.txt 2>&1
  echo "== $c: DRC $(grep -c 'generated an exception' work/r$R/drc_$c.txt) exc; $(grep -o 'Total # of DRC violations.*\|No DRC violations detected\|violations[^|]*' work/r$R/drc_$c.txt | tail -1); LVS $(grep -o 'Netlists match\|Netlists don.t match\|PASS[^|]*\|FAIL[^|]*' work/r$R/lvs_$c.txt | tail -1); $(grep summary work/r$R/sym_$c.txt)"
done
