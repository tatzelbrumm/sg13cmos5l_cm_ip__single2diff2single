# References — 2026-10-02 to 2026-10-08 — Opus class-AB pad driver session

Sources consulted for
[`../2026-10-02_opus_class_ab_pad_driver_improvements.md`](../2026-10-02_opus_class_ab_pad_driver_improvements.md),
indexed per this directory's rule (index, do not copy).

## Papers and theses

- The user's own copies under `~/DoNotLitter/`, read in place on his computer and never copied:
  - `TimEdwards/`, `LogDomain/` and `FloatingGate/`, including `FloatingGate/Hasler/thesis_chapter*.ps`;
  - `Sarpeshkar_R_1997.pdf`, a scan, OCR'd locally on that computer.
  - Which papers were used, and for what: `design_considerations/class_ab_pad_driver/improvements/literature_notes.md`.
- R. Sarpeshkar, PhD thesis, Caltech 1997: <https://thesis.caltech.edu/3063/>, pointed out by the
  user as an alternative to OCR.
- H. J. Oguey, D. Aebischer, "CMOS current reference without resistance", IEEE JSSC 32(7), 1997.
  Cited for the bias variant `d2s_bias_oa`; not fetched.
- The claude.ai project doc `claude/sg13cmos5l_pad_cell_internals.md`.

## PDKs

- IHP-Open-PDK: <https://github.com/IHP-GmbH/IHP-Open-PDK>, branch `dev`, sparse checkout in the
  cloud container at `3591278` (2026-10-02). The simulation results in `improvements/` come from it.
- The iic-jku fork that IIC-OSIC-TOOLS installs: <https://github.com/iic-jku/IHP-Open-PDK>.
  - Commit `c271a7e97a7bab201c1d0a399215969d2ee19573`, which the user read from the 2026.09 image's
    `$PDK_ROOT/ihp-sg13cmos5l/COMMIT`.
- gf180mcu:
  - primitives at <https://github.com/fossi-foundation/globalfoundries-pdk-libs-gf180mcu_fd_pr>,
    HEAD `e11a8c9`;
  - <https://github.com/RTimothyEdwards/open_pdks>;
  - the ciel release asset `gf180mcu-1689ac3f2dc763876eaf967227c7dfe831b031ae/common.tar.zst` at
    <https://github.com/fossi-foundation/ciel-releases>.

## Tools

- IIC-OSIC-TOOLS: <https://github.com/iic-jku/IIC-OSIC-TOOLS>, tag `2026.09`, which supplied
  `_build/tool_metadata.yml`, `RELEASE_NOTES.md` and the PDK install scripts.
- xschem: Ubuntu's 3.4.4 at first. Then <https://github.com/StefanSchippers/xschem>, tag `3.4.7` and
  commit `ddc734480d5326fb787993dad24f4062e5d28434` (3.4.8RC).
- ngspice: Ubuntu's ngspice 42 at first. Then `ngspice-47` from the mirror
  <https://github.com/danchitnis/ngspice-sf-mirror>.
- OpenVAF-reloaded: <https://github.com/arpadbuermen/OpenVAF>, built from source; commit `5ed9e63`.
- ciel 3.0.1 from PyPI. Its download failed on the GitHub API, so the release asset was fetched
  directly.
