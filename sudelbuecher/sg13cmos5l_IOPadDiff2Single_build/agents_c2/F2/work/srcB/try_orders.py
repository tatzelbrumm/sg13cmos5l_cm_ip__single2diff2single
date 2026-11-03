import sys, os, itertools
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/sudel/sudelbuecher/design_considerations/pad_buffer_layout/oa_core_pd_v2_2026-10-28/v2")
import generator as G
SA = ["sa_A", "sa_B", "sa_C1", "sa_C2", "sb_A", "sb_B", "sb_C1", "sb_C2"]
LONG = ["vabp", "vabn", "vbpc", "vbnc", "vbn", "en_3v3", "en_3v3_b"]
REST = ["x", "y", "l1", "l2", "pl", "pr", "a", "b", "dabp", "dabn", "ni", "iref", "vinp", "vinn", "vref", "vfb"]
orders = {"A": ["vabp", "vabn", "en_3v3", "en_3v3_b", "sb_C2", "sb_C1", "sb_B", "sb_A", "sa_C2", "sa_C1", "sa_B", "sa_A", "vbpc", "vbnc", "vbn"] + REST,
          "B": SA + LONG + REST, "C": ["sb_C2", "sb_C1", "sb_B", "sb_A"] + LONG + ["sa_A", "sa_B", "sa_C1", "sa_C2"] + REST,
          "E": ["dabp", "dabn", "sb_C2", "sb_C1", "sb_B", "sb_A"] + LONG + ["sa_A", "sa_B", "sa_C1", "sa_C2"] + REST,
          "F": ["dabp", "dabn", "vabp", "vabn", "en_3v3", "en_3v3_b", "sb_C2", "sb_C1", "sb_B", "sb_A", "sa_C2", "sa_C1", "sa_B", "sa_A", "vbpc", "vbnc", "vbn"] + REST,
          "D": ["en_3v3", "en_3v3_b", "vabp", "vabn"] + SA[::-1] + ["vbpc", "vbnc", "vbn"] + REST}
for k in sys.argv[2:]:
    cfg = G.load_config(sys.argv[1])
    cfg["ROUTE_ORDER"] = orders[k]
    blk, rep = G.build(cfg, None, log=lambda *a: None)
    print(k, [f[0] for f in blk.failed], flush=True)
