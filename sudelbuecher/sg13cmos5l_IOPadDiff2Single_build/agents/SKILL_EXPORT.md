# Addendum for A2, A3, A4: export transferable layout skills (2026-10-28 02:50)

The user, verbatim: "let the agents develop (and export) transferable layout design skills. are non-verbal formulations
of these skills available? I think not only in words, but very much in graphical (and musical) patterns."

On top of your cells, deliver in `out/skill/` what a future agent (who has never seen this session) needs to repeat
your work on another block, e.g. the bandgap's bg_nab / bg_misc_n / bg_pmir_pcas / bg_misc_p. The point is
transfer, not description. Formulate every pattern in three forms that say the same thing:

1. **Symbol / score form** (`patterns.md`): each array as a sequence or matrix of device letters, with the transform
   that generates it. For example, a row `d A B B A d` = translation + mirror. Use these terms consistently:
   - translation = repetition;
   - mirror = retrogradation;
   - point symmetry = retrograde inversion;
   - interdigitation = alternation (hocket);
   - an end dummy = the rest that closes a phrase.

   For 2-D arrays, give the matrix and the symmetry operations that map it onto itself, plus the "voices": which
   device sits on which row / track / Metal2 lane. Keep it exact enough that a script could parse it.
2. **Picture form**:
   - (a) a pattern tile rendered from YOUR GDS, not hand-drawn: device letters on the fingers, taps, tracks and pins
     labelled, a scale bar;
   - (b) before / after at the same scale with the outline dimensions;
   - (c) one picture that shows the rule that drove each saving (e.g. where the inner tap row was and what replaced
     it), annotated with the rule and its value.
   PNG, readable at 1:1.
3. **Generator form** (`generator.py`): the parametric function(s) that turn a pattern string / matrix, a device cell
   and the rule values (read from `sg13cmos5l_tech_default.json`, with keys cited) into the cell. It must be
   importable and reusable for a block with other devices: no hard-coded oa net names inside, they are arguments.

Plus:
- `rules.md`: the do / don't list you actually followed, each with the deck rule and value that forces it, and the
  pitfalls you hit (what failed DRC or LVS first, and why).
- `SKILL_draft.md`: a draft in SKILL.md form (YAML frontmatter `name`, `description`; then when to use, the procedure
  step by step, the pattern notation, the pitfalls, and pointers to the pictures and the generator by relative path).

Keep `out/skill/` self-contained (relative paths only). Put its file list with sha256 into your final reply.

## Addendum 2 (03:04): process-agnostic skills

The user, verbatim: "nwell doesn't have to be rectangular if polygonal shapes are allowed by the design rules. make
sure that transferrable layout skills are process agnostic, in the sense that process specific design rules are very
important, but the skills themselves must be adaptable to a different set of design, parasitic extraction, device
model, and LvS rules."

- **Wells:** NWell (and tap) outlines follow the devices as polygons, within what the deck allows. Read the deck's
  angle / grid rules for NWell, and cite them. Use 45° edges only where the deck permits them; otherwise rectilinear
  polygons, never a bounding rectangle by default.
- **Split process from skill.** Structure the skill material in two layers:
  1. **Process adapter**, one file per process. For sg13cmos5l, `process/ihp_sg13cmos5l.py` or `.json`. It holds every
     process-specific item, each with its source (deck file / json key / model file):
     - the layer map;
     - the DRC values the generators use;
     - the device cells or PCells and how LVS recognizes each device (recognition layers, terminal derivation,
       bulk rule);
     - the latch-up rules (LU distances, which taps count);
     - the well rules (NW spacing same net / different net, angles);
     - the parasitic-extraction facts that drive the layout (which layers carry significant R / C, as far as the
       PEX rules say);
     - the model facts that drive it (e.g. which W / L / nf the models are characterized for, the finger-width
       limits).
  2. **Process-free skill:** the patterns (score and picture forms), the procedure, and the generators. Generators
     take every value from the adapter: no rule number, layer number or device name inside the generator.
- **Porting procedure:** `SKILL_draft.md` gets a section "porting to another process". For each adapter field it says
  where to find the value in a new PDK (DRC deck, LVS deck, PEX rules, model cards) and how to verify it, e.g. a
  self-test cell that must pass that PDK's DRC / LVS.
- **Generic tools:** the check scripts (DRC subset, extraction / LVS, verify) become adapter-driven too, or say
  clearly which parts are IHP-only.

## Addendum 3 (03:14): two kinds of skill, kept apart

The user, verbatim: "record both skills specific for IHP, and process agnostic skills, and clearly distinguish between
them."

Split `out/skill/` into two parts, each with its own `SKILL_draft.md`:

- `out/skill/generic/`: the process-agnostic skill.
  - It holds the patterns (score and picture forms), the procedure, the generators (adapter-driven), and the porting
    section.
  - It contains no IHP name, layer number or rule value. Where an example needs numbers, write it as "e.g., in
    IHP sg13cmos5l: … (see ../ihp_sg13cmos5l/)".
- `out/skill/ihp_sg13cmos5l/`: the IHP-specific skill.
  - It holds the process adapter (the data file), plus the IHP know-how that is more than numbers:
    - the SG13_dev / sg13cmos5l device cells and PCells and their quirks;
    - which deck files implement which rule, and which ones are missing from the uploaded copy;
    - LU as the IHP deck computes it;
    - the hv-device (ThickGateOx) and NWell specifics;
    - the pin / text layer conventions of this library;
    - the IHP-specific pitfalls you hit, and the workarounds (e.g. the Python DRC subset when the KLayout Ruby deck
      can't run).
  - It points to `../generic/` for the procedure itself.

Mark every rule and lesson in `rules.md` and in your report as **[generic]** or **[IHP]**. If a lesson has both a
generic core and an IHP value, write it once in generic form and once as the IHP instance. Both SKILL_drafts have
frontmatter whose `description` says which kind it is, e.g. "process-agnostic …" vs. "IHP sg13cmos5l-specific …".
