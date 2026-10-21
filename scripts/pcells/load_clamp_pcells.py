# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Register the KLayout library 'SG13_cm_clamps' (PCells Clamp_N, Clamp_P).

GUI, inside the IIC-OSIC-TOOLS container with the PDK sourced:
    klayout -e -rm scripts/pcells/load_clamp_pcells.py  <file.gds>
Batch / other scripts:
    import runpy; runpy.run_path('scripts/pcells/load_clamp_pcells.py')

In the GUI the PDK's own autorun macro has already put the IHP PyCell library on
sys.path. 'klayout -b' skips autorun macros, so if the PDK library or its 'cni' API is
not yet importable this loader adds the same two directories the PDK's
libs.tech/klayout/tech/pymacros/autorun.lym adds, found via $KLAYOUT_PATH or $PDKPATH.
"""

import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
PACKAGE = 'sg13cmos5l_cm_clamps'


def _pdk_python_dirs():
    roots = []
    for p in os.environ.get('KLAYOUT_PATH', '').split(os.pathsep):
        if p:
            roots.append(p)
    if os.environ.get('PDKPATH'):
        roots.append(os.path.join(os.environ['PDKPATH'], 'libs.tech', 'klayout'))
    for r in roots:
        py = os.path.join(r, 'python')
        if os.path.isdir(os.path.join(py, 'sg13cmos5l_pycell_lib')):
            return [py, os.path.join(py, 'pycell4klayout-api', 'source', 'python')]
    return []


def _missing():
    return [m for m in ('sg13cmos5l_pycell_lib', 'cni') if importlib.util.find_spec(m) is None]


if _missing():
    for d in _pdk_python_dirs():
        if d not in sys.path:
            sys.path.append(d)
    if _missing():
        raise ImportError('%s not found: source the project .designinit (KLAYOUT_PATH / PDKPATH) first'
                          % ' and '.join(_missing()))

if PACKAGE not in sys.modules:
    _spec = importlib.util.spec_from_file_location(
        PACKAGE, os.path.join(_HERE, '__init__.py'), submodule_search_locations=[_HERE])
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules[PACKAGE] = _mod
    _spec.loader.exec_module(_mod)
