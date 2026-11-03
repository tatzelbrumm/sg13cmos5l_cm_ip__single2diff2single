#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F2 stage B: checks of a run_all_B.sh output dir.   sh run_checks_B.sh <out_dir> <log_dir>
S=$(cd "$(dirname "$0")" && pwd); O=$(cd "$1" && pwd); L=$(mkdir -p "$2" && cd "$2" && pwd)
T=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech; P=sg13cmos5l_IOPadDiff2Single
N=/home/user/sudel/sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_2026-10-31
R=$L/runs; rm -rf "$R"; mkdir -p "$R"
python3 $T/drc/run_drc.py --path="$O/pad_candidate.gds" --topcell=$P --no_density --antenna --mp=4 --run_dir="$R/pad_drc" > "$L/pad_drc.log" 2>&1
python3 $T/lvs/run_lvs.py --layout="$O/pad_candidate.gds" --netlist="$O/pad_candidate.cdl" --topcell=$P --run_dir="$R/pad_lvs" \
  --disable_tap_extraction --ignore_top_ports_mismatch > "$L/pad_lvs.log" 2>&1
python3 $T/lvs/run_lvs.py --layout="$O/cells/d2s_block.gds" --netlist="$O/cells/d2s_block.cdl" --topcell=d2s_block \
  --run_dir="$R/block_lvs" --disable_tap_extraction --ignore_top_ports_mismatch --implicit_nets=iovdd,iovss,pad > "$L/block_lvs.log" 2>&1
mkdir -p "$L/row_check"; python3 -B $N/row_check.py "$O/pad_candidate.gds" $P "$L/row_check" > "$L/row_check/stdout.txt" 2>&1
rm -f "$L/row_check/row.gds"
python3 -B $N/path_widths.py "$O/pad_candidate.gds" $P 1.5,4,26.4,38.5,52.2,64.5,84.3 > "$L/path_widths_pad_candidate.md" 2>&1
python3 -B "$S/gate_metal.py" "$O/cells/d2s_block.gds" > "$L/router_metal_over_gates.txt"
mkdir -p "$R/pex"; cp "$O/pad_candidate.gds" "$R/pex/$P.gds"
( cd "$R/pex" && PDK_ROOT=/foss/pdks PDK=ihp-sg13cmos5l PDKPATH=/foss/pdks/ihp-sg13cmos5l sak-pex.sh -m 2 -w "$R/pex" $P.gds > pex.log 2>&1 )
python3 -B /home/user/sg13cmos5l_cm_ip__single2diff2single/scripts/cace/pex_for_sim.py "$R/pex/$P.pex.spice" "$R/pex/tied.spice" \
  --tie iovss 1e12 > "$L/pex_capacitor_only_nodes.txt"; grep "^Rtie" "$R/pex/tied.spice" >> "$L/pex_capacitor_only_nodes.txt"
{ echo "pad DRC: $(grep -oE 'Check Passed|Violated rules are : .*' "$L/pad_drc.log") (exceptions $(grep -c 'generated an exception' "$L/pad_drc.log"), antenna table run: $(grep -c 'antenna runset' "$L/pad_drc.log"))"
  echo "pad LVS: $(grep -oE 'PASS \(netlists match\)|FAIL[^|]*' "$L/pad_lvs.log" | head -1)"
  echo "block LVS: $(grep -oE 'PASS \(netlists match\)|FAIL[^|]*' "$L/block_lvs.log" | head -1)"
  echo "row check: $(grep -c DIFFERENT "$L/row_check/edges.md") edge layers DIFFERENT, $(grep -c FAIL "$L/row_check/nets.md") bands / rails FAIL"
  echo "router metal over gates: $(tail -1 "$L/router_metal_over_gates.txt")"
  echo "PEX (magic, C-coupled, mode 2): $(head -1 "$L/pex_capacitor_only_nodes.txt")"; } > "$L/summary.txt"
cat "$L/summary.txt"
