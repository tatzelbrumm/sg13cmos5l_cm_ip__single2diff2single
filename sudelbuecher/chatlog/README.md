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
: Looked up the chatlog/README conventions and wrote them into `CLAUDE.md` §6.

[2026-09-28_sonnet_sg13cmos5l_io_klib_reference_and_sg13_dev_pcells.md](2026-09-28_sonnet_sg13cmos5l_io_klib_reference_and_sg13_dev_pcells.md)
: New session, on `macros/sg13cmos5l_IOPadDiff2Single`: replaced copied-GDS `sg13cmos5l_io` pad cells with a real `.klib` by-reference entry, traced the mechanism to KLayout's `LibraryManagerPlugin` Salt package, found IHP's `SG13_dev` PCells already registered with zero extra setup, worked out the Levels=1 flatten for the pad wrapper from the real GDS hierarchy, confirmed `Clamp_*`/`DCNDiode`/`DCPDiode` have no standalone PCell anywhere in the public PDK, and hit an unresolved hash mismatch between GitHub's `ihp-sg13cmos5l` `main` and the user's IIC-OSIC-TOOLS container copy.

[2026-09-28_sonnet_chatlog_export_meta_and_formatting_corrections.md](2026-09-28_sonnet_chatlog_export_meta_and_formatting_corrections.md)
: Split off from the file above at the user's request: exporting that session verbatim ran into a checksum mismatch traced to macOS stamping C2PA/JUMBF metadata into images, then two rounds of getting this very log's own formatting conventions wrong (README one-sentence rule, `*[ ]*` block line breaks) and being corrected, and later a second, unrelated episode recovering chat content lost to a mid-session context compaction via `read_conversation`.

[2026-09-28_opus_sg13cmos5l_clamp_pcells_skill_and_worktree_questions.md](2026-09-28_opus_sg13cmos5l_clamp_pcells_skill_and_worktree_questions.md)
: New Opus session: parametrized `Clamp_N`/`Clamp_P` PCells, the `ihp-flat-cell-to-pcell` skill, installing the PCells into `sg13cmos5l_IOPadDiff2Single`, a minimal `feol_contact` PCell, and how KLayout finds PCell libraries.

[2026-09-28_opus_safety_stops_and_chatlog_export.md](2026-09-28_opus_safety_stops_and_chatlog_export.md)
: Split off from the file above: six `[reasoning_extraction]` safety stops, and how the verbatim chat log was then built.

[2026-10-02_sonnet_edwards_cauwenberghs_log_domain_references_in_donotlitter.md](2026-10-02_sonnet_edwards_cauwenberghs_log_domain_references_in_donotlitter.md)
: Read-only search of the user's `~/DoNotLitter` PDF collection for three Edwards & Cauwenberghs log-domain papers (ISCAS 1997, ISCAS 1998, 2000), plus a Minch-thesis lookup and a whole-collection title scan.

[2026-10-02_opus_class_ab_pad_driver_improvements.md](2026-10-02_opus_class_ab_pad_driver_improvements.md)
: Opus session, 2–8 Oct: resistor- and MOM-free improvements to the class-AB pad driver, four real bias variants with xschem sheets and figures, separate output-stage rails, hand-offs for a gf180 port and a power-down enable, and a cloud simulation environment pinned to IIC-OSIC-TOOLS 2026.09.
