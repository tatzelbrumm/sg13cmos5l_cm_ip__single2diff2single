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

Not the place for design renders: those are generated artifacts and belong in
`render/img/`, produced by `make render-gds`.
