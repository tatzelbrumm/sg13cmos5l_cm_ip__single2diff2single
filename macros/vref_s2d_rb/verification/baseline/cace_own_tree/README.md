# vref_s2d_rb CACE results with its own bias tree (until 2026-11-07)

CACE 2.11.0 results of vref_s2d_rb as a stand-alone block with its own copy of the bias lines (reference NI, BP, BNC), from the
suite `macros/vref_s2d_rb/verification/cace/vref_s2d_rb.yaml` that `gen_cace.py` wrote on 2026-11-06 (its templates are in git history).
Since 2026-11-07 vref_s2d_rb hangs on the shared tree `bias_tree_rb` inside `pad_ref_rb`; its CACE suite is
`macros/pad_ref_rb/verification/cace/pad_ref_rb.yaml`. Kept here to compare the two (docs/replica_bias/SUMMARY.md).
