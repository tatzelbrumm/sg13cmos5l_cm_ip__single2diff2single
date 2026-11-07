# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Claude, agent F (C4): F's changed copies of the rows -> <cells dir>/rb_f_cells.gds / .cdl.
    python3 build_f_cells.py <inputs dir> <cells dir>
bypass_rb_f: agent N's own generator (inputs/N/build_rb_n.py, unchanged, its --bypass option) with 2 rows x 6
columns instead of 3 x 4: the same 12 capacitors (4 x CBM on vcm, 8 x CBR on vref, 12u x 12u hv NMOS, S = D = B =
vss), the same unit, gate columns, facing column pairs, ring and buses; only the array shape changes, so the array
is as wide as rb_casc and 12.9 um lower. Cell renamed bypass_rb_4_8_2x6 -> bypass_rb_f."""
import os
import subprocess
import sys

import klayout.db as db

I, C = sys.argv[1], sys.argv[2]
tmp = os.path.join(C, 'bypass_tmp')
os.makedirs(tmp, exist_ok=True)
env = dict(os.environ, PDK_ROOT=os.environ.get('PDK_ROOT', '/foss/pdks'), PDK='ihp-sg13cmos5l')
out = subprocess.run([sys.executable, '-I', os.path.join(I, 'N', 'build_rb_n.py'), '--bypass', '4', '8', '2', '6'],
                     cwd=tmp, env=env, capture_output=True, text=True)
print(out.stdout)
stem = os.path.join(tmp, 'bypass_rb_4_8_2x6')
ly = db.Layout()
ly.read(stem + '.gds')
ly.cell('bypass_rb_4_8_2x6').name = 'bypass_rb_f'
opt = db.SaveLayoutOptions()
opt.gds2_write_timestamps = False
ly.write(os.path.join(C, 'rb_f_cells.gds'), opt)
cdl = open(stem + '.cdl').read().replace('bypass_rb_4_8_2x6', 'bypass_rb_f')
cdl = cdl.replace('* One line', '* F (Claude, agent F, C4): cell renamed bypass_rb_f by build_f_cells.py.\n* One line')
open(os.path.join(C, 'rb_f_cells.cdl'), 'w').write(cdl)
print('bypass_rb_f', ly.cell('bypass_rb_f').dbbox())
