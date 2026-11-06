# SUMMARY: slot 7 delivery repository

**DELIVERY_REPO:** https://github.com/tatzelbrumm/sg13cmos5l_cm_slot7, branch `main` (only branch, no inherited history),
commit `c5d50034d83d075ad8f719f4982167d4d3f15ba1`. Steps and commands: `RUNLOG.md`; logs and check scripts: `logs/`.

## Files (sha256; `.spice` = hash of the source, i.e. the file without its 4-line provenance header)

| file | source (design repo) | sha256 |
|---|---|---|
| LICENSE | toplevel 91a7da8 `LICENSE` | a7fd04ca6fa87a80afd79015999a48e6e5db4966926af0a69182cb8c2d836d9f |
| final/gds/slot_7.gds | harness-test 4611357 | 5624ae45efb7761fd0b405ecc785a3f2f3c3a93d93203d0aaca9feb15bedc11c |
| final/lef/slot_7.lef | harness-test 4611357 | 9fd8d5b1c57d7a2d26ad8e4883d8634f5dec4bfc36a9026ad9becc5401c9d8a8 |
| final/lib/slot_7.lib | harness-test 4611357 | 6137d6230046318850c9f1fba2d8e79322ce28d9e18f0e2e64385099c419bd56 |
| final/vh/slot_7.vh | harness-test 4611357 | 1ba0f560eb7b9e23258d2f371b1e8ab0936b4103aeb7ccaece69990c75086976 |
| final/pads/sg13cmos5l_IOPadDiff2Single.gds | toplevel 91a7da8 `.klay.gds` | 13e176ab106d0cb307a6ebc42acf647ce38b6abc52183a9f1d9ffead2f6c2b17 |
| final/pads/sg13cmos5l_IOPadSingle2Diff.gds | toplevel 91a7da8 `.klay.gds` | f4b0e07320821248872780b344d71845d08bc250a4bfc9bcf8633a39bdef0182 |
| final/pads/sg13cmos5l_IOPadDiff2Single.spice | toplevel 91a7da8 `_magic.spice` | b8d9103230bd7ced5c75a0fb38d56f078ec3cbf48d0f82a3772b85ff1edc2c1c |
| final/pads/sg13cmos5l_IOPadSingle2Diff.spice | toplevel 91a7da8 `_magic.spice` | 5a4e67f9b12f5f9017978ad0da4305fb331c9aa3abf4657ec48f5c77a8d32810 |
| final/pads/pads.txt | written (task file) | dc1419d445ba69e8077fde47bb15ffeb94e4d1d6ae4dfec73f665e10590665fa |
| README.md | written | (provenance, pin table, config.txt lines, LVS note, stand-in statement) |

## Checks (Phase 2): all pass

1. sha256 equal to the source: 9/9. 2. slot_7.gds: one top cell `slot_7`, bbox 0..537.15 x 0..273; pad GDS: one top cell
named like the file, bbox -0.62..80.62 x 0..180; every pads.txt pin is a top-cell text on 10/25 at y 179.74 (S2D) / 179.715
(D2S); the 13 `s7_an_*` Metal3 texts match `slot7_pins.md` (nine also have a Metal4 stub label, by design of the stand-in).
First run of this check failed on that over-strict condition; kept in the log. 3. `.subckt` pins = pads.txt + iovdd iovss vdd vss pad: both OK.
4. KLayout DRC slot_7.gds (PDK deck, FEOL+BEOL, deep): 0 violations. 5. fresh clone: `.git` 732K, tree 3.3M.

## Harness flow (Phase 3): pass

Harness fork branch `delivery-test` (from custom-pad-test 79302da), commit 93e459d: config.txt s7 -> sg13cmos5l_cm_slot7
`main c5d5003`. `make projects-clean SLOTS=7`, `make projects SLOTS=7`, `make projects-gds SLOTS=7`: exit 0; slot_7.gds found in
`dependencies/slot_7/final/gds/` and placed at 1379.95 2170.05 (`scripts/user_projects.tcl` unchanged). Submodule git dir 736K
(160 MB before). The delivered pad GDS are byte-identical to the harness's `magic/custom_io/gds/*.gds`.

## Harness rework to read the pads from the slot repository (not done; separate task)

`scripts/setup_custom_io.sh` would take each pad GDS from `dependencies/slot_7/final/pads/<cell>.gds` (copy into
`magic/custom_io/gds/` before `custom_io_uniquify.py`) and build its `CUSTOM_IO` list (cell + prefix) from `pads.txt`;
`scripts/parse_config.py` would fill `CUSTOM_PADS` (core-side pin order) from `pads.txt` instead of the hard-coded table;
`netlist/schematic/custom_io.spice` would be generated from `final/pads/*.spice`, dropping the second copy of
`.subckt unit_r2` (both pad netlists contain it, identical); `magic/custom_io/PROVENANCE.md` would name the delivery
repository and commit; and the Makefile / README sequence would have to run `make projects` before `setup_custom_io.sh` and
`make padframe`, since the pads are now a project dependency rather than tracked harness files.

## Open points

- `slot_7.gds` is the plumbing stand-in; the real slot circuit has to be committed to the delivery repo and `s7_version` bumped.
- Known LVS note (`vss` pin, substrate merge) stays as documented in the pads' READMEs; not re-run here.
- Nothing was sent to `RTimothyEdwards/*`; telling Tim about the delivery repo is the user's step.

## Follow-up (same day): bias cores added

Delivery `main` now `40ba9b030d0c3e321438600fea5ae0a13439799a`: `macros/bg_core_pd/` (Banba bandgap) and `macros/oa_core_pd/`
(Oguey–Aebischer), each about 5 uA sourced from `iout` into a pad's `iref` (sha256 in the delivery README). KLayout PDK DRC
0 / 0; magic + netgen LVS (`sak-lvs.sh`) match uniquely for both. Not placed in `slot_7.gds` yet; the harness does not read
`macros/`. Harness `delivery-test` f327570 follows 40ba9b0: projects-update / projects-gds exit 0, placement unchanged,
submodule git dir 1.2M. Tim's requirement (pads on the slot repo's default branch, used as a submodule) is met by `final/pads/`.
