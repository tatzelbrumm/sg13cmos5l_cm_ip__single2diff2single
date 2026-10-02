# `ref/`

Pointers to sources used by the notes in `sudelbuecher/`, one file per
session, named to match the transcript.

Rule: **index, do not copy.** Third-party documents stay at their source —
this repository carries SPDX headers throughout and is a Chipalooza
submission, so unlicensed copies of other people's docs do not belong in it.

- [`references.md`](references.md) — the `i_claude` rename session and everything since
- [`2026-09-04_references.md`](2026-09-04_references.md) — the ocd-reconciliation /
  OgueyAebischerBias CACE session (was missing from this index until now)
- [`2026-09-04_opus_references.md`](2026-09-04_opus_references.md) — the parallel
  Opus CACE-templates / OAB-sizing session (ditto)
- [`2026-09-05_references.md`](2026-09-05_references.md) — xschem explainer +
  `IOPadInOut30mA` sourcing session
- [`2026-09-17_references.md`](2026-09-17_references.md) — the SG13CMOS5L
  `bondpad`/`sg13cmos5l_io` PCell-and-CDL deep-dive session (public
  IHP-Open-PDK GitHub source + ReadTheDocs), which also settled where
  Claude's own working notes for this project should live
- [`2026-09-28_references.md`](2026-09-28_references.md) — the `sg13cmos5l_io`
  by-reference / PCell-discovery session: the PDK's own `libs.ref/sg13cmos5l_io/`
  layout (from the user's own in-container `find`, not fetched by the
  assistant), the project's own PCell-internals doc, and the KLayout Salt
  packages (`LibraryManagerPlugin`/`KLayoutPluginUtils`, IIC-JKU) identified
  live in the GUI
- [`2026-09-28_opus_references.md`](2026-09-28_opus_references.md) — the Opus
  `Clamp_N`/`Clamp_P` PCell session: the IHP GitHub repos and commits cloned in the cloud
  container, the user's own `sg13cmos5l_io.{gds,cdl}` copies, and the KLayout versions used
- [`2026-10-02_sonnet_references.md`](2026-10-02_sonnet_references.md) — the Edwards &
  Cauwenberghs log-domain search session: two earlier claude.ai chats and the user's own
  `~/DoNotLitter` PDFs and `.bib` files, indexed by path and not copied

Run logs live one level up in [`../logs/`](../logs/) and are committed to the
branch that produced them, so their contents differ per branch. The chat log,
this directory and `../pix/` are deliberately untracked pending a decision on
how to version them.
