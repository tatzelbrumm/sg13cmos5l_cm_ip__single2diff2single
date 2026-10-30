<!-- Moved verbatim from CLAUDE.md (blob 6201ab3, commit 1903407). Read only when the task needs it. -->

# Stage-specific traps

**KLayout: launch from the file's own directory** (`cd layout && klayout -e <file>`) —
that is what `sak-open.py` does, and the `.klib`'s relative `lib_path` depends on it.
Do **not** pass `-nn <techfile>` when `KLAYOUT_PATH` is set: it registers a duplicate
technology `<name>[1]` and the PDK machinery fails.

**`x2` / `x3` in every testbench are unwired spares.** To go post-layout, change `x1`'s
symbol to `<CELL>_pex.sym` at the same coordinates. Do not clear their `spice_ignore`.

**The template's `adm_db` is not a gain** — it divides absolute peaks including the DC
offset. Real small-signal gain is `vout_pp / vin_pp`.

**`sim-xschem` runs `xschem save`** and can leave the testbench `.sch` modified even on
a clean pass.

**Icarus cannot model IHP stdcell `ifnone` `specify` paths** (68 warnings). Gate-level
sim is functionally accurate, not timing-accurate. Timing comes from LibreLane STA.

**A cosmetic CACE error to ignore:** `Unable to open … sg13g2.lyp`. CACE hardcodes a
fallback filename for the sibling PDK; this one ships `sg13cmos5l.lyp`. It only breaks
the datasheet's layout thumbnail, after all numbers are computed.

## Local-only: agent git access (does NOT apply in cloud sessions, where git commit/push is the normal way to deliver work)

**Agent git access here: read-only, and even that isn't safe — treat it as fully
off-limits.** The sandbox can't `unlink`/`rename` in a connected folder's `.git/`, and a
bare `status`/`log`, not just `add`/`commit`, can leave an unremovable `index.lock`
(confirmed 2026-09-05). No git commands without asking first; if one locks, name the
exact file and stop — don't retry.

## History: renaming the top cell in a GDS

Renaming the top cell inside a GDS normally needs KLayout. It was once done as a
byte patch because the old and new names were both exactly 36 characters; a
later real KLayout re-export proved the patch byte-exact.

## Full text of the four traps summarised in CLAUDE.md

**Full-RC PEX is not reproducible.** Identical geometry, three runs: devices 90/90/90,
C 82/82/82, **R 574 / 833 / 376**. Magic's `extresist` reduction is threshold-driven and
unstable. Never read a PEX diff as a regression; judge by element counts. Use
`EXT_MODE=2` when you need a repeatable number. The digital flow *is* deterministic —
LibreLane reproduced a GDS bit-for-bit across machines.

**Mismatch Monte Carlo is vacuous on an extracted netlist.** `mm_ok=1` appears on the
schematic devices and on none of the extracted ones, and Magic splits `ng=20` into
twenty separate fingers. Symptom: min = typ = max in the CACE summary, which *looks*
like a pass. Run mismatch on `-s schematic`; process MC (`tt_stat`) survives extraction.

**CACE silently falls back to the schematic netlist** when `paths:` in the `.yaml` has
no `layout:` key — the default `-s best` tries extracted, fails to find a layout, and
says nothing. Always pass `-s` explicitly.

**`#` inside a `\`-continued make recipe is a *shell* comment** and eats the rest of the
`&&` chain → `Syntax error: end of file unexpected`. Comments are only safe at column 0
with no preceding backslash.
