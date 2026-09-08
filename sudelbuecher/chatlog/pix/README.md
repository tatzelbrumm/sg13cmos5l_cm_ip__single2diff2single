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

Not the place for design renders: those are generated artifacts and belong in
`render/img/`, produced by `make render-gds`.
