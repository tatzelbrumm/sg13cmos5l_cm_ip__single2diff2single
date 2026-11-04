#!/bin/bash
# render.sh <sheet.sch|.sym> <out.png> [rcfile]: headless xschem render via SVG + cairosvg
set -u
export PDK_ROOT=${PDK_ROOT:-/foss/pdks} PDK=${PDK:-ihp-sg13cmos5l}
f=$(readlink -f "$1"); out=$(readlink -f "$2"); d=$(dirname "$f")
rc=${RC:-$d/xschemrc}
svg=${out%.png}.svg
rm -f "$svg" "$out"
( cd "$d" && PWD="$d" xvfb-run -a xschem -q --rcfile "$rc" --command "xschem zoom_full; xschem print svg $svg; xschem exit closewindow force" "$f" ) >/dev/null 2>&1
python3 -c "import cairosvg,sys; cairosvg.svg2png(url=sys.argv[1], write_to=sys.argv[2], output_width=int(sys.argv[3]), background_color='white')" "$svg" "$out" ${3:-2400} && rm -f "$svg" && echo "rendered $out"
