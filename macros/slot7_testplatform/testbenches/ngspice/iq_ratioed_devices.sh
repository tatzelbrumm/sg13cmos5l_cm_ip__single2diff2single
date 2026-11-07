#!/bin/bash
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Static current of the always-on devices of tp_en_ctrl / tp_en_ctrl_b (operating point, schematic devices):
#   PU<k>: hv PMOS 0.3/20, gate on vss_3v3, drain at xb<k> ~ 0.05 V (channel enabled) -> current from vdd_3v3 per channel
#   NRD  : hv NMOS 0.3/20, gate on vdd_3v3, drain on vdd_1v2 (stage A only)  -> current from vdd_1v2, always
# Usage (from this directory): export PDK_ROOT=/foss/pdks PDK=ihp-sg13cmos5l; ./iq_ratioed_devices.sh
# Writes results_iq/iq_ratioed_devices.txt; netlists in a temporary directory.
set -e
OUT=$(pwd)/results_iq/iq_ratioed_devices.txt
D=$(mktemp -d); cp "$PDK_ROOT/$PDK/libs.tech/ngspice/.spiceinit" "$D/"; cd "$D"
echo "# corner temp  I_PU_per_enabled_channel(A, from vdd_3v3)  I_NRD(A, from vdd_1v2; ngspice sign: negative = delivered)" > "$OUT"
for c in tt:27 ss:-40 ss:27 ff:27 ff:125; do co=${c%%:*}; T=${c##*:}
cat > tb.cir <<CIR
* static current of the ratioed pull-up and of NRD
.lib cornerMOShv.lib mos_$co
.temp $T
V3 vdd3 0 3.3
V1 vdd1 0 1.2
Vx xb 0 0.05
XPU xb 0 vdd3 vdd3 sg13_hv_pmos w=0.3u l=20u ng=1
XNRD vdd1 vdd3 0 0 sg13_hv_nmos w=0.3u l=20u ng=1
.control
op
echo "RESULT $co $T \$&i(Vx) \$&v1#branch"
.endc
.end
CIR
ngspice -b tb.cir 2>&1 | sed -n 's/^RESULT //p' >> "$OUT"
done
cat "$OUT"
