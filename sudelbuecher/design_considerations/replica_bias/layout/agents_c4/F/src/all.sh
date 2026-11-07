#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent F (C4): build, check and draw pad_ref_rb (v2).   sh all.sh <inputs dir> <out dir> <work dir>
set -e
S=$(cd "$(dirname "$0")" && pwd); I=$(cd "$1" && pwd); mkdir -p "$2" "$3"; O=$(cd "$2" && pwd); W=$(cd "$3" && pwd)
L=$O/logs; mkdir -p "$L" "$O/previews" "$O/cells/logs"
sh "$S/run.sh" "$I" "$O" "$W"
sh "$S/check.sh" "$O/pad_ref_rb.gds" "$O/pad_ref_rb.cdl" pad_ref_rb "$W/chk" "$L" > "$L/summary.txt"
cp "$W/chk/lvs/pad_ref_rb_extracted.cir" "$L/"
# the capacitor blocks on their own: DRC, maximal + LU, LVS against capgen's CDL, symmetry
: > "$O/cells/logs/sym_caps.txt"
for c in capr capm capt capv; do
  sh "$S/check.sh" "$O/cells/rb_caps.gds" "$O/cells/rb_caps.cdl" $c "$W/chk_$c" "$O/cells/logs" >> "$L/summary.txt"
  echo "== $c" >> "$O/cells/logs/sym_caps.txt"; python3 -B "$I/sym_check.py" "$O/cells/rb_caps.gds" $c >> "$O/cells/logs/sym_caps.txt" 2>&1
done
python3 -B "$S/metal_conn.py" "$O/pad_ref_rb.gds" pad_ref_rb > "$L/metal_conn.txt"
python3 -B "$S/row_xor.py" "$O/pad_ref_rb.gds" "$I/P3/rb_avg_v3.gds" "$I/P/rb_p_cells.gds" "$I/N/rb_n_cells.gds" > "$L/row_xor_vs_inputs.txt"
: > "$L/sym_check.txt"
for c in rb_tree_p rb_tails rb_tubs rb_avg rb_tree_n rb_mirror rb_cload rb_casc; do
  o="--no-y"; [ $c = rb_casc ] && o=""
  echo "== $c $o" >> "$L/sym_check.txt"; python3 -B "$I/sym_check.py" "$O/pad_ref_rb.gds" $c $o >> "$L/sym_check.txt" 2>&1
done
# negative LVS test: one gate moved in the reference (BA's gate m -> gh) must not match
sed 's/^Mc_BA c_bd c_m /Mc_BA c_bd c_gh /' "$O/pad_ref_rb.cdl" > "$W/neg.cdl"
python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout="$O/pad_ref_rb.gds" --netlist="$W/neg.cdl" \
    --topcell=pad_ref_rb --run_dir="$W/neg" --disable_tap_extraction > "$W/neg.log" 2>&1 || true
echo "negative LVS test (BA gate m -> gh in the reference): $(grep -oE 'Netlists match|Netlists don.t match' "$W/neg.log" | head -1)" >> "$L/summary.txt"
echo "metal connectivity: $(tail -1 "$L/metal_conn.txt")" >> "$L/summary.txt"
grep -c identical "$L/row_xor_vs_inputs.txt" | sed 's/^/rows identical to the delivered cells: /;s/$/ of 8 placed/' >> "$L/summary.txt"
grep -h summary "$L/sym_check.txt" "$O/cells/logs/sym_caps.txt" | sed 's/^/sym: /' >> "$L/summary.txt"
grep "gate area" "$L/compose_cdl.txt" >> "$L/summary.txt"
grep "block pad_ref_rb" "$L/route.txt" | head -1 >> "$L/summary.txt"
python3 -B "$S/pin_map.py" "$I/P3/rb_avg_v3.gds" "$I/P/rb_p_cells.gds" "$I/N/rb_n_cells.gds" "$O/pad_ref_rb.gds" "$S/rb_place.py" "$O/pin_map.md" "$O/net_list.md" "$O/cells/rb_caps.gds"
R="python3 -B $S/render.py $O/pad_ref_rb.gds $O/netmap.gds $S/rb_place.py"
$R "$O/previews/pad_ref_rb.png"
$R "$O/previews/core.png" 18 32 74.5 62 "vcm_rb core (tails, tubs, avg, mirror), tree_p, tree_n"
$R "$O/previews/top.png" -0.5 44 74.5 76.5 "top: capv, cload over the tubs, capt, the vcm pin"
$R "$O/previews/bottom.png" -0.5 -0.5 74.5 46 "bottom: capr, rb_casc, tree_n / tails / tree_p, vref pin, inputs"
python3 -B "$S/context.py" "$I/slot/slot.klay.gds" "$I/slot/slot7_pins.md" "$O/pad_ref_rb.gds" 535.0 "$O/previews/context.png" 2>/dev/null >> "$L/summary.txt"
cat "$L/summary.txt"
