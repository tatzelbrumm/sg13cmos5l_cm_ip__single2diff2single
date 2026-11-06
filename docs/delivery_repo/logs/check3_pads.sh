# Phase 3.3: delivery pads vs harness magic/custom_io/gds
H=/home/user/sg13cmos5l_ocd_chipalooza; fail=0
for c in sg13cmos5l_IOPadDiff2Single sg13cmos5l_IOPadSingle2Diff; do
  a=$H/dependencies/slot_7/final/pads/$c.gds; b=$H/magic/custom_io/gds/$c.gds
  if cmp "$a" "$b"; then echo "IDENTICAL $c.gds $(sha256sum < $a | cut -c1-64)"; else echo "DIFFER $c.gds"; fail=1; fi
done
git -C $H/dependencies/slot_7 rev-parse HEAD
exit $fail
