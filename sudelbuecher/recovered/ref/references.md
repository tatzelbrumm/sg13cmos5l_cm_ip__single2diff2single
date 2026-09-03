# References — 2026-08-30 session

Index only. No third-party documents are copied into this repository; each
entry points at the source. Fetch what you need at read time.

## External

| Ref | Source | Used for |
|---|---|---|
| R1 | <https://github.com/iic-jku/IIC-OSIC-TOOLS> | Container image (`docker.io/hpretl/iic-osic-tools`), launcher scripts, env vars (`DESIGNS`, `DOCKER_TAG`, `CONTAINER_USER/GROUP`, `WEBSERVER_PORT`, `VNC_PORT`, `DRY_RUN`), `/foss/designs` mount point, noVNC password `abc123`, ~4 GB image / ≥20 GB free |
| R2 | <https://github.com/HeiChips/heichips26-template> | `nix-shell` alternative to the container (cited by the project README) |
| R3 | <https://iic-jku.github.io/ihp-sg13cmos5l-ams-chip-template/index.html> | ihp-sg13cmos5l AMS chip design tutorial (cited by the project README) |
| R4 | `git@github.com:tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single.git` | This repository's `origin` |

## Local, outside this repository

| Ref | Path | Used for |
|---|---|---|
| L1 | `~/EDA/IIC-OSIC-TOOLS` | Launcher-script clone, at `2026.08-3-gdb8e081b`. Read-only during this session. |
| L2 | `~/EDA/cheatsheets/iic-osic-tools_cheatsheet.md` | The user's own container recipes — X11 start command, `LIBGL_ALWAYS_SOFTWARE=1`, per-tag container naming, "do not use `docker start`", `sak-pdk`, alias persistence via `$HOME/EDA/.designinit`. Read-only, by instruction. |
| L3 | `~/EDA/cheatsheets/docker_cheatsheet.md`, `git-submodule-cheatsheet.md`, `codex_cheatsheet.md` | Present, not read this session. |
| L5 | `.../skel/foss/tools/sak/sak-open.py` (in the IIC-OSIC-TOOLS clone) | Authoritative answer to "how does JKU launch KLayout": `klayout -e <file>`, cwd = the file's own directory, no technology flag |
| L6 | `$PDKPATH/libs.tech/klayout/tech/` | `sg13cmos5l.lyt` (technology), `sg13cmos5l.lyp` (layer properties), `sg13cmos5l.map`. Note: no `ihp-sg13cmos5l.lyp` and no `sg13g2.lyp` — the reason CACE's thumbnail fails |
| L8 | `macros/counter/rtl/{constants,counter,counter_top}.sv` | the digital RTL; `TOP = counter_top`, hardened to 194.16 × 85.10 µm |
| L7 | CACE 2.11.0, `cace/common/common.py:173` and `cace/cace_cli.py:128` | `get_klayout_layer_props()` hardcoded fallback; the `-s/--source` choices |
| L4 | `$HOME/EDA/.designinit` | The file the container actually sources, because `DESIGNS="$HOME/EDA"`. Distinct from this repo's own `.designinit`. |

## In this repository

| Ref | Path | Used for |
|---|---|---|
| P1 | `README.md` § "To rename the project" | The procedure this session followed |
| P2 | `Makefile` (`TOP`, `CELL`, `_GDS_EXT`) | Target and variable reference |
| P3 | `submission.yaml` | Precheck fields; `top-cell` must equal `TOP` |
| P4 | `scripts/check_boundary.py` | PR boundary check, layer 189; also the cheapest validator of the GDS top-cell name |
| P5 | `layout/*.klay.klib` | KLayout library binding to `macros/inverter/layout/inverter.gds` |
| P6 | `macros/inverter/README.md` | Full reference for every Makefile target and parameter |
| P7 | `macros/inverter/verification/cace/inverter.yaml` | CACE datasheet: pins, conditions, the three parameter sets and their `corner_mos` / `corner_r` selections |
| P8 | `macros/inverter/verification/cace/templates/inverter_tb_ac.sch` | CACE testbench template; `.lib cornerMOSlv.lib mos_{corner_mos}` is where the statistical models enter |

## Git objects from this session

| Object | SHA | Note |
|---|---|---|
| `main`, `origin/main` | `baf9173` | Initial commit, untouched |
| tag `from_template` | → `baf9173` | Annotated. "repository as forked from template" |
| branch `generated_deleted` | `baf9173` | Redundant with the tag |
| `i_claude`, `origin/i_claude` | `743c8a8` | The rename: 26 renames + 4 edits |
| `i_claude` | `cf2bfef` | `make klayout-verify-all` — successful run after renames |
| `i_claude` | `dd78933` | `make magic-verify-all` — successful run after renames |
| `i_claude` | `7eb861a` | plots redrawn after `make sim-view-xschem` |
| `i_claude` | `692ee56` | `make -C macros/inverter magic-pex` — locally re-run |
| `inverter_pex` | `ad09f82` | inverter testbenches hand-edited to use `inverter_pex` as DUT (local branch, not pushed) |
| `inverter_pex` | `18e5e54` | after re-export of the tapeout GDS from `.klay.gds` |
| `inverter_pex` | `622e07d` | check-boundary + klayout-verify-all + magic-verify-all + build-top after the re-export |

### After the commit resort (2026-08-31)

Seven commits on `inverter_pex` were split by purpose into three branches off a
shared base. Old SHAs survive only via `pre-resort-*` tags and the reflog.

| Branch | SHA | Note |
|---|---|---|
| `i_claude` | `0ba2efb` | tapeout GDS re-export (was `18e5e54`, minus the CACE csv) |
| `i_claude` | `4ac0fee` | check-boundary + verify-all + build-top (was `622e07d`) |
| `i_claude` | `bedcc83` | `sudelbuecher/logs/` — rename and top-level runs |
| `counter_digital` | `87b798a` | counter lint/RTL/cocotb/LibreLane (was `d83b0ae`) |
| `counter_digital` | `7f247f6` | counter magic-pex (was `82e250b`) |
| `counter_digital` | `649fd99` | `sudelbuecher/logs/` — counter digital flow, LibreLane log gzipped |
| `inverter_pex` | `1104af4` | inverter testbenches → `_pex` DUT (was `ad09f82`) |
| `inverter_pex` | `a0a1f05` | sim-cace with `-s`, CACE_SOURCE work (was `ca45746`) |
| `inverter_pex` | `e49b81e` | rebuilt inverter figures (was `b875f27`) |
| `inverter_pex` | `a0ececc` | `sudelbuecher/logs/` — inverter PEX runs |

Author on all resorted commits is Christoph Maier; committer on those and on
the four log/resort commits is `I, Claude <claude@invalid>`, set repo-local
with the user's authorisation and unset afterwards.

## Run logs in this directory

| File | Produced by |
|---|---|
| `magic-verify-all.out` | `make magic-verify-all > >(tee ...)` — 228 lines. Magic DRC clean, Magic+Netgen LVS "Circuits match uniquely", PEX ports all connected. |
| `magic-verify-all.err` | stderr of the same run — 6 lines, Xschem announcing `XSCHEM_SHAREDIR` and PDK model paths. Informational, not failures. |
| `make_klayout-verify-all.makelog`, `make_build-top.makelog` | make transcripts of those targets |
| `sim-all.out` / `.err` | top-level `make sim-all` — pre-layout transient |
| `sim-view-xschem.out` / `.err` | top-level plot regeneration |
| `inverter_magic_pex.out` / `.err` | `make -C macros/inverter magic-pex` |
| `inv-sim-all.out` / `.err` | inverter `sim-all` — post-layout testbenches + CACE on schematic |
| `counter-lint.*`, `counter-sim-rtl-verilog.*`, `counter-sim-rtl-cocotb.*` | the RTL tier of the digital flow — Verilator, Icarus, cocotb 4/4 |
| `counter-build-top.out.gz` / `.err` | LibreLane hardening, 799 KB gzipped to 51 KB. `zless` / `zgrep`. All eight checkers clear. |
| `counter-magic-pex.*` | full-RC PEX of `counter_top`, all ports connected |
| `counter-sim-gl-cocotb.*` | gate-level cocotb 4/4; the 68 stderr lines are Icarus `ifnone` limitations |
| `counter-sim-gl-xschem.*` | XSPICE co-simulation; `Reducing trtol to 1 for xspice 'A' devices` |
| `inv-cace-pex.out` / `.err` | `sim-cace` with `-s pex`; shows the collapsed mismatch distribution and the `sg13g2.lyp` datasheet error |
| `i_claude_rename.gitlog` | A `git status` dump of the pre-commit staging state. Superseded by `git show --stat -M 743c8a8`, which additionally pairs the Magic LVS report as a rename. |

## Verbatim-quoted command output

All command output reproduced in the transcript was quoted by the user in
their own messages (`docker images`, `docker ps --all`, the `make
check-boundary` run). Tool-call output produced by the assistant is not
reproduced; it is reconstructible from the repository and from git history —
notably `git show --stat -M 743c8a8`.
