#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# F (C3) stage B: every check of a run_B.sh output dir.   sh checks_B.sh <inputs dir> <inputs_B dir> <out dir> <run dir>
S=$(cd "$(dirname "$0")" && pwd); I=$(cd "$1" && pwd); IB=$(cd "$2" && pwd); O=$(cd "$3" && pwd); mkdir -p "$4"; W=$(cd "$4" && pwd)
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDKPATH=/foss/pdks/ihp-sg13cmos5l FCELLS="$O/cells" FINPUTS="$I" SYMCHECK="$I/sym_check.py"
L=$O/logs; mkdir -p "$L" "$O/cells/logs" "$O/previews"
# changed cells: DRC, maximal + LU, LVS, sym_check; XOR against the primitives they come from
sh "$S/check_cells.sh" "$O/cells/s2d_pins_f.gds" "$O/cells/s2d_pins_f.cdl" "$W/cells" s2d_loads_f s2d_casc_p_f > "$O/cells/logs/summary_B.txt"
sh "$S/check_cells.sh" "$O/cells/s2d_casc_n_f.gds" "$O/cells/s2d_casc_n_f.cdl" "$W/cells" s2d_casc_n_f >> "$O/cells/logs/summary_B.txt"
sh "$S/check_cells.sh" "$O/cells/s2d_tails_f.gds" "$O/cells/s2d_tails_f.cdl" "$W/cells" s2d_tails_hi_f:no-y s2d_tails_lo_f:no-y >> "$O/cells/logs/summary_B.txt"
python3 -B "$S/row_xor.py" "$I/P/s2d_p3_cells.gds" "$O/cells/s2d_tails_f.gds" > "$O/cells/logs/row_xor_vs_P.txt"
for c in s2d_loads_f s2d_casc_p_f s2d_casc_n_f s2d_tails_hi_f s2d_tails_lo_f; do
  mkdir -p "$O/cells/logs/$c"; cp "$W/cells/$c/drc.log" "$W/cells/$c/maximal.log" "$W/cells/$c/lvs.log" "$W/cells/$c/sym.txt" "$O/cells/logs/$c/"
done
python3 -B "$S/xor_cells.py" "$I/P/s2d_p3_cells.gds" "$I/N/s2d_n3_cells.gds" "$O/cells/s2d_pins_f.gds" "$O/cells/s2d_casc_n_f.gds" > "$O/cells/logs/xor_vs_primitives.txt"
# pad: DRC, maximal + LU, deep LVS
sh "$S/pad_checks.sh" "$O" "$W/pad" > /dev/null
python3 -B "$S/circuit_check_pad.py" "$O/pad_candidate.cdl" "$I/circuit" "$IB/s2d_pad_esd_xschem.spice" > "$L/circuit_check.txt"
python3 -B "$S/reserve_check.py" "$O/pad_candidate.gds" > "$L/reserve_check.md"
python3 -B "$S/tpl_xor.py" "$I/template/sg13cmos5l_IOPadSingle2Diff_template.gds" "$O/pad_candidate.gds" > "$L/template_unchanged_B.txt"
mkdir -p "$W/row"; python3 -B "$I/row_check.py" "$O/pad_candidate.gds" sg13cmos5l_IOPadSingle2Diff "$W/row" > "$W/row/stdout.txt" 2>&1
cp "$W/row/edges.md" "$L/row_check_B_edges.md"; cp "$W/row/nets.md" "$L/row_check_B_nets.md"
# PEX (magic, C-coupled, EXT mode 2 as C2 F2): nodes that only capacitors touch
mkdir -p "$W/pex"; cp "$O/pad_candidate.gds" "$W/pex/sg13cmos5l_IOPadSingle2Diff.gds"
( cd "$W/pex" && PDK=ihp-sg13cmos5l sak-pex.sh -m 2 -w "$W/pex" sg13cmos5l_IOPadSingle2Diff.gds > pex.log 2>&1 )
python3 -I /home/user/sg13cmos5l_cm_ip__single2diff2single/scripts/cace/pex_for_sim.py "$W/pex/sg13cmos5l_IOPadSingle2Diff.pex.spice" \
    "$W/pex/tied.spice" --tie iovss 1e12 > "$L/pex_capacitor_only_nodes.txt" 2>&1
grep "^Rtie" "$W/pex/tied.spice" >> "$L/pex_capacitor_only_nodes.txt"
R="python3 -B $S/render_B.py $S/block_cfg.py $O/pad_candidate.gds"
$R "$O/previews/pad_candidate.png"
$R "$O/previews/pad_candidate_input_group.png" 0 104 80 163 "input group: tail-to-tub links, R feeders"
$R "$O/previews/pad_candidate_pockets.png" 0 26 80 112 "pockets: NMOS fold, PMOS output stage, vin"
$R "$O/previews/pad_candidate_top.png" 0 144 80 181 "top band: core-side pins, cload, pd_p, bias tree"
{ echo "changed cells:"; cat "$O/cells/logs/summary_B.txt"; cat "$O/cells/logs/xor_vs_primitives.txt"
  cat "$L/pad_checks.txt"; tail -1 "$L/circuit_check.txt"; tail -1 "$L/reserve_check.md"; tail -1 "$L/template_unchanged_B.txt"
  echo "row_check: bands / rails pass $(grep -c '| pass' "$L/row_check_B_nets.md") of $(($(grep -c '^| ' "$L/row_check_B_nets.md") - 1)), edge layers DIFFERENT $(grep -c DIFFERENT "$L/row_check_B_edges.md")"
  echo "PEX: $(head -1 "$L/pex_capacitor_only_nodes.txt")"; } > "$L/summary_B.txt"
cat "$L/summary_B.txt"
# stage B2: lengths and parallel runs of the long nets (before = out/stageB_v1, if present), the long-net picture
NM="python3 -B $S/net_metrics.py"; N="pad vbp vbnc vbn outp outn"
{ echo "## after (this pad candidate)"; $NM "$L/pad_candidate.lvsdb" "$O/pad_candidate.gds" $N
  $NM "$L/pad_candidate.lvsdb" "$O/pad_candidate.gds" pad --d=0.69 | sed -n '/longest/,$p'
  if [ -f "$O/stageB_v1/logs/pad_candidate.lvsdb" ]; then
    echo; echo "## before (stageB_v1)"; $NM "$O/stageB_v1/logs/pad_candidate.lvsdb" "$O/stageB_v1/pad_candidate.gds" $N
    $NM "$O/stageB_v1/logs/pad_candidate.lvsdb" "$O/stageB_v1/pad_candidate.gds" pad --d=0.69 | sed -n '/longest/,$p'; fi
} > "$L/long_nets_B2.md" 2>&1
python3 -B "$S/render_nets.py" "$L/pad_candidate.lvsdb" "$O/pad_candidate.gds" "$O/previews/long_nets_B2.png" \
    'pad:#1f4fff' 'vbp:#e01010' 'vbnc:#10a010' --shield '#ff9f1f'
