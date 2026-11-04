#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F (C3) stage A: per changed cell IHP run_drc.py (--no_density), the maximal deck with latch-up, IHP LVS
# (--disable_tap_extraction), sym_check.py.   sh check_cells.sh <gds> <cdl> <run_dir> <cell>[:no-y] ...
G=$1; C=$2; R=$3; shift 3
T=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech
S=${SYMCHECK:-$(cd "$(dirname "$0")/../../inputs" && pwd)/sym_check.py}
mkdir -p "$R"
for spec in "$@"; do
  cell=${spec%%:*}; opt=""
  [ "$spec" != "$cell" ] && opt="--no-y"
  d=$R/$cell; mkdir -p "$d"
  python3 $T/drc/run_drc.py --path="$G" --topcell="$cell" --no_density --mp=4 --run_dir="$d/drc" > "$d/drc.log" 2>&1
  klayout -b -r $T/drc/rule_decks/sg13cmos5l_maximal.drc -rd input="$G" -rd topcell="$cell" \
      -rd report="$d/maximal.lyrdb" -rd latchUpRules=true -rd thr=4 > "$d/maximal.log" 2>&1
  python3 $T/lvs/run_lvs.py --layout="$G" --netlist="$C" --topcell="$cell" --run_dir="$d/lvs" \
      --disable_tap_extraction > "$d/lvs.log" 2>&1
  python3 -B $S "$G" "$cell" $opt > "$d/sym.txt" 2>&1
  exc=$(grep -c "exception" "$d/drc.log")
  drc=$(grep -oE "No DRC violations detected|Violated rules are : .*|Total DRC violations.*" "$d/drc.log" | tail -1)
  mx=$(grep -oE "Number of DRC errors for maximum rule set: [0-9]+" "$d/maximal.log" | grep -oE "[0-9]+$"); lu=$(grep -c "Rule LU" "$d/maximal.log")
  lvs=$(grep -oE "Netlists match|Netlists don.t match" "$d/lvs.log" | head -1)
  sym=$(grep -i summary "$d/sym.txt")
  echo "$cell | DRC: $drc (exception lines $exc) | maximal errors: $mx (LU rules run: $lu) | LVS: $lvs | $sym"
done
