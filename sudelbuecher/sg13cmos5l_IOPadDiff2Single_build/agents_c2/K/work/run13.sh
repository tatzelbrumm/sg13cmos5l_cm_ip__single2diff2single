#!/bin/bash
# deck 13 over the swing, both loads; v0 first at each vd (its op seeds the others' nodeset)
cd /home/user/c2/K/work
VDS="-1.4 -1.05 -0.7 -0.35 0 0.35 0.7 1.05 1.3"
OPP=op13c1e-10 RLOAD=1000 CLOAD=1e-10 DECKS=loop13_sweep VARIANTS="v0 v5 v6 v7 v8 v7d" VDS="$VDS" ./run78.sh
OPP=op13c3e-10 RLOAD=1G CLOAD=3e-10 DECKS=loop13_sweep VARIANTS="v0 v5 v6 v7 v8 v7d" VDS="$VDS" ./run78.sh
