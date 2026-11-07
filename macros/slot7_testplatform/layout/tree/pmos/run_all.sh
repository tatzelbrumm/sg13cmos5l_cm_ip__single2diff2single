#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# tree_pmos: build, PDK DRC, Magic+Netgen LVS, geometric checks, pictures. Run from anywhere.
# Logs: tree_pmos_drc.lyrdb, tree_pmos_drc.log, tree_pmos_lvs.log, tree_pmos_lvs.out, tree_pmos_checks.txt
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../../../.." && pwd)
export PDK_ROOT=${PDK_ROOT:-/foss/pdks}
export PDK=${PDK:-ihp-sg13cmos5l}
cd "$REPO"
. ./.designinit
cd "$HERE"
python3 build_tree_pmos.py 2>&1 | grep -v -e psutil -e tkinter
sha256sum tree_pmos.gds tree_pmos.spice
klayout -b -zz -r "$PDK_ROOT/$PDK/libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc" -rd input=tree_pmos.gds \
  -rd report=tree_pmos_drc.lyrdb -rd feol=True -rd beol=True -rd run_mode=deep -rd threads=4 \
  -rd topcell=tree_pmos > tree_pmos_drc.log 2>&1
python3 -c "
import klayout.rdb as rdb
r = rdb.ReportDatabase(); r.load('tree_pmos_drc.lyrdb')
print('DRC items:', r.num_items(), [(c.name(), c.num_items()) for c in r.each_category() if c.num_items()])"
rm -rf /tmp/tree_pmos_lvs
sak-lvs.sh -d -w /tmp/tree_pmos_lvs -s tree_pmos.spice -l tree_pmos.gds -c tree_pmos > tree_pmos_lvs.log 2>&1 || true
cp /tmp/tree_pmos_lvs/tree_pmos.magic.lvs/tree_pmos.lvs.out tree_pmos_lvs.out
grep "Final result" tree_pmos_lvs.out
python3 check_tree_pmos.py > tree_pmos_checks.txt
cat tree_pmos_checks.txt
python3 render_tree_pmos.py
