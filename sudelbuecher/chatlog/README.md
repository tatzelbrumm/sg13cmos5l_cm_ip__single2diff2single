# Chatlog index

[2026-08-30_i_claude_rename.md](2026-08-30_i_claude_rename.md)
: Rename of the forked template repo to `sg13cmos5l_cm_ip__single2diff2single`, functional verification, and the git cleanup that followed.

[2026-09-04_ocd_reconciliation_and_ogueyaebischerbias_cace.md](2026-09-04_ocd_reconciliation_and_ogueyaebischerbias_cace.md)
: Reconciled docs against the `sg13cmos5l_ocd_chipalooza` harness, rewrote `submission.yaml`'s long-description, and started CACE-characterizing `OgueyAebischerBias`.

[2026-09-04_opus_cace_templates_and_oab_sizing.md](2026-09-04_opus_cace_templates_and_oab_sizing.md)
: Authored the four missing CACE testbench templates for `OgueyAebischerBias`, then diagnosed its poor PSRR/matching and derived a sizing method.

[2026-09-04_sonnet_oab_cace_unit_fixes_and_toplevel_handoff.md](2026-09-04_sonnet_oab_cace_unit_fixes_and_toplevel_handoff.md)
: Fixed unit-display bugs in `OgueyAebischerBias`'s `reference.yaml`, debugged the CACE testbenches, then handed the `toplevel` branch off to a fresh session.

[2026-09-04_sonnet_toplevel_pin_mapping_and_harness_review_prep.md](2026-09-04_sonnet_toplevel_pin_mapping_and_harness_review_prep.md)
: Building the `toplevel` testbench/CACE skeleton turned into a pin-mapping investigation that surfaced a real inconsistency in the chipalooza harness, ahead of a design review.

[2026-09-05_sonnet_xschem_explainer_and_iopad30ma_sourcing.md](2026-09-05_sonnet_xschem_explainer_and_iopad30ma_sourcing.md)
: Explained what's in `schematic/xschem/`, then traced the real data source for `sg13cmos5l_IOPadInOut30mA` after a colleague's unverified ChatGPT guess.

[2026-09-17_sonnet_sg13cmos5l_pad_docs_and_project_setup.md](2026-09-17_sonnet_sg13cmos5l_pad_docs_and_project_setup.md)
: Deep dive on IHP's `bondpad` PCell and the `sg13cmos5l_io` cell library, plus deciding where Claude's working notes should live.

[2026-09-27_sonnet_git_worktree_to_sg13cmos5l_ocd_chipalooza.md](2026-09-27_sonnet_git_worktree_to_sg13cmos5l_ocd_chipalooza.md)
: Worktree surgery on `sg13cmos5l_ocd_chipalooza`: moved the primary worktree to `tatzelbranch` and split off a new orphan `sudel_buecher` worktree.

[2026-09-27_sonnet_single2diff2single_toplevel_structure_and_chipalooza_magic_authoring.md](2026-09-27_sonnet_single2diff2single_toplevel_structure_and_chipalooza_magic_authoring.md)
: `toplevel` structure work, a chipalooza Magic-authoring question, the `layout/klayout`+`layout/gds` split and its correction, and a compaction-recovery episode.
