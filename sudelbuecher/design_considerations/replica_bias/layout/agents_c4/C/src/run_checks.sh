#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent C (C4): checks of s7_ctrl (from E's src/run_checks.sh / check.sh). Run from $WS/work after
#   cd <repo> && export PDK_ROOT=/foss/pdks && source .designinit
E=/home/user/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/replica_bias/layout/agents_c4/E/src
O=../out; L=$O/logs; T=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py; export PDK=ihp-sg13cmos5l
sh $E/check.sh $O/s7_ctrl.gds $O/s7_ctrl.cdl s7_ctrl runs $L        # run_drc.py, maximal + latchUpRules, LVS
sed 's/^XT1 vddh vss ld ld_b outp vinp tg_hv/XT1 vddh vss ld_b ld outp vinp tg_hv/' $O/s7_ctrl.cdl > s7_ctrl_neg.cdl
python3 $T --layout=$(realpath $O/s7_ctrl.gds) --netlist=$(realpath s7_ctrl_neg.cdl) --topcell=s7_ctrl \
  --run_dir=$(realpath .)/runs/lvs_neg --disable_tap_extraction > $L/s7_ctrl_lvs_negative.log 2>&1
python3 -I $E/sym_check.py $O/s7_ctrl.gds s7_ctrl --no-y > $L/sym_check.log 2>&1
python3 -I $E/extra.py metal $O/s7_ctrl.gds s7_ctrl; python3 -I $E/extra.py poly $O/s7_ctrl.gds s7_ctrl
(cd .. && python3 out/src/ident.py)
