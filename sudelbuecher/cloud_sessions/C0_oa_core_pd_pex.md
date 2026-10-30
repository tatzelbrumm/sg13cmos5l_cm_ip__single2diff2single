<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C0: oa_core_pd PEX in a cloud session (proof of concept)

Claude Code cloud session, environment `sg13cmos5l`, clone of `toplevel` (the macros aren't on `main`
yet). Read `sudelbuecher/cloud_environment.md` (reference IIC-OSIC-TOOLS 2026.10, section "Claude Code
cloud sessions") first. The block is `macros/oa_core_pd`, the Oguey-Aebischer bias core (agent A2,
2026-10-28; `sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents/A2_oa_core_pd_layout/report.md`).
Its sibling `macros/bg_core_pd` was run the same way in the Cowork session on 2026-10-29 (results
below); don't repeat it here.

**How:** only the macro's own Makefile targets (the Dorrer / Edwards template conventions), from
`macros/oa_core_pd` after `source .designinit` in the repository root. They use magic and netgen with
`$PDKPATH/libs.tech/magic/ihp-sg13cmos5l.magicrc` and `$PDK_ROOT/$PDK/libs.tech/netgen/ihp-sg13cmos5l_setup.tcl`,
the same setup as the Chipalooza harness's `magic/run_extract_*.sh` and `validate/run_lvs_*.sh`. Don't edit
the schematic, the GDS, the Makefile or `scripts/`. If a target fails because of the cloud (a missing package
or path), fix the environment only and record it; if it fails because of the design, report it, don't fix it.

**Known from the bg_core_pd run:** pass `SCRIPTS_DIR=../../scripts` to every `make` (the PEX targets look
for `check_pex_ports.py` under the macro; it's in the repository root). `kpex` must be the setup script's
wrapper (`kpex.pip` beside it), because kpex 0.6.8 rejects the template's `--pdk ihp_sg13cmos5l`. bg_core_pd
for comparison: DRC clean, LVS match, 123 devices; C elements in magic modes 1/2/3 = 50/313/347, R in
mode 3 = 359, KLayout-PEX mode 2 = 317 C; every target about 1 s.

**Git, for this task only (Christoph's permission):** `git fetch origin sudel_buecher`, the worktree in step 1,
commits on `claude/c0-oa-core-pd-pex` (from `toplevel`) and `claude/c0-oa-core-pd-pex-sudel` (from
`sudel_buecher`), and pushing those two branches. Nothing else: never push `main`, `toplevel` or
`sudel_buecher`, no tags, no force pushes, no merges.

1. **Branches:** `git switch -c claude/c0-oa-core-pd-pex`; `git fetch origin sudel_buecher && git worktree add
   -b claude/c0-oa-core-pd-pex-sudel ../sudel origin/sudel_buecher`. Never switch the main checkout to
   `sudel_buecher`.
2. **Toolchain:** read `/foss/setup.log` (every `_OK` line, `SETUP_DONE`; under about 300 s means it gets cached).
   Record: `klayout -b -v` (0.30.12), `magic -dnull -noconsole --version` (8.3.685), netgen (1.5.324),
   `xschem --version`, `ngspice -v` (ngspice-47), `kpex --version` (0.6.8), `ls /usr/local/bin/sak-*`,
   `git -C /foss/pdks/IHP-Open-PDK rev-parse HEAD`. Stop and report if magic, netgen, xschem or the PDK is missing.
3. **Run, in this order, each tee'd to `../sudel/sudelbuecher/logs/claude/c0-oa-core-pd-pex/<target>.out` / `.err`,
   with its wall time, all with `SCRIPTS_DIR=../../scripts`:**
   - `make magic-drc`
   - `make magic-lvs-netlist`, `make magic-lvs` (the PEX is only meaningful after a match)
   - `make magic-pex EXT_MODE=1`, `EXT_MODE=2`, `EXT_MODE=3`
   - `make klayout-pex EXT_MODE=2`, for comparison (kpex 0.6.8 with its magic engine; a deprecation
     warning about the missing subcommand is expected)
4. **Check and summarize** (no new scripts in the repository; one-off commands are fine):
   - LVS: netgen's verdict, device and net counts.
   - Each PEX netlist: `check_pex_ports.py` result (part of the targets), port order against
     `oa_core_pd_pex.sym`, number of devices, R and C elements.
   - Total capacitance to ground and coupling per port net (iout, vdd, vss, en_3v3, en_3v3_b), modes 1–3 and
     KLayout-PEX side by side; largest few internal nets.
   - Harness fit: the magic commands `sak-pex.sh` actually ran against `magic/run_extract_user_project.sh`
     of `github.com/tatzelbrumm/sg13cmos5l_ocd_chipalooza` (clone it read-only if the session can reach it);
     list the differences.
5. **Deliver:**
   - On `claude/c0-oa-core-pd-pex`: only the files the targets wrote under `macros/oa_core_pd/` (netlists,
     `oa_core_pd_pex.sym`, reports), as the template commits generated outputs. Commit, push.
   - On `claude/c0-oa-core-pd-pex-sudel`: the logs, one line per output file in `sudelbuecher/MANIFEST.tsv` in
     its existing format, and `sudelbuecher/cloud_sessions/C0_oa_core_pd_pex_report.md` (SPDX header; short):
     versions and setup times, per-target result and time, the step-4 summary, every environment adaptation,
     what failed and why. Commit, push.
   - Then say in the session that it's done, with both branch names.
