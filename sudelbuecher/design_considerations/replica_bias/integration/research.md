# Slot 7 integration research (read-only), cloud session C4, 2026-11-08

Abbreviations. D = this design repo (`sg13cmos5l_cm_ip__single2diff2single`). H-up = `RTimothyEdwards/sg13cmos5l_ocd_chipalooza` main b346a27 (2026-11-06, local clone, grafted). H-fork = `tatzelbrumm/sg13cmos5l_ocd_chipalooza` (local clone). S7 = `tatzelbrumm/sg13cmos5l_cm_slot7` (public git clone, 4 branches; the GitHub MCP denied it, `git clone --depth 1` worked). Nothing was run, written or sent apart from this file.
Mark: [F] fact with source, [D] decision (by Christoph, as recorded), [P] proposal, [O] open.
Coverage limit: of the sessions I read only the newest pages of 8KytNQ (37 + a partial earlier page) and 77upRZ (newest ~10 events). I did NOT read 5LbmFC (C6); C6 facts come from its branch files. Event times below are UTC 2026-11-07.

## A. Harness slot-7 interface, semantics and defaults

Sources: H-up `verilog/rtl/{slot7_wrapper,user_project_control,user_project_control_base,chipalooza_frame}.v`, `netlist/schematic/chipalooza_frame.spice`, `scripts/setup_custom.sh`, `config.txt`; D `docs/slot7_testplatform/PLAN.md` s.1 (branch claude/c5-slot7-schematics).

| signal | semantics [F] | source |
|---|---|---|
| `vdd_3v3` | gated, high side only: `power_stage2` = hv PMOS 10u/0.4u m=700, enable `select & power_3v3_ena` (reg 0x51 bit1). Off = floating, not pulled low | frame.spice:621; control_base.v:134 |
| `vdd_1v2` | same, `power_stage1v2` = lv PMOS 5u/0.13u m=500, reg 0x51 bit2. Gated domain of the slot only (see [O] below on the harness SPI/sequencer) | frame.spice:611 |
| `vss_3v3`, `vss_1v2` | NOT switched: global nets `vss3v3`, `vss1v2` | frame.v:1133-1136 |
| pad-ring `iovdd/iovss` and core ring `vdd/vss` | not slot supplies, never gated (custom pad cells tap them, D `macros/slot/README.md`) | D slot/README.md |
| `enable` | `select & proj_ena`; buffered `buf_8` on the harness always-on 1.2 V rail, so a valid level even with the slot's `vdd_1v2` off; 0 when slot not selected | control_base.v:129; PLAN s.1 |
| `dig_in[23:0]` | router output (SPI reg 0x20+i, source 0..B = pad io[n], 0xD = 0, 0xE = 1, 0xF = sequencer) -> latch `dlhrq_1` (gate `dig_ena`, RESET_B = `select`) -> `buf_8`. 0 whenever slot 7 is not selected. Reset value of the route regs is 0x0 = pad io[0]: bits follow that pad until written (PLAN: set 0x20..0x37 = 0x0D first) | control.v:~80-110; PLAN s.1, s.5 |
| `dig_out[11:0]` | taken from the slot only if `select & dig_ena`, else the daisy-chain relay; readable by SPI reg 0x38/0x39 without a pad | control_base.v:102 |
| `clk` | gated by an explicit `sg13cmos5l_lgcp_1` clock-gate on `select` (harness now glitch-free; D TOP_LEVEL_MODULE.md line 63 "select & clk" is stale) | control.v:~125 |
| `reset` | `reset_sync` 2 flops, cleared by `enable`=0; "projects that do not use a clock should not use reset" | control_base.v:116-126 |
| `analog_bus0..3` | shared chip pads `analog[0..3]` (`user_analog_shared[k]`, one net for all 18 slots) -> per slot one `analog_switch_med` (hv N+P 10u x 40) enabled by `select & analog_ena[k]` (reg 0x51 bits 4..7). Project-0 diagnostic switches on the same nets, on only when `proj_sel`=0. Default (0x51=0): open | frame.v:~880-900; PLAN s.1 |
| `ibias0/1` | iDAC sources (reg 0x19 / 0x1A, 5 bit, sourced current) through per-slot `analog_pswitch_small` (CURRENT_MODE) enabled by reg 0x52 bits 0/1. Switch supplied from the always-on `vdd3v3/vdd1v2`, so a current can flow into a slot whose supply is gated off | frame.v:~905-935; frame.spice:55-56; ps doc 0x52 |
| `vbias` | `voltgen_v3` tapped-resistor output (steps of vbg/4 or vbg/3, regs 0x1B/0x1E/0x1F), per-slot `analog_switch_small` enabled by reg 0x52 bit2; same always-on supply caveat | frame.v:941; biasgen doc voltgen_v3.md |
| `s7_an[0:1]`, `s7_an_0_esd` | foundry route: two `IOPadAnalog` pads (+587 ohm secondary protection node `_esd` on pad 0). Custom route: those three ports are REPLACED by 13 core-side nets (below) | slot7_wrapper.v; custom_io_verilog.py output |
| power-up defaults | reg 0x51 = 0 (PLAN s.5 step 1: "With 0x51 still 0 everything in the slot is off"); `proj_sel` must be written (0x50=7). So a slot that is not selected sees: supplies floating, enable 0, dig_in 0, buses/ibias/vbias open | PLAN s.5 |
| what the slot sees if harness digital misbehaves | `enable`/`dig_in` stay valid 1.2 V levels while `vdd_1v2` is gated (always-on rail) -> a block fed from them with a gated-off supply gets a live input on an unpowered domain. D case already seen: `analog_switch_small`'s antennanp charged a floating gated-off `vdd_1v2` to 0.62 V and cores started at ff/fs 125 C | PLAN s.2 "Changed in phase 2" |

[O] Whether the 1.2 V `power_stage1v2` also powers parts of the harness (D TOP_LEVEL_MODULE.md line 58 says "also powers the harness's own SPI/sequencer"; the netlist shows only a PMOS switch from `vdd1v2`): not verified.
[O] Voltage level of `vbias` (vbg/4 steps, vbg value not read) and the iDAC full-scale are not in the files I read.
[F] H-up already declares in `config.txt`: `s7_source` = S7, `s7_an[0]: sg13cmos5l_IOPadSingle2Diff s7_an_0`, `s7_an[1]: sg13cmos5l_IOPadDiff2Single s7_an_1`, `s7_version: - -` (config.txt:89,111,156-157). Upstream has `make setup-custom` (`scripts/setup_custom.sh`) that finds a pad GDS in `final/<view>/`, `<view>/`, `pads/<pad>/` of the slot submodule (matches the S7 layout `pads/<cell>/`). Upstream `slot7_wrapper.v` still shows the old s7_an ports (generated by `make wrappers`).

## B. Fallback session (8KytNQ, "slot7 setup without pads"): resources and proposals

Sources: D branch claude/c5-slot7-schematics `docs/slot7_testplatform/{PLAN,SUMMARY}.md` s.2-9, `macros/slot7_testplatform/README.md`; S7 `README.md`, `docs/PROGRESS.md`; session events 20:20-21:43.

| resource | use now (stage A = on S7 main; stage B = S7 branch claude/c5-testplatform) | status |
|---|---|---|
| `dig_in[0]` / `[1]` | OA core / BG core enable (AND `enable` AND slot `vdd_1v2` present) | built, DRC/LVS/PVT sim, harness flow OK |
| `dig_in[2]` / `[3]` | xgate OA -> `analog_bus0` / BG -> `analog_bus1` (5 uA, SMU on `analog[0/1]`) | built |
| `dig_in[4..6]` | tree reference select: OA / BG / harness `ibias0` -> `bias_tree_noab_pd` iref | stage B built |
| `dig_in[7]` | tree enable | stage B built |
| `dig_in[8..11]` | `vbp vbn vbpc vbnc` -> `analog_bus2` (one voltmeter, one line at a time) | stage B built |
| `dig_in[12]` | harness `ibias1` -> `analog_bus3` (xgate) | stage B built; user (21:43) judged it redundant, would free bus3, dig_in[12], 1 xgate; nothing changed yet [O] |
| `dig_in[13..23]` | unused (11 free) | free |
| `dig_out[3:0]` | read-back of 4 stage-A enables (SPI 0x38); `dig_out[11:4]` held low by hv NMOS (gate `vdd_1v2`) | built |
| `analog_bus0/1/2/3` | OA current / BG current / 4 bias voltages / ibias1 | as above |
| `ibias0` | into the tree (via xgate), not measured itself | built |
| `ibias1`, `vbias` | ibias1 -> bus3; `vbias` unused | |
| `clk`, `reset`, custom-pad stubs | unused; 13 `s7_an_*` Metal3 stubs kept unchanged (outp->vinp, outn->vinn stand-in joins) | |
| enable cell | `tp_en_ctrl` (A, 43 hv devices) / `tp_en_ctrl_b` (B, 9 channels, 56 hv): ratioed hv PMOS 0.3/20 pull-up vs NMOS stack, no latch; costs 1.2-1.75 uA per enabled channel + 3.2-4.9 uA from `vdd_1v2` (iq_ratioed_devices.sh, commit 2c1903e6) | in `slot_7.gds` |
| draft replacement | `en_ctrl_stage_b` (one `en_ctrl_3v3`, `ls_up_1v2_3v3` per channel, nand2_hv + inv_hv): schematic only, netlist matches, no layout/sim; pushed to branch claude/c5-slot7-schematics 2c1903e6 (14:14). Session 77upRZ: user said it is "the fix", fallback keeps reduced scope with library cells | [P]/draft |

Fail-safe in the fallback [F]: every enable = `dig_in[k] AND enable AND slot vdd_1v2 present`; vdd_1v2 gated off with dig_in/enable high (1 uA injected) gives all 495 sim points correct; vdd_3v3 gated off with 0.7 V on bus: <= 87 nA into slot (TG PMOS to n-well), vdd_3v3 floats 0.5-0.67 V; procedure: open bus switches and SMU 0 V before gating vdd_3v3 (PLAN s.5). Supplies: vdd_3v3 19-30 uA both cores on, <= 7 nA off (SUMMARY).
Deliverables: S7 `main` (stage A, slot_7.gds sha abc7a362...), S7 `claude/c5-testplatform` c4e60b8 (stage B + matched tree layout, fork flow `claude/c5-testplatform-test` f443ce1: exit 0, XOR empty, 49 used + 14 unused pins OK, "ready for main, merge is slot owner's decision"). Design repo branches: claude/c5-slot7-testplatform, -schematics, -tree-layout, slot7-stage-a. Gap: no analog-bus monitor of the pads' internal bias (vcm, vref, iref, tree voltages) exists, because the pads/rb cells are not in the fallback.
[P] 8Kyt, 21:39 (stage B mux reasoning): add xgates for `vbn`/`vbp` onto bus0/bus1 when cores are off so two voltages read at once (+2 dig_in bits, +2 xgates). Not built.

## C. Fail-safe: what exists, and what was discussed

Source: D `macros/en_ctrl_3v3/README.md` (CACE 2026-10-20, schematic only, no layout, no MC); D `macros/README.md`; D `macros/slot/README.md`.

- Function [F]: `en_3v3 = en_1v2 AND vdd_1v2 present AND vdd_3v3 present`; `sel*_3v3` = level-shifted `sel*_1v2`; `en_3v3_b = NOT en_3v3` (XIB inv_hv 1u/0.45u). Ports: `vddh vddl vss en_1v2 sel0_1v2 sel1_1v2 vdd1v2_sense vdd3v3_sense en_3v3 sel0_3v3 sel1_3v3 en_3v3_b`.
- Parts: 3 x `ls_up_1v2_3v3`; 2 x `pg_det` (hv NMOS 2u/0.45u gate on sensed supply vs weak hv PMOS 0.3u/50u; RD hv NMOS 0.3u/100u pulls a floating sense low; PU/RD gated by level-shifted enable); `nor3_hv`. 1.2 V supply (vddl) only for the ls_up input inverters.
- It gates [F]: the pad's bias generation (`bias_gen_pd` / trees, via `en_3v3`, `en_3v3_b`, selects) and in the slot fallback the pad's `en_3v3`; it does NOT gate pad-ring supplies (`iovdd`, `iovss` cannot be switched). A disabled pad draws current from the ring only by leakage.
- Quiescent current [F]: enabled (tt-corner worst over PVT): vddh <= 1.94 uA (limit 2.5), `vdd1v2_sense` <= 1.43 uA, `vdd3v3_sense` <= 1.73 uA (RD pulls), vddl <= 39 nA, `en_1v2` input <= 0.2 nA. Disabled by `en_1v2`=0: pA (leakage only). Delay: enable 3.7 ns, disable 5.4 ns worst (50 fF). Supply loss (1 V -> 0 in 1 us) -> en_3v3 low within 0.92 us.
- Known weakness [F]: with vddl = 0 and en_1v2 still high, en_3v3 stays correctly low but ss/-40 C/low supply the ls_up latch draws 152 uA from vddh (0.33-0.97 uA elsewhere). In the pad cell vddl = always-on core ring (does not occur); in the slot fallback `en_1v2` falls with gated `vdd_1v2`. [O] a slot `vdd_1v2` that floats rather than ramps was not simulated.
- In the custom-pad route sense wires: `vdd1v2_sense`, `vdd3v3_sense` = the slot's gated supplies, two slot-to-pad wires (D slot/README.md). BUT the delivered pad cells have core-side pins `... en_3v3 en_3v3_b iref` only (S7 `pads/pads.txt`): `en_ctrl_3v3` and `bias_gen_pd` are therefore NOT inside the pads any more; they are slot-side blocks [F: pins; inference: en_ctrl moved out; README text not updated].
- Discussed elsewhere: 8Kyt/77upRZ: a fail-safe built from existing cells once per slot (`en_m`), per-channel level shifter, masking the undefined shifter output when `vdd_1v2` is missing (21:38 reply). A 3.3 V std-cell library `sg13cmos5l_stdcell_hv` exists only in the PDK `dev` ref (D docs in sudelbuecher `R_report.md`, agent R, 2026-11-08); not in our checkout. [O] no source found where a pad-ring supply is switched.

## D. Hand-over repo (S7) and C6

- S7 contents [F] (README.md, pads/pads.txt): `final/{gds,lef,lib,vh}/slot_7.*` (tracked on main = stage A), `pads/sg13cmos5l_IOPadSingle2Diff/{.gds,.spice}`, `pads/sg13cmos5l_IOPadDiff2Single/{.gds,.spice}`, `pads/pads.txt` manifest, `macros/{oa_core_pd,bg_core_pd}` (GDS + netlist, DRC 0, LVS match), `docs/PROGRESS.md`. Branches: main (stage A), claude/slot7-stage-a, claude/c5-testplatform (stage B, newest c4e60b8 2026-11-07), claude/c6-pads-layout (pads + plumbing stand-in slot_7). No LEF for pads (harness sets FIXED_BBOX 0 0 80 180). Pad LVS note: `vss` pin merges with `iovss` (accepted 2026-11-03).
- Delivered pad core-side pins [F, pads.txt]: S2D `vref outp outn vcm en_3v3 en_3v3_b iref`; D2S `vinp vinn vref iref en_3v3_b en_3v3`; ring pins `iovdd iovss vdd vss pad`. Chip nets: 13 (`s7_an_0_vref, _outp, _outn, _vcm, _en_3v3, _en_3v3_b, _iref, s7_an_1_vinp, _vinn, _vref, _iref, _en_3v3_b, _en_3v3`); wrapper loses `s7_an[1:0]`, `s7_an_0_esd`. Pin y-positions at slot right edge x 535.05-536.45: S2D y 112-160, D2S y 222-262 (S7 README).
- C6 [F, H-fork branch claude/c6-submodule-pads 0774ac3 2026-11-06 14:15, `docs/custom_io/TIM_STEPS.md`, `DRYRUN.md`]: Tim's manual steps = merge `claude/c6-pads-layout` into S7 main, edit 4 lines of config.txt, `make projects SLOTS=7`, `setup`, `custom-io`, hand-edit chip Verilog from `custom_io_verilog.py` (4 files), `clean-config config padframe frame-custom-io wrappers gds-slots projects-gds SLOTS=7 gds-prefill`, then netcheck (all 13 pins OK in the dry run); `make lvs-top` not run, 17 other slots not fetched. H-fork branches custom-pad-test (s7_version claude/c5-testplatform c0726799, i.e. stage B) and claude/c5-testplatform-test hold the same flow with stage B.
- Plan for Tim [F]: S7 README "pads on main", "merge is the slot owner's decision" (stage A delivered on main 2026-11-06; stage B + matched tree not yet on main). Missing in S7: the real slot circuit with pads (S2D/D2S, pad_ref_rb, bias_dist_pd, en_ctrl, bypass caps) and any layout of them; pads' bias/en inputs are unconnected stubs in every delivered slot_7.gds (outp->vinp, outn->vinn joins only).
- Note for upstream: H-up has its own `setup_custom.sh` (not C6's `custom-io`); the S7 `pads/<cell>/` layout is accepted by it (header comment). [O] whether Tim uses setup_custom (upstream) or C6's scripts (fork): the C6 hand-edit of Verilog may be redundant upstream.

## E. Conflicts / open questions between the plans

1. Stale pin lists. `macros/slot/README.md` lists pad core pins `vinp vinn vref ibias en_1v2 sel0_1v2 sel1_1v2 vdd1v2_sense vdd3v3_sense` (19 wires); the delivered pad cells have `... en_3v3 en_3v3_b iref` (13). The slot-side hook-up (en_ctrl_3v3, bias_gen/bias_dist_pd, pad_ref_rb) is not described in any README. [O] decide which README is authoritative.
2. Bias placement: pads take `iref` (sourced 5 uA, one per pad) from the slot; `bias_dist_pd` gives iout0 -> pad_ref_rb, iout1 -> S2D, iout2 -> D2S, iout3 spare, inputs OA core, BG core, ibias0, ibias1 (D macros/README.md, bias_dist_pd README). Fallback uses ibias0 as tree reference (dig_in[6]) and ibias1 -> bus3. [P] same `dig_in` bits cannot serve both; the allocation for the integrated slot is open.
3. Supply of rb/dist blocks: `pad_ref_rb` and `bias_dist_pd` use `vddh/vssh`, to be the pads' rails ("custom-pad route: padframe rails") or `vdd_3v3/vss_3v3` (slot fallback). The pad rails are never gated, the slot rails are. If these blocks sit on the slot supply while pads sit on the ring, a slot gated off with ibias/vbias/bus live can back-feed (87 nA already seen). [O] one domain per block must be chosen; sense wires `vdd1v2_sense/vdd3v3_sense` presently only exist in en_ctrl_3v3.
4. Enable cell choice: fallback built a ratioed `tp_en_ctrl*` (costly, 1.2-1.75 uA/channel), the lead's hand-over uses `en_ctrl_3v3` (1.4-1.9 uA/rail, ~2 uA from vddh) per pad plus `ls_up` shifters; 8Kyt/77upRZ now want the draft `en_ctrl_stage_b` (one en_ctrl_3v3 + ls_up + nand2_hv/inv_hv, no layout). `hv_logic`, `ls_up_1v2_3v3`, `en_ctrl_3v3`: schematic only; no hv std-cell library locally. Layout cost is open.
5. Which design goes into `slot_7.gds`: fallback (stage B, ready, merge undecided) versus the pad-integrated one (nothing laid out at slot level). Also `analog_bus` use: fallback uses all four; a pad-integrated slot needs monitor taps on the buses for vcm/vref/iref and tree voltages (not proposed anywhere). `ocd_analog_switches` (xgate, `analog_switch_*`) exist as KLayout copies, DRC/LVS not done in D (macros/README.md).
6. Default states: `dig_in` route reset 0x0 follows pad io[0] (PLAN); the pads' enable must not follow it. The en_ctrl fail-safe already requires `enable` AND supplies present, but it does not defend against `enable`=1 with `dig_in` routed from a toggling pad io[0] while the supplies are on. [O] whether pad enable should come from `enable` alone, from a `dig_in` bit, or both.
7. Docs inconsistency: TOP_LEVEL_MODULE.md still lists `analog_pin[2:0]`, `select & clk`, and `ibias_ena[1:0]` as separate ports; H-up code uses different wrapper ports (dedicated `s7_an`, `ibias0/1`, `vbias`) and the glitch-free clock gate.
8. Process: fallback session's stage-B build and 77upRZ's `en_ctrl_stage_b` draft landed on branch claude/c5-slot7-schematics (2c1903e6) from two sessions; the user said stage B is a "quick and dirty fallback that is going to change" (21:43) and ibias1->bus3 is redundant. Merge of S7 `claude/c5-testplatform` into main is open.
