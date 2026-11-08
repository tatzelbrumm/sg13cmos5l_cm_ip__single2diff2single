#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Claude, agent F (C4): build pad_ref_rb.   sh run.sh <inputs dir> <out dir> <work dir>
set -e
S=$(cd "$(dirname "$0")" && pwd); I=$(cd "$1" && pwd); mkdir -p "$2" "$3"; O=$(cd "$2" && pwd); W=$(cd "$3" && pwd)
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=ihp-sg13cmos5l PDKPATH=/foss/pdks/ihp-sg13cmos5l FCELLS="$W/cells" FINPUTS="$I"
mkdir -p "$W/cells" "$O/logs"
python3 -B "$S/build_f_cells.py" "$I" "$W/cells" > "$O/logs/build_f_cells.txt" 2>&1
mkdir -p "$O/cells"; cp "$W/cells/rb_f_cells.gds" "$W/cells/rb_f_cells.cdl" "$O/cells/"
python3 -B "$S/make_frame.py" "$S/rb_place.py" "$W/cells/frame_f.gds" > "$O/logs/route.txt"
python3 -B "$S/route_rb.py" "$S/rb_cfg.py" "$W/routed.gds" "$O/netmap.gds" >> "$O/logs/route.txt" 2>&1
python3 -B "$S/finalize.py" "$W/routed.gds" "$O/pad_ref_rb.gds" "$S/rb_place.py" >> "$O/logs/route.txt"
C=$I/circuit
python3 -B "$S/compose_cdl_rb.py" "$O/pad_ref_rb.cdl" $C/pad_ref_rb.spice $C/vcm_rb.spice $C/vref_s2d_rb.spice > "$O/logs/compose_cdl.txt"
grep -E "round|failed|ports" "$O/logs/route.txt"
