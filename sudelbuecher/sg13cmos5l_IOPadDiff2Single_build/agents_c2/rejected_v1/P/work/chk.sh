#!/bin/bash
# chk.sh <dir with d2s_p_cells.gds/.cdl> <cell> [drc|lvs|both]
D=$1; C=$2; M=${3:-both}
export PDK_ROOT=/foss/pdks
if [ "$M" != lvs ]; then
 rm -rf $D/drc_$C
 python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=$D/d2s_p_cells.gds --topcell=$C --no_density --mp=4 --run_dir=$D/drc_$C > $D/drc_$C.out 2>&1
 grep -c "generated an exception" $D/drc_$C.out
 grep -h "generated an exception" $D/drc_$C/*.log | head -3 | cut -c1-150
 python3 - <<PY
import re,glob,collections
n=collections.Counter()
for f in glob.glob("$D/drc_$C/*.lyrdb"):
    t=open(f).read()
    for m in re.finditer(r"<item>.*?<category>'?([^<']*)'?</category>",t,re.S): n[m.group(1)]+=1
print("DRC violations:",sum(n.values()),dict(n))
PY
fi
if [ "$M" != drc ]; then
 rm -rf $D/lvs_$C
 python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout=$D/d2s_p_cells.gds --netlist=$D/d2s_p_cells.cdl --topcell=$C --run_dir=$D/lvs_$C --disable_tap_extraction $4 > $D/lvs_$C.out 2>&1
 grep -h "Outcome\|Status  " $D/lvs_$C.out
fi
