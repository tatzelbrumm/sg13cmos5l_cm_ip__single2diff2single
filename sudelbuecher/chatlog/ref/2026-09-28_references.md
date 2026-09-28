# References — 2026-09-28 — `sg13cmos5l_io` by-reference / PCell-discovery session

Sources consulted for
[`../2026-09-28_sonnet_sg13cmos5l_io_klib_reference_and_sg13_dev_pcells.md`](../2026-09-28_sonnet_sg13cmos5l_io_klib_reference_and_sg13_dev_pcells.md),
indexed per this directory's rule (index, do not copy).

## IHP PDK — `ihp-sg13cmos5l`, as installed in the running IIC-OSIC-TOOLS container

- `$PDK_ROOT/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/` — full directory layout (`gds/`,
  `spice/`, `lib/`, `doc/`, `vacask/`, `lef/`, `verilog/`, `cdl/`) enumerated by the user's
  own `find $PDKPATH/libs.ref/sg13cmos5l_io -maxdepth 2`, run inside the container and
  attached as `find_sg13com5l_io.log` (Turn 2 of the transcript). Not fetched by this
  assistant — this session has no shell inside the container itself (`docker` unavailable
  from the device-bridge sandbox), only the host-mounted project folders.
- `libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds` and
  `libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spice` — referenced by path only; their
  contents were not opened this session. Existence and location confirmed by the `find`
  output above; their role (the combined pad-cell GDS; an ngspice-`.include`-able netlist
  deck) inferred from the project's own `claude/sg13cmos5l_pad_cell_internals.md` doc
  (below) plus `scripts/extract_pad.py`'s existing use of the same `.gds` file.
- `libs.tech/klayout/python/sg13cmos5l_pycell_lib/ihp/` — the KLayout PyCell sources
  (`bondpad_code.py`, `sealring_code.py`, etc.). Not read directly this session; cited via
  the project doc below, which had already read them in a prior session
  (`2026-09-17_sonnet_sg13cmos5l_pad_docs_and_project_setup.md` / its matching
  `ref/2026-09-17_references.md`).

## This project's own Claude-Project doc (outside the git repo)

- `claude/sg13cmos5l_pad_cell_internals.md` — read in full via `Projects.project_read` at
  the start of this session. Source of the `IOPadAnalog` pin-order trap
  (SG13CMOS5L: `iovdd iovss pad padres vdd vss`, vs. SG13G2's different order), the
  `pad`/`padres` split behind `SecondaryProtection`'s ~587 Ω series resistor, and the
  `sg13cmos5l_pycell_lib` path used to point the user at IHP's own PCell conventions.

## KLayout Salt packages (seen live in the running session's GUI, not independently fetched)

- **`LibraryManagerPlugin` 0.27** — "Library manager for hierarchical layouts," author
  Martin Jan Köhler, identified via the Salt Package Manager's Current Packages list
  (Turn 8/9 screenshots). This is the plugin that owns the `.klib` JSON format
  (`{"technology":..., "statements": [{"lib_name":..., "lib_path":...}]}`), the
  `File > Manage Cell Library Map...` / `File > Reload Cell Libraries` menu items, and
  (confirmed this session) `$PDKPATH`-style environment-variable expansion in `lib_path`.
- **`KLayoutPluginUtils` 0.28** — "Utility Library for KLayout Plugins," same author,
  used by various IIC-JKU KLayout plugins. Documentation link as shown in that package's
  own Details pane in the Salt Package Manager screenshot:
  <https://github.com/iic-jku/klayout-plugin-utils> — this URL was read off the GUI
  screenshot, not fetched by this assistant (no `WebFetch`/`WebSearch` call was made this
  session).
- Same author/organization (IIC-JKU) as the wider IIC-OSIC-TOOLS toolchain already on file
  in `/areas/analog-circuit-course.md`, consistent rather than independently verified this
  session.

## Not usable / limits encountered (noted so a future session doesn't retry the same thing)

- `docker` is not installed in this assistant's device-bridge sandbox (`device_bash`) —
  `docker ps` / `docker exec <container> ...` both failed with "command not found." There is
  no way for this assistant to get a shell inside the running IIC-OSIC-TOOLS container
  directly; anything that needs to run *inside* the container (enumerating `$PDKPATH`
  contents, checking `KLAYOUT_PATH`'s pymacro registration, etc.) has to be run by the user
  and pasted back, as was done for the `find_sg13com5l_io.log` attachment.
- No git command (`status`, `log`, `diff`, `show`) was run against
  `sg13cmos5l_cm_ip__single2diff2single` from this assistant's `device_bash` sandbox, on
  request, given this repo's own documented finding (`CLAUDE.md` §3/§5) that even read-only
  git through that sandbox can leave an unremovable `index.lock`.
