<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Running log: building `sg13cmos5l_IOPadDiff2Single` (layout and macro)

Session 2026-10-27, Claude (configured model `claude-opus-5-5`; the serving model may differ), cloud
container linked to Christoph's computer, attached to the claude.ai Project "Chipalooza sg13cmos5l".
Newest entries are at the bottom. Times are Europe/Berlin (CET).

Task: the session title "Put together the sg13cmos5l_IOPadDiff2Single layout and macro" (09:46), with
Christoph's correction of 09:47 ("You don't need to do it outright, all on your own, quite yet. But your
looking for information is good.") and his note of 09:54: "But now the design goes from the sudelbuecher
design considerations into the actual macro in the main git repository."

Chat log: `sudelbuecher/chatlog/2026-10-27_opus_iopaddiff2single_build.md`, exported at checkpoints.

## 09:46–09:55: state found (read only)

- Macro layout `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds`:
  80 × 180 µm, boundary 189/4. Clamp_P_M1 at y 65–84, two Clamp_N_M1 at y 5–26, DCPDiode (y 51–65),
  DCNDiode (y 25–40), TopLayersTo4, Metal3ViasUp, contacts, pdrainwire, ndrainwire, via stacks. The circuit
  zone y 84–178 is empty. Labels: `pad` (10/25), `sub!` (63/0).
- `sudelbuecher/design_considerations/pad_buffer_layout/klayout/pad_buffer_cells.gds`: 13 d2s cells, 10 s2d
  cells, the bias tree (4), the OA core and the bandgap core; DRC clean, LVS against `pad_buffer_cells.cdl`
  (38 subckts). Fit heights in 80 µm (zone 94 µm): d2s front 74.0, with Miller capacitors 82.5;
  bias tree + OA + bandgap 102.3.
- `pad_buffer_layout/klayout/cell_tree.md` predates the rework of the night: it still lists `oa_pmir_a/b`,
  `bg_pmir`, `bg_pcas` (now `oa_pmir`, `bg_pmir_pcas`).
- No layout yet: `en_ctrl_3v3`, `ls_up_1v2_3v3`, `hv_logic`, the decode of `d2s_bias_sel_pd`.
- The macro README's "Not done" says the pad cell has no layout yet; the `.klay.gds` has the ESD / output part.

## 09:59–10:05: decisions

1. Reference cores: "Reference cores go in the slot". Bias interface (answer 10:05): "One current, sel in
   slot". The pad keeps `d2s_bias_in_tree_pd`, fed by one sourced current (~5 µA) from the slot's bias
   root; decode, harness TG, OA core and bandgap core move to the slot; `sel0_1v2` / `sel1_1v2` leave the pad.
2. Cell library: "Separate cell-library GDS bound through .klay.klib for now." Location (answer 10:05):
   "Shared by both pads".
3. "layout driven netlist changes": the list in `pad_buffer_layout/klayout/README.md` ("Netlist changes the
   cells imply") and `layout_primitives.md` §7.
4. Logging: "session results in the sudelbuecher go into sg13cmos5l_IOPadSingle2Diff_build. Export chat log
   at checkpoints." (09:54); folder (answer 10:05): "omit the design_considerations from your suggestion
   sg13cmos_IOPadDiff2Single_build", read as `sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/` (this folder).

## 10:05–10:12: export script

- `design_considerations/pad_buffer_alternatives/export.py` extended: AskUserQuestion questions with their
  options, and the user's answers, are written verbatim (they are tool records, which the script dropped).
- First chat-log export.

## 10:21–10:30: clean slate in the macro's layout folder; `oldvias` removed (Christoph: "For starters, look at
## sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds
## and sg13cmos5l_IOPadDiff2Single.klay.klib. Move the other hierarchical design attempts in there into the backups to
## clean the slate. Then get rid of leftover vias from the wiring I started to try and replace by hand in the cell.";
## 10:26: "oldvias are obsolete; I isolated them so they can be replaced and eventually deleted.")

- `.klay.klib` binds only `sg13cmos5l_io` (`$PDKPATH/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds`); unchanged.
- Moved into `layout/klayout/backups/`, names unchanged (`backups/` is gitignored, so git sees them as deleted):
  `clamps`, `sg13cmos5l_IOPadDiff2Single_manualPcell`, `sg13cmos5l_IOPadDiff2Single_use_clamp_cells_swap_in_view`,
  `test` (`.klay.gds` and `.klay.klib` each). `size_mockup/` stays (device-area mockup, used by
  `layout_primitives.md`).
- `oldvias`: 368 Via1, no metal, one instance at (36.737, 27.245); 204 of them without Metal2 above. With them, the pad
  Metal2 was tied to the DCNDiode anode comb (iovss), the DCPDiode cathode comb (iovdd) and the guard-ring / tap
  Metal1. Without them, the pad Metal2 reaches only DCN cathodes, DCP anodes and the Clamp_P / Clamp_N drains (55
  top-level via_stack instances plus the drain-wire cells). Cell and instance deleted.
- Kept: the 226 Via1 and 1084 Via2 drawn in the top cell (all with metal on both sides: ring and tap plate), the
  marker shapes on 63/0.
- Written with the KLayout 0.30.12 Python module in the cloud container: only Via1 differs (3710 → 3342 shapes); the 63
  PCell-context strings (`SG13_dev` via_stack, `SG13_cm_clamps`) are identical. 3397894 bytes, sha256 `6f2484ee…`.
- The auto-backup of 2026-10-24 22:10 differs from the saved cell only in Clamp_N contacts / Metal1 (y 8–23),
  presumably the PCell re-evaluated on opening; not used.

## 10:24–10:30: auto-backup volume (Christoph: "Autosave produces HUGE amounts of data. How can I (or you, for me) keep
## these from completely running away?"; 10:26: "ok i need to configure the klayout-auto-backup it seems.")

- `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/backups/`: 787 MB, 394 layouts (most from 30 Sep – 2 Oct).
- Plugin iic-jku/klayout-auto-backup (read from its source): every 5 min by default, only when the layout has unsaved
  changes that differ from the previous backup; file format "same as source" by default; naming by timestamp or
  incremental number; it never deletes old backups.
- Compressed GDS for one 3.43 MB backup: 0.64 MB (gzip).

## 10:29–10:33: chat-log checkpoint

- `export.py` extended again: messages sent while a turn runs (`queued_command` attachments in the transcript) become
  user turns marked "sent mid-turn"; before, they were dropped (10:24 and 10:26 here).
- Chat log re-exported (9 turns, every user and assistant text present, no overlap with the reasoning).

## 10:39–10:45: what fills `macros/` (Christoph: "Still lots of clutter in the macros directory, but I probably got rid
## of a lot of auto backups already.", with his `du -h -d 2`: 240 MB)

- Gitignored, regenerable, about 133 MB: OgueyAebischerBias `verification/cace/_runs` 67 MB and
  `testbenches/xschem/simulations` 13 MB; counter `flow/librelane/runs` 27 MB, `testbenches/xschem/simulations`
  5.7 MB, `flow/final` 2.5 MB; inverter `testbenches/xschem/simulations` 5.5 MB; IOPadDiff2Single `backups/` 12 MB
  (10 files left).
- Template examples, teardown pending (main repo `CLAUDE.md` §7): inverter 54 MB without its simulations (48 MB of it
  the four `.mat` lookup tables in `scripts/sizing/data`), counter 14 MB without runs and simulations (8.8 MB
  `plot_simulations`).
- `IOPad/layout/klayout`: 22 MB, six copies of IHP IO-cell GDS; no file in the repository refers to them.
- OgueyAebischerBias apart from its runs: under 1 MB (superseded by `d2s_bias_oa_pd`).

## 10:51–11:00: how IHP contacts the IO cell; text-layer reminders removed (Christoph: "in the pad layout that you
## started to clean, I moved some old metal2 lines to text. the leftmost one has bulges to the left that used to be
## clamp diode contacts. If you can get an idea how the original I/O pads are contacted, you can get rid of the text
## layer reminders for me.")

- `sg13cmos5l_IOPadAnalog` (copy in `macros/IOPad/layout/klayout/`), metal-only connectivity with the labels:
  - pad: one Metal2 comb, the bar y 0–3 (pin `pad`, x 5–75) and 9 lines 0.61 µm wide, pitch 3.02 µm, x 26.105 …
    50.875, y 3–179, joined at y 179–180 (core-side `pad` pin); one more line at x 53.3 up to the secondary
    protection. Via1 down to the clamp drains, the DCN cathodes and the DCP anodes.
  - iovss: Metal2 straps 0.2 µm wide on the source stripes (x 27.82 + k·3.02, y 8.1–51.8) plus a 1.53 µm strap at
    x 23.47–25 whose bulge lands on the DCN end; Via1 down to the Clamp_N sources, the DCN anode and the guard rings,
    Via2 up to the iovss Metal3 rails (19 per strap).
  - iovdd: the same at y 53.1–82.1: Via1 to the Clamp_P sources and the DCP cathode, Via2 to the iovdd rails (42 per strap).
- `sg13cmos5l_IOPadDiff2Single.klay.gds` today: the pad net is complete (clamp drains, DCN cathodes, DCP anodes).
  Not yet on the rails: the DCN anode comb, the DCP cathode comb, the clamp sources (iovss / iovdd straps of the IHP
  cell). Open wiring item.
- Christoph's reminders on 63/0 were these straps (16 shapes: two with the bulges at x 23.47, 14 lines 0.2 µm);
  deleted. Kept: the `sub!` label and the rectangle (36.355, 147.73; 45.815, 180.62), which is not a Metal2 line of
  the IHP cell (question to Christoph). Only 63/0 changed (17 → 1 shapes), PCell context identical. 3396822 bytes,
  sha256 `0d371ec1…`.
- `device_commit_files` silently wrote the previous file once (new mtime, old content) when the staging path was
  reused; a fresh staging path fixed it. Check the hash after every write.

## 11:25: library moved into IOPad by Christoph ("to work on the layout primitives, I exported their gds in the
## sudelbuecher and it became an unwieldy mess for me quickly. How can we keep things tidy in IOPad? For now, I just
## moved the pad_buffer_cells.gds and .cdl into IOPad. I uncluttered IOPad from the IHP pad copies by moving them into
## backup.")

- Now `macros/IOPad/layout/klayout/pad_buffer_cells.gds` (sha256 `fe2c540f…`) and `pad_buffer_cells.cdl`
  (`52fb7fad…`): the state of 26 Oct 09:15 in `pad_buffer_layout/log.md`. The six IHP IO-cell copies are in
  `macros/IOPad/layout/klayout/backups/`.
- Left in `design_considerations/pad_buffer_layout/klayout/`: 46 entries, 33 per-cell GDS exports, three DRC run
  folders, `backups/` (5.7 MB).

## 11:39: correction (Christoph: "NO. You're introducing `netlist/source` . Is there any precedent for this? There IS a
## `schematic/xschem` directory, and YOU'RE JUST FUCKING IT UP WITH COMPLETE DISREGARD FOR SIDE EFFECTS.")

- Nothing was moved; the proposal of 11:25 is withdrawn.
- Checked: the template's `netlist/` holds generated output (`NET_SCH_DIR := netlist/schematic`, `netlist/layout`,
  `netlist/pex`); `make klayout-lvs-netlist` writes the LVS reference CDL from the xschem sheet into
  `netlist/schematic/<cell>_klayout.cdl`. `netlist/source/` exists in seven macros only because the consolidation
  session (Claude, 20 Oct) created it for hand-written decks; it is not a template convention.

## 11:44–11:55: IOPad inventory (Christoph: "First, handle the correspondence of the IOPad*.gds layouts and the
## schematic/xschem construction site, where I started putting together schematics and symbols for IHP's standard
## cells. I probably did similar work elsewhere in the sudelbuecher for the single2diff and diff2single schematics.
## IOPad as shared, consolidated library might be a good attractor for these, if we're ABSOLUTELY METICULOUS about
## avoiding software engineers' mindset and systematically ignoring side effects."; 11:51: "When you have a little
## time, sanity check the sg13cmos5l_IOPadDiff2Single.klay.klib I edited.")

- Read only. Result: `iopad_inventory.md` (this folder): the two kinds of file in `IOPad/schematic/xschem`, the six
  IHP IO-cell copies against the local PDK, the pad's PCells against its netlist (ON: 68 fingers drawn, 66 in the
  netlist; the diodes 63.78 µm drawn, IHP's 27.78 µm in the sheet), three IHP IO netlists with different pin orders,
  every reference to IOPad, and a proposal.
- `.klay.klib` (Christoph's edit): valid JSON; `pad_buffer_cells` → `../../../IOPad/layout/klayout/pad_buffer_cells.gds`
  exists. The Library Manager plugin (iic-jku/klayout-library-manager, current source) resolves relative paths
  against the `.klib`'s own folder and expands `$PDKPATH` from the environment (set by `.designinit`); a library path
  with `.klay` among its suffixes makes the plugin read a `.klay.klib` next to it, so the library keeps the plain
  `.gds` suffix.

## 12:44–12:47: PDK revision of the container (Christoph: "cat $PDK_ROOT/ihp-sg13cmos5l/COMMIT; ls
## $PDK_ROOT/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/spice/ a49358cc0b20635fcb53c0940505e3563763fc7a sg13cmos5l_io.spice")

- `a49358c` is iic-jku/IHP-Open-PDK dev of 2026-10-15. Its `sg13cmos5l_io.spice`, `.cdl` and `.gds` (fetched by
  commit from GitHub) are byte-identical to the local checkout (IHP-GmbH dev `0488153`) and to the cloud CACE
  revision (iic-jku dev `c271a7e`): one IO library in use. The black-box symbols match it.
- Outdated: `sudelbuecher/sg13cmos5l_IOPadInOut30mA/sg13cmos5l_io.spi` (2024-05-27) and the excerpt taken from it,
  the six IHP GDS copies in `IOPad/layout/klayout/backups/`, and the pin-order section of the project doc
  `claude/sg13cmos5l_pad_cell_internals.md`. `iopad_inventory.md` §3 rewritten accordingly.

## 13:00–13:04: project doc corrected (Christoph: "Yes, and yes ... while I still need to catch up with your logs and
## results.", to: correct the pin-order section of the project doc; sheets and symbols for the four PCells)

- `claude/sg13cmos5l_pad_cell_internals.md` (claude.ai project) and its copy
  `sudelbuecher/description/sg13cmos5l_pad_cell_internals.md` (identical before, identical after; sha256 `13dfca1c…`):
  dated correction note at the top; `IOPadAnalog` pin order and the CDL excerpts of `IOPadAnalog` and
  `SecondaryProtection` as in the PDK in use; the pin-order section rewritten (order changed across revisions); one
  source line. Flagged in the note but not rewritten: `sg12g2_Gallery` and the commented `*.GLOBAL sub!` no longer
  exist; `LevelDown` is now `core pad iovdd iovss vdd vss` with its first stages on iovdd / iovss. Section 1 (bondpad)
  not re-checked.

## 13:04–13:07: what the PCell sheets have to contain

- `scripts/pcells/README.md`: `Clamp_N_M1` pins `gate iovss pad`, one sg13_hv_nmos (D pad, G gate, S iovss), W =
  4.4 µm·ng, L = `l`, plus an unlabelled NWell guard ring to be tied to iovdd above; `Clamp_P_M1` pins
  `gate iovdd iovss pad`, one sg13_hv_pmos (S, B iovdd), W = 13.32 µm·ng (two rows); `DCNDiode` / `DCPDiode` pins
  `anode cathode guard`, 2 × dantenna (sub → cathode) / dpantenna (anode → cathode), w = 1.26u, l = `l`.
  `clamp_netlist.py` covers only the older `Clamp_N` / `Clamp_P`; no netlist exists yet for the M1 clamps or for the
  diodes at `l` ≠ 27.78u.
- LVS of the macros (`make klayout-lvs` → `sak-lvs.sh -k`, IIC-OSIC-TOOLS main): IHP `run_lvs.py --run_mode=deep
  --disable_tap_extraction`. No ptap1 / ntap1 in the sheets; NMOS bulk on the tapped net (as in
  `pad_buffer_cells.cdl`). The deck's `align` flattens cells without a same-named counterpart, so sheet names need not
  equal the layout cell names; equal names only give per-cell pairing.
- For the D2S pad: OP / ON are plain devices in `d2s_mpdda_pd` and are compared, after flattening, with the clamp
  frames (OP 82 × 6.66/0.6 matches; ON 68 drawn vs 66). DN / DP are IHP's black boxes (27.78 µm) against the PCells
  (63.78 µm), so the diode sheets are the ones LVS needs.

## 13:09: decisions (answers to three questions)

- "Which sheets should I draw now?" → "Diodes and both clamps".
- "What should the new sheets and symbols be called?" → "Layout cell names" (`DCNDiode`, `DCPDiode`, `Clamp_N_M1`,
  `Clamp_P_M1`, as the PCell cells; deep LVS pairs them by name).
- "ON: 68 fingers drawn (2 × 34), 66 in the netlist. Which wins?" → "Netlist follows layout" (ON ng = 68, w = 299.2u).

## 13:09–13:24: PCell sheets drawn; ON to 68 fingers

- Cloud workspace: xschem 3.4.4 (apt), the PDK's `libs.tech/xschem` of iic-jku/IHP-Open-PDK `a49358c` (fetched by
  commit). Found on the way (13:12): that commit has `libs.tech/xschem/sg13cmos5l_io/` with the fifteen pad cells as
  links to the SG13G2 symbols; `sg13cmos5l_IOPadAnalog.sym` netlists its pins as vss vdd iovss iovdd pad padres pad,
  not in the order of the PDK's own subcircuit. The project places none of them. `iopad_inventory.md` §1b corrected.
- 13:18: eight xschemrc files start with a UTF-8 BOM (IOPad, OgueyAebischerBias ×2, inverter ×2, slot testbenches, top
  schematic and testbenches); xschem 3.4.4 rejects such an rc. Tests here used a copy of IOPad's rc without the three
  bytes; the files are unchanged.
- New in `macros/IOPad/schematic/xschem` (13:21): `DCNDiode`, `DCPDiode`, `Clamp_N_M1`, `Clamp_P_M1` (`.sym`, `.sch`),
  as listed in `iopad_inventory.md` §1c. Symbols: copies of the black boxes with the same pin positions,
  `type=subcircuit`; the clamps with a `gate` pin and no gate tie. Checked: netlists as subcircuits and from a test
  parent with a label on every pin, spice and LVS mode, device by device against the source: 0 mismatches; a planted
  fault (bulk on the gate net) was caught; rendered and looked at (diodes moved 100 units right after the first look).
  No file in the repository places them yet. No duplicate symbol names across `macros/*/{schematic,testbenches}/xschem`.
- ON (13:21): `d2s_mpdda_pd.sch` and `netlist/source/d2s_mpdda_pd.spice`: w = 290.4u → 299.2u, ng = 66 → 68. Netlisted
  before and after: only the `XON` line differs. Not changed: `netlist/source/d2s_mpdda.spice` (66; included by
  `tb_s2d_loopback.spice` of the S2D macro). Stale now: the CACE results and the macro README's numbers (ON = 66).
- Times in this log and in the inventory that had been written ahead of the clock (13:25, 13:27, 13:30, 12:55, 12:10,
  12:12) were corrected from the transcript's timestamps.

## 14:29–14:48: pad cell stripped to clamps and diodes; what the silicon contacts are for (Christoph: "Now, strip all
## the internals except the clamp and protection diode structures from underneath the metal lines needed for pad ring
## continuity. Also figure out what the contact structures to silicon are good for. Maybe there need to be guard
## structures at the edge of the pads.")

- Sources: IHP layout rules `ihp-sg13cmos5l/libs.doc/doc/SG13CMOS5L_os_layout_rules.pdf` §7.2 "Latch-up Guidelines"
  (pp. 54–55); `libs.tech/klayout/tech/drc/rule_decks/sg13cmos5l_maximal.drc` lines 133–137 and 2564–2597; the PDK's
  IO GDS (sha256 e6f0d64b…) and spice (1b07a9ee…). Cells extracted flat with KLayout (Activ split by pSD, Cont, M1,
  Via1 … TopMetal1, with the label layers).
- Every IHP IO cell, every filler and the corner carry the same silicon bands at the same heights, edge to edge, so
  abutting cells close them into rings around the die (like the metal rails):

  | y (µm) | silicon | net in the IHP pad cells | tied in the cell by |
  |---|---|---|---|
  | 6–61 (NWell 5.38–61.62) | n+ in NWell, frame around the n-channel clamp and DCNDiode | no supply in IOPadAnalog, In, Out, InOut, IOVss, Vss ("guard" of DCNDiode); netlist: DCNDiode guard = iovdd | only IOPadIOVdd (its pad is iovdd) |
  | 65–84.4 | p+ outer ring of the p-channel clamp | iovss | via the plate |
  | 84.5–140 | p+ plate, pSD, Substrate 40/0, `sub!` | iovss (ptap1 0.2148 Ω in the IOPadAnalog netlist) | M2 strap x 0.21–5.89, y 126–134, 192 Via1 + 192 Via2 to the iovss rail |
  | 148.35–148.65 (NWell 147.73–149.27) | n+ strip | iovdd | M2 x 79.18–79.79 from y 148.6 down to the iovdd rail at 118.7, 2 + 2 vias |
  | 156.85–157.15 | p+ strip | vss (ptap1 22.6 Ω) | 3 µm M2 stubs at both cell ends, 8 + 8 vias each |
  | 166.85–167.15 (NWell 166.23–167.77) | n+ strip | vdd | as above |

  The fillers and the corner have M1 and silicon on these bands, M1 labels (iovdd, iovss, vss), and no Via1, M2 or
  Via2: their bands get the potential only by abutment from the neighbouring pad cells.
- Rules behind it (§7.2.1): guard rings (VSS, VDD ties) around any NMOS and PMOS tied to a pad; double guard rings
  (N-Well isolator and P+ isolator) between n- and p-channel output buffers, and between output buffers and the internal
  circuit area. §7.2.2: LU.a / LU.b, at most 20 µm from any P+Activ in NWell to an nSD-NWell tie and from any N+Activ in
  PWell to a pSD-PWell tie; LU.c, c1, d, d1: tie Activ at most 6 µm beyond a Cont (hence the dense contacting). The
  document says latch-up rules are not checked by default; the maximal deck sets `$latchUpRules` true when it is not
  given, and implements LU.a, c, c1, d, d1 (no LU.b).
- The pad cell before the strip (sha256 0d371ec1…) had the same bands and ties: plate with Clamp_P_M1's outer ring →
  iovss via the left strap, n+ 148 → iovdd via the right strap, p+ 157 / n+ 167 → vss / vdd via the stubs. That plate
  tie was the only connection of any clamp or diode supply terminal to a rail.
- Stripped (14:44), from the top cell: plate and the three strips on Activ, NWell (strips), pSD, Substrate 40/0, M1;
  the `sub!` text on the plate; the six M2 straps and stubs; all 226 top-level Via1; 226 Via2 (the 858 on the pad bar
  stay); in `contacts` 32906 Cont (plate and strips), 2839 stay on the n+ frame. Kept: the five PCells, `pdrainwire`,
  `ndrainwire`, the 55 `via_stack$2`, `Metal3ViasUp`, `TopLayersTo4`, the pad bar (M2, pin, label, Via2), the n+ frame
  y 15.56–61 with NWell and M1 (the DCNDiode guard and the N-isolator band), the TEXT box (36.355,147.73;45.815,180.62),
  the boundary. Clamp_P_M1 has its own Activ, pSD, M1 and Substrate to x = 0 and 80, so the top-level columns along it
  were redundant.
- File: `layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds` now sha256 18149412…, 1259816 bytes. The version before:
  `layout/klayout/backups/sg13cmos5l_IOPadDiff2Single_before_strip_2026-10-27.klay.gds` (0d371ec1…).
- Checked: no shape added on any layer; removed areas only in y ≥ 84.26 (pSD from 84.44, Via2 from 118.76); every
  cell other than the top cell and `contacts` unchanged; instances unchanged; texts: only `sub!` removed; the 64 PCell
  context strings identical. Flat extraction after: pad = DCN cathode, DCP anode, clamp drains, pad bar up to
  TopMetal1; no clamp or diode supply terminal reaches a rail; the n+ frame is a net of its own (DCNDiode "guard").
- Two duplicate Cont at (1.645,33.6) and (2.005,33.6) in `contacts`, on the frame, were there before; left as they are.

## 14:53–14:55: guard-band table in the pad-cell-internals doc (Christoph: "Yes, add the guard-band table.")

- New section 3 "Guard bands: silicon that runs through every IO cell" and a Sources line in
  `sudelbuecher/description/sg13cmos5l_pad_cell_internals.md` (13dfca1c… → b39d6aae…, 24 lines added, none changed)
  and in the claude.ai Project doc `claude/sg13cmos5l_pad_cell_internals.md` (written from the same file; the Project
  copy read before matched the sudelbuecher copy in the corrected passages checked). Content: the band table of the
  14:29 entry with the netlist lines behind it, the fillers and corner without vias, §7.2.1 and §7.2.2 of the layout
  rules, what the maximal deck checks, and the consequence for our own pad cell, marked as reasoning. Stub via counts
  (8 + 8 per strip) and the plate gaps (y 89.56, 114.62) re-checked in `IOPadAnalog` before writing.

## 17:28–17:31: pad pitch in the Chipalooza frame; padrow; the TEXT box (Christoph: "Intended to put custom pads side
## by side with standard IHP IO pads. Ideas for a better place to put this are welcome. but something like this is
## obviously needed. So far, the clamp transistors still align, as does the nwell strap. Is a pad to pad distance of
## 80um correct, or should this be slightly different?")

- `sudelbuecher/design_considerations/pad_buffer_layout/klayout/padrow.klay.gds` (Christoph's, 17:23, no `.klay.klib`):
  top cell `PADROW`, `sg13cmos5l_IOPadTriOut16mA` at x = −80, `sg13cmos5l_IOPadDiff2Single` at 0, `IOPadAnalog` at
  80, abutted at the 80 µm cell boundary.
- Chipalooza frame (`sg13cmos5l_ocd_chipalooza/magic/sg13cmos5l_padframe.mag`, from `scripts/gen_padframe.tcl`): every
  pad is followed by `sg13cmos5l_Filler4000` (20 µm) + `sg13cmos5l_Filler2000` (10 µm), pitch 110 µm; at domain
  boundaries `sg13cmos5l_ocd_Split2000` takes the place of a Filler2000. Slot 7 on the right edge: Filler2000 at
  2250, `pad_s7_an_0` at 2260, Filler4000 / Filler2000 at 2340 / 2360, `pad_s7_an_1` at 2370, Filler4000 / Filler2000
  at 2450 / 2470, `pad_s8_an_0` at 2480 µm. Bond pads: separate 70 × 100 µm cells `bondpad_LX3CBX` outside the IO row,
  5.62 µm in from the cell origin in x. The script's comment "6um of spacers ... a Filler1000 and a Filler200" does
  not match its code (Filler4000 + Filler2000).
- The TEXT (63/0) box (36.355,147.73;45.815,180.62) in the pad cell is exactly the footprint of IHP's
  `sg13cmos5l_GateDecode` as placed in `IOPadTriOut4mA` / `16mA` / `30mA` (the `InOut*` cells place it at x = 16.355).

## 17:39–17:46: padrow moved into IOPad and bound; Miller capacitors in the gap? (Christoph: "ok move the gds where
## you think it fits, to the macros, and add a .klay.klib binding. Question about the custom diff2single pad: can the
## gap between the clamps be filled by the compensation capacitors? do they fit in there?")

- `padrow.klay.gds` is now `macros/IOPad/layout/klayout/padrow.klay.gds` (sha256 b5da8a98…, 7966728 bytes), with
  `padrow.klay.klib` (5162ff11…): `sg13cmos5l_io` → `$PDKPATH/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds`,
  `sg13cmos5l_IOPadDiff2Single` → `../../../sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds`.
  The old file in `design_considerations/pad_buffer_layout/klayout/` (3ffa05dd…, unchanged since 17:23) is deleted;
  deletion in the sudelbuecher folder was granted for this session.
- Before: the IHP pads in PADROW were already library cells of `sg13cmos5l_io`; the custom pad was a plain copy whose
  clamps and diodes had lost their PCell identity. Now that copy is replaced by a library reference to
  `sg13cmos5l_IOPadDiff2Single`, same placement (0,0); the PCells inside are PCell references again
  (`SG13_cm_clamps`, `SG13_dev`). Kept: every old context string, the `Hierarchical Layout` meta flag, the three
  placements, all 299 texts. The plugin's own map reader (`library_map_config.py`) resolves the map without issues
  in a mirror of the folders; with both libraries registered, no IHP or pad cell is defunct.
- Flattened XOR old → new: differences only in `Clamp_N_M1` (both instances), Cont / Metal1 / Metal1 pin at the gate
  heads, x 7.93–72.07. The copy had 3 contacts per gate head (the PCell code since the adaptive gate contacts of
  2026-10-15, l = 1 µm); the geometry stored in the pad cell file still has 1 (1525 vs 1661 Cont per instance).
  KLayout recomputes it when the pad cell is opened with `SG13_cm_clamps` loaded; tools that read the stored shapes
  (batch DRC / LVS) see the old one until the pad cell is saved once with the library loaded.
- Miller capacitors: `d2s_mpdda_pd` uses wc = lc = 16u, 256 µm² of gate per capacitor; the cells `d2s_cma` /
  `d2s_cmb` (pad_buffer_cells) are 17.92 × 19.0 µm with NWell. The gap y 42.56–51.42 leaves, for a capacitor NWell of
  another net, y 44.98–51.18 (NW.b1 1.80 to the n+ band's NWell at 43.18, NW.f 0.24 to the DCP guard ring) and
  x 2.57–77.43; p+ Activ inside (NW.c1 0.62): 4.96 × 73.6 µm = 365 µm². Both capacitors need 512 µm² plus
  overhead: they do not fit. One reshaped capacitor (W 4.96 µm, about 51.6 µm of gate, e.g. 8 fingers) fits with
  about 15 µm to spare.

## 17:54–17:57: Miller capacitors as polygons, CMB's distance to ON, where the class-AB replicas go (Christoph: "the
## geometry of the Miller capacitors can become adaptive polygons. also: would it be a problem if the distance from cmb
## to the corresponding nmos transistor becomes a bit long? where could the matching translinear mesh transistor
## stacks end up in the pad? their geometry is also not cast in stone as you cast in on silicon; the outline,
## especially the guard rings, may change."; 17:54: "conceivably, the miller capacitors could even be split in two as
## the pad geometry requires.")

- Sources: `layout_primitives.md` P7 (replicas inside the clamp frames) and P9 (MOS capacitors, CMA's pad-connected
  well); `netlist/source/d2s_mpdda_pd.spice`, `d2s_bias_lp.spice`, `d2s_bias_ref.spice`; `clamp_engine.py` (P frame:
  two device rows, one poly column per gate through both rows, gate contacts at both heads and in the middle).
- Finger counts: RP1 = w 13.32u, ng 2 (two 6.66/0.6 fingers) = one gate column of the P frame; RN1 = w 8.8u, ng 2
  (two 4.4/1 fingers) = an S-G-D-G-S pair in the N frame's single row. Drawn: 82 P fingers = OP 80 + RP1 2 (P7's
  proposal), 68 N fingers = ON 66 + RN1 2. With the replicas inside the frames the netlist's ON goes back to 66,
  against the 13:09 answer "Netlist follows layout" (68).
- P7's "S-G-D-G-S group cut out of a row" holds as written for N only. In P a gate column spans both rows, so RP1
  is one column; it has a drain of its own only at the end of an odd-ng array (the 0.74 µm end drain), or if two
  columns are split between the rows.

## 18:19–18:27: review of the d2s suites before freezing dimensions; replica agent started (Christoph: "so ...
## review the d2s_mpdda_pd.sch verification and characterization suites, suggest where the specifications should be
## tightened or even improved, to make sure that we can freeze device dimensions, as preparation for cramming in the
## layout primitives in the pad. spawn an agent to tentatively work the class AB replicas into the clamp structures.")

- Review written to `spec_review_before_freeze.md` (this folder, sha256 03f639c6…): seven decisions that move device
  sizes (mismatch offset, gain accuracy vs rhigh width, input common mode and supply range, maximum load / phase
  margin, PSRR, noise, THD), cheap specification gaps (no maximum short-circuit current; corners, temperatures,
  supplies and resistor corners missing in the load, loop, tran, noise and THD groups; Monte Carlo too short and
  tt only; unpowered pad not in CACE), netlist changes the layout forces (DN / DP → 63.78 µm sheets, ad / as / pd / ps
  of OP / ON, replica finger accounting, reshaped Miller capacitors, antenna diodes), and a freeze procedure.
  Nothing was simulated; numbers are the README's (2026-10-20, ON = 66).
- Replica prototype: a background agent works on copies in the cloud workspace only (no writes to this computer, no
  git): RN1 / RP1 inside `Clamp_N_M1` / `Clamp_P_M1` via a copy of `clamp_engine.py`, with regression XOR of the
  default cells, extraction, and DRC if KLayout 0.28.16 with the shim works. Staged for it: `scripts/pcells/*`, the
  four bias / driver netlists, `layout_primitives.md`, the IHP DRC deck.

## 18:56–18:58: replica prototype back (background agent, 18:23–18:56)

- Saved in `replica_prototype/` (this folder): the agent's `report.md` (its text unchanged, with a provenance
  comment on top), `clamp_engine.diff` and `clamp_base_code_UNTESTED.diff` (proposals against `scripts/pcells`, not
  applied), `replica_cells.gds`, `pad_mock.gds`, three renders, five logs. The scripts stay in the cloud workspace.
  The three PNGs arrived with an extra C2PA chunk (`caBX`) added in transfer: their checksums differ from the
  cloud copies, header and pixel data are identical.
- Agent's result: RN1 as an S-G-D-G-S pair at the centre of the upper N frame; RP1 as the centre gate column of the
  P frame (both rows, 2 fingers) with its drain partner as a dummy (gate on iovdd); no front-end layer changes, only
  Cont / Metal1; new M1 pin `rep`; carved at today's ng: OP 78, ON 66, I_Q ≈ 195 µA. Pad mock: P comb line
  x = 40.755 → n1, N comb line x = 40.000 cut between the frames (pad below, n2 above), four bridging via stacks onto
  DCN / DCP removed. Verified by the agent: default output element-for-element identical to the original engine
  (54 cells), 271 variant cells extracted and XOR-checked, pad mock extracted (OP 519.48 / 0.6, RP1 and dummy
  13.32 / 0.6, ON 149.6 + 140.8 / 1, RN1 8.8 / 1), its own M1 / M2 rule checks. Not run: the IHP DRC deck (KLayout
  0.28.16 lacks what the maximal deck needs; main deck includes were not staged), PDK LVS, the cni PyCell path,
  simulation of the new ratios.
- Checked here (18:57) on the current pad cell (sha256 18149412…): M2 spacing errors between N and P comb lines
  where they overlap (y ≈ 29–61), all on the pad net: x ≈ 32.0, 0.045 µm, and x ≈ 40.4, 0.135 µm (Mn.b 0.21);
  x ≈ 47.2, 0.225 µm (Mn.e 0.24: a line wider than 0.39 µm, parallel run > 1 µm).

## 19:08–19:20: Metal2 comb rewired; design note corrected; replica mock-up with grown frames (Christoph: "clean up
## the pad layout metal2 spacing errors. my hand wiring is bad and awkward. fix the design-note inconsistency. if the
## agent migrated reference transistors into the arrays, grow them accordingly. put the pad mockup somewhere it makes
## sense, is out of the way of the toplevel macro structure (for now) and where I have a chance to find it.")

- Pad cell (19:13): `layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds` 18149412… → bb99b7d7…; the version before is
  `backups/sg13cmos5l_IOPadDiff2Single_before_m2cleanup_2026-10-27.klay.gds`. New Metal2 scheme: the N comb
  (`ndrainwire`, 17 lines) runs from the pad bar up to y 50, the P comb (`pdrainwire`, 21 lines) from y 44 up to the
  P frame, and a junction bar (Metal2, x 9.13–71.265, y 44–50, in the bare gap between DCNDiode and DCPDiode) joins
  them. N and P lines no longer run side by side. The 55 hand-placed top-level `via_stack$2` (cross-feeds of the
  other comb onto the diodes, and bridges) are removed; DCN cathode is fed by the N comb's own via stacks, DCP anode by
  the P comb's. Checked: no Metal2 width / space / notch / Mn.e / area error (10 space errors before), Metal1
  unchanged, the 64 context strings identical; flat extraction: pad bar, all N and P drains, DCN cathode, DCP anode
  and the bar are one net, gates and rails distinct. `padrow.klay.gds` follows through its library binding.
- `design_considerations/pad_buffer_layout/layout_primitives.md` (895efdbc… → 01123fb7…), P7, the floorplan sketch and
  open item 5: ON = 68 (was 66; a dated correction line), RN1 as the centre S-G-D-G-S pair of the upper N frame, RP1
  as one P gate column with a dummy partner, frames grown by the replica fingers (Clamp_P ng 43 = OP 82 + RP1 2 +
  dummy 2, both Clamp_N ng 35 = ON 68 + RN1 2; the two N frames share the comb, so one ng), sketch "OP 82 f + RP1 2 f
  + dummy 2 f" and "ON 68 f + RN1 2 f".
- Mock-up (19:19) in `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/replica_mockup/`, next to `size_mockup/`
  (the precedent for mock-ups of this macro; the Makefile picks layouts by cell name in `layout/klayout/`, not in
  subfolders): `sg13cmos5l_IOPadDiff2Single_replica_mockup.gds` (f680fcbd…), `README.md`, `replica_mockup.png`.
  Built from the cleaned pad cell with the prototype engine: Clamp_P_M1 ng 43 (rep single, centre), 2 × Clamp_N_M1
  ng 35 (upper: rep pair, centre), DCNDiode l 67.6 µm and DCPDiode l 65.8 µm centred (the wider combs need longer
  stripes), the top-level n+ band clipped around the longer DCNDiode; Metal2 in the new scheme, n1 straight up from
  the RP1 drain, n2 from the RN1 drain with a jog to x 37.735 and through a gap in the junction bar, both to y 88.
  Checked: devices OP 546.12 / 0.6, RP1 and dummy 13.32 / 0.6, ON 154.0 + 145.2 / 1, RN1 8.8 / 1; nets pad / n1 / n2
  / gates / rails distinct; own Metal1 / Metal2, NWell, contact and via checks clean. Not run: IHP DRC deck, LVS.
