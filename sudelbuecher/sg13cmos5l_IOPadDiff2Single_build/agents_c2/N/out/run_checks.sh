#!/bin/bash
# usage: run_checks.sh <cell> [<cell> ...]   DRC (main + maximal tables, LU incl.) and LVS per cell into logs/
# run from out/; needs PDK_ROOT=/foss/pdks (source .designinit) for the PDK paths used below
D=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech
cd "$(dirname "$0")"; mkdir -p logs
for c in "$@"; do
  rm -rf logs/drc_$c logs/lvs_$c
  python3 $D/drc/run_drc.py --path=d2s_n_cells.gds --topcell=$c --no_density --mp=4 --run_dir=logs/drc_$c > logs/drc_$c.txt 2>&1
  n=$(python3 - "$c" <<'P'
import sys,glob,re
c=sys.argv[1]; f=glob.glob("logs/drc_%s/*_full.lyrdb"%c)
tot=0
for x in f:
    tot+=len(re.findall(r"<item>",open(x).read()))
print(tot)
P
)
  ex=$(grep -rli "generated an exception" logs/drc_$c | wc -l)
  echo "DRC $c: items=$n exceptions=$ex"
  python3 $D/lvs/run_lvs.py --layout=d2s_n_cells.gds --netlist=d2s_n_cells.cdl --topcell=$c --run_dir=logs/lvs_$c --disable_tap_extraction $LVSOPT > logs/lvs_$c.txt 2>&1
  echo "LVS $c: $(grep -o 'Outcome .*' logs/lvs_$c.txt | head -1)"
done
