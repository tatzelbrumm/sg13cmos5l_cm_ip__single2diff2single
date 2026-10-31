<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# A5: inputs

Staged into the cloud workspace on 2026-10-31 at 04:08, under `/mnt/user-data/uploads/`, from Christoph's computer: the PDK files from his checkout `IHP-Open-PDK` at `6ac9bb9d` (2026-10-26; some resolve through the PDK's links to `ihp-sg13g2` paths), the pad macro files, and two notes. Read-only for the agent.

| sha256 | bytes | file |
|---|---:|---|
| 26e28c28024411a9… | 944701 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.doc/doc/SG13CMOS5L_os_process_spec.pdf` |
| 6c921a403b30c309… | 1153031 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.doc/doc/SG13CMOS5L_os_layout_rules.pdf` |
| 4704625f619ad55a… | 3244 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/ngspice/models/cap_cmomf.lib` |
| ea8e1e2b2efcb072… | 4070 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/ngspice/models/cap_cmomi.lib` |
| 6813c423f6669bf0… | 3025 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/ngspice/models/cornerCAP.lib` |
| 68f3fc5450d6185c… | 6665 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSCAP.lib` |
| 4873c91eb09fbd16… | 2202 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_moscap_mod.lib` |
| 52e62c52e7097b3d… | 32352 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_moscap_parm.lib` |
| b6ae39c7334c75c2… | 5179 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_svaricaphv_mod.lib` |
| 5a1f862dc304fdfe… | 24384 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/cornerMOShv.lib` |
| 58ce3084c253f2d3… | 9279 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_moshv_mod.lib` |
| eea5bbed39184cb1… | 64329 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_moshv_parm.lib` |
| 6b39225c5e4ff875… | 7222 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/verilog-a/cap_cmomf/cap_cmomf.va` |
| 5d107c82f363d581… | 25481 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/verilog-a/cap_cmomi/cap_cmomi.va` |
| 146eec0c2a9c3c43… | 35538 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/verilog-a/mosvar/mosvar.va` |
| c981ee834d00424c… | 14453 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/verilog-a/mosvar/mosvarpspMacros.va` |
| 1ab3b5fbb4281654… | 21421 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/cap_cmomf_code.py` |
| d10090d8df3319c2… | 29254 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/cap_cmomi_code.py` |
| baa4b65aad44c68a… | 14916 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/python/sg13g2_pycell_lib/ihp/moscap_n_code.py` |
| ee1ca881d71e2816… | 16137 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/python/sg13g2_pycell_lib/ihp/moscap_p_code.py` |
| 6ff0eebe417b3a71… | 7538 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/SVaricap_code.py` |
| d9830b9f0841f707… | 1544 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/xschem/sg13cmos5l_pr/cap_cmomf.sym` |
| 9cf1014e40b7ab91… | 1536 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/xschem/sg13cmos5l_pr/cap_cmomi.sym` |
| 58737591dfe7cbad… | 1462 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/xschem/sg13cmos5l_pr/cap_cmomi.tcl` |
| 6a82c8d060ed9228… | 1615 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/moscap_n.sym` |
| cd0a277247876340… | 1637 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/moscap_p.sym` |
| 3999f7161db38870… | 1613 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/sg13_svaricap.sym` |
| e793b434ff6a2fc0… | 138178 | `IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_maximal.drc` |
| a71a4f6250b0220a… | 42605 | `IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/layers_def.drc` |
| f1176d9c55624cd2… | 2410 | `sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadDiff2Single/netlist/source/sg13cmos5l_IOPadDiff2Single.spice` |
| aa4290437add6954… | 1094 | `sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadDiff2Single/netlist/source/d2s_out.spice` |
| cf65a6e2b379de18… | 3206 | `sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadDiff2Single/netlist/source/d2s_mpdda_pd.spice` |
| 73b630687680d7c8… | 21135 | `sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadDiff2Single/README.md` |
| e270a2192a51860d… | 1571914 | `sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds` |
| 01123fb7c54a10af… | 17587 | `sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/pad_buffer_layout/layout_primitives.md` |
| debbfa40598bc6d1… | 26201 | `sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/esd_protection/ihp_sg13cmos5l_io_esd_notes.tex` |
