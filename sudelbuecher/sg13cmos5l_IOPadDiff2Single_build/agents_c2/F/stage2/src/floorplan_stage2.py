"""Variant 1 as of stage 2 (measured sizes of F's cells; P / N still at their requested maxima).
Usage: python3 floorplan_stage2.py <out.png>"""
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.insert(0, "/home/user/c2/F/work")
import floorplan_stage1 as F

V1s2 = [
    ("casc_p (P)", 2.5, 88.6, 15.0, 122.6, "P"),
    ("loads (P)", 2.5, 123.2, 17.7, 156.2, "P"),
    ("d2s_rhigh\n13.92x15.41", 15.6, 88.6, 29.52, 104.01, "R"),
    ("sa/sb channel (M1)", 15.6, 104.2, 53.5, 108.0, "S"),
    ("ab_n", 30.1, 88.6, 37.6, 98.1, "N"),
    ("ab_p", 38.4, 88.6, 46.2, 98.1, "P"),
    ("pd_p", 47.0, 88.6, 51.0, 91.6, "P"),
    ("pd_n", 51.7, 88.6, 55.2, 91.1, "N"),
    ("CMB reserve\n(next to b join)", 47.0, 92.2, 66.0, 103.9, "S"),
    ("", 54.1, 104.5, 66.0, 123.0, "S"),
    ("tails (BP)", 19.5, 108.2, 53.5, 123.2, "P"),
    ("d2s_inputs", 19.5, 125.0, 53.5, 152.0, "T"),
    ("casc_n", 66.5, 88.6, 77.5, 122.6, "N"),
    ("sinks_6x6\nupright", 59.5, 123.5, 77.5, 177.0, "N"),
    ("bias_tree_pd 52.36 x 11.82 (library cells, wired)", 2.6, 157.0, 54.96, 168.82, "B"),
    ("spare", 2.5, 169.4, 59.0, 177.5, "S"),
]
F.check("V1 stage 2", V1s2)
fig, ax = plt.subplots(figsize=(7.5, 9.5))
F.draw(ax, "Variant 1, stage 2: F's cells at measured size", V1s2,
       [("iref", 24.2), ("en_3v3", 25.9), ("en_3v3_b", 26.7), ("vinp", 56.0), ("vref", 57.5), ("vinn", 59.0)], [])
fig.tight_layout()
fig.savefig(sys.argv[1], dpi=150)
