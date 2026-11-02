#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Agent F, C2 2026-10-31: rebuild every cell of F and the pad candidate from scratch, then run the checks.
#   sh run_all.sh <out_dir> <run_dir>
set -e
S=$(dirname "$0"); O=$1; R=$2
mkdir -p "$O/cells" "$R"
python3 "$S/build_d2s_rhigh.py" "$O/cells/d2s_rhigh.gds" "$O/cells/d2s_rhigh.cdl"
python3 "$S/build_bias_tree_pd.py" "$O/cells/bias_tree_pd.gds" "$O/cells/bias_tree_pd.cdl"
python3 "$S/build_block.py" "$O/cells/d2s_block.gds" "$O/cells/d2s_block.cdl"
python3 "$S/build_pad.py" "$O/pad_candidate.gds" "$O/cells" "$O/cells/d2s_block.gds"
python3 "$S/compose_pad_cdl.py" "$O/cells/d2s_block.cdl" "$O/pad_candidate.cdl"
