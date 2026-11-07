#!/bin/bash
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# bias_tree_noab_pd assembly: build (twice, byte compare), PDK DRC (main + maximal deck), Magic+Netgen LVS against
# the source netlist, geometric / latch-up checks, pictures. Run from anywhere. Written 2026-11-07, Claude.
# Logs in checks/: drc_bias_tree_noab_pd{.log,.lyrdb,_max.log,_max.lyrdb,_max.out}, lvs.stdout,
# lvs/bias_tree_noab_pd.magic.lvs/bias_tree_noab_pd.lvs.out, check_tree.txt, build.txt, sha256.txt
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../../../.." && pwd)
export PDK_ROOT=${PDK_ROOT:-/foss/pdks}
export PDK=${PDK:-ihp-sg13cmos5l}
cd "$REPO"
. ./.designinit > /dev/null 2>&1 || true
cd "$HERE"
mkdir -p checks
T=$(mktemp -d)
python3 build_tree.py | tee checks/build.txt
python3 build_tree.py "$T/second.gds" > /dev/null
cmp bias_tree_noab_pd.gds "$T/second.gds" && echo "reproducible: two builds give the same bytes" | tee -a checks/build.txt
rm -rf "$T"
bash ../nmos/checks/drc.sh "$HERE/bias_tree_noab_pd.gds" bias_tree_noab_pd "$HERE/checks/drc_bias_tree_noab_pd"
python3 make_ref.py
rm -rf checks/lvs
sak-lvs.sh -d -w "$HERE/checks/lvs" -s "$HERE/checks/bias_tree_noab_pd_source_ref.spice" \
  -l "$HERE/bias_tree_noab_pd.gds" -c bias_tree_noab_pd > checks/lvs.stdout 2>&1 || true
OUT=checks/lvs/bias_tree_noab_pd.magic.lvs/bias_tree_noab_pd.lvs.out
grep "Final result" $OUT
echo "property errors (lines with 'property' other than the symmetry note):"
grep -i "propert" $OUT | grep -v "Resolving symmetries by property value" || echo "  none"
python3 check_tree.py | tee checks/check_tree.txt
python3 render_tree.py 2>&1 | grep -v -i -e psutil -e tkinter
sha256sum bias_tree_noab_pd.gds build_tree.py make_ref.py check_tree.py render_tree.py run_checks.sh \
  checks/bias_tree_noab_pd_source_ref.spice $OUT | tee checks/sha256.txt
