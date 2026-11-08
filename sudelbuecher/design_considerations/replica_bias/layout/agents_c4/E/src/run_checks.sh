#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent E (C4): every check of ls_up_fs and en_ctrl_3v3; summary in ../out/logs/summary.txt
#   cd work && sh run_checks.sh      (after: export PDK_ROOT=/foss/pdks; source .designinit in the repo)
R=runs; L=../out/logs; O=../out; X=exp; mkdir -p $L $X
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=ihp-sg13cmos5l
T=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py
lvs() { python3 $T --layout=$(realpath $1) --netlist=$(realpath $2) --topcell=$3 --run_dir=$(realpath $X)/lvs_$4 \
          --disable_tap_extraction > $L/lvs_$4.log 2>&1; echo "$4: $(grep -oE 'Netlists match|Netlists don.t match' $L/lvs_$4.log | head -1)"; }
{
echo "== DRC (run_drc.py --no_density, exception count), maximal + latchUpRules, LVS --disable_tap_extraction"
sh check.sh $O/ls_up_fs.gds $O/ls_up_fs.cdl ls_up_fs $R $L
sh check.sh $O/en_ctrl_3v3.gds $O/en_ctrl_3v3.cdl en_ctrl_3v3 $R $L
echo "== negative LVS (must not match): XPF gate y -> in; XS0 / XS1 outputs swapped"
sed 's/^MPF x y vddh vddh/MPF x in vddh vddh/' $O/ls_up_fs.cdl > $X/ls_neg.cdl
sed 's/^XS0 vddh vss sel0_1v2 sel0_3v3/XS0 vddh vss sel0_1v2 sel1_3v3/; s/^XS1 vddh vss sel1_1v2 sel1_3v3/XS1 vddh vss sel1_1v2 sel0_3v3/' \
    $O/en_ctrl_3v3.cdl > $X/en_neg.cdl
lvs $O/ls_up_fs.gds $X/ls_neg.cdl ls_up_fs ls_up_fs_negative
lvs $O/en_ctrl_3v3.gds $X/en_neg.cdl en_ctrl_3v3 en_ctrl_3v3_negative
echo "== en_ctrl_3v3 without the stubs of vddl / vdd1v2_sense / vdd3v3_sense"
python3 -I nostub.py $O/en_ctrl_3v3.gds $X/en_ctrl_nostub.gds
lvs $X/en_ctrl_nostub.gds $O/en_ctrl_3v3.cdl en_ctrl_3v3 en_ctrl_3v3_nostub
echo "== extracted top pins and devices"
for c in ls_up_fs en_ctrl_3v3; do f=$R/lvs_$c/${c}_extracted.cir
  echo "$c pins: $(sed -n '/^.SUBCKT/,/^M/p' $f | grep -v '^M' | tr -d '+\n' | sed 's/  */ /g')"
  grep '^M' $f | awk '{print $6,$7,$8}' | sort | uniq -c | sed "s/^/$c devices: /"; done
echo "== sym_check N check (narrow contacted poly beyond the endcap zone)"
for c in ls_up_fs efs_ls_core efs_inv_hv efs_xn1; do
  python3 -I sym_check.py $O/ls_up_fs.gds $c --no-y | grep -E "^ +N |summary" | sed "s/^/$c: /"; done
python3 -I sym_check.py $O/en_ctrl_3v3.gds en_ctrl_3v3 --no-y | grep -E "^ +N |summary" | sed "s/^/en_ctrl_3v3: /"
echo "== contacted gate poly outside Activ (no endcap-zone subtraction)"
for c in ls_up_fs efs_inv_hv efs_xn1; do python3 -I extra.py poly $O/ls_up_fs.gds $c; done
echo "== supply connectivity through tie Activ / Cont / M1 / Via1 / M2 only"
python3 -I extra.py metal $O/ls_up_fs.gds ls_up_fs
python3 -I extra.py metal $O/en_ctrl_3v3.gds en_ctrl_3v3
echo "== efs_inv_hv vs D's bdp_inv_hv (macros/bias_dist_pd/layout/klayout/bias_dist_pd.klay.gds), all layers"
python3 -I extra.py xor $O/ls_up_fs.gds efs_inv_hv \
  /home/user/sg13cmos5l_cm_ip__single2diff2single/macros/bias_dist_pd/layout/klayout/bias_dist_pd.klay.gds bdp_inv_hv
echo "== gds sha256"; sha256sum $O/*.gds | cut -c1-16
} 2>&1 | grep -v "psutil\|tkinter" | tee $L/summary.txt
