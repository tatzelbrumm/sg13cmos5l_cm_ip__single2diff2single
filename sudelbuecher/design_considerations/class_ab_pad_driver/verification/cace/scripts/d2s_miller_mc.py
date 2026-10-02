# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""CACE post-processing for mm_params / mc_params of d2s_miller: collects the per-iteration
results into arrays for the histograms. Values are rescaled for the plot axes
(Vos_out in mV, IqP in uA, Gain in V/V).
Do not print from this hook: CACE 2.11 redirects stdout into its logger while the script
runs, and a print recurses without end (same note as in the inverter example)."""
from typing import Any


def postprocess(results: dict[str, list], conditions: dict[str, Any]) -> dict[str, list]:
    return {'Vos_out_arr': [float(v) * 1e3 for v in results['Vos_out']],
            'Gain_arr': [float(v) for v in results['Gain']],
            'IqP_arr': [float(v) * 1e6 for v in results['IqP']]}
