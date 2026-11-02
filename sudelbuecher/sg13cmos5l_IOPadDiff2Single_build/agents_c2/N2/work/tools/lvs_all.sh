#!/bin/bash
# lvs_all.sh <gds> <cdl> <outdir> cells...
gds=$1; cdl=$2; out=$3; shift 3
for c in "$@"; do
  python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout=$gds --netlist=$cdl --topcell=$c --run_dir=$out/$c --disable_tap_extraction > $out/$c.log 2>&1
  echo "== $c: $(grep -h -i 'match\|ERROR' $out/$c.log | tail -3 | tr '\n' ' ')"
done
