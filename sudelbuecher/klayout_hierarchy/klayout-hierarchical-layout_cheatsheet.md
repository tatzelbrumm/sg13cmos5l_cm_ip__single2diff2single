# KLayout Hierarchical Layout — Checklists

Companion to `sg13cmos5l_cm_ip__single2diff2single/CLAUDE.md` §5 and `README.md`
("KLayout editing source"). Two paths to the same result — pick one, don't mix
mid-session.

## A. Open path — `make open` / `sak-open.py` (recommended default)

* Container running:
  ```sh
  cd ~/EDA/IIC-OSIC-TOOLS
  DESIGNS="$HOME/EDA" DOCKER_TAG=2026.08 CONTAINER_NAME=iic-osic-tools-2026-08-sw \
    DOCKER_EXTRA_PARAMS='-e LIBGL_ALWAYS_SOFTWARE=1' ./start_x.sh
  ```
  (X11, not VNC; restart by rerunning this, not `docker start`)
* Inside container: `cd /foss/designs/sg13cmos5l_cm_ip__single2diff2single && source .designinit`
* `make open` (= `sak-open.py .`; add `OPEN_ARGS=--all` to also see build outputs)
* Pick `layout/klayout/sg13cmos5l_cm_ip__single2diff2single.klay.gds` from the
      browser — **not** the plain `.gds` (that's the tapeout export, not the editing source)
* Confirm the `inverter` library resolved: Library Selector / cell view shows
      `inverter` as real geometry, not an empty/missing placeholder
* Edit, place macro instances, draw geometry
* Save (stays as `.klay.gds` — symbolic, PCells + library refs intact)
* `File > Export Layout For Tapeout` → overwrites `layout/sg13cmos5l_cm_ip__single2diff2single.gds`
* `make check-boundary` — cheapest check that the top-cell name still matches
* `make klayout-verify-all` (DRC + LVS) before committing

## B. Manual path — direct `klayout` invocation

Only if you have a reason to bypass `sak-open.py` (scripting, remote X quirks). Every
item below is a documented trap (`CLAUDE.md` §5) — skip one and you get a silent or
confusing failure, not an error message.

* Container running + `.designinit` sourced (same two steps as A) — sets `PDK`,
      `PDKPATH`, `STD_CELL_LIBRARY`, `KLAYOUT_PATH`
* `echo $KLAYOUT_PATH` is non-empty, points at `.../ihp-sg13cmos5l/libs.tech/klayout`
* `cd layout/` — the **parent** of `layout/klayout/`. Not `layout/klayout/` itself,
      not the repo root.
  - Reason: `klayout/sg13cmos5l_cm_ip__single2diff2single.klay.klib`'s `lib_path`
    (`../macros/inverter/layout/inverter.gds`) resolves against **cwd at launch**, not
    the `.klib` file's own location. Wrong cwd → library silently fails to bind,
    `inverter` instances draw empty/missing.
* `klayout -e klayout/sg13cmos5l_cm_ip__single2diff2single.klay.gds`
  - `-e` = edit mode. **No `-nn <techfile>`.** `KLAYOUT_PATH` already registers the
    technology; `-nn` creates a duplicate `sg13cmos5l[1]` and breaks both the PDK and
    the `.klib` binding (which deliberately declares `"technology": ""`).
* Verify `inverter` resolved (as in A) before touching anything else

### Referencing an existing macro as a library cell

* If its `.klib` entry already exists, it's already listed — instantiate via
      Library Selector / New Cell, library name = that entry's `lib_name`

### Adding a *new* macro as a library reference

* Build/harden it first (`make build-<macro>` or equivalent) so its GDS exists on disk
* Edit `layout/klayout/sg13cmos5l_cm_ip__single2diff2single.klay.klib` (plain JSON)
      — append to `statements`:
  ```json
  {"lib_name": "<macro>", "lib_path": "../macros/<macro>/<path-to-gds>"}
  ```
  Path is relative to `layout/` (per the cwd rule above), **not** to the `.klib` file's
  own location.
* Reload libraries in KLayout (or relaunch) — new entry appears in the Library Selector
* Place the instance

### Finishing, either way

* Save — `.klay.gds` stays symbolic (PCells + library refs), not static geometry
* `File > Export Layout For Tapeout` → writes/overwrites
      `layout/sg13cmos5l_cm_ip__single2diff2single.gds` — the static file every
      DRC/LVS/PEX/build target actually reads. Editing `.klay.gds` and forgetting this
      step means signing off on stale geometry.
* If anything was renamed: confirm the **GDS cell name inside both `.gds` and
      `.klay.gds`** still equals `TOP` in the `Makefile` and `top-cell:` in
      `submission.yaml`. `make check-boundary` checks this cheaply.
* `make klayout-verify-all` before committing — re-run the full sign-off after any
      layout change, not just DRC. Generated outputs are committed, so `git diff` after
      re-running is the regression test.

---

Sources: `sg13cmos5l_cm_ip__single2diff2single/CLAUDE.md` §§2, 4, 5; `README.md`
("KLayout editing source" section, mixed-signal `.klib` example); the cwd-resolution
bug as debugged in `save_from_claudes_fuckup/2026-08-30_i_claude_rename.md`.
