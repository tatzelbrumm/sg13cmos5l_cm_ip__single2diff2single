# Phase 2 check 1: sha256 of delivery files vs the sources at the fixed commits
D=/home/user/sg13cmos5l_cm_ip__single2diff2single; R=/home/user/sg13cmos5l_cm_slot7
T=91a7da8b67ac56a26c605501146667a1fde28c32; H=4611357166b7368be4fbf8e176b1e82b8a9a85d0
fail=0
chk() { # commit srcpath dest strip
  local s d; s=$(git -C $D show "$1:$2" | sha256sum | cut -c1-64)
  if [ "$4" = strip ]; then d=$(tail -n +5 "$R/$3" | sha256sum | cut -c1-64); else d=$(sha256sum < "$R/$3" | cut -c1-64); fi
  if [ "$s" = "$d" ]; then r=OK; else r=FAIL; fail=1; fi
  echo "$r $d $3 <= ${1:0:7}:$2${4:+ (after stripping the 4-line header)}"
}
chk $T LICENSE LICENSE
for f in gds/slot_7.gds lef/slot_7.lef lib/slot_7.lib vh/slot_7.vh; do chk $H final/$f final/$f; done
for c in sg13cmos5l_IOPadDiff2Single sg13cmos5l_IOPadSingle2Diff; do
  chk $T macros/$c/layout/klayout/$c.klay.gds final/pads/$c.gds
  chk $T macros/$c/netlist/schematic/${c}_magic.spice final/pads/$c.spice strip
done
exit $fail
