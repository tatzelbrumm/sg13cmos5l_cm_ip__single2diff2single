#!/bin/sh
# run_all_checks.sh (agent N, C4): DRC / LVS (C3's checks.sh), sym_check, LU, pad regression and pad comparison on
# out/rb_n_cells.gds; logs in out/logs. Run from out/ after 'python3 build_rb_n.py'.
PAD=/home/user/sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/sg13cmos5l_IOPadSingle2Diff.klay.gds
L=logs
{ echo "DRC / LVS on rb_n_cells.gds, $(TZ=Europe/Berlin date)"
  sh checks.sh rb_n_cells.gds rb_n_cells.cdl $L rb_tree_n rb_casc rb_mirror rb_cload bypass_rb; } > $L/checks_summary.txt 2>&1
{ for c in rb_casc bypass_rb; do python3 sym_check.py rb_n_cells.gds $c; done
  echo "(--no-y: one row)"; for c in rb_tree_n rb_mirror rb_cload; do python3 sym_check.py rb_n_cells.gds $c --no-y; done
  python3 lu_check.py rb_n_cells.gds rb_tree_n rb_casc rb_mirror rb_cload bypass_rb; } > $L/sym_lu.txt 2>&1
mkdir -p regress && (cd regress && python3 ../build_rb_n.py --pad > /dev/null 2>&1)
{ echo "== regression: the pad's rows rebuilt by build_rb_n.py --pad against the drawn S2D pad (all layers)"
  for c in bias_tree_noab_n_c3 sinks_6x6_s2d_c3_core s2d_cload_c3; do python3 xor_cells.py regress/pad_regress.gds $c $PAD $c; done
  python3 xor_cells.py regress/pad_regress.gds s2d_casc_n_c3 $PAD s2d_casc_n_f
  echo "   (s2d_casc_n_f = s2d_casc_n_c3 + F's two M2 exits, build_f_casc_n.py: the 10/0 and 10/2 residual)"
  echo "== replica rows against the pad's rows; device layers Activ 1/0, GatPoly 5/0, Cont 6/0 unless noted"
  D=1/0,5/0,6/0
  python3 xor_cells.py rb_n_cells.gds rb_tree_n $PAD bias_tree_noab_n_c3 --layers $D --win -2.75,-0.2,-0.125,7.5
  python3 xor_cells.py rb_n_cells.gds rb_tree_n $PAD bias_tree_noab_n_c3 --layers $D --dx 4.9 --win 4.775,-0.2,22.575,7.5
  python3 xor_cells.py rb_n_cells.gds rb_tree_n $PAD bias_tree_noab_n_c3 --layers $D --dx 9.8 --win 27.475,-0.2,30.1,7.5
  python3 xor_cells.py rb_n_cells.gds rb_casc $PAD s2d_casc_n_f --layers $D --win -1.0,-0.3,68.7,10.25
  echo "   rb_casc whole cell, device layers incl. pSD 14/0 and TGO 44/0 (the ring is smaller):"
  python3 xor_cells.py rb_n_cells.gds rb_casc $PAD s2d_casc_n_f --layers $D,14/0,44/0
  echo "   rb_casc band (x -1.0..68.7, y 3.68..6.27), M1 / Via1 / M2 (round 5: dummy tracks in the empty places):"
  python3 xor_cells.py rb_n_cells.gds rb_casc $PAD s2d_casc_n_f --layers 8/0,19/0,10/0 --win -1.0,3.68,68.7,6.27
  python3 xor_cells.py rb_n_cells.gds rb_mirror $PAD sinks_6x6_s2d_c3_core --layers $D --win -0.92,-0.2,8.375,6.9
  python3 xor_cells.py rb_n_cells.gds rb_mirror $PAD sinks_6x6_s2d_c3_core --layers $D --dx -31.25 --win 8.375,-0.2,17.67,6.9
  echo "   rb_cload whole cell, all layers:"
  python3 xor_cells.py rb_n_cells.gds rb_cload $PAD s2d_cload_c3
  python3 xor_cells.py rb_n_cells.gds bypass_rb $PAD s2d_cload_c3 --layers $D --win -0.2,-0.2,12.65,12.75
} > $L/compare_pad.txt 2>&1
echo done
