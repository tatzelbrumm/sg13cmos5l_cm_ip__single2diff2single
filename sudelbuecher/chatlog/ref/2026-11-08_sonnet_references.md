<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# References of the session `2026-11-08_sonnet_tughra_metal_art_and_skill.md`

Pointers only (index, do not copy). Everything below was read in this session unless marked.

## Project repositories
- `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single`: work repo. Branch `art/tughra-metal` (art, scripts, `ART_NOTES.md`, `ART_LAYERS.md`, `art/skill/`), based first on `main` `60f270a`, rebased onto `toplevel` `4223a63`; companion branch `art/tughra-metal-sudelbuecher` (this one).
- `tatzelbrumm/sg13cmos5l_cm_slot7` (read only), commit `454da6a`: `final/gds/slot_7.gds` (sha256 5f8fd14a...bd), `netlist/slot_7.cdl`, `README.md`, `docs/FOR_TIM.md`, `docs/PROGRESS.md`, `docs/slot_7.md`, `docs/slot_7.png`.
- `tatzelbrumm/claude-cloud-config` (read only): `README.md` (cloud environment: tools under `/foss/tools`, PDK under `/foss/pdks`, KLayout 0.30.12).
- Branch `claude/c5-slot7-testplatform` of the work repo: `docs/slot7_testplatform/tools/export_chatlog.py` (base of the extended export tool in `verbatim_chatlog_recovery/`).

## PDK files (IHP-Open-PDK fork on the container, `/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/`)
- `sg13cmos5l.lyp`, `sg13cmos5l.map`: layer names and GDS layer/datatype (Metal1 8/0, Metal2 10/0, Metal3 30/0, Metal4 50/0, TopMetal1 126/0, GatPoly 5/0, Activ 1/0, nofill = datatype 23, filler = 22).
- `drc/rule_decks/sg13cmos5l_tech_default.json`: rule values (M1_*, Mn_*, TM1_*, Gat_*, Act_*, LU_*, density).
- `drc/rule_decks/beol/5_16_metal1.drc`, `5_17_metaln.drc`, `5_22_topmetal1.drc`, `7_3_metalslits.drc`; `geometry/3_1_offgrid.drc`, `3_2_angle.drc` (metals and poly 0/45/90 only; 5 nm grid); `forbidden/3_2_forbidden_cmos5l.drc`; `density.drc`; `feol/7_2_latchup.drc`, `5_9_gatpolyfiller.drc`; `layers_def.drc`.
- `drc/run_drc.py`, `lvs/run_lvs.py`: the DRC / LVS runners; `drc/docs/precheck_rules.md`.
- `scripts/filler.py`, `macros/sg13cmos5l_filler_Metal.lym`, `macros/sg13cmos5l_filler_ActGatP.lym`: the PDK filler (honours the nofill datatypes and layer 160/0; fills inside layer 39/0 only).
- `xsect/sg13cmos5l_for_EM.xs`: layer stack heights (poly/active about 1 um under Metal1).

## Not fetched, not consulted
SKY130 and GF180MCU rule decks: the statements about them in the skill (`Claude/skills/layout-art-from-image/references/pdk_checklist.md`) are marked as guesses.
