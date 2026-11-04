#!/bin/sh
# checks.sh <gds> <cdl> <logdir> <cell>...: IHP DRC (no density) and LVS per cell, summaries in <logdir>.
G=$(realpath "$1"); N=$(realpath "$2"); L=$3; shift 3
T=/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech
mkdir -p "$L"
for c in "$@"; do
  rm -rf "$L/drc_$c" "$L/lvs_$c"
  python3 $T/drc/run_drc.py --path="$G" --topcell="$c" --no_density --mp=4 --run_dir="$L/drc_$c" > "$L/drc_$c.log" 2>&1
  ex=$(grep -il "exception" "$L/drc_$c.log" "$L/drc_$c"/*.log 2>/dev/null | wc -l)
  nv=$(grep -c "<item>" "$L/drc_$c"/*_full.lyrdb 2>/dev/null)
  cats=$(python3 - "$L/drc_$c" <<'EOF'
import sys, glob, re, collections
f = glob.glob(sys.argv[1] + "/*_full.lyrdb")
t = open(f[0]).read() if f else ""
c = collections.Counter(re.findall(r"<item>\s*<tags/>\s*<category>'?([^<']+)'?</category>", t))
print(" ".join("%s:%d" % kv for kv in sorted(c.items())))
EOF
)
  echo "== $c DRC: violations $nv, files mentioning exception $ex  $cats"
  python3 $T/lvs/run_lvs.py --layout="$G" --netlist="$N" --topcell="$c" --run_dir="$L/lvs_$c" \
      --disable_tap_extraction > "$L/lvs_$c.log" 2>&1
  echo "== $c LVS: $(grep -o 'Netlists match\|Netlists don.t match\|ERROR.*' "$L/lvs_$c.log" | head -2 | tr '\n' ' ')"
done
