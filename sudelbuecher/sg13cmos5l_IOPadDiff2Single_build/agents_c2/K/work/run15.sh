#!/bin/bash
# stage 8: deck 15 (both loads), 16, 17 for v0, v8, v9; nodeset from v0's mid-rail op (deck 7 loaded / deck 13 unloaded)
cd /home/user/c2/K/work
OPP=op RLOAD=1000 CLOAD=1e-10 DECKS=step15_large VARIANTS="v0 v8 v9" VDS="0" ./run78.sh
OPP=op13c3e-10 RLOAD=1G CLOAD=3e-10 DECKS=step15_large VARIANTS="v0 v8 v9" VDS="0" ./run78.sh
OPP=op DECKS=rail16_recovery VARIANTS="v0 v8 v9" VDS="0" ./run78.sh
OPP=op DECKS=thd17_swing VARIANTS="v0 v8 v9" VDS="10e3 100e3 1e6" ./run78.sh
echo all-done
