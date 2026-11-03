#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F2 stage A: IHP DRC (main tables + maximal incl. latch-up), IHP LVS, sym_check.py of every changed cell.
#   sh check_cells.sh <gds> <cdl> <run_dir> <cell>[:no-y] ...
G=$1; C=$2; R=$3; shift 3
T=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech
S=/home/user/sudel/sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_2026-10-31/sym_check.py
mkdir -p "$R"
for spec in "$@"; do
  cell=${spec%%:*}; opt=""
  [ "$spec" != "$cell" ] && opt="--no-y"
  d=$R/$cell; mkdir -p "$d"
  python3 $T/drc/run_drc.py --path="$G" --topcell="$cell" --no_density --mp=4 --run_dir="$d/drc" > "$d/drc.log" 2>&1
  python3 $T/lvs/run_lvs.py --layout="$G" --netlist="$C" --topcell="$cell" --run_dir="$d/lvs" \
      --disable_tap_extraction > "$d/lvs.log" 2>&1
  python3 -B $S "$G" "$cell" $opt > "$d/sym.txt" 2>&1
  exc=$(grep -c "generated an exception" "$d/drc.log")
  drc=$(grep -E "Check Passed|Violated rules|Total" "$d/drc.log" | tail -1)
  lvs=$(grep -ciE "netlists match|congratulations" "$d/lvs.log")
  sym=$(grep summary "$d/sym.txt")
  echo "$cell | DRC: $drc (exceptions $exc) | LVS match lines: $lvs | $sym"
done
