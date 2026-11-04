#!/bin/bash
# run_checks.sh: every check of BA's note, in order, logs in out/logs (C3 BA, 2026-11-04)
BA=$(cd "$(dirname "$0")/../.." && pwd); W=$BA/work; L=$BA/out/logs; TL=$BA/out/tools
cd $W; export PDK_ROOT=/foss/pdks; source .designinit >/dev/null 2>&1
M=macros/sg13cmos5l_IOPadSingle2Diff; X=$M/schematic/xschem; T=$M/verification/cace/templates; S=$W/$M/netlist/source
SRC="$W/macros/sg13cmos5l_IOPadDiff2Single/netlist/source/units.spice $W/macros/bias_tree_pd/netlist/source/bias_ref_pd.spice $W/macros/bias_tree_noab_pd/netlist/source/bias_tree_noab_pd.spice $S/s2d_mpdda.spice $S/s2d_pd.spice $S/sg13cmos5l_IOPadSingle2Diff.spice"
TOP="X0 iovdd iovss vdd vss pad outp outn vcm vref iref en_3v3 en_3v3_b sg13cmos5l_IOPadSingle2Diff"
SHEETS="$(grep '\.sch$' $BA/out/changed_files.txt) $X/s2d_mpdda_pd_sel.sch $T/s2d_mpdda_pd_sel_tb_loop.sch macros/bias_sel_noab_pd/schematic/xschem/bias_sel_noab_pd.sch"
( for s in $SHEETS; do for mode in "" --lvs; do python3 $TL/netl.py $W $s $BA/out/net_all/$(basename $s .sch) $mode 2>&1 | grep -v '^Sourcing\|^MODELS_\|^$'; done; done ) > $L/netlist_changed_sheets.log 2>&1
echo "netlist_changed_sheets: $(grep -c ', 0 missing' $L/netlist_changed_sheets.log) of $(grep -c '^netlist ' $L/netlist_changed_sheets.log) netlists with 0 missing symbols"
make -C $M klayout-lvs-netlist SCRIPTS_DIR=../../scripts > $L/klayout_lvs_netlist.log 2>&1; echo "klayout-lvs-netlist exit $?"
python3 $TL/cdl_compare.py $BA/inputs/pad_candidate.cdl sg13cmos5l_IOPadSingle2Diff $W/$M/netlist/schematic/sg13cmos5l_IOPadSingle2Diff_klayout.cdl -- "$TOP" > $L/check_sheet_vs_cdl.log 2>&1; tail -1 $L/check_sheet_vs_cdl.log | sed 's/^/sheet CDL vs layout: /'
python3 $TL/cdl_compare.py $BA/inputs/pad_candidate.cdl sg13cmos5l_IOPadSingle2Diff $SRC -- "$TOP" > $L/check_source_vs_cdl.log 2>&1; tail -1 $L/check_source_vs_cdl.log | sed 's/^/sources vs layout: /'
( for p in "sg13cmos5l_IOPadSingle2Diff $X/sg13cmos5l_IOPadSingle2Diff.sch" "s2d_mpdda_pd $X/s2d_mpdda_pd.sch" "s2d_mpdda $X/s2d_mpdda.sch" "s2d_pad_esd $X/s2d_pad_esd.sch" "bias_tree_noab_pd macros/bias_tree_noab_pd/schematic/xschem/bias_tree_noab_pd.sch" "unit_r2 macros/sg13cmos5l_IOPadDiff2Single/schematic/xschem/unit_r2.sch"; do set -- $p; python3 $TL/sheet_vs_source.py $W $1 $2 $SRC; done ) > $L/check_sheets_vs_source.log 2>&1; echo "sheets vs source: $(grep -c '^equivalent' $L/check_sheets_vs_source.log) of 6 equivalent"
USERS="macros/slot/schematic/xschem/slot.sch schematic/xschem/sg13cmos5l_cm_ip__single2diff2single.sch $(for t in ac dc enable noise pd range tran; do echo $T/sg13cmos5l_IOPadSingle2Diff_tb_$t.sch; done) $X/s2d_mpdda_pd_sel.sch $T/s2d_mpdda_pd_sel_tb_loop.sch $X/sg13cmos5l_IOPadSingle2Diff.sch $X/s2d_mpdda_pd.sch $X/s2d_mpdda.sch macros/bias_tree_noab_pd/schematic/xschem/bias_tree_noab_pd.sch macros/bias_sel_noab_pd/schematic/xschem/bias_sel_noab_pd.sch"
python3 $TL/intended_equiv_s2d.py $BA/out/old_root $W $USERS > $L/intended_equiv_users.log 2>&1; tail -1 $L/intended_equiv_users.log | sed 's/^/intended_equiv: /'
make check-boundary > $L/check_boundary.log 2>&1; echo "check-boundary exit $?"
