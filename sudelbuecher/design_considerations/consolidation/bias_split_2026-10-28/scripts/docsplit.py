"""2026-10-28 bias split: READMEs and yaml comments. usage: docsplit.py <root>"""
import sys, os
M = os.path.join(sys.argv[1], 'macros')
def edit(rel, pairs):
    p = os.path.join(M, rel); t = open(p).read()
    for a, b in pairs:
        assert t.count(a) == 1, (rel, a[:60], t.count(a)); t = t.replace(a, b)
    open(p, 'w').write(t)
D, S = 'sg13cmos5l_IOPadDiff2Single', 'sg13cmos5l_IOPadSingle2Diff'
edit('README.md', [
    ('│   ├── bias_sel_noab_pd ── hv_logic, oa_core_pd, bg_core_pd, bias_tree_noab_pd\n',
     '│   ├── bias_gen_pd ── hv_logic, oa_core_pd, bg_core_pd\n│   ├── bias_tree_noab_pd\n'),
    ('    ├── bias_sel_pd ── hv_logic, oa_core_pd, bg_core_pd, bias_tree_pd\n',
     '    ├── bias_gen_pd ── hv_logic, oa_core_pd, bg_core_pd\n    ├── bias_tree_pd\n'),
    ('| `bias_sel_pd` | the pads\' bias: one mirror tree, reference = harness ibias / Oguey–Aebischer / bandgap (generator in the pad) | sheets + CACE |',
     '| `bias_sel_pd` | `bias_gen_pd` + `bias_tree_pd` in one cell: one mirror tree, reference = harness ibias / Oguey–Aebischer / bandgap. The pads\' bias until 2026-10-28; since then the pads instantiate `bias_gen_pd` and the tree side by side (same devices), and this cell stays as the reference for its CACE results | sheets + CACE |'),
    ('| `bias_sel_noab_pd`, `bias_tree_noab_pd` | the same without the class-AB branches, for the s2d pad | sheets, 2026-10-27; netlist-checked against `bias_sel_pd` / `bias_tree_pd` |',
     '| `bias_sel_noab_pd`, `bias_tree_noab_pd` | the same without the class-AB branches, for the s2d pad (since 2026-10-28 the pad uses `bias_gen_pd` + `bias_tree_noab_pd`) | sheets, 2026-10-27; netlist-checked against `bias_sel_pd` / `bias_tree_pd` |'),
    ('| `bias_gen_pd` | `bias_sel_pd` without the tree: selectable reference current for the slot\'s main area | sheet, 2026-10-27, not simulated |',
     '| `bias_gen_pd` | `bias_sel_pd` without the tree: selectable reference current, in both pads (`xg`, next to the tree `xt`) since 2026-10-28, or in the slot\'s main area | sheet, 2026-10-27; on its own not simulated |')])
edit(D + '/README.md', [
    ('`en_3v3_b` = NOT `en_3v3` for `xb` and `xd` |', '`en_3v3_b` = NOT `en_3v3` for `xt` and `xd` |'),
    ('| `xb` | `bias_sel_pd` (`../bias_sel_pd`) | six bias lines from one mirror tree; reference selected by `sel1 sel0` |',
     '| `xg` | `bias_gen_pd` (`../bias_gen_pd`) | the reference current `iref` (sourced), selected by `sel1 sel0` |\n'
     '| `xt` | `bias_tree_pd` (`../bias_tree_pd`) | six bias lines from one mirror tree fed by `iref`. `xg` + `xt` are the former `xb` = `bias_sel_pd`, device for device (split 2026-10-28) |'),
    ('`bias_sel_pd` and `d2s_mpdda_pd` as a port;', '`bias_sel_pd` (since 2026-10-28 `bias_tree_pd`) and `d2s_mpdda_pd` as a port;'),
    ('`d2s_mpdda_pd` and `bias_sel_pd`), whenever', '`d2s_mpdda_pd` and the bias, `bias_gen_pd` + `bias_tree_pd`), whenever')])
edit(S + '/README.md', [
    ('`en_3v3_b` for `xb` and `xa` |', '`en_3v3_b` for `xt` and `xa` |'),
    ('| `xb` | `bias_sel_noab_pd` (`../bias_sel_noab_pd`) | four bias lines vbp vbn vbpc vbnc from one mirror tree; reference selected by `sel1 sel0`; until 2026-10-27 `bias_sel_pd`, whose class-AB legs stayed unused here |',
     '| `xg` | `bias_gen_pd` (`../bias_gen_pd`) | the reference current `iref` (sourced), selected by `sel1 sel0` |\n'
     '| `xt` | `bias_tree_noab_pd` (`../bias_tree_noab_pd`) | four bias lines vbp vbn vbpc vbnc from one mirror tree fed by `iref`. `xg` + `xt` replace `xb` = `bias_sel_noab_pd` (2026-10-27 to 2026-10-28; before that `bias_sel_pd`, whose class-AB legs stayed unused here), device for device |'),
    ('| `s2d_mpdda_pd_sel.{sch,sym}` | CACE-only fixture: `s2d_mpdda_pd` + `bias_sel_noab_pd`, `vfbp` / `vfbn` as pins (loop gain) |',
     '| `s2d_mpdda_pd_sel.{sch,sym}` | CACE-only fixture: `s2d_mpdda_pd` + `bias_gen_pd` + `bias_tree_noab_pd` (until 2026-10-28 `bias_sel_noab_pd`), `vfbp` / `vfbn` as pins (loop gain) |')])
edit('bias_gen_pd/README.md', [
    ('For the floorplan in which the generator sits in the slot\'s main area and only the trees (`bias_tree_pd`) go into the\n'
     'pads; `bias_sel_pd` remains the version with the tree attached, for a generator inside the pad.',
     'Since 2026-10-28 both pads instantiate it next to their tree (`xg` + `xt` in place of `bias_sel_pd` /\n'
     '`bias_sel_noab_pd`, device for device); the same cell serves the floorplan in which the generator sits in the slot\'s\n'
     'main area and only the trees go into the pads. `bias_sel_pd` stays as the combined reference cell with its CACE suite.')])
edit('bias_sel_pd/README.md', [
    ('The s2d pad uses `bias_sel_noab_pd`, this block without the class-AB branches.\n',
     'The s2d pad uses `bias_sel_noab_pd`, this block without the class-AB branches.\n\n'
     '**Since 2026-10-28 the pads no longer instantiate this cell.** Each pad has `bias_gen_pd` (`xg`, this cell without\n'
     '`Xt`) and the tree (`xt`: `bias_tree_pd`, in the s2d pad `bias_tree_noab_pd`) side by side, joined by `iref`; the\n'
     'flattened netlists of both pads, both loop fixtures, all CACE templates and `slot` are unchanged by it. This cell and\n'
     'its CACE results stay as the characterization of that combination.\n')])
edit('bias_sel_noab_pd/README.md', [
    ('`bias_sel_pd`, whose vabp / vabn stayed unused there.\n',
     '`bias_sel_pd`, whose vabp / vabn stayed unused there. Since 2026-10-28 the pad has `bias_gen_pd` + `bias_tree_noab_pd`\n'
     'side by side instead (same devices); this cell is kept as the combined reference.\n')])
edit('bias_tree_pd/README.md', [
    ('This is the part that goes into a pad. Its reference comes either from the selector next to it (`bias_sel_pd`, the\n'
     'generator in the pad) or from the slot\'s main area (`bias_gen_pd`, optionally through `bias_dist_pd`).',
     'This is the part that goes into a pad. Its reference comes from `bias_gen_pd`: next to it in the pad (`xg` + `xt`\n'
     'since 2026-10-28; before, the two were one cell, `bias_sel_pd`) or in the slot\'s main area, optionally through\n'
     '`bias_dist_pd`.')])
edit('bias_tree_noab_pd/README.md', [
    ('Used by `bias_sel_noab_pd` (generator in the pad); with the generator in the slot\'s main area it takes `bias_gen_pd`\'s\n'
     'or `bias_dist_pd`\'s current like `bias_tree_pd`.',
     'Used by `sg13cmos5l_IOPadSingle2Diff` (`xt`, next to `xg` = `bias_gen_pd`, since 2026-10-28) and by\n'
     '`bias_sel_noab_pd`; with the generator in the slot\'s main area it takes `bias_gen_pd`\'s or `bias_dist_pd`\'s current\n'
     'like `bias_tree_pd`.')])
edit(D + '/verification/cace/sg13cmos5l_IOPadDiff2Single.yaml', [
    ('selectable bias bias_sel_pd, fail-safe enable', 'selectable bias bias_gen_pd + bias_tree_pd (one bias_sel_pd until 2026-10-28), fail-safe enable')])
edit(S + '/verification/cace/sg13cmos5l_IOPadSingle2Diff.yaml', [
    ('# s2d_input_buffer.md), selectable bias bias_sel_pd, fail-safe enable en_ctrl_3v3, IHP input\n',
     '# s2d_input_buffer.md), selectable bias bias_gen_pd + bias_tree_noab_pd (until 2026-10-28 one bias_sel_noab_pd,\n# before 2026-10-27 bias_sel_pd), fail-safe enable en_ctrl_3v3, IHP input\n')])
print('docs ok')
