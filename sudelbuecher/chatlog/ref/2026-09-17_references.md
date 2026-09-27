# References — 2026-09-17 — SG13CMOS5L pad docs session

Sources consulted for
[`../2026-09-17_sonnet_sg13cmos5l_pad_docs_and_project_setup.md`](../2026-09-17_sonnet_sg13cmos5l_pad_docs_and_project_setup.md),
indexed per this directory's rule (index, do not copy).

## GitHub — IHP-Open-PDK

- [PR #1223 — stdcell and IO alignment sg13g2 and sg13cmos5l](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1223) —
  adds `sg13cmos5l_io`'s ESD/level-shift primitives (`LevelDown`,
  `DCPDiode`/`DCNDiode`, `Clamp_P15N15D`/`N15N15D`, `GateDecode`,
  `SecondaryProtection`, `RCClampResistor`); layout fix to
  `sg13cmos5l_LevelDown`'s input threshold/receiver balance.
- [PR #1207 — libs.ref: add sg13cmos5l_stdcell_hv](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1207) —
  lands the 3.3V HV stdcell library for CMOS5L by symlinking SG13G2's
  thick-oxide cells; author's comment: "the I/O cells and level shifters
  need to be designed" (this PR predates #1223).
- [PR #1072 — KLayout PyCell bondpad: Fixed evaluation of parameter fill](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1072) —
  fixes a dead `fill == 't'` condition in `bondpad_code.py`; gave the real
  file path `.../sg13cmos5l_pycell_lib/ihp/bondpad_code.py` used to locate
  the source directly.
- [Issue #1109 — KLayout PyCells use inconsistent and undocumented cell-origin conventions](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/1109) —
  audits 37 PCells' origin conventions; `bondpad`/`via_stack` are
  bbox-center, most active-device PCells are core-lower-left; maintainer
  thread (`dnltz`/`sergeiandreyev`) on `bondpad`'s origin vs. OpenROAD's
  lower-left requirement, unresolved as of reading.
- [Issue #1229 — Correct pad cell for flip-chip bump attach](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/1229) —
  asks whether `bondpad` with `FlipChip="yes"`, `shape="octagon"` is the
  right cell for a 60 µm flip-chip bump opening; unanswered by maintainers
  as of reading. Filed against SG13G2.
- `ihp-sg13g2/libs.tech/klayout/python/sg13g2_pycell_lib/ihp/bondpad_code.py`
  (raw.githubusercontent.com, `main` branch) — read in full (529 lines);
  the SG13G2 counterpart diffed against CMOS5L's copy.
- `ihp-sg13g2/libs.ref/sg13g2_io/cdl/sg13g2_io.cdl` (same host) — grepped
  for `.SUBCKT`, `IOPadAnalog`'s port list, and `.GLOBAL` occurrences (none
  found).
- `.gitmodules` (repo root) — lists the PDK's external submodules
  (`pycell4klayout-api`, `pypreprocessor`, digital/openems/palace
  integrations); consulted while hunting for `bondpad_code.py`'s actual
  path before PR #1072 gave it directly.

## GitHub — IHP-GmbH/ihp-sg13cmos5l (satellite repo)

- `libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/bondpad_code.py`
  (raw.githubusercontent.com, `main` branch) — read in full (475 lines);
  the file PR #1072 actually touched (404s from the main `IHP-Open-PDK`
  monorepo — it lives here instead).
- `libs.ref/sg13cmos5l_io/cdl/sg13cmos5l_io.cdl` (same host) — read in full
  (947 lines); every `.SUBCKT` name extracted, plus full bodies of
  `GateDecode`, `SecondaryProtection`, `LevelDown`, `IOPadIn`,
  `IOPadAnalog`, and the `sg12g2_Gallery` test/gallery cell (note the "12"
  typo in that one name).
- Repo root page (WebFetch) — description as a temporary satellite/wrapper
  repo for the CMOS5L PDK during a build/migration script effort.

## GitHub — iic-jku/ihp-sg13cmos5l

- `libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/bondpad_code.py`
  (raw.githubusercontent.com, `main` branch) — spot-checked, matches the
  `IHP-GmbH` copy byte-for-byte at this path (both returned HTTP 200 with
  the same content when probed).

## IHP OpenPDK documentation (ReadTheDocs)

- [IO and Periphery Library — Available Cells](https://ihp-open-pdk-docs.readthedocs.io/en/latest/contents/io_library/01_available_cells.html) —
  full `sg13g2_io` cellset with per-cell descriptions (signal pads, supply
  pads, corner/filler cells).
- [IO and Periphery Library — Output Drive Strength](https://ihp-open-pdk-docs.readthedocs.io/en/latest/contents/io_library/02_drive_strength.html) —
  4/16/30 mA naming convention and the underlying NMOS/PMOS finger-count
  scaling.
- Docs root (`/en/latest/`) — used only to locate the two pages above via
  its table of contents; no other section read this session.

## Not usable / dead ends (noted so a future session doesn't retry)

- `codeload.github.com` and `api.github.com` — blocked by this sandbox's
  proxy without an `add_repo` grant; `raw.githubusercontent.com` works fine
  for the same content and was used instead throughout.
- `grep.app`, `sourcegraph.com`, `data.jsdelivr.com` (package listing) —
  either proxy-blocked or returned no usable structured result when tried
  as alternatives to GitHub's own (blocked) code search.
- GitHub's own `/tree/...` and `/search?...&type=code` pages — robots.txt
  disallowed for `WebFetch`.
