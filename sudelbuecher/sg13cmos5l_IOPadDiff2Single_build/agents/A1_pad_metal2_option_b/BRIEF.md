# Brief: Metal2 rework of the pad cell `sg13cmos5l_IOPadDiff2Single` (option B), 2026-10-28

Workspace (yours, nothing else): `/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/m2agent/`
(`inputs/` read-only, `work/` scripts and scratch, `out/` deliverables). Call it `$A` below.

## Hard rules

- Work only in the cloud workspace above. Do **not** use any `mcp__remote-devices__*` tool, do not write to the
  user's computer, do not run **any** git command (not even read-only), do not touch `inputs/`.
- Do not change the PCell code. Keep the PCell instances as they are (library `SG13_cm_clamps`, live PCells with
  context info). If a PCell change looks necessary, stop at that point and describe it in the report.
- New geometry goes into the top cell or into new static sub-cells with descriptive names (e.g. `m2_comb_n`,
  `m2_comb_p`, `cap_cma`, `cap_cmb`, `gate_feeds`), never into the PCell variants.
- Save GDS with `write_context_info = True` (see `inputs/switch.py`), top cell name unchanged.
- Report facts you measured; mark reasoning as reasoning. No invented rule numbers: take every rule value from
  `/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/` (the `.drc` files and
  `sg13cmos5l_tech_default.json`) and cite file + rule name.
- Times in the report: `TZ=Europe/Berlin date`.

## Inputs

| file | what |
|---|---|
| `inputs/pad_pcells_2026-10-28.klay.gds` (sha256 8520e315…) | the pad cell as of 00:45, the starting point (also on the user's computer) |
| `inputs/pad_pcells_2026-10-28.png` | render of it (device layers + Metal1, no Metal2 comb) |
| `inputs/switch.py`, `reopen.py`, `verify.py`, `render_pad.py` | how the cell was built, how to open it with the PCell library registered, a flat extraction + rule subset, a renderer. Reuse them. |
| `inputs/build_log.md` | running log; read the entries from "## 22:01–22:26" onward (IHP's Metal2 scheme measured on `IOPadAnalog`, the band above DCNDiode, capacitor fits, the decisions) |
| `inputs/layout_primitives.md` | the design note (P7 replicas, P9 MOS capacitors, floorplan) |
| `inputs/replica_report.md`, `inputs/answers_report_section8.txt` | the replica prototype report and the user's decisions on its section 8 |
| `inputs/pad_buffer_cells.gds` | library with `d2s_cma` / `d2s_cmb` (16 × 16 µm accumulation-mode hv PMOS capacitors) as construction templates |
| `inputs/d2s_mpdda_pd.spice` | the circuit: `XOP vout a vddo vddo` (546.12/0.6, 82 f), `XON vout b vsso vsso` (299.2/1, 68 f), `XCMA vout a vout vout sg13_hv_pmos w={wc} l={lc}` (gate a; S, D, well on the pad), `XCMB b vout b b` (gate on the pad; S, D, well on b), `XRP1 dabp dabp vddo vddo`, `XRPD dabp vddo vddo vddo`, `XRN1 dabn dabn vsso vsso`; in the pad vout = pad, vddo = iovdd, vsso = iovss |
| `inputs/project_CLAUDE.md` | the user's project rules (for context; the hard rules above win) |
| IHP IO library | `/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds` (`sg13cmos5l_IOPadAnalog`, `IOPadInOut30mA`, `IOPadOut4mA`: the reference for the scheme) |
| PCell code / PDK | `…/scratchpad/pcw/new/pcells` (engine `clamp_engine.py`: `columns()`, `FAMILY`, `generate_m1_wiring()`), PDK cni at `…/scratchpad/pcw/pdk/ihp-sg13cmos5l` (set `PDKPATH`, then `runpy.run_path(load_clamp_pcells.py)`) |
| Tools | `klayout.db` 0.30.12 (Python), xschem, matplotlib, Playwright/Chromium. The IHP DRC deck cannot run here (needs the KLayout application ≥ 0.29.11; only 0.28.16 is installable) → implement the relevant rules in Python. |

## The cell today (absolute µm, origin lower left, cell 80 × 180)

- Pad bar Metal2 x 5–75, y 0–3, Via2 to the pad rail. Rails in Metal3 / Metal4 / TopMetal1 (cells `Metal3ViasUp`,
  `TopLayersTo4`): pad y 0–3, **iovss y 7–32.5 and 34.5–60**, **iovdd y 66–91.5**. Do not change the rails.
- Lower N frame `Clamp_N_M1` ng 35, l 1u, 80u, origin (0, 6); upper N frame same, origin (0, 15.56); each with a
  wiring cell (`Clamp_N_M1_wiring`): upper roles `16:rep 17:rep` (RN1, net `dabn`), lower no roles; gate net `b`.
  N drains (18 columns) x = 8.485 + k·3.82, sources x = 6.575 + k·3.82 (check with `E.columns(35, 1000, x0)`).
  The RN1 drain is the upper frame's column at **x 39.045**; the lower frame's column at the same x is an ON drain (pad).
  Gate bus rows: `FAMILY['N']['bus']` = 7370–7530 nm above the frame origin; the upper frame's bus is split in two
  segments by RN1, the lower one is whole.
- `DCNDiode` l 67.6u at (3.56, 27.12): stripes (cathode = pad) y 29.37–30.63 and 33.87–35.13, bars (anode = iovss)
  y 27.12–28.38, 31.62–32.88, 36.12–37.38, own n+ guard ring (`guard`, iovdd) to y 39.66 (NWell).
- The top-level n+ band ("U frame", Activ / Metal1 / NWell polygons and cell `contacts`): the N-well isolator around
  the n-channel side (IHP's 6–61 band): the top-level polygons span y 15.56–61 (NWell 14.94–61.62) and continue the
  N frames' outer rings below; crossbar at y 38.7–42.56 (NWell 38.08–43.18) above DCNDiode, cell edge to cell edge.
  Verify these numbers yourself before relying on them.
- `DCPDiode` l 65.8u at (4.46, 53.08): guard ring (p+, iovss) from y 51.24, stripes (anode = pad) y 55.33–56.59 and
  59.83–61.09, bars (cathode = iovdd) y 53.08–54.34, 57.58–58.84, 62.08–63.34.
- P frame `Clamp_P_M1` ng 43, l 0.6u, 80u, origin (0, 65), wiring roles `20:dummy 21:rep`, gate net `a`, replica net
  `dabp`. P drains (22) x = 9.045 + k·3.02, sources x = 7.535 + k·3.02. RP1 drain (= dummy drain) at **x 39.245**.
  Bus row `FAMILY['P']['bus']` = 16730–16890 nm above the origin, split in two by RP1 / dummy.
- Metal2 today: only the pad bar. The drains are unconnected (57 separate `pad` nets in `verify.py`).
- Devices today (`verify.py`): ON 299.2 / 1 (G b), RN1 8.8 / 1 (G = D = dabn), OP 546.12 / 0.6 (G a), RP1 13.32 / 0.6
  (G = D = dabp), dummy 13.32 / 0.6 (G iovdd, D dabp). Known: `guard,iovss` is one net (DCPDiode guard ring merged
  with the P clamp's outer ring) — intended.

## What to build (decided by the user)

1. **Option B Metal2 comb, IHP's scheme at two pitches.** Read the 22:01 log entry first. Per region:
   - N side (pad bar → N frames → DCNDiode): pad lines 0.61 µm on the N drain columns, Via1 on the N drains and on the
     DCNDiode cathode stripes; 0.2 µm iovss straps on the N source columns with Via1 on the N sources and DCNDiode
     anode bars, **Via2 into the iovss rail** (y 7–32.5 / 34.5–60).
   - P side (DCPDiode → P frame): pad lines on the P drain columns, Via1 on the DCPDiode anode stripes and P drains;
     iovdd straps on the P source columns with Via1 on the DCPDiode cathode bars and P sources, **Via2 into the iovdd
     rail** (y 66–91.5).
   - **Pad junction in Metal2** in the gap between DCNDiode and DCPDiode joining the two combs (they have different
     pitches). iovss crosses it in the **iovss rail (Metal3 34.5–60), which must not be cut**: Via2 from the N-side
     straps below the junction and from short Metal2 stubs on the **DCPDiode guard ring** (p+, iovss) above it, as
     IHP ties its vss / vdd strips.
   - **Wide Metal2 over the diode side bars** where the comb does not reach (IHP rule measured in the log: Metal2 of
     the diode's supply net over the uncovered bars, Via1 on every bar of that net, merged with the straps): iovss over
     DCNDiode's side bars, iovdd over DCPDiode's side bars, both sides.
   - The column x 39.045 above the lower N frame is not pad (see dabn); give the lower frame's ON drain there its pad
     connection from the bar.
2. **Replica nets.** `dabp` from the RP1 drain (x 39.245) straight up out of the P frame; `dabn` from the RN1 drain
   (x 39.045, upper N frame) to the top as well. Both end at Metal2 pins + labels just above the P frame (y ≈ 85–88),
   where RP2 / RN2 will sit ("keep RP2, RN2 close to the output/clamp structures"). dabn must pass DCNDiode, the gap,
   DCPDiode and the P frame without touching pad lines or straps: find a track (e.g. the frame ends x < 7 or x > 73,
   or a strap position you give up, with the strap's job covered otherwise) and justify it. Metal3 is the rails: not
   available for routing.
3. **Gate buses `a` and `b`.** Each bus half is fed from its own end of the frame (a Metal2 hop across the middle
   would cross the replica line), at x < 9 or x > 71 where no comb lines run; join the halves outside the comb and bring
   `a` and `b` to Metal2 pins + labels at the top (y ≈ 85–88) next to dabp / dabn. The two N frames' `b` buses must be
   joined too.
4. **Band above DCNDiode narrowed** to DCNDiode's own guard ring (NWell top 39.66): remove the crossbar's extra width,
   keep the 6–61 ring continuous from cell edge to cell edge in Activ + Metal1 (side bars ↔ DCN guard ring), keep the
   contacts consistent (`contacts` cell), check NW / Activ / Cont rules.
5. **Both Miller capacitors CMA and CMB in the gap** between the narrowed band and the DCPDiode guard ring (log: well
   ≈ 9.72 µm high, ≈ 8.48 µm gate width, ≈ 30 µm long each, two separate wells, ≈ 70 of 74.9 µm with ntap and gate
   contact at the ends). Construction as `d2s_cma` / `d2s_cmb` (hv PMOS in accumulation: gate over n-well, S/D and
   ntap on the well net). CMA: gate `a`, well / S / D = pad. CMB: gate = pad, well / S / D = `b`. Match the schematic
   area 16 × 16 µm (256 µm²) as closely as the room allows and **report the drawn W / L** (the schematic will follow
   the layout). NWell spacing to other-net wells (NW.b1) and to p+ (NW.f), well enclosures: cite and check. Route `a`
   to CMA's gate and `b` to CMB's well from the bus feeds; the pad side from the junction.
6. **Review the entire hand wiring** of the top cell (everything that is not a PCell): near-misses (spacings within
   10 % of the rule), stray shapes, labels on the right nets, Via2 / Via3 / TopVia fields against the rails. Fix what
   is clearly wrong; list the rest.
7. **Design-note consistency**: list every statement in `inputs/layout_primitives.md` (and the replica report) that
   disagrees with the layout you deliver, with the corrected wording, in favour of the actual layout. Do not edit
   the notes themselves; put the list in the report.

## Checks you must run and report (numbers, not adjectives)

- Flat extraction (FEOL … Metal3, Via1, Via2, labels): expected devices exactly as today plus CMA / CMB as MOS
  (gate area); one net each: `pad` (pad bar, all ON / OP drains, DCN cathode stripes, DCP anode stripes, CMA S/D/well,
  CMB gate), `iovss` (N sources and rings, DCN anode bars, DCP guard ring, P outer ring, iovss rail), `iovdd` (P
  sources, DCP cathode bars, iovdd rail; the band / `guard` net may stay separate as today — say so), `a`, `b`
  (all bus segments of both N frames + CMB), `dabp`, `dabn`. No net carrying two different labels except the known
  `guard,iovss`. Probe points for each.
- Rules in Python from the deck: Metal1, Metal2, Metal3 width / space / notch / area / Mn.e (wide-metal spacing),
  Via1 / Via2 size, space, enclosure by the metals below and above, Cont rules where you add or remove contacts,
  NWell width / space (NW.b1 for different nets) / NW.f, Activ, GatPoly over Activ for the capacitors, pSD / nSD
  where you draw implants. Zero violations, or each one listed with a reason.
- The Metal3 rails are byte-for-byte unchanged (compare the `Metal3ViasUp` / `TopLayersTo4` cells and Metal3 / Via3
  shapes before and after).
- Re-open the output with the library registered (`reopen.py`): all PCell instances still live with the same
  parameters.
- Render PNGs (Metal2 by net over the device layers) of the whole y 0–92 µm area and of the gap.

## Deliverables in `$A/out/`

- `sg13cmos5l_IOPadDiff2Single.klay.gds` (the candidate), its sha256.
- `build_m2.py` (your builder, start → candidate, rerunnable), `check_m2.py` (all checks above).
- `report.md`: what you built with coordinates, the dabn / a / b routing and why, capacitor geometry with drawn
  W / L, every check with its numbers and rule source, open points, the design-note list (item 7), and what you could
  not verify. Keep it compact; tables where they help.
- `m2_full.png`, `m2_gap.png`.

When done, reply with: the sha256, the check summary (counts), the drawn CMA / CMB W / L, the dabn track, open points.
