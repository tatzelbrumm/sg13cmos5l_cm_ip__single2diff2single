# Per-PDK checklist (fill in before writing any geometry)

Look every item up in the PDK files; write the source next to the value. Items marked [guess] are general knowledge, not checked in any session: verify them.

| item | where to look | IHP sg13cmos5l (checked) |
|---|---|---|
| GDS layer / datatype of each drawing layer, nofill, filler, pin, boundary | layer properties (.lyp), tech file, map file | `.lyp` -> 8/0 Metal1, 10/0, 30/0, 50/0, 126/0 TopMetal1, 5/0 GatPoly, 1/0 Activ; nofill = datatype 23, filler = 22, 189/4 prBoundary |
| which layers exist (metal count, local interconnect, top metal, poly levels) | tech docs, DRC deck forbidden-layer rules | M1-M4 + TM1 only; M5, TM2, MIM forbidden |
| manufacturing grid | DRC deck offgrid rule | 5 nm |
| allowed edge angles | DRC deck angle rule | metals and poly: 0 / 45 / 90 only |
| min width, min space per art layer, wide-metal and 45-degree variants | tech rule file | M1 0.16 / 0.18; M2-4 0.20 / 0.21; wide-line space 0.24 (0.6 for > 10 um); TM1 1.64 / 1.64; GatPoly 0.13 / 0.18 |
| min area | rule file | M1 0.09, M2-4 0.144 um2 |
| density rules (global, window) and what chip area they use | rule file + density deck | global per chip 35-60 % M1-4; window 800 x 800 um with fill 25-75 % |
| antenna rules | antenna deck | floating shapes tied to no gate: nothing |
| front-end layers that create devices; tap / latch-up rules | deck | poly over active needs implants for a device but the active alone needs a tap within 20 um (LU.b) |
| fill tool and how it is told to stay out | PDK filler script / macros | filler macros exclude Activ / GatPoly / Metal / TopMetal nofill (x/23) and NoMetFiller 160/0; fills inside a seal ring (39/0) only |
| DRC command, LVS command and what the host's README uses | PDK scripts, host docs | `run_drc.py --path --topcell --run_dir --antenna`; `run_lvs.py --run_mode=deep --disable_tap_extraction` with the host CDL |
| layer stack heights (what hides what from above) | cross-section file | poly/active about 1 um below Metal1, then M1-M4, TM1 on top; all dielectric transparent |
| host layout: boundary, existing shapes, strap layers, docs with keep-outs, harness fill/seal conventions | host repo | slot_7: 537.15 x 273 um, TM1 straps at y 130-140 and 232-242 |

## Other PDKs: what to check first [guess]
- SKY130: [guess] local interconnect (li1) plus met1-met5 plus poly and diff; probably enough layers for one colour per layer; rule decks for KLayout / Magic differ from IHP's; check the angle rule, the density and antenna rules, how fill is done (OpenLane or a fill tool) and whether nofill-like marker layers exist.
- GF180MCU: [guess] poly2, comp, Metal1-Metal5 variants, a thick top metal; check the metal option chosen, which DRC deck (KLayout) is current, and the fill convention.
- All: run the DRC deck on the untouched host first to get the baseline rule set; assume nothing about angles, grid or density until read.
