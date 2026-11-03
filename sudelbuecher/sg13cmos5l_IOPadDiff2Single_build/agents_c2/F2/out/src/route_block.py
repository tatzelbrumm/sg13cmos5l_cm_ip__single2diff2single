# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 stage B: place and route d2s_block with generator.py (oa_core_pd_v2_2026-10-28/v2, used unchanged).
    python3 route_block.py <block_cfg.py> <out.gds>"""
import sys
import time
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/sudel/sudelbuecher/design_considerations/pad_buffer_layout/oa_core_pd_v2_2026-10-28/v2")
import generator as G  # noqa: E402
t0 = time.time()
cfg = G.load_config(sys.argv[1])
blk, rep = G.build(cfg, sys.argv[2])
print("failed:", rep["failed"] if "failed" in rep else blk.failed, "time %.0f s" % (time.time() - t0))
