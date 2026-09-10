# `pix/`

Images for the notes in `sudelbuecher/`.

- `2026-09-04_opus_oab_trouble_spots.png` / `.svg` — annotated
  `OgueyAebischerBias` core schematic marking the three measured weaknesses
  (supply-tracking Vds on M13/M14/M10, the `vbr` positive-feedback loop, the
  1 µm² device area). Belongs to
  [`../2026-09-04_opus_cace_templates_and_oab_sizing.md`](../2026-09-04_opus_cace_templates_and_oab_sizing.md).
  Generated, not hand-drawn: the source is
  `macros/OgueyAebischerBias/doc/trouble_spots.py` in the design repo, which
  builds it from a transcription of `reference.spice` via the
  `analog-schematic` skill's netlist-first renderer. The copy here is the
  figure as it stood at the end of that session.
- `2026-09-04_opus_oab_unannotated.png` — the same circuit before the
  annotation overlay was added. Kept because it is the readable version if
  you only want the topology.

- `2026-09-06_sonnet_gatedecode_npath_drc.png` / `.svg` — DRC-clean
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

- `2026-09-10_sonnet_clamp_n20n0d_unitcell_drc.png` / `.svg` — DRC-clean
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

Not the place for design renders: those are generated artifacts and belong in
`render/img/`, produced by `make render-gds`.
