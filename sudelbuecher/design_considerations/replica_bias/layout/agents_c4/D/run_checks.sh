#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent D (C4): every check of bias_dist_pd and its cells; summary in logs/summary.txt.
#   cd out && sh run_checks.sh <run dir>
R=$1; L=logs; I=../inputs; mkdir -p $L
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=ihp-sg13cmos5l
{
echo "== DRC (run_drc.py --no_density, exception count), maximal + latchUpRules, LVS --disable_tap_extraction"
sh check.sh bias_dist_pd.gds bias_dist_pd.cdl bias_dist_pd $R $L
for c in nand2_hv inv_hv tg_hv bdp_slice bdp_tdn bdp_svpd bdp_mirror_n bdp_mirror_p; do
  sh check.sh cells/$c.gds cells/$c.cdl $c $R $L; done
echo "== negative LVS: TIP0's gate ei0_b -> ei0 in the reference"
sed 's/^MTIP0 iin0 ei0_b ni vddh/MTIP0 iin0 ei0 ni vddh/' bias_dist_pd.cdl > $R/bias_dist_pd_neg.cdl
python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout=$(realpath bias_dist_pd.gds) \
  --netlist=$(realpath $R/bias_dist_pd_neg.cdl) --topcell=bias_dist_pd --run_dir=$(realpath $R)/lvs_neg \
  --disable_tap_extraction > $L/bias_dist_pd_lvs_negative.log 2>&1
echo "negative LVS: $(grep -oE 'Netlists match|Netlists don.t match' $L/bias_dist_pd_lvs_negative.log | head -1)"
echo "== sym_check (one row each: --no-y)"
for c in bdp_mirror_n bdp_mirror_p; do python3 -I $I/sym_check.py cells/$c.gds $c --no-y; done
echo "== sym_check N check (narrow contacted poly beyond the endcap zone) on the switch cells and the flat top cell"
for c in nand2_hv inv_hv tg_hv bdp_slice bdp_tdn bdp_svpd; do
  python3 -I $I/sym_check.py cells/$c.gds $c --no-y | grep -E "^ +N |summary" | sed "s/^/$c: /"; done
python3 -I $I/sym_check.py bias_dist_pd.gds bias_dist_pd --no-y | grep -E "^ +N |summary" | sed "s/^/bias_dist_pd (flat): /"
echo "== contacted gate poly outside Activ (no endcap-zone subtraction)"
for c in nand2_hv inv_hv tg_hv bdp_slice bdp_tdn bdp_svpd; do python3 -I extra.py poly cells/$c.gds $c; done
echo "== supply connectivity through tie Activ / Cont / M1 / Via1 / M2 only"
python3 -I extra.py metal bias_dist_pd.gds bias_dist_pd
echo "== bdp_mirror_n vs N's rb_mirror (all layers)"
python3 -I extra.py xor cells/bdp_mirror_n.gds bdp_mirror_n $I/N/rb_n_cells.gds rb_mirror
echo "== bdp_mirror_p vs P's rb_tails, left row end (D + PO0 slot), rows only (ring strips excluded)"
python3 -I extra.py xor cells/bdp_mirror_p.gds bdp_mirror_p $I/P/rb_p_cells.gds rb_tails -1 0.35 11.5 7.6
echo "== same window with the ring strips"
python3 -I extra.py xor cells/bdp_mirror_p.gds bdp_mirror_p $I/P/rb_p_cells.gds rb_tails -1 -2 11.5 9
} 2>&1 | grep -v "psutil\|tkinter" | tee $L/summary.txt
