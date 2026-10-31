#!/bin/sh
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# Agent F, C2 2026-10-31: all checks of the deliverables in <out_dir>; summary on stdout, runs in <run_dir>.
#   sh run_checks.sh <out_dir> <run_dir>
S=$(dirname "$0"); O=$1; R=$2; P=sg13cmos5l_IOPadDiff2Single
N=/home/user/c2/F/inputs/notes
mkdir -p "$R"
TZ=Europe/Berlin date
python3 "$S/checks.py" drc "$O/pad_candidate.gds" $P "$R/drc_pad"
python3 "$S/checks.py" drc "$O/cells/d2s_block.gds" d2s_block "$R/drc_block"
for c in d2s_rhigh bias_tree_pd d2s_cma d2s_cmb cm_rings; do python3 "$S/checks.py" drc "$O/cells/$c.gds" $c "$R/drc_$c"; done
python3 "$S/checks.py" lvs "$O/pad_candidate.gds" "$O/pad_candidate.cdl" $P "$R/lvs_pad" "implicit=iovdd,iovss,vdd,vss" ignoreports
python3 "$S/checks.py" lvs "$O/cells/d2s_block.gds" "$O/cells/d2s_block.cdl" d2s_block "$R/lvs_block" "implicit=iovdd,iovss" ignoreports
for c in d2s_rhigh bias_tree_pd d2s_cma d2s_cmb; do python3 "$S/checks.py" lvs "$O/cells/$c.gds" "$O/cells/$c.cdl" $c "$R/lvs_$c"; done
python3 "$S/probe_nets.py" "$O/pad_candidate.gds" $P "$S/probes_stage3.txt" --metal | tail -1
rm -rf "$R/ant"; python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path="$O/pad_candidate.gds" \
  --topcell=$P --antenna_only --run_dir="$R/ant" > "$R/ant.log" 2>&1
python3 -c "import sys,glob,xml.etree.ElementTree as E; f=glob.glob(sys.argv[1]+'/*antenna.lyrdb')[0]; print('antenna items:', len(list(E.parse(f).getroot().iter('item'))))" "$R/ant"
rm -rf "$R/row"; mkdir -p "$R/row"; python3 $N/row_check.py "$O/pad_candidate.gds" $P "$R/row" > "$R/row/stdout.txt" 2>&1
echo "row check: $(grep -c DIFFERENT "$R/row/edges.md") edge layers DIFFERENT, $(grep -c FAIL "$R/row/nets.md") bands/rails FAIL"
python3 "$S/checks.py" drc "$R/row/row.gds" row "$R/drc_row"
