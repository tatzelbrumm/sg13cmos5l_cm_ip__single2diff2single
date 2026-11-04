#!/bin/bash
# usage: check.sh <round> [cells...]  -- DRC, LVS, sym_check of out/s2d_p3_cells.gds, logs to work/r<round>/
R=$1; shift
WS=/tmp/claude-0/-home-user-sg13cmos5l-cm-ip--single2diff2single/9625f5bb-27cd-530e-a9cf-d1aa15a8223d/scratchpad/agents/P
cd $WS
GDS=out/s2d_p3_cells.gds; CDL=out/s2d_p3_cells.cdl
D=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech
mkdir -p work/r$R
for c in "$@"; do
  python3 $D/drc/run_drc.py --path=$GDS --topcell=$c --no_density --mp=4 --run_dir=work/r$R/drc_$c > work/r$R/drc_$c.txt 2>&1
  python3 $D/lvs/run_lvs.py --layout=$GDS --netlist=$CDL --topcell=$c --run_dir=work/r$R/lvs_$c --disable_tap_extraction $([ $c = s2d_inputs_c3 ] && echo --run_mode=deep) > work/r$R/lvs_$c.txt 2>&1
  ny=""; case $c in s2d_pd_p_c3|bias_tree_noab_p_c3|tub_p20x1_c3) ny="--no-y";; esac
  python3 inputs/sym_check.py $GDS $c $ny > work/r$R/sym_$c.txt 2>&1
  echo "== $c: DRC exc $(grep -ci 'exception' work/r$R/drc_$c.txt); $(grep -o 'Total # of DRC violations.*\|No DRC violations detected\|Violated rules.*' work/r$R/drc_$c.txt | tail -1); LVS $(grep -o 'Netlists match\|Netlists don.t match\|PASS[^|]*\|FAIL[^|]*\|ERROR[^|]*' work/r$R/lvs_$c.txt | tail -1); $(grep summary work/r$R/sym_$c.txt)"
done
