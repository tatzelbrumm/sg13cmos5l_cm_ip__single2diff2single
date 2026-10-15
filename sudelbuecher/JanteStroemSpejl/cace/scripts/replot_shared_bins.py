# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# Re-plot CACE's collated histograms with ONE set of bin edges per parameter.
# CACE 2.11.0 calls ax.hist(..., bins="auto") once per condition set, so every
# histogram gets its own bin width ~ its own sigma, and all peaks come out the same
# height. Here all condition sets of a parameter share the same edges.
#
# Usage:  python3 cace/scripts/replot_shared_bins.py runs/RUN_<date>
# Writes: runs/RUN_<date>/parameters/<parameter>/<parameter>_shared_bins.svg

import sys, glob, os
import numpy as np
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

run = sys.argv[1]
for pdir in sorted(glob.glob(os.path.join(run, "parameters", "*"))):
    sets = []
    for cdir in sorted(glob.glob(os.path.join(pdir, "run_*"))):
        cond = yaml.safe_load(open(os.path.join(cdir, "run_0", "conditions.yaml")))
        files = glob.glob(os.path.join(cdir, "run_*", "*.data"))
        v = np.array([float(x) for f in files for x in open(f).read().split()])
        sets.append((cond, v))
    # label with the conditions that differ between the sets
    keys = [k for k in ("iref", "dvds") if len({str(c[k]) for c, _ in sets}) > 1]
    edges = np.histogram_bin_edges(np.concatenate([v for _, v in sets]), bins="auto")
    fig, ax = plt.subplots()
    for cond, v in sets:
        label = ", ".join(f"{k} = {cond[k]}" for k in keys)
        ax.hist(v, bins=edges, alpha=0.5,
                label=f"{label} (σ = {100 * v.std(ddof=1):.2f} %, n = {v.size})")
    name = os.path.basename(pdir)
    ax.set_title(f"{sets[0][0]['DUT_name']} {name}, common bin width {100 * (edges[1] - edges[0]):.3f} %")
    ax.set_xlabel("Relative current error")
    ax.set_ylabel("Count per bin")
    ax.legend(loc="upper left")
    out = os.path.join(pdir, f"{name}_shared_bins.svg")
    fig.savefig(out, bbox_inches="tight")
    print(out)
