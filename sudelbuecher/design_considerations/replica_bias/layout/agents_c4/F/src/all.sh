#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent F (C4): build, check and draw pad_ref_rb.   sh all.sh <inputs dir> <out dir> <work dir>
set -e
S=$(cd "$(dirname "$0")" && pwd); I=$(cd "$1" && pwd); mkdir -p "$2" "$3"; O=$(cd "$2" && pwd); W=$(cd "$3" && pwd)
L=$O/logs; mkdir -p "$L" "$O/previews"
sh "$S/run.sh" "$I" "$O" "$W"
sh "$S/check.sh" "$O/pad_ref_rb.gds" "$O/pad_ref_rb.cdl" pad_ref_rb "$W/chk" "$L" > "$L/summary.txt"
cp "$W/chk/lvs/pad_ref_rb_extracted.cir" "$L/"
python3 -B "$S/metal_conn.py" "$O/pad_ref_rb.gds" pad_ref_rb > "$L/metal_conn.txt"
python3 -B "$S/row_xor.py" "$O/pad_ref_rb.gds" "$I/P3/rb_avg_v3.gds" "$I/P/rb_p_cells.gds" "$I/N/rb_n_cells.gds" > "$L/row_xor_vs_inputs.txt"
: > "$L/sym_check.txt"
for c in rb_tree_p rb_tails rb_tubs rb_avg rb_tree_n rb_mirror rb_cload bypass_rb_f rb_casc; do
  o="--no-y"; [ $c = rb_casc ] && o=""; [ $c = bypass_rb_f ] && o=""
  echo "== $c $o" >> "$L/sym_check.txt"; python3 -B "$I/sym_check.py" "$O/pad_ref_rb.gds" $c $o >> "$L/sym_check.txt" 2>&1
done
# F's changed copy on its own: DRC, maximal + LU, LVS against its CDL
sh "$S/check.sh" "$O/cells/rb_f_cells.gds" "$O/cells/rb_f_cells.cdl" bypass_rb_f "$W/chk_f" "$O/cells/logs" >> "$L/summary.txt"
# negative LVS test: one gate moved in the reference (BA's gate m -> gh) must not match
sed 's/^Mc_BA c_bd c_m /Mc_BA c_bd c_gh /' "$O/pad_ref_rb.cdl" > "$W/neg.cdl"
python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout="$O/pad_ref_rb.gds" --netlist="$W/neg.cdl" \
    --topcell=pad_ref_rb --run_dir="$W/neg" --disable_tap_extraction > "$W/neg.log" 2>&1 || true
echo "negative LVS test (BA gate m -> gh in the reference): $(grep -oE 'Netlists match|Netlists don.t match' "$W/neg.log" | head -1)" >> "$L/summary.txt"
echo "metal connectivity: $(tail -1 "$L/metal_conn.txt")" >> "$L/summary.txt"
grep -c identical "$L/row_xor_vs_inputs.txt" | sed 's/^/rows identical to the delivered cells: /;s/$/ of 9/' >> "$L/summary.txt"
python3 -B "$S/pin_map.py" "$I/P3/rb_avg_v3.gds" "$I/P/rb_p_cells.gds" "$I/N/rb_n_cells.gds" "$O/pad_ref_rb.gds" "$S/rb_place.py" "$O/pin_map.md" "$O/net_list.md" "$O/cells/rb_f_cells.gds"
R="python3 -B $S/render.py $O/pad_ref_rb.gds $O/netmap.gds $S/rb_place.py"
$R "$O/previews/pad_ref_rb.png"
$R "$O/previews/core.png" 16 55 78 99.5 "vcm_rb core (tubs, tails, avg, mirror) and the bias tree"
$R "$O/previews/ports.png" 55 80 78 99.5 "the port group on the right edge"
$R "$O/previews/left_channel.png" -0.5 36 36 75 "left channel: vssh / vddh rails, casc's vdd strap, vbnc"
python3 -B "$S/context.py" "$I/slot/slot.klay.gds" "$I/slot/slot7_pins.md" "$O/pad_ref_rb.gds" 446.78 20.0 "$O/previews/context.png" >> "$L/summary.txt"
cat "$L/summary.txt"
