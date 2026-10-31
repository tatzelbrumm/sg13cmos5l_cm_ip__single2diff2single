#!/bin/bash
# runs deck 7 once per variant and vd, deck 8 once per variant; variant.inc selects the fixture, nodeset.inc seeds
# the op with the present variant's (v0) node voltages at the same vd (v0 runs first, with an empty nodeset)
export PDK_ROOT=/foss/pdks PDK=ihp-sg13cmos5l SPICE_USERINIT_DIR=/foss/pdks/ihp-sg13cmos5l/libs.tech/ngspice
W=/home/user/c2/K/work; cd /home/user/c2/K/out/decks
for deck in $DECKS; do for v in $VARIANTS; do for vd in ${VDS:-0}; do
  printf '.subckt fix_sel vdd vss vddo vsso vinp vinn vref vout vfb ibias en_3v3 sel0_3v3 sel1_3v3 en_3v3_b\nxsel vdd vss vddo vsso vinp vinn vref vout vfb ibias en_3v3 sel0_3v3 sel1_3v3 en_3v3_b fix_%s\n.ends\n' $v > $W/variant.inc
  if [ $v = v0 ] || [ ! -f $W/${OPP:-op}_v0_$vd.txt ]; then : > $W/nodeset.inc
  else awk '$2=="=" && $1 !~ /#|\(|^@|^x1\.xsel\.xk/ {print ".nodeset v(" $1 ")=" $3}' $W/${OPP:-op}_v0_$vd.txt > $W/nodeset.inc; fi
  sed "s/\$variant/$v/g; s/\$vdv/$vd/g" $deck.spice > $W/run_$deck.spice
  timeout 900 ngspice -b $W/run_$deck.spice > ../logs/${deck}_${v}_$vd.log 2>&1
done; done; done
