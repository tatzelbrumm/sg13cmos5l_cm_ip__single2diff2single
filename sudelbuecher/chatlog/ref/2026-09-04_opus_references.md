# References — 2026-09-04 (Opus session: CACE templates + OgueyAebischerBias sizing)

Sources for
[`../2026-09-04_opus_cace_templates_and_oab_sizing.md`](../2026-09-04_opus_cace_templates_and_oab_sizing.md).

Rule, per [`README.md`](README.md): **index, do not copy.**

**No external document was fetched in this session.** No web search, no page
fetch, no download. Everything below is either a file already in one of the
connected working folders, or a piece of standing device-physics knowledge
used from memory and flagged as such. That matters for reading the transcript:
where the assistant quoted a device constant it was an estimate, and it said
so — the only numbers that came from measurement are the ones in the CACE run
logs listed below.

---

## 1. Primary literature (cited, not opened)

- H. J. Oguey and D. Aebischer, "CMOS current reference without resistance,"
  *IEEE Journal of Solid-State Circuits*, vol. 32, no. 7, pp. 1132–1135,
  July 1997. DOI `10.1109/4.597305`.
  The topology the macro implements. Cited in the header text of every
  `reference_tb_*.sch` template. **Not consulted this session** — the circuit
  was read off the netlist, not off the paper.

## 2. In-repo, design worktree (`sg13cmos5l_cm_ip__single2diff2single`)

Read this session:

- `CLAUDE.md` — project context, invariants, the "traps that have already cost
  hours" list.
- `HANDOVER.md` — the seed context written by the preceding Sonnet session.
- `macros/OgueyAebischerBias/verification/cace/netlist/schematic/reference.spice`
  — the flattened netlist. **This is the authority** for the circuit as drawn
  in `pix/2026-09-04_opus_oab_trouble_spots.png`; the figure is a hand
  transcription of it.
- `macros/OgueyAebischerBias/verification/cace/reference.yaml` — the CACE deck.
- `macros/OgueyAebischerBias/schematic/xschem/OgueyAebischerBias.sch` — read for
  device symbol/parameter syntax and the ammeter instances.
- `macros/OgueyAebischerBias/verification/cace/templates/reference_tb_dc.sch`,
  `reference_tb_tran.sch` — the two pre-existing templates, used as the format
  precedent for the four new ones.
- `macros/inverter/verification/cace/inverter.yaml`,
  `templates/inverter_tb_ac.sch`, `templates/xschemrc` — the older CACE format
  precedent (`collate: iterations`, post-processing script, histogram plots).
- `macros/inverter/Makefile` — the `sim-cace` target, i.e. how CACE is meant to
  be driven and which artifacts get copied out of `_runs/`.

## 3. Measurement records (the numbers everything rests on)

All from the `cace` branch of the design worktree:

- `sudelbuecher/logs/cace-oguey.out` — full six-parameter CACE run,
  `RUN_2026-09-04_08-27-47`, including the summary table. Committed in
  `6885be7`. **The single most useful file in the session**; every measured
  figure quoted in the transcript comes from here or from the CSV below.
- `macros/OgueyAebischerBias/verification/cace/_runs/RUN_2026-09-04_08-27-47/summary.md`
  — the same table, standalone. Untracked (in `_runs/`).
- `.../_runs/RUN_2026-09-04_05-03-39/parameters/dc_params/simulation_summary.csv`
  — the 45-row corner sweep. Source of the 47 nA figure and of the line
  sensitivity, which the CACE summary table cannot show because it formats
  amps to three decimals and prints `0.000 A`.

Numbers extracted and used in the analysis:

| quantity | value | where from |
|---|---|---|
| `Ibias` at tt/27 °C/3.3 V | 46.65 nA | dc CSV, run_22 |
| line sensitivity | 43.18 → 50.89 nA over 3.0→3.6 V = 27.5 %/V | dc CSV, run_21/23 |
| `vbr` line rejection | 0.995 → 1.032 V = 61.7 mV/V ⇒ −24.19 dB | dc CSV |
| `PSRR_vbr` @ 1 kHz | 24.348 dB | `cace-oguey.out` |
| `Leg_matching` typ | +5.568 % | `cace-oguey.out` |
| `Leg_matching` min/max | −17.305 % / +39.645 % | `cace-oguey.out` |
| `Ibias_accuracy` min/max | −76.324 % / +148.048 % | `cace-oguey.out` |
| `Iq_enabled` / `Iq_disabled` | 338 nA / 66 pA | `cace-oguey.out` |
| `t_startup` | 242 ns (argued in-session to be a measurement artifact) | `cace-oguey.out` |
| `Ibias_noise` @ 1 Hz | 0.521 nA/√Hz | `cace-oguey.out` |

Derived in-session from the above, not measured directly:

- PMOS output conductance `(1/I)·dI/dVsd = 2.70 %/V`, `V_A ≈ 37 V`, from
  `Leg_matching` typ over the 2.06 V drain-voltage difference between M12 and
  M13.
- `A_VT ≈ 5–7 mV·µm`, from `σ(Leg_matching) ≈ 12 %` and an assumed
  `gm/I_D = 15–20 S/A`. **The gm/I_D assumption is unverified** — extracting it
  is the outstanding characterization task.
- Loop amplification `≈ 10×` (PSRR) and `≈ 4×` (mismatch), as the ratio of
  output sensitivity to per-device sensitivity.

## 4. Precedent repos (named, not opened this session)

Both are indexed in [`2026-09-04_references.md`](2026-09-04_references.md)
from the preceding session; nothing new was read from either.

- `~/EDA/TinyTapeout/designs/tt10-analog-tatzelreference` — the sky130 original
  the macro was ported from, hence the un-re-derived device sizes.
- `~/EDA/chipalooza2024/sky130_cm_ip__biasgen` — origin of the inherited spec
  targets in `reference.yaml`. Three of them were argued in-session to be
  meaningless for this circuit: `Ibias_val` min 200 nA (actual 47 nA),
  `Iq_enabled` typ 10 µA (actual 338 nA), `t_startup` typ 20 µs (actual 242 ns).

## 5. Tooling

- `analog-schematic` skill, from the `anthropic-skills` plugin installed in
  this Cowork session. Cached read-only under the session's skills directory;
  provenance beyond "shipped with the session's skill set" is unknown to the
  assistant, which said so when asked. Files used: `SKILL.md`,
  `scripts/sch_netlist.py`, `tests/golden.py`, `references/conventions.md`.
  Netlist-first: components and nets are declared, a DRC gates the render on
  floating pins and untied bulks, and the SVG is derived from the netlist.
  **The DRC proves well-formedness, not fidelity** — it cannot check the
  drawing against `reference.spice`.
- `cairosvg`, installed into the sandbox with
  `pip install cairosvg --break-system-packages`, for rasterizing the SVG so it
  could be visually inspected.

## 6. Device physics used from memory (verify before relying on)

Flagged here because these shaped the argument and none of them were looked up:

- Weak-inversion output conductance is DIBL-dominated, `gm·ro ≈ n·U_T/η`.
  Asserted early in the session as the cause of the poor PSRR and **retracted**
  once `Leg_matching` gave the real `V_A ≈ 37 V`.
- `σ(ΔI/I) = (gm/I_D)·σ(ΔV_th)` in weak inversion; `σ(ΔV_th) = A_VT/√(W·L)`.
- `I_spec□ = 2·n·µC_ox·U_T²`, order 200 nA/□ estimated for a 3.3 V NMOS from
  `t_ox ≈ 7 nm`. **Estimate only** — the real value needs a gm/I_D sweep.
- EKV inversion-coefficient framing (`IC = I/(I_spec□·W/L)`), used to argue M11
  may be sitting near `IC ≈ 1` rather than in weak inversion.
