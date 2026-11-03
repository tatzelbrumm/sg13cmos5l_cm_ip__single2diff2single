#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F2 stage B: rebuild everything from the reviewed primitives: cells, pad context, block (placed and routed by
# generator.py), pad candidate, reference netlists, pictures.   sh run_all_B.sh <out_dir>
set -e
S=$(cd "$(dirname "$0")" && pwd); O=$(mkdir -p "$1" && cd "$1" && pwd)
P2=/home/user/sudel/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/P2/out
mkdir -p "$O/cells" "$O/padctx" "$O/previews"
export F2CELLS="$O/cells"
python3 -B "$S/build_f2b_n.py" "$O/cells/d2s_f2b_n_cells.gds" "$O/cells/d2s_f2b_n_cells.cdl" > "$O/cells/build_n.txt"
python3 -B "$S/build_f2b_p.py" "$O/cells/d2s_f2b_p_cells.gds" "$O/cells/d2s_f2b_p_cells.cdl" > "$O/cells/build_p.txt"
python3 -B "$S/build_f2b_sp.py" "$O/cells/d2s_f2b_sp_cells.gds" "$O/cells/d2s_f2b_sp_cells.cdl" > "$O/cells/build_sp.txt"
python3 -B "$S/src_F/build_pad.py" "$O/padctx/pad_ctx.gds" "$O/padctx" > "$O/padctx/build.txt"
python3 -B "$S/make_ctx.py" "$O/padctx/pad_ctx.gds" "$O/cells/ctx.gds"
python3 -B "$S/make_pwr.py" "$O/cells/pwr.gds"
python3 -B "$S/strip_tub_labels.py" "$P2/d2s_p2_cells.gds" "$O/cells/p2_tubnolabel.gds"
cp "$O/cells/d2s_f2b_n_cells.gds" "$O/cells/f2b_n.gds"; cp "$O/cells/d2s_f2b_p_cells.gds" "$O/cells/f2b_p.gds"
cp "$O/cells/d2s_f2b_sp_cells.gds" "$O/cells/f2b_sp.gds"
python3 -B "$S/route_block.py" "$S/block_cfg.py" "$O/cells/d2s_block.gds" > "$O/cells/route.txt"
rm -f "$O/cells/f2b_n.gds" "$O/cells/f2b_p.gds" "$O/cells/f2b_sp.gds"
python3 -B "$S/build_pad_B.py" "$O/padctx/pad_ctx.gds" "$O/cells/d2s_block.gds" "$O/pad_candidate.gds"
python3 -B "$S/compose_cdl.py" "$P2/d2s_p2_cells.cdl" "$O/cells/d2s_f2b_p_cells.cdl" "$O/cells/d2s_f2b_n_cells.cdl" \
    "$O/cells/d2s_f2b_sp_cells.cdl" "$O/cells/d2s_block.cdl" "$O/pad_candidate.cdl"
