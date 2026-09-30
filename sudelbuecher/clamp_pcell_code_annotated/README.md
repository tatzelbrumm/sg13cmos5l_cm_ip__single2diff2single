<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Clamp PCell code: dependency trees

`cni` = IHP-GmbH/pycell4klayout-api @ `ad47f5f7`, `source/python/cni/`.
`PDK` = IHP-GmbH/ihp-sg13cmos5l @ `597570ee`, `libs.tech/klayout/`; `sg13_tech.py`, `geometry.py`,
`utility_functions.py` are under `PDK python/sg13cmos5l_pycell_lib/`.
Files without a path are in this folder; `scripts/pcells/…` are not copied here.

## Imports

```
Clamp_N_code.py, Clamp_P_code.py
└── clamp_base_code.py
    ├── cni dlo.py ─────────────── star-imports cni layer, box, point, pointlist, font, dlogen, … (dlo.py:21-46)
    │                              used: DloGen, ChoiceConstraint, Layer, Box, Point, PointList, Font
    ├── PDK geometry.py ────────── used: dbReplaceProp, dbCreateRect, dbCreatePolygon, dbCreateLabel
    │   ├── cni dlo.py
    │   └── PDK utility_functions.py ── strToAlignt, strToOrient (inside dbCreateLabel)
    ├── PDK utility_functions.py ── imported, nothing used
    ├── clamp_engine.py ────────── used: FAMILY, generate, cell_name, ClampError   (imports nothing)
    └── clamp_refdata.py ───────── used: REFDATA                                    (imports nothing)

scripts/pcells/load_clamp_pcells.py     (run by hand in KLayout)
└── scripts/pcells/__init__.py          (loaded as package sg13cmos5l_cm_clamps)
    ├── pya
    ├── PDK sg13cmos5l_pycell_lib/__init__.py ── creates technology SG13_dev
    │   └── PDK sg13_tech.py ── reads PDK sg13cmos5l_tech.json, PDK tech/sg13cmos5l.lyp
    ├── cni tech.py (Tech), cni dlo.py (PCellWrapper)
    └── Clamp_N_code.py, Clamp_P_code.py   (by name, from moduleNames)
```

## Calls: KLayout start to library

```
PDK tech/pymacros/autorun.lym:37-39
└── import sg13cmos5l_pycell_lib ── sg13_tech.py:106 Tech.register(SG13_Tech())
    ├── sg13_tech.py:41      techParams   ← sg13cmos5l_tech.json
    └── sg13_tech.py:49-75   layer table  ← tech/sg13cmos5l.lyp  (json "Layers" only if no .lyp)

load_clamp_pcells.py (Shift+F5)
└── __init__.py ClampPyCellLib()
    ├── Tech.get('SG13_dev')
    ├── for Clamp_N, Clamp_P:
    │   ├── Clamp_X() → DloGen.__init__                 cni dlogen.py:169  (props, tech)
    │   └── PCellWrapper(that object, tech, …)          cni dlo.py:166
    │       ├── impl.setTech(tech)                       cni dlogen.py:209
    │       └── Clamp_X.defineParamSpecs(wrapper)        clamp_base_code.py
    │           ├── wrapper.tech.getTechParams()         sg13_tech.py:95
    │           └── wrapper(...) ×5                      cni dlo.py:190 → pya.PCellParameterDeclaration
    ├── layout().register_pcell('Clamp_X', wrapper)
    └── register('SG13_cm_clamps')
```

## Calls: one variant drawn

```
KLayout → PCellWrapper.produce                           cni dlo.py:277
├── params_as_hash                                       cni dlo.py:266
└── with PyCellContext(tech, cell, impl)                 cni dlo.py:91, :280
    ├── impl.addCellContext(cell)                        cni dlogen.py:158
    ├── impl.setupParams(params)                         clamp_base_code.py
    └── impl.genLayout()                                 clamp_base_code.py
        ├── generate(FAMILY, ng, tie, REFDATA)           clamp_engine.py
        │   ├── plan ─── reads REFDATA
        │   │   ├── nearest_ref, interp, snap
        │   │   ├── expand, shift_texts
        │   │   └── check_limits ── array_extent, _bbox
        │   ├── array_shapes ── array_extent, columns, gate_lefts, _box
        │   ├── bus_shapes ──── gate_lefts, _box
        │   └── rule_texts ──── columns
        ├── dbReplaceProp ×7                             PDK geometry.py:1051 → DloGen.props (never read)
        ├── Layer(lay, pur)                              cni layer.py:24
        │   ├── PyCellContext.tech.stream_layers()       sg13_tech.py:98 (.lyp table)
        │   └── PyCellContext.layout.layer(l, d, name)
        ├── dbCreateRect                                 PDK geometry.py:283
        │   └── cni Rect                                 cni rect.py:28
        │       ├── cni Shape → DloGen.addShape          cni shape.py:35, :44-45
        │       └── PyCellContext.cell.shapes(l).insert(pya.DBox)   cni rect.py:35
        ├── dbCreatePolygon                              PDK geometry.py:293
        │   ├── PointList.compress                       cni pointlist.py:29
        │   └── cni Polygon → pya.DSimplePolygon         cni polygon.py:35
        └── dbCreateLabel                                PDK geometry.py:365
            ├── cni Text → pya.DText                     cni text.py:30
            ├── strToAlignt → Text.setAlignment          PDK utility_functions.py:333, cni text.py:68
            └── strToOrient → Text.setOrientation        PDK utility_functions.py:305, cni text.py:104
    exceptions → PCellWrapper._printTraceBack            cni dlo.py:284-285 (console; cell stays empty)
```

## Data

```
clamp_refdata.py  (REFDATA)
└── written by scripts/pcells/extract_clamp_refdata.py
    ├── IHP sg13cmos5l_io.gds, sg13cmos5l_io.cdl       (sha256 in the file header)
    ├── extract LAYERS table      GDS number → layer/purpose name
    └── clamp_engine.array_shapes, bus_shapes          subtracted: REFDATA = IHP cell − rules

layer/purpose name → GDS number, three tables that must agree:
├── PDK tech/sg13cmos5l.lyp via sg13_tech.py          PCell path (clamp_base_code.genLayout)
├── scripts/pcells/clamp_klayout.py GDS               batch path (gen_clamp.py, verify_clamp.py)
└── scripts/pcells/extract_clamp_refdata.py LAYERS    inverse, extraction

clamp_engine.FAMILY keys
├── array_shapes, bus_shapes, rule_texts, check_limits     geometry
├── model ── clamp_base_code (inert parameter default), scripts/pcells/clamp_netlist.py
├── w_finger, n_dev ── clamp_netlist.py, lvs_clamp.py, verify_clamp.py
└── height ── extract_clamp_refdata.py
```
