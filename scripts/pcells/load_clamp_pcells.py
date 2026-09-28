# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Register the KLayout library 'SG13_cm_clamps' (PCells Clamp_N, Clamp_P).

GUI, inside the IIC-OSIC-TOOLS container with the PDK sourced:
    klayout -e -rm scripts/pcells/load_clamp_pcells.py  <file.gds>
Batch / other scripts:
    import runpy; runpy.run_path('scripts/pcells/load_clamp_pcells.py')
"""

import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
PACKAGE = 'sg13cmos5l_cm_clamps'

if PACKAGE not in sys.modules:
    _spec = importlib.util.spec_from_file_location(
        PACKAGE, os.path.join(_HERE, '__init__.py'), submodule_search_locations=[_HERE])
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules[PACKAGE] = _mod
    _spec.loader.exec_module(_mod)
