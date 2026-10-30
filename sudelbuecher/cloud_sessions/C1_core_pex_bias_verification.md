<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C1: PEX of oa_core_pd and bg_core_pd in the bias verification (cloud session)

Claude Code cloud session, environment `sg13cmos5l` with the setup script of
`github.com/tatzelbrumm/claude-cloud-config` (prebuilt IIC-OSIC-TOOLS 2026.10 tools; same text as
`sudelbuecher/cloud_sessions/setup_script_claude_cloud_config`). The session starts on
`claude/c1-core-pex-verif`, which Christoph created from `toplevel`; `claude/c1-core-pex-verif-sudel`
was created from `sudel_buecher`. Read first: `CLAUDE.md`, `sudelbuecher/cloud_environment.md`, and
the C0 report `sudelbuecher/cloud_sessions/C0_oa_core_pd_pex_report.md` (what C0 ran, the template
workarounds, the magic / KLayout-PEX differences).

**Goal:** the bias verification shows what the layouts of the two reference cores do to the bias
currents. The cores are `macros/oa_core_pd` (Oguey-Aebischer) and `macros/bg_core_pd` (bandgap). Both are
instantiated in `macros/bias_sel_pd` (`Xoa`, `Xbg`), whose CACE limits are proposals from pre-layout runs
(see the header of `bias_sel_pd.yaml`). The pre-layout results are committed in
`macros/bias_sel_pd/verification/cace/results/bias_sel_pd/`.

**Git, for this task only (Christoph's permission):** `git fetch`; `git cherry-pick 82a57ec` (C0's
oa_core_pd outputs, new files only); a worktree `../sudel` on `claude/c1-core-pex-verif-sudel`; commits
on the two `claude/c1-core-pex-verif*` branches and pushing them. Nothing else: never push `main`,
`toplevel` or `sudel_buecher`, no tags, no force pushes, no merges.

1. **Branches and tools:** `git fetch origin claude/c0-oa-core-pd-pex claude/c1-core-pex-verif-sudel`;
   `git cherry-pick 82a57ec`; a worktree `../sudel` on a local `claude/c1-core-pex-verif-sudel` that
   tracks `origin/claude/c1-core-pex-verif-sudel`. Check `/foss/setup.log` for `SETUP_DONE`;
   record the versions as in C0. `pip install --break-system-packages cace==2.11.0` (the 2026.10 pin);
   if it rejects `cace_format: 5.2`, record that and use the lowest CACE version that accepts it. Every
   change to the environment is recorded.
2. **bg_core_pd PEX**, as C0 did for oa_core_pd, from `macros/bg_core_pd` after `source .designinit`,
   every `make` with `SCRIPTS_DIR=../../scripts`: `magic-drc`, `magic-lvs-netlist`, `magic-lvs`,
   `magic-pex EXT_MODE=1`, `2`, `3`, `klayout-pex EXT_MODE=2`. Expected (Cowork run, 2026-10-29):
   DRC clean, LVS match, 123 devices, C 50 / 313 / 347 (magic 1/2/3), R 359 (mode 3), 317 C (kpex).
3. **Core PEX in bias_sel_pd:** run `bias_sel_pd`'s CACE groups with the cores as schematic (baseline,
   must reproduce the committed results) and as magic PEX mode 2 (coupled C). Add mode 3 (RC) for the
   groups where wiring resistance can move DC currents (at least `iref` and `pvt`). How the PEX views go
   in is your choice (the template's `<cell>_pex.sym` is a primitive that needs an `.include` of the
   netlist, subckt `<cell>_pex`). Constraint: with no option given, everything behaves as now (schematic
   cores, same netlists, same results folder). Long runs go in the background (`CACE_JOBS` ≤ 3 on 4
   vCPU); check on them sparingly.
4. **Adequacy of the verification:** where the CACE files, testbenches, `scripts/cace/*.py` or the
   Makefiles can't show the core-PEX effect, extend them. Where checks are redundant (for example the flat
   copies of the pre-layout cores in `bias_bg_pd` and `bias_oa_pd`, if `bias_sel_pd` with sel = 1 / 2
   covers them), dropping or slimming them is acceptable instead of extending. Pad-level CACE
   (`sg13cmos5l_IOPadDiff2Single`, `…Single2Diff`) is out of scope; say what it would need.
   Don't edit the cores' schematics or GDS, or any design sheet; testbench and verification files only.
5. **Deliver:**
   - `claude/c1-core-pex-verif`: the cherry-picked oa outputs, bg_core_pd's generated outputs (as C0's
     list), the verification changes, the new CACE results next to the committed ones (one folder per
     core view). Commit, push.
   - `claude/c1-core-pex-verif-sudel`: logs in `sudelbuecher/logs/claude/c1-core-pex-verif/`, one
     `MANIFEST.tsv` row per output file; `sudelbuecher/cloud_sessions/C1_core_pex_bias_verification_report.md`
     (versions, setup, per-target and per-group results and times, a table schematic / PEX 2 / PEX 3 per
     parameter with the limit and the change in %, every limit violation, environment adaptations);
     `sudelbuecher/cloud_sessions/C1_verification_changes.md`: **concise**, for Christoph's review after
     the fact, one entry per change or omission (file, what, why, how to undo); a verbatim chatlog in
     `sudelbuecher/chatlog/` as C0 did. SPDX headers on new text files. Commit, push.
   - Then say in the session that it's done, with both branch names.
