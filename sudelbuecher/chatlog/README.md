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
: Deep dive on IHP's `bondpad` PCell and the `sg13cmos5l_io` cell library, plus deciding where Claude's own working notes should live.

[2026-09-27_sonnet_git_worktree_to_sg13cmos5l_ocd_chipalooza.md](2026-09-27_sonnet_git_worktree_to_sg13cmos5l_ocd_chipalooza.md)
: Worktree surgery on `sg13cmos5l_ocd_chipalooza`: moved the primary worktree to `tatzelbranch` and split off a new orphan `sudel_buecher` worktree.

[2026-09-27_sonnet_single2diff2single_toplevel_structure_and_chipalooza_magic_authoring.md](2026-09-27_sonnet_single2diff2single_toplevel_structure_and_chipalooza_magic_authoring.md)
: `toplevel` structure work, a chipalooza Magic-authoring question, the `layout/klayout`+`layout/gds` split and its correction, and a compaction-recovery episode.

[2026-09-27_sonnet_klayout_hierarchical_layout_invocation_and_cheatsheet_iteration.md](2026-09-27_sonnet_klayout_hierarchical_layout_invocation_and_cheatsheet_iteration.md)
: How to invoke KLayout for hierarchical editing and reference macros via the `.klib`, `make`-vs-manual `klayout` invocation, a cheatsheet checklist iterated down to plain bullets, a `device_commit_files` stale-write bug caught and fixed, and a `make open` cwd mistake. Live/ongoing.

[2026-09-27_sonnet_xschem_schematic_from_symbol_crash_and_codex_fix.md](2026-09-27_sonnet_xschem_schematic_from_symbol_crash_and_codex_fix.md)
: Continuation of the klayout-hierarchical-layout session: `slot.sch` created but "Make schematic from symbol" not working, a system crash and recovery, and the fix (place the symbol as an instance first) from a colleague's intervention.

[2026-09-27_sonnet_chatlog_integrity_correction_and_handover.md](2026-09-27_sonnet_chatlog_integrity_correction_and_handover.md)
: The user caught a fabricated sentence in the klayout-hierarchical-layout log's Turn 21; audit, correction, and a session handover (paired with `HANDOVER_xschem_makefile_lvs_and_chatlog_integrity.md` at the main repo root) to close out an unwieldy session.

[2026-09-28_sonnet_makefile_magic_recs_and_inverter_clean_recovery.md](2026-09-28_sonnet_makefile_magic_recs_and_inverter_clean_recovery.md)
: Retrieved the handover's Makefile-verification recommendations for the `layout/magic`+`layout/klayout` split, then walked the user through recovering `macros/inverter` from a `make clean` (PEX, DRC/LVS, sim/CACE, render, `build-top`) one deleted-file group at a time.

[2026-09-28_sonnet_toplevel_verify_targets_and_check_boundary_gds_mismatch.md](2026-09-28_sonnet_toplevel_verify_targets_and_check_boundary_gds_mismatch.md)
: Continuation, split into a new file at the user's request: which top-level `make` targets to try first, then confirming exactly which GDS `check-boundary` checks and why a clean pass doesn't mean much while the top level's schematic and layout describe different designs.

[2026-09-28_sonnet_slot_makefile_scaffold_and_klayout_lvs_debugging.md](2026-09-28_sonnet_slot_makefile_scaffold_and_klayout_lvs_debugging.md)
: New session: scaffolded `macros/slot`'s Makefile (DRC/LVS/PEX first, then a full inverter-based copy per the user's own call), interactive-KLayout and `build-top`/tapeout-export explainers, a `klayout-lvs-netlist` failure triaged from a log paste, and a `slot.klay.gds` vs. the `sg13cmos5l_ocd_chipalooza` harness's `slot7_wrapper.gds` diff that cleared a removed TopMetal1 sliver as LVS-safe.

[2026-09-28_sonnet_chatlog_convention_lookup_and_claude_md_pointer.md](2026-09-28_sonnet_chatlog_convention_lookup_and_claude_md_pointer.md)
: New session: looked up the established rules for unabridged/verbatim logging and the README-index summaries, survived a mid-session device-bridge disconnect, then wrote both rules into the main repo's `CLAUDE.md` §6 so any future chat in this project picks them up automatically.
