#!/bin/bash
# drc_all.sh <gds> <outdir> cells...
gds=$1; out=$2; shift 2
for c in "$@"; do
  python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=$gds --topcell=$c --no_density --mp=4 --run_dir=$out/$c > $out/$c.log 2>&1
  echo "== $c: exceptions: $(grep -c 'generated an exception' $out/$c.log)"
  python3 /home/user/c2/N2/work/tools/drcsum.py $out/$c/*_full.lyrdb
done
