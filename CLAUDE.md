# CLAUDE.md — project context (cloud-task version)

Analog-on-top IC for **Chipalooza 2026**, PDK **ihp-sg13cmos5l**, forked from the Chipalooza Analog Project template.
Target: a **single-ended → differential → single-ended converter**. The repo still holds the template's example
circuits (`macros/inverter`, `macros/counter`); replacing them is the open task.

## Environment (Claude Code cloud session)

Tools are at `/foss/tools` (symlinked into `/usr/local/bin`), the PDK at `/foss/pdks/ihp-sg13cmos5l`, set up by the
environment's Setup script (`tatzelbrumm/claude-cloud-config`). Before any `make`, in the repo root:

```sh
export PDK_ROOT=/foss/pdks; source .designinit
```

Git works here: commit to the session branch and push it. No pull request, no chat log, unless asked.

**Local (non-cloud) sessions:** before anything else read `docs/local-container.md` and the "Local-only" section of
`docs/traps.md`. Local sessions run no git commands without asking first; the line above does not apply to them.

## Hard invariant: the top-cell name

`sg13cmos5l_cm_ip__single2diff2single` must agree in: `Makefile` `TOP =`, `submission.yaml` `top-cell:`, the file
names under `layout/`, `schematic/xschem/`, `testbenches/xschem/`, and the **GDS cell name inside `layout/*.gds` and
`layout/*.klay.gds`**. `make check-boundary` is the cheapest check.

## Make targets

`make -C <dir> <target>` for `macros/inverter`, `macros/counter` too.

```sh
make                      # help
make check-boundary       # cheapest sanity check after any rename
make klayout-verify-all   # DRC + LVS
make magic-verify-all     # DRC + LVS + PEX
make build-top            # boundary, LEF, LIB, verilog stub, GDS, render
make sim-all              # transient
```

Avoid `make all`: it runs the counter's LibreLane + FPGA flow, which is not installed in the cloud. Generated outputs
are committed, so re-run a target and `git diff` is the regression test.

## Traps

- **Full-RC PEX is not reproducible** (R varies 376–833 on identical geometry). Judge by element counts, never by diff;
  `EXT_MODE=2` gives a repeatable number.
- **Mismatch Monte Carlo is vacuous on an extracted netlist** (min = typ = max looks like a pass). Run mismatch on
  `-s schematic`; process MC (`tt_stat`) survives extraction.
- **CACE falls back to the schematic silently** without a `layout:` key in `paths:`. Always pass `-s` explicitly.
- **`#` in a `\`-continued make recipe is a shell comment** and eats the rest of the `&&` chain. Comments only at column 0.

## Read on demand (not imported — open the file only when the task needs it)

| file | when |
|---|---|
| `docs/traps.md` | KLayout launch, Xschem testbenches, Icarus, CACE — layout, schematic or simulation work |
| `docs/state-and-next-task.md` | what is verified, and the teardown list for replacing the template modules |
| `docs/record-keeping.md` | only if asked for a chat log, or to file run logs |
| `docs/local-container.md` | only for local Docker use, worktrees, and the `sudel_buecher` notes branch |

Never switch the checkout to the orphan branch `sudel_buecher`: it empties the working tree.
