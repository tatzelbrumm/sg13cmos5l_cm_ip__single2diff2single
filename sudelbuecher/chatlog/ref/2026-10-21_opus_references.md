# References — 2026-10-21 to 2026-10-22 — Opus Banba bandgap / schematic session

Sources consulted for
[`../2026-10-21_opus_banba_bandgap_schematics_and_bg_core_cleanup.md`](../2026-10-21_opus_banba_bandgap_schematics_and_bg_core_cleanup.md),
indexed per this directory's rule (index, do not copy).

## Literature

- H. Banba, H. Shiga, A. Umezawa, T. Miyaba, T. Tanzawa, S. Atsumi, K. Sakui, "A CMOS bandgap reference
  circuit with sub-1-V operation," *IEEE JSSC*, vol. 34, no. 5, pp. 670–674, May 1999. The PDF was
  attached by the user in Turn 2 (IEEE Xplore download, UC San Diego licence); it is not copied here.
- K. N. Leung, P. K. T. Mok, "A sub-1-V 15-ppm/°C CMOS bandgap voltage reference without requiring low
  threshold voltage device," *IEEE JSSC*, vol. 37, no. 4, April 2002. Cited from memory; a reproduction
  was found at <https://www.slideshare.net/slideshow/a-sub1v-15ppm-c-cmos-band-gap-voltage-reference/53107024>.
- Other citations in Turn 1 (Kuijk 1973, Brokaw 1974, Widlar 1971, Malcovati 2001, Rincon-Mora & Allen
  1998, Neuteboom 1997, Annema 1999, Sanborn/Ma/Ivanov 2007) were given from memory, not looked up.

## Web pages fetched or found

- <https://inst.eecs.berkeley.edu/~ee140/sp18/banba.pdf> — the Banba paper, behind a Berkeley login
  (redirect, not read).
- <https://alab.iee.nycu.edu.tw/~mdker/Referred%20Journal%20Papers/Ker_JSChen_IEICE_2005.pdf> — Ker and
  Chen, IEICE 2005, sub-1-V bandgap without low-V_T devices (listed as a source, not read).

## Tools and PDK (cloud container, as pinned in `sudelbuecher/cloud_environment.md`)

- xschem <https://github.com/StefanSchippers/xschem> at `ddc734480d5326fb787993dad24f4062e5d28434`
  (3.4.8RC). Building it also needed the apt packages `flex` and `bison`, which the recipe does not list.
- IHP-Open-PDK, iic-jku fork <https://github.com/iic-jku/IHP-Open-PDK> at
  `c271a7e97a7bab201c1d0a399215969d2ee19573`, sparse checkout of `ihp-sg13cmos5l/libs.tech/xschem/` and
  `ihp-sg13g2/libs.tech/xschem/`.
- The analog-schematic skill (`anthropic-skills:analog-schematic`), its `scripts/sch_netlist.py` and
  `tests/golden.py`.

## Project files read

- Main repo: `CLAUDE.md`; `macros/README.md`; `macros/d2s_bias_bg_pd/README.md` and its sheet, symbol and
  `xschemrc`; `macros/d2s_bias_sel_pd/README.md`, `bg_core_pd.sch` / `.sym`, `xschemrc`;
  `macros/d2s_bias_in_pd/README.md`, `d2s_bias_out_pd/README.md`, `d2s_bias_oa_pd/README.md`; git history
  of `power_down/xschem/` (commits `8bdbbb0`, `685c2bc`).
- Notes worktree: `class_ab_pad_driver/improvements/bias.md` (variant 4), `improvements/xschem/README.md`,
  `improvements/xschem/scripts/export_figures.py`, `power_down/xschem/d2s_bias_bg_pd.sch`,
  `port_gf180/kickoff_port_gf180.md` (as a model for the kickoff), `sudelbuecher/cloud_environment.md`,
  `verbatim_chatlog_recovery/verbatim-chatlog-export.md`, and `chatlog/2026-10-06_opus_class_ab_pad_driver_power_down.md`
  (as a model for this log).
