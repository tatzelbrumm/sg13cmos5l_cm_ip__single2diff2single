# `pix/`

Images for the notes in `sudelbuecher/`.

- [`2026-09-04_opus_oab_trouble_spots.png`](./2026-09-04_opus_oab_trouble_spots.png) / [`.svg`](./2026-09-04_opus_oab_trouble_spots.svg) — annotated
  `OgueyAebischerBias` core schematic marking the three measured weaknesses
  (supply-tracking Vds on M13/M14/M10, the `vbr` positive-feedback loop, the
  1 µm² device area). Belongs to
  [`../2026-09-04_opus_cace_templates_and_oab_sizing.md`](../2026-09-04_opus_cace_templates_and_oab_sizing.md).
  Generated, not hand-drawn: the source is
  `macros/OgueyAebischerBias/doc/trouble_spots.py` in the design repo, which
  builds it from a transcription of `reference.spice` via the
  `analog-schematic` skill's netlist-first renderer. The copy here is the
  figure as it stood at the end of that session.
- [`2026-09-04_opus_oab_unannotated.png`](./2026-09-04_opus_oab_unannotated.png) — the same circuit before the
  annotation overlay was added. Kept because it is the readable version if
  you only want the topology.

- [`2026-09-06_sonnet_gatedecode_npath_drc.png`](./2026-09-06_sonnet_gatedecode_npath_drc.png) / [`.svg`](./2026-09-06_sonnet_gatedecode_npath_drc.svg) — DRC-clean
  transistor-level render of `sg13cmos5l_IOPadInOut30mA`'s `GateDecode`
  N-path (`io_inv_x1` → `io_nor2_x1` → `LevelUp`), built with the
  `analog-schematic` skill from a transcription of the ChatGPT-produced
  `.spi` in `sudelbuecher/sg13cmos5l_IOPadInOut30mA/`. Belongs to
  [`../2026-09-05_sonnet_xschem_explainer_and_iopad30ma_sourcing.md`](../2026-09-05_sonnet_xschem_explainer_and_iopad30ma_sourcing.md).
  This session's own generated output (unlike the ChatGPT/Opus artifacts in
  that same cell folder, which stay where they are and are only linked, not
  copied — see that transcript's turn 3 and `ref/2026-09-05_references.md`
  §4). Source of truth is
  `sudelbuecher/sg13cmos5l_IOPadInOut30mA/sg13cmos5l_GateDecode_npath_drc.py`;
  the copy here is the figure as it stood at the end of that turn. DRC
  proves this transcription internally well-formed, not that it matches the
  real IHP cell — see the transcript for the caveat in full.

- [`2026-09-10_sonnet_clamp_n20n0d_unitcell_drc.png`](./2026-09-10_sonnet_clamp_n20n0d_unitcell_drc.png) / [`.svg`](./2026-09-10_sonnet_clamp_n20n0d_unitcell_drc.svg) — DRC-clean
  transistor-level render of `sg13cmos5l_Clamp_N20N0D`'s unit cell (3 of
  its 20 parallel self-biased NMOS fingers, plus the `Roff` bias resistor
  that holds the shared gate node near `iovss`), a dependency of
  `sg13cmos5l_IOPadAnalog`. Unlike the GateDecode render above, built
  directly from the real `sg13cmos5l_io.spi` (not a ChatGPT
  transcription) — see
  `sudelbuecher/sg13cmos5l_IOPadAnalog/sg13cmos5l_IOPadAnalog_real_hierarchy.spi`
  for the sourced excerpt with line numbers, and
  `sudelbuecher/sg13cmos5l_IOPadAnalog/sg13cmos5l_Clamp_N20N0D_unitcell_drc.py`
  for the build script (source of truth; the copy here is the figure as
  it stood when generated). No chat-log transcript covers this work yet —
  linked here in advance of one being requested. DRC proves the netlist
  internally well-formed; the topology it draws (self-biased passive
  clamp: gates tied to one internal node, biased by a single resistor, no
  external gate pin) is read directly off the real subckt, not inferred.
  `sg13cmos5l_IOPadAnalog` has no digital control path at all (no
  `GateDecode`/`LevelUp` — see that `.spi` excerpt file's header note), so
  this unit cell is the only part of the cell that is both fully
  MOSFET/resistor-only and small enough to render legibly; the rest is
  either more of this same clamp array or diode-primitive ESD structures
  the skill cannot draw.

- [`2026-09-28_sonnet_klayout_sg13cmos5l_io_library_resolved.png`](./2026-09-28_sonnet_klayout_sg13cmos5l_io_library_resolved.png) — screenshot
  of the running KLayout session's main window (Cells/Layers/Libraries
  panels, "SG13CMOS5L PDK" custom menu), Libraries dropdown showing
  `sg13cmos5l_io - sg13cmos5l_io.gds` resolved with real cell names listed
  below it. Belongs to
  [`../2026-09-28_sonnet_sg13cmos5l_io_klib_reference_and_sg13_dev_pcells.md`](../2026-09-28_sonnet_sg13cmos5l_io_klib_reference_and_sg13_dev_pcells.md)
  (Turn 6). User-taken screenshot of their own screen, not generated. Proves
  the `.klib` `lib_path` entry `$PDKPATH/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds`
  (added earlier that same turn sequence) resolves — i.e. the KLayout
  `LibraryManagerPlugin` expands `$PDKPATH` at load time. Does not prove
  anything about which specific cells are safe to place yet, only that the
  library itself is reachable.
- [`2026-09-28_sonnet_salt_package_manager_current_packages.png`](./2026-09-28_sonnet_salt_package_manager_current_packages.png) — screenshot
  of KLayout's Salt Package Manager, "Current Packages" tab, listing
  `KLayoutPluginUtils`, `AlignToolPlugin`, `AutoBackupPlugin`,
  `LayerShortcutsPlugin`, `LibraryManagerPlugin`, `MoveQuicklyToolPlugin`,
  `NetlistImportPlugin`, `PinToolPlugin`, `VectorFileExportPlugin`, `xsection`;
  `KLayoutPluginUtils` highlighted, its Details pane showing author Martin
  Jan Köhler and a `github.com/iic-jku/klayout-plugin-utils` documentation
  link. Belongs to the same file, Turn 8. Identifies the actual author/origin
  (IIC-JKU) of the `.klib` mechanism and the custom "SG13CMOS5L PDK" menu
  used earlier in that session — see `ref/2026-09-28_references.md`.
- [`2026-09-28_sonnet_cell_library_manager_dialog.png`](./2026-09-28_sonnet_cell_library_manager_dialog.png) — screenshot of the
  `LibraryManagerPlugin`'s own "Cell Library Manager" dialog
  (`File > Manage Cell Library Map...`), showing the Layout/Library-Map
  paths for `sg13cmos5l_IOPadDiff2Single`, and the Library Mappings table:
  `sg13cmos5l_io` → `$PDK_ROOT/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds`,
  Status `OK`. Belongs to the same file, Turn 9. This is the GUI equivalent
  of hand-editing the `.klib` JSON that the earlier turns in that session
  did manually — found by the user, not this assistant (no screen access
  from this session).
- [`2026-09-28_sonnet_sg13_native_pcell_lib_cells_panel.png`](./2026-09-28_sonnet_sg13_native_pcell_lib_cells_panel.png) — screenshot of
  the Cells/Libraries panel with `SG13_native_pcell_lib - SG13G2 Native
  PCells [Technology sg13cmos5l]` selected, cell list showing `Via`. Belongs
  to the same file, Turn 10.
- [`2026-09-28_sonnet_sg13_dev_pcell_lib_cells_panel.png`](./2026-09-28_sonnet_sg13_dev_pcell_lib_cells_panel.png) — screenshot of the
  same panel with `SG13_dev - IHP SG13CMOS5L Pcells [Technology sg13cmos5l]`
  selected instead, listing the full device-primitive set: `NoFillerStack`,
  `SVaricap`, `bondpad`, `cap_cmomf`, `cap_cmomi`, `chipText`, `dantenna`,
  `dpantenna`, `esd`, `guard_ring`, `nmos`, `nmosHV`, `ntap1`, `pmos`,
  `pmosHV`, `pnpMPA`, `ptap1`, `rfnmos`, `rfnmosHV`, `rfpmos`, `rfpmosHV`,
  `rhigh`, `rppd`, `rsil`, `sealring`, `via_stack`. Belongs to the same file,
  Turn 10. Proves the `SG13_dev` PCell library (Python-code PCells,
  registered via `KLAYOUT_PATH`, not a `.klib` path entry) was already fully
  registered with zero extra setup — the actual finding of that turn.
- [`2026-09-28_sonnet_bingo_reaction.jpg`](./2026-09-28_sonnet_bingo_reaction.jpg) — a reaction still (Christoph Waltz
  in character, captioned "THAT'S A BINGO!") sent alongside the two panel
  screenshots above, Turn 10 of the same file. **Not evidence of anything
  technical** — kept only because the chat-log rule for this export is
  unabridged/verbatim and the user sent it as part of that turn. Flagged,
  not silently decided: this is a copyrighted film still with meme text
  overlay, third-party material, and `ref/README.md`'s "index, do not copy"
  rule (adopted because this repository carries SPDX headers throughout as
  a Chipalooza submission) was written with exactly this kind of unlicensed
  third-party copy in mind, even though that rule as stated is about
  external *documents* rather than reaction images specifically. `pix/` and
  this whole `sudelbuecher/` tree are the orphaned notes branch, not part of
  the submission's tracked design content — but the branch still lives in
  the same repository. Worth the user's own explicit call on whether this
  one file should stay, rather than this assistant deciding it unilaterally
  either way.

Not the place for design renders: those are generated artifacts and belong in
`render/img/`, produced by `make render-gds`.
