#!/bin/bash
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# G7 / G8 of docs/replica_bias/SURVEY.md: the pads' CACE suites with changed defaults (temporary yaml copies, see
# run_cace_copy.py), results into the replica macros. Run from the repo root after: export PDK_ROOT=/foss/pdks; source .designinit
set -u
B=macros/vcm_rb/verification/baseline
R=macros/vref_s2d_rb/verification/baseline
D2S=sg13cmos5l_IOPadDiff2Single
S2D=sg13cmos5l_IOPadSingle2Diff
date -u +%FT%TZ
# G7: D2S at the new reference (vref = vicm = vterm = 1.2 V) and, for continuity, at the suite's 1.65 V, current schematic
python3 -I $B/run_cace_copy.py --pad $D2S --yaml $D2S.yaml --set vref=1.2 vicm=1.2 vterm=1.2 --tag d2s_1v2 \
  --out $B/d2s_1v2 --groups dc_params dc_3v0_params ac_params tran_params pd_params enable_params -j 4
python3 -I $B/run_cace_copy.py --pad $D2S --yaml $D2S.yaml --tag d2s_1v65 \
  --out $B/d2s_1v65 --groups dc_params dc_3v0_params ac_params tran_params pd_params enable_params -j 4
python3 -I $B/run_cace_copy.py --pad $D2S --yaml d2s_mpdda_pd_sel.yaml --set vref=1.2 vicm=1.2 vterm=1.2 --tag loop_1v2 \
  --out $B/d2s_loop_1v2 --groups loop_params -j 4
python3 -I $B/run_cace_copy.py --pad $D2S --yaml d2s_mpdda_pd_sel.yaml --tag loop_1v65 \
  --out $B/d2s_loop_1v65 --groups loop_params -j 4
# G8: S2D mismatch and process Monte Carlo at the chosen operating point (vref 0.5 V, vcm 1.2 V), schematic
python3 -I $B/run_cace_copy.py --pad $S2D --yaml $S2D.yaml --set vref=0.5 --tag s2d_mc_0v5 \
  --out $R/s2d_mc_vref0v5 --groups mm_params ac_mm_params mc_params -j 4
date -u +%FT%TZ
