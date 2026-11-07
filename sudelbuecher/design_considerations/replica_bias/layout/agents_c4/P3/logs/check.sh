#!/bin/bash
# usage: check.sh <round>  -- DRC, LVS, sym_check, LU, surround, pad comparison of out/rb_avg_v3.gds; logs to work/r<round>/
R=$1
WS=/tmp/claude-0/-home-user-sg13cmos5l-cm-ip--single2diff2single/f7165478-7787-531e-a1d8-6ec7206ebfcb/scratchpad/layout_rb/P3
cd $WS
export PDK_ROOT=/foss/pdks; source /home/user/sg13cmos5l_cm_ip__single2diff2single/.designinit >/dev/null 2>&1
GDS=out/rb_avg_v3.gds; CDL=out/rb_avg_v3.cdl; c=rb_avg
D=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech
PAD=/home/user/sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/sg13cmos5l_IOPadSingle2Diff.klay.gds
mkdir -p work/r$R
python3 $D/drc/run_drc.py --path=$GDS --topcell=$c --no_density --mp=4 --run_dir=work/r$R/drc > work/r$R/drc.txt 2>&1
python3 $D/lvs/run_lvs.py --layout=$GDS --netlist=$CDL --topcell=$c --run_dir=work/r$R/lvs --disable_tap_extraction > work/r$R/lvs.txt 2>&1
python3 work/sym_check.py $GDS $c --no-y > work/r$R/sym.txt 2>&1
python3 work/sym_check.py $GDS rb_avg_u --no-y >> work/r$R/sym.txt 2>&1
python3 work/sym_check.py $GDS rb_avg_l --no-y >> work/r$R/sym.txt 2>&1
python3 work/lu.py $GDS $c > work/r$R/lu.txt 2>&1
python3 out/logs/surround_v3.py $GDS > work/r$R/surround.txt 2>&1
python3 out/logs/compare_pad_v3.py $GDS $PAD > work/r$R/compare_pad.txt 2>&1
echo "== $c: DRC exc $(grep -ci 'exception' work/r$R/drc.txt); $(grep -o 'Total # of DRC violations.*\|No DRC violations detected\|Violated rules.*' work/r$R/drc.txt | tail -1); LVS $(grep -o 'Netlists match\|Netlists don.t match\|PASS[^|]*\|FAIL[^|]*\|ERROR[^|]*' work/r$R/lvs.txt | tail -1 | tr -s ' '); $(grep summary work/r$R/sym.txt | tr '\n' ' '); $(grep -o 'farthest.*' work/r$R/lu.txt)"
cat work/r$R/surround.txt work/r$R/compare_pad.txt
