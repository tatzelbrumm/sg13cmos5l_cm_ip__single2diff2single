# References — 2026-09-28 — Opus session: parametrized `sg13cmos5l` Clamp_N/Clamp_P PCells

Sources consulted for
[`../2026-09-28_opus_sg13cmos5l_clamp_pcells_skill_and_worktree_questions.md`](../2026-09-28_opus_sg13cmos5l_clamp_pcells_skill_and_worktree_questions.md),
indexed per this directory's rule (index, do not copy). The PDK repositories below were
cloned into the session's cloud container only; nothing from them was copied into this
repository apart from the geometry that `scripts/pcells/clamp_refdata.py` extracts from the
Apache-2.0 `sg13cmos5l_io` cells (with IHP's copyright line carried in that file's header).

## The user's own files (connected folders)

- `~/EDA/chipalooza_cmos5L/sg13cmos5l_io.gds` (67,512,320 bytes) and
  `~/EDA/chipalooza_cmos5L/sg13cmos5l_io.cdl` — the reference layouts and netlists of
  `sg13cmos5l_Clamp_{N,P}{2,8,15}N..D`, `..._{N,P}20N0D` and `..._N43N43D4R`. Staged into
  the container and read with `klayout.db`; their sha256 sums are recorded in the header of
  `scripts/pcells/clamp_refdata.py`.
- `sudelbuecher/chatlog/` (`README.md`, `ref/README.md`, `pix/README.md`,
  `2026-09-28_sonnet_chatlog_export_meta_and_formatting_corrections.md`) and both
  `CLAUDE.md` files — read for the chat-log conventions in Turn 14
  (split off into `2026-09-28_opus_safety_stops_and_chatlog_export.md`).

## This project's own Claude-Project doc (outside the git repo)

- `claude/sg13cmos5l_pad_cell_internals.md` — read at the start of the session: the
  `sg13cmos5l_io` cell list, the undeclared `sub!` node, and the PyCell origin conventions.

## IHP PDK sources (GitHub, sparse clones in the cloud container)

- [`IHP-GmbH/ihp-sg13cmos5l`](https://github.com/IHP-GmbH/ihp-sg13cmos5l) at
  `597570eec556a473d1eedb22c055545d4522f442` (2026-09-23):
  - `libs.tech/klayout/python/sg13cmos5l_pycell_lib/__init__.py` — `moduleNames` and the
    `PyCellLib` registration pattern copied by `scripts/pcells/__init__.py`.
  - `libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/esd_code.py` — the "extracted
    polygons" convention used for the frame and tie-block data.
  - `libs.tech/klayout/tech/sg13cmos5l.lyp` — layer name → GDS layer/datatype map.
  - `libs.tech/klayout/tech/drc/` (`ihp-sg13cmos5l.drc`, `run_drc.py`, `rule_decks/`) —
    run on KLayout 0.28.16 with a one-line compatibility shim (see the log, Turn 1).
  - `libs.tech/klayout/tech/lvs/run_lvs.py` — refused to run below KLayout 0.30.2.
  - `libs.tech/xschem/sg13cmos5l_pr/{dantenna,dpantenna,ptap1,rppd,sg13_hv_nmos,sg13_hv_pmos}.sym`
    — ngspice `format` strings used by `scripts/pcells/clamp_netlist.py`.
- [`IHP-GmbH/IHP-Open-PDK`](https://github.com/IHP-GmbH/IHP-Open-PDK) at
  `5e6d592e4002946a4616f798c357f0f3c06cf3b6` (2026-09-01), `ihp-sg13g2/...` — targets of the
  symlinks above: `sg13g2_pycell_lib/ihp/{geometry,utility_functions,nmosHV_code,rfnmos_code,rfmosfet_base_code}.py`,
  `tech/drc/rule_decks/layers_def.drc`, `tech/lvs/rule_decks/*`, `xschem/sg13g2_pr/*.sym`.
- [`IHP-GmbH/pycell4klayout-api`](https://github.com/IHP-GmbH/pycell4klayout-api) at
  `ad47f5f7d5708103d6415a61b87a7218b65de495` (2026-09-24) — the `cni` API (`dlo.py`,
  `layer.py`, `text.py`, `point.py`, `box.py`); a submodule left empty in the sparse clone.
- [`IHP-GmbH/pypreprocessor`](https://github.com/IHP-GmbH/pypreprocessor) at
  `cf1ff9bad0fb5338cf1c5b990b2b816b1ea01a64` (2024-12-09) — needed to import
  `sg13cmos5l_pycell_lib` standalone; also an empty submodule in the sparse clone.

## Tools

- [`klayout` on PyPI](https://pypi.org/project/klayout/) 0.30.12 — `klayout.db` (geometry,
  XOR, `LayoutToNetlist` for `scripts/pcells/lvs_clamp.py`) and `pya` for the PCell runtime.
- Ubuntu 24.04 package `klayout` 0.28.16 — batch DRC (`klayout -b -r`). Newer KLayout
  builds (klayout.org, conda-forge) were unreachable from the container.
