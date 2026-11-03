#!/bin/bash
# deck 14 (v9 over the swing, both loads; nodeset from deck 13's v0 ops) and deck 12 reused for v9's step
cd /home/user/c2/K/work
VDS="-1.4 -1.05 -0.7 -0.35 0 0.35 0.7 1.05 1.3"
OPP=op13c1e-10 RLOAD=1000 CLOAD=1e-10 DECKS=loop14_v9 VARIANTS="v9" VDS="$VDS" ./run78.sh
OPP=op13c3e-10 RLOAD=1G CLOAD=3e-10 DECKS=loop14_v9 VARIANTS="v9" VDS="$VDS" ./run78.sh
DECKS=step12_seriesR VARIANTS="v9" VDS="0" ./run78.sh
