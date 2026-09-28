########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# KLayout library "SG13_cm_clamps" with the parametrized ESD clamps Clamp_N /
# Clamp_P, registered the same way sg13cmos5l_pycell_lib registers "SG13_dev":
# every <name>_code.py module in moduleNames provides class <name>, wrapped in
# cni.dlo.PCellWrapper against the SG13_dev technology.
#
# The IHP PDK library must be importable (KLAYOUT_PATH set by the PDK); it is
# imported first because it creates the SG13_dev technology.
#
########################################################################

import importlib

import pya

import sg13cmos5l_pycell_lib                      # noqa: F401  (creates SG13_dev)
from cni.tech import Tech
from cni.dlo import PCellWrapper

LIB_NAME = 'SG13_cm_clamps'

moduleNames = [
    'Clamp_N_code',   # NMOS clamp pad -> iovss
    'Clamp_P_code',   # PMOS clamp pad -> iovdd
]


class ClampPyCellLib(pya.Library):
    def __init__(self):
        self.description = 'sg13cmos5l ESD clamps (parametrized from sg13cmos5l_io)'
        # Deliberately NOT restricted to technology sg13cmos5l (unlike SG13_dev): GDS does not
        # store a layout's technology, so a restricted library cannot re-attach to its PCell
        # instances when a saved layout is read back. The PCells take all rules from the
        # SG13_dev Tech object, not from the layout's technology.
        tech = Tech.get('SG13_dev')
        for moduleName in moduleNames:
            module = importlib.import_module('%s.%s' % (__name__, moduleName))
            name = moduleName[:-len('_code')]
            path = module.__file__
            self.layout().register_pcell(name, PCellWrapper(getattr(module, name)(), tech, None, path))
        self.register(LIB_NAME)


ClampPyCellLib()
