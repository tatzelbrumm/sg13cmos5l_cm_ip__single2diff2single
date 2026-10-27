<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
<!-- Written 2026-10-27 18:23–18:56 by a background agent (Claude) on copies in the cloud workspace, for Christoph's request of 18:19 ("spawn an agent to tentatively work the class AB replicas into the clamp structures"); saved here unchanged by the main session. Files next to it: clamp_engine.diff, clamp_base_code_UNTESTED.diff (proposals against scripts/pcells, not applied), replica_cells.gds, pad_mock.gds, render_*.png, *.log. The scripts that produced the logs stay in the cloud workspace. -->

# Class-AB replicas RP1 / RN1 inside the M1-only clamp frames: prototype

## 1. Result in brief
- **N side (RN1):** an S-G-D-G-S pair at the centre of the **upper** N frame (y = 15.56). It is gates 16 and 17 around drain column 8, at x = 40.000 µm. No dummy is needed.
- **P side (RP1):** one interior gate column at the array centre, column 20 at x = 39.865 µm. It spans both rows, so it is 2 fingers.
  - Its drain partner, column 21, becomes a **dummy** with gate on iovdd and drain on the replica drain.
  - RP1's offset from OP's centroid is 0.09 µm in x and 0 in y.
- **No front-end layer changes.** Activ, GatPoly, pSD, NWell, ThickGateOx and Substrate are XOR-identical to the default cell. Only Cont (top-head contacts removed) and Metal1 change, so the replicas are physically OP / ON fingers.
- **New M1 pin `rep`** (replica gate = drain). The `gate` bus stays one piece: it crosses the replica's poly heads without contacting them. The replica gate joins its drain through an M1 link at the bottom.
- **Pad level:**
  - the P comb line at x = 40.755 becomes n1;
  - the N comb line at x = 40.000 is cut between the two N frames: pad below, n2 above;
  - 4 via stacks that bridged these lines onto DCN / DCP are removed.
- **Finger accounting as prototyped (carved at today's ng):** OP 78, ON 66. That gives I_Q ≈ 39 × 5 µA ≈ 195 µA, against 205 µA today.

## 2. Options compared

### N side: middle vs. end of a frame

| | middle (chosen) | end |
|---|---|---|
| x offset to ON's centroid | 0.000 µm (drain 8 is the exact centre of ng = 34) | 32.5 µm |
| surroundings | interior, 0.64 µm sources on both sides | outer finger next to the 0.47 µm end source and STI edge (LOD) |

**Upper frame, not lower:**
- n2 only has to go up, and the lower frame's column 8 keeps a short pad stub to the bar.
- With RN1 in the lower frame, n2 would collide with the upper frame's column 8, which is pad, on the same x.
- The cost is a 4.9 µm y offset from ON's centroid. That is irrelevant next to random mismatch (about 5 µV at 1 mV/mm).
- Alternative: one finger plus a dummy in each frame, cross-coupled. It is centred in y as well, but the N ratio drops to 64/2 = 32.

### P side: one gate column = 2 fingers

| | (a) end column of odd ng | (b) poly split between rows | **(c) interior column + dummy partner** | (d) S-G-D-G-S, 2 columns |
|---|---|---|---|---|
| x / y offset to OP centroid | **30.8 µm** / 0 | ≈ 0.8 / 3.5 µm | **0.09 / 0** | ≈ 0.8 / 0 |
| edge effects | drain ends at STI after 0.74 µm (LOD); x-side NWell edge 1.36 µm from the gate (WPE); cool end of the array | new poly end cap in the row gap | none | none |
| DRC | trivial | **not feasible**: row gap 0.44 µm < 2 × 0.18 end cap + 0.18 space = 0.54 µm | M1/Cont only, checked | M1/Cont only, checked |
| how n1 leaves | line at 70.955, which today overlaps N line 70.56; must start above y 61.3 | neat: same x, pad below and n1 above | line at 40.755, starting on the P drain | as (c) |
| OP at ng = 41 / ratio | 80 / 40 | 78 or 80 | 78 / 39 | 78 / 19.5 (I_Q halves) |

- **Why (c):** it is the only option that keeps RP1 an identical interior finger in both rows, at OP's centroid, without changing RP1's size or any front-end layer.
- **(a) as fallback:** it costs nothing, but its LOD, WPE and thermal effects are systematic. I have no model data here to size them.
- **(b) is out:** it can't be drawn without widening the row gap in every cell or notching the Activ (W error). The two leftover-row fingers also can't reach `gate` in M1, because the source columns block them.
- **(d) is out:** it contradicts the netlist (RP1 = 2 fingers) and would need iab doubled.

### `gate` bus: continuous (implemented) vs. split
- **What is implemented:** the replica and dummy columns lose their top-head contact, and their M1 strip stops 0.22 µm below the bus (M1.e). The bus crosses over them.
- **Why not a literal split:** the two `gate` pieces could only be joined in M2 by crossing the n1/n2 line, and M3 is the IO ring. So `a`/`b` would need two separate drops from the front end.

## 3. Prototype: `generate_m1(family, ng, l, width=None, rep=None, rep_at='centre', rep_side=None)`

**Parameters:**
- `rep`:
  - `None` = unchanged cell;
  - `'pair'` = both gates of one drain;
  - `'single'` = one gate, with the drain's other gate (if any) as a dummy tied to the inner ring.
- `rep_at`: `'centre'`, `'end'`, or a drain index.
- `rep_side`: `'L'` or `'R'`.

There is also a new helper `replica_plan()`, plus `REP_PIN = 'rep'` and `M1_E = 220`.

**Geometry:**
- **Replica drain column:** M1 pin `rep` instead of `pad`, extended down to y = 2.37 µm.
- **Bottom link:** M1 at y 2.37–2.69 µm (below the Activ, 0.23 µm above the inner ring) to the replica gate strip(s).
- **Replica and dummy gates:** no top-head contact. Their strip runs up to the bus minus 0.22 µm. The dummy's strip starts in the inner ring.
- **Bus:** spans the outermost output gates, so it only shortens when the replica sits at an array end.

**Rejected parameter sets:** ng = 2 (no output finger left), `'pair'` at the one-gate end drain of an odd ng, and an out-of-range drain index.

**PyCell wrapper (`clamp_base_code_UNTESTED.diff`):** a proposal only, never run, because `cni` isn't available here.
- It adds `rep` (none / pair / single), `rep_at` and `rep_side`, and `pin#` goes up by one when `rep` is set.
- Existing instances default to `rep = none`, so their geometry doesn't change.

## 4. Finger accounting and I_Q
I_Q uses your (OP / RP1) × 5 µA rule. Re-simulate any choice; today's simulation gives 212 µA.

| choice | P ng | OP / RP1 / dummy | I_Q | N ng (both frames) | ON / RN1 (N ratio) | comb impact |
|---|---|---|---|---|---|---|
| today | 41 | 82 / 2 / – | 205 µA | 34 | 68 / 2 (34) | – |
| **(c) carve, prototyped** | 41 | 78 / 2 / 2 | **195 µA** | 34 | 66 / 2 (33) | two lines retargeted |
| (a) carve | 41 | 80 / 2 / – | 200 µA | 34 | 66 / 2 | n1 at 70.955 |
| (c), ng = 42 | 42 | 80 / 2 / 2 | 200 µA | 34 | 66 / 2 | all P lines shift −0.755 µm |
| (c), add fingers | 43 | 82 / 2 / 2 | 205 µA | 35 | 68 / 2 (34) | all lines move, one extra N line |

**Netlist values that would follow (I changed no netlist):**
- **(c) at 41 / 34:**
  - `XOP … w=519.48u ng=78`
  - `XON … w=290.4u ng=66`
  - new `XDUM n1 vddo vddo vddo sg13_hv_pmos w=13.32u l=0.6u ng=2`
- **P ng = 42 (or option a):** OP `w=532.8u ng=80`.
- **43 / 35:** OP and ON lines unchanged; only the dummy line is added.

**Comb beat:** every P/N `ng` combination leaves 2–3 comb pairs closer than 0.24 µm, because the P pitch is 3.02 µm and the N pitch 3.82 µm (`report_numbers.log`). Picking an `ng` doesn't remove the problem.

## 5. Pin name and hierarchy
- **Pin name:** `rep` is generic at cell level. At pad level the nets are **n1 / n2**, and the mock labels them so in M2.
- **LVS:** n1 / n2 are today internal nodes of `d2s_bias_lp` / `d2s_bias_diodes`.
  - RP1, RN1 and the dummy need to move next to OP/ON in `d2s_mpdda_pd` (or into a clamp-plus-replica subckt), with n1/n2 as ports.
  - The alternative is to flatten for LVS.
  - This is the same situation as decision 4 in `layout_primitives.md` (BP/BN/BPC/BNC).

## 6. Pad-level wiring (mock)

**Clamps, now static engine cells:**
- P at (0, 65): rep = single.
- N at (0, 15.56): rep = pair.
- N at (0, 6): default, regenerated, because the stored copy predates the adaptive gate contacts (1525 vs. 1661 contacts; the stored P copy is identical).

**P line 10 (x = 40.755) → n1:**
- Its M2 now starts at y = 67.865 on the P drain, with the same two via_stack$4.
- It runs up through the frame rings to y = 88, a placeholder for RP2.
- There is no M2 below the frame, so no vias onto DCP or DCN.

**N line 8 (x = 40.000):**
- The pad stub keeps y 0–13.145, with its vias on the bar and the lower frame's drain.
- n2 starts on the upper frame's drain (via at y = 20.505). It jogs 0.755 µm left at y 26.0–26.62 to x = 39.245, then runs up to y = 88.
- After the jog it keeps 0.89 µm to P line 9 and to n1. At x = 40.000 it would sit only 0.135 µm from n1.
- It has no vias onto DCN or DCP.

**Removed:** the top-level via_stack$2 at (40.41, 30 / 34.5) and (40.345, 55.96 / 60.46). They bridged N8 and P10 to each other and to the diode stripes, and would now short n1/n2 to pad.

**Effect on the diodes:**
- DCN and DCP each lose 4 feeds around x ≈ 40.
- The nearest remaining feeds are at 37.7–38.0 and 43.8 µm, so about 6 µm of stripe is fed from its neighbours.
- I expect the extra ESD path resistance to be negligible, but I didn't calculate it.

**Coupling and routing:**
- n2 now crosses the pad stripes and runs about 40 µm beside pad lines. My rough estimate is ~1 fF against ~20 fF on n2; not extracted.
- If RN2 sits in the NMOS zone (119–140 µm), n2 runs about 100 µm up the cell.

## 7. Verification (what actually ran, klayout.db 0.30.12 in the container)

1. **Default unchanged (`regress_default.log`):**
   - 54 cells: the README test set plus the pad's N 34 / 1 µm / 80u and P 41 / 0.6 µm / 80u.
   - With `rep=None`, the patched engine's shape and text lists are **element-for-element identical** to the original's. Per-layer XOR is empty and the labels are identical.
   - The 80u limits check out: P ≤ 49 at 0.6 µm and N ≤ 38 at 1.0 µm.
2. **Variants (`verify_variants.log`, `replica_cells.gds`): 271 cells, 0 failing.**
   - **Cells:** 11 named 80u cases plus 260 swept ones (N/P × ng 2, 3, 4, 8, 9 × five l values × seven replica settings, fit frame). 90 parameter sets were rejected by design (see section 3).
   - **Extraction, as in `lvs_clamp.py` / `test_m1.py`:**
     - exactly one output MOS with W = w_f × rows × n_out, L = l, S/D = rail/pad, G = gate;
     - one replica with G = rep and S/D = rail/rep;
     - for single mode, one dummy with G = rail and S/D = rail/rep;
     - no other devices;
     - named nets exactly pad / gate / rep / iovss (/ iovdd), each one net, so no shorts or opens;
     - unnamed-net count equal to the default's.
   - **XOR against the default:**
     - front-end layers identical over the whole cell;
     - every layer identical outside the window between the neighbouring output gates' strips;
     - inside that window, only Cont, Metal1 and Metal1 pin differ;
     - labels identical except pad → rep, and one `gate` label on the bus pin;
     - the variant's contacts are a subset of the default's, with the expected number removed.
3. **Pad mock (`pad_mock.log`):** flat extraction up to M2, with 23 probe points.

   | device | W / L (µm) | terminals |
   |---|---|---|
   | OP | 519.48 / 0.6 | |
   | RP1 | 13.32 / 0.6 | G = D = n1 |
   | dummy | 13.32 / 0.6 | G = S = iovdd, D = n1 |
   | ON lower | 149.6 / 1.0 | |
   | ON upper | 140.8 / 1.0 | |
   | RN1 | 8.8 / 1.0 | G = D = n2 |

   - The pad net is intact: bar, all output drains, the lower frame's column 8, and the DCN/DCP stripes.
   - n1 and n2 contain only the replica's drain, its gate strip and the wire top.
   - Pad, n1, n2, the three gate buses and the rails are distinct.
4. **My own Python rule checks (not the IHP deck):**
   - **Cells:** M1.a, M1.b, M1.e (approximate), M1.d, Cnt.h, and M1.c/c1 per contact. **0 violations** on every variant and on the default baselines.
   - **Mock, M2:**
     - The near-misses at x ≈ 40.4 disappear, because those lines are now n1/n2.
     - The rest **already exist in strip_1435**: N 32.36 vs. P 31.695 has a 0.045 µm gap, and N 47.64 vs. P 46.795 is 0.225 µm, below the 0.24 µm Mn.e limit.
5. **IHP DRC deck: not run.**
   - The copy lacks the main deck's `%include` files (layers_def.drc, several feol/beol decks) and both JSON rule files.
   - The self-contained `sg13cmos5l_maximal.drc` aborts on apt KLayout 0.28.16 with `uninitialized constant RBA::EdgePairToEdgeOperator`, which needs ≥ 0.29. I stopped there.
   - Why this is probably low risk: front-end layers are identical and contacts are only removed, so only M1-dependent rules can change, and those were checked in item 4.
6. **Not verified:**
   - PDK LVS;
   - the PyCell / `cni` path for the new parameters;
   - antenna;
   - I_Q simulation with the new ratios;
   - the size of the LOD/WPE effects;
   - ESD and latch-up with the replicas in the frames;
   - parasitic coupling onto n1/n2;
   - the full IHP DRC.

**Housekeeping:**
- Loading the original modules with importlib made Python write `__pycache__/` (two .pyc files) into `/mnt/user-data/uploads/…/scripts/pcells/`.
- I deleted it, so the directory contents are back to the original, but the directory's mtime changed. Later runs set `sys.dont_write_bytecode`.
- I also installed the `klayout` 0.28.16 apt package in the container for the DRC attempt.

## 8. Decisions for you
1. **P replica:** (c) interior column + dummy (recommended, prototyped), or (a) end column (OP 80, no dummy, but edge effects).
2. **Finger accounting:**
   - 41 / 34: 195 µA, smallest pad change, prototyped;
   - P ng = 42: 200 µA, all P comb lines move;
   - 43 / 35: netlist OP/ON unchanged at 205 µA, all combs move, one extra N line.
3. **Pin name:** `rep`, or something else such as `diode`.
4. **Dummy gate:** tied to the iovdd ring inside the cell (as built), or its own pin so it could be strapped to n1 to make RP1 4 fingers.
5. **N layout:** RN1 pair in the upper frame (as built), or cross-coupled single fingers in both frames (ratio 32, centred in y).
6. **Schematic hierarchy for LVS:** move RP1/RN1/dummy out of `d2s_bias_*`, or flatten.
7. **Where RP2/RN2 sit:** this sets how far n1/n2 run.
8. **Pre-existing M2 near-misses** in strip_1435 at x ≈ 32.0 and 47.2 need fixing either way.
9. **Design note inconsistency:** `layout_primitives.md` P7 says "ON = 66 + RN1 = 2", and the floorplan sketch says "ON 64 f + RN1 2 f", while the netlist has ON ng = 68. This report assumes 68 drawn and 66 + 2 after carving.
