#!/bin/bash
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
# PDK KLayout DRC of one cell: the main deck (ihp-sg13cmos5l.drc, the required check) and the maximal rule deck
# (sg13cmos5l_maximal.drc, which also checks Gat.b1, pSD.d, TGO.*). Paths must be absolute. Written 2026-11-07, Claude.
# usage: drc.sh <gds> <cell> <outprefix>
D=$PDK_ROOT/$PDK/libs.tech/klayout/tech/drc
klayout -b -zz -r $D/ihp-sg13cmos5l.drc -rd input=$1 -rd report=$3.lyrdb -rd feol=True -rd beol=True -rd run_mode=deep -rd threads=4 -rd topcell=$2 > $3.log 2>&1
klayout -b -zz -r $D/rule_decks/sg13cmos5l_maximal.drc -rd input=$1 -rd report=$3_max.lyrdb -rd run_mode=deep -rd threads=4 -rd topcell=$2 -rd log=$3_max.log > $3_max.out 2>&1
for f in $3.lyrdb $3_max.lyrdb; do python3 -c "
import klayout.rdb as r,sys
db=r.ReportDatabase(''); db.load(sys.argv[1]); n=0
for it in db.each_item():
  n+=1; cat=db.category_by_id(it.category_id()).name()
  for v in it.each_value(): print(' ',cat, v.to_s()[:140]); break
print(sys.argv[1], 'items', n)
" $f | tail -25; done
