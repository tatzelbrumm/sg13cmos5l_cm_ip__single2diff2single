# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""C3 phase 1, budget: compacted area of the s2d blocks against the free core-side region of IOPadAnalog.

python3 budget.py            (run in this folder of the notes worktree; prints the markdown tables of report.md §1.3)

Estimate per block = library bbox (pad_buffer_cells.gds) x the compaction ratio C2's reviewed rebuild (P2 / N2)
measured on the d2s counterpart. Density = C2's achieved sum of cell bboxes / its free region (F2's d2s_block,
read from the C2 notes branch with git show).
"""
import subprocess, tempfile
import klayout.db as db

NOTES = '../../..'                                       # sudelbuecher/
LIB = '../klayout/pad_buffer_cells.gds'
P2 = NOTES + '/sg13cmos5l_IOPadDiff2Single_build/agents_c2/P2/out/d2s_p2_cells.gds'
N2 = NOTES + '/sg13cmos5l_IOPadDiff2Single_build/agents_c2/N2/out/d2s_n2_cells.gds'
C2REF = 'origin/claude/c2-pad-layout-sudel'
BLOCK = 'sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/F2/out/cells/d2s_block.gds'
IO = '/foss/pdks/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds'


def areas(path):
    ly = db.Layout()
    ly.read(path)
    return {c.name: c.dbbox().area() for c in ly.each_cell() if not c.dbbox().empty()}


lib, c2 = areas(LIB), {**areas(P2), **areas(N2)}
ratio = lambda new, old: c2[new] / lib[old]
# s2d block: (library cell, count, ratio source, ratio)
S2D = [('s2d_inputs', 1, 'd2s_inputs', ratio('d2s_inputs_c2', 'd2s_inputs')),
       ('s2d_tails', 1, 'd2s_tails', ratio('d2s_tails_c2', 'd2s_tails')),
       ('s2d_loads', 1, 'd2s_loads', ratio('d2s_loads_c2', 'd2s_loads')),
       ('s2d_casc_p', 1, 'd2s_casc_p', ratio('d2s_casc_p_c2', 'd2s_casc_p')),
       ('s2d_casc_n', 1, 'd2s_casc_n', ratio('d2s_casc_n_c2', 'd2s_casc_n')),
       ('sinks_6x6', 1, 'sinks_6x6_s2d_c2 itself', ratio('sinks_6x6_s2d_c2', 'sinks_6x6')),
       ('s2d_sinks_cmfb', 1, 'sinks_6x6', ratio('sinks_6x6_c2', 'sinks_6x6')),
       ('s2d_rhigh', 1, 'd2s_rhigh', ratio('d2s_rhigh_c2', 'd2s_rhigh')),
       ('s2d_pd_p', 2, 'd2s_pd_p', ratio('d2s_pd_p_c2', 'd2s_pd_p')),
       ('s2d_pd_n', 2, 'd2s_pd_n', ratio('d2s_pd_n_c2', 'd2s_pd_n')),
       ('s2d_cload', 1, 'none (gate area fixed)', 1.0)]
TREE = [('bias_tree_n', 1, 'bias_tree_n', ratio('bias_tree_n_c2', 'bias_tree_n')),
        ('bias_tree_p', 1, 'bias_tree_p', ratio('bias_tree_p_c2', 'bias_tree_p'))]

# C2's achieved density: sum of the placed cells' bboxes in F2's d2s_block / the block's free region
with tempfile.NamedTemporaryFile(suffix='.gds') as f:
    f.write(subprocess.run(['git', 'show', f'{C2REF}:{BLOCK}'], capture_output=True, check=True).stdout)
    f.flush()
    ly = db.Layout()
    ly.read(f.name)
blk = ly.cell('d2s_block')
placed = [i for i in blk.each_inst() if i.cell.name not in ('padtop_ctx_f2', 'pwr_f2')]
c2_cells = sum(i.dbbox().area() for i in placed)
C2_REGION = db.DBox(0.66, 85.74, 77.85, 180.0)          # F2's d2s_block in the C2 macro (above the NW isolator)
density = c2_cells / C2_REGION.area()

# C3's free region: C2's region minus IHP's SecondaryProtection (kept in place) with 1 µm around it
io = db.Layout()
io.read(IO)
sp = [i.dbbox() for i in io.cell('sg13cmos5l_IOPadAnalog').each_inst() if i.cell.name == 'sg13cmos5l_SecondaryProtection'][0]
free = C2_REGION.area() - sp.enlarged(1.0, 1.0).area()

print('| block | library µm² | ratio from (C2 P2 / N2) | ratio | estimate µm² |\n|---|---:|---|---:|---:|')
tot = {}
for group, rows in (('xa', S2D), ('xt', TREE)):
    s = 0.0
    for name, n, src, r in rows:
        est = n * lib[name] * r
        s += est
        print(f'| {name}{" × %d" % n if n > 1 else ""} | {n * lib[name]:.0f} | {src} | {r:.2f} | {est:.0f} |')
    tot[group] = s
    print(f'| **{group} total** | | | | **{s:.0f}** |')
cl = lib['s2d_cload']
print(f'\nC2 density: {c2_cells:.0f} µm² of cells in {C2_REGION.area():.0f} µm² = {density:.2f}')
print(f'SecondaryProtection {sp}; C3 free region {free:.0f} µm²')
for label, need in (('xa', tot['xa']), ('xa without cload', tot['xa'] - cl), ('xa + xt', tot['xa'] + tot['xt'])):
    print(f'| {label} | cells {need:.0f} µm² = {need / free:.0%} of the region | at C2 density {need / density:.0f} µm² '
          f'= {need / density / free:.2f} × the region | cells allowed at C2 density {free * density:.0f}, '
          f'to remove {need - free * density:.0f} |')
