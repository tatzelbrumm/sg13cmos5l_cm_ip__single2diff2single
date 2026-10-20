# References — 2026-10-20 — Opus pad input buffer session

Sources consulted for
[`../2026-10-20_opus_s2d_input_buffer_architecture_and_verification.md`](../2026-10-20_opus_s2d_input_buffer_architecture_and_verification.md),
indexed per this directory's rule (index, do not copy).

## Project files read (the user's own, read in place or staged read-only)

- `_sudelbuecher/CLAUDE.md`; main repo `CLAUDE.md` (§6), `TOP_LEVEL_MODULE.md` §1–§4.
- `sudelbuecher/chatlog/README.md`, `chatlog/2026-10-06_opus_class_ab_pad_driver_cace_verification_setup.md`.
- `sudelbuecher/verbatim_chatlog_recovery/{verbatim-chatlog-export.md, chat-recovery-after-compaction.md}`,
  `sudelbuecher/cloud_environment.md`.
- `sudelbuecher/description/s2d_d2s_pinbuffers.md`.
- `sudelbuecher/design_considerations/`: `s2d_input_buffer_topology_verbatim.md`,
  `pad_test_circuit_suggestions_verbatim.md`.
- `design_considerations/class_ab_pad_driver/`:
  - `class_ab_pad_driver.md`;
  - `improvements/`: `proposed_improvements.md`, `bias.md`, `log.md`; `sim/units.spice`,
    `d2s_mpdda.spice`, `d2s_bias_lp.spice`, `d2s_bias_ref.spice`, `ccomp.spice`, `run_improvements.py`,
    `run_bias.py`, `tb/tb_mpdda_{loop,dc,noise,op}.spice`; `xschem/{unit_r2,d2s_mpdda,d2s_mpdda_biased}.{sch,sym}`,
    `xschem/xschemrc`, `xschem/check_xschem.py`, `xschem/README.md`, `xschem/scripts/export_figures.py`;
  - `power_down/`: `kickoff_power_down.md`, `log.md`, `sim/d2s_mpdda_pd.spice`, `sim/d2s_bias_ref_pd.spice`,
    `sim/tb/tb_pd_leak.spice`;
  - `build_verification_suite/kickoff_build_verification_suite.md`, `port_gf180/kickoff_port_gf180.md`;
  - `verification/cace/`: `README.md`, `d2s_miller_biased.yaml`, `first_run_summary.md`,
    `scripts/d2s_miller_mc.py`, `templates/d2s_miller_biased_tb_{dc,loop,noise,ac,tran}.sch`,
    `templates/xschemrc`; `xschem/d2s_miller_biased.{sch,sym}`, `run_d2s.py`.
- Main repo `macros/`: `sg13cmos5l_IOPadSingle2Diff` and `sg13cmos5l_IOPadDiff2Single` (sheets and
  symbols), `ls_up_1v2_3v3/verification/cace/ls_up_1v2_3v3.yaml`; `scripts/cace/{cace_to_csv.py, spec_table.py}`.
- `sg13cmos5l_ocd_chipalooza`: `config.txt` (pad types), `scripts/parse_config.py`,
  `verilog/gl/sg13cmos5l_padframe.v`, `verilog/rtl/chipalooza_frame.v` (grep only).
- The claude.ai project doc `claude/sg13cmos5l_pad_cell_internals.md`.

## PDK and tools (cloud container, as pinned in `cloud_environment.md`)

- IHP-Open-PDK, iic-jku fork: <https://github.com/iic-jku/IHP-Open-PDK>, branch `dev`, commit
  `c271a7e97a7bab201c1d0a399215969d2ee19573`, sparse checkout of the cmos5l and sg13g2 xschem / ngspice /
  verilog-a directories plus `ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/cdl/`.
  - `libs.tech/ngspice/models/cornerRES.lib`, `resistors_mod.lib`, `resistors_stat.lib` (a symlink into
    ihp-sg13g2): read for why the `res_stat` process Monte Carlo varies rhigh per instance.
  - `libs.tech/xschem/sg13cmos5l_pr/sg13_hv_{nmos,pmos}.sym`, `xschemrc`.
- xschem: <https://github.com/StefanSchippers/xschem>, commit `ddc734480d5326fb787993dad24f4062e5d28434`.
- ngspice: <https://github.com/danchitnis/ngspice-sf-mirror>, tag `ngspice-47`.
- OpenVAF: <https://github.com/arpadbuermen/OpenVAF>, commit `5ed9e63afe70ac95129a78af7b3732e7d431b1e5`.
- IIC-OSIC-TOOLS: <https://github.com/iic-jku/IIC-OSIC-TOOLS>, tag `2026.09`: `_build/tool_metadata.yml`
  and `_build/images/iic-osic-tools/skel/headless/scripts/install_eda.sh` (CACE 2.11.0).
- CACE 2.11.0 from PyPI, under Python 3.12: `cace/common/cace_regenerate.py` and
  `cace/parameter/parameter_ngspice.py`, read for how the DUT and the templates are netlisted (`.spice`
  templates are not implemented in 2.11).

## Literature (cited from memory in `s2d_input_buffer.md`, not fetched)

- E. Säckinger, W. Guggenbühl, IEEE JSSC SC-22(2), 1987 (differential difference amplifier).
- B. A. Minch, Ph.D. thesis, Caltech, 1997 (function inversion by negative feedback).
- J. F. Duque-Carrillo, Analog Integrated Circuits and Signal Processing 4, 1993 (common-mode control).
- H. J. Oguey, D. Aebischer, IEEE JSSC 32(7), 1997 (current reference without resistance).
