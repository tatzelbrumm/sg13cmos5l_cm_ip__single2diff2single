# References — 2026-10-06 to 2026-10-08 — Opus power-down session

Sources consulted for
[`../2026-10-06_opus_class_ab_pad_driver_power_down.md`](../2026-10-06_opus_class_ab_pad_driver_power_down.md),
indexed per this directory's rule (index, do not copy).

## Project files read (the user's own, read in place or staged read-only)

- `sudelbuecher/design_considerations/class_ab_pad_driver/power_down/kickoff_power_down.md` (the task).
- `class_ab_pad_driver/improvements/`: `log.md`, `bias.md`, `xschem/README.md`; `sim/d2s_mpdda.spice`,
  `d2s_bias_lp.spice`, `d2s_bias_ref.spice`, `d2s_lc2.spice`, `units.spice`, `ccomp.spice`, `run_bias.py`,
  `run_improvements.py`, `results_bias.txt`, `results_improvements.txt`; the hand-edited sheets in `xschem/`
  that the `_pd` sheets were copied from.
- `class_ab_pad_driver/class_ab_pad_driver.md`, `run_d2s.py`, `d2s_bias.spice`, `d2s_miller.spice`,
  `d2s_loadcomp.spice`.
- `sudelbuecher/cloud_environment.md` (the pinned tool versions), and
  `sudelbuecher/verbatim_chatlog_recovery/verbatim-chatlog-export.md` (how this log was built).
- Main repo: `CLAUDE.md`, `TOP_LEVEL_MODULE.md` §2–§4,
  `macros/OgueyAebischerBias/verification/cace/_docs/reference.md` and
  `macros/OgueyAebischerBias/verification/cace/netlist/schematic/reference.spice` (`ToBiasStartup`'s
  `disable`).
- The claude.ai project doc `claude/sg13cmos5l_pad_cell_internals.md`.

## PDK and tools (cloud container, as pinned in `cloud_environment.md`)

- IHP-Open-PDK, iic-jku fork: <https://github.com/iic-jku/IHP-Open-PDK>, branch `dev`, commit
  `c271a7e97a7bab201c1d0a399215969d2ee19573` (2026-09-21), sparse checkout of the cmos5l and sg13g2
  xschem / ngspice / verilog-a directories plus `ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/cdl/`.
  - `sg13cmos5l_io.cdl`: the clamp cells (`Clamp_P20N0D`, `Clamp_N20N0D`, `Clamp_P15N15D`,
    `Clamp_N15N15D`, `Clamp_N43N43D4R`), `LevelUp`, `LevelUpInv`, `GateDecode`, `GateLevelUpInv`, and the
    pad cells `IOPadAnalog`, `IOPadOut30mA`, `IOPadInOut30mA`, `IOPadVdd`, `IOPadIOVdd`. Read for how IHP
    ties clamp gates.
- xschem: <https://github.com/StefanSchippers/xschem>, commit `ddc734480d5326fb787993dad24f4062e5d28434`
  (3.4.8RC).
- ngspice: <https://github.com/danchitnis/ngspice-sf-mirror>, tag `ngspice-47`.
- OpenVAF: <https://github.com/arpadbuermen/OpenVAF>, commit `5ed9e63afe70ac95129a78af7b3732e7d431b1e5`,
  built as `openvaf-r` with LLVM 18.
