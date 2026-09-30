########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# Parametrized NMOS ESD clamp (pad -> iovss), family of sg13cmos5l_io
# sg13cmos5l_Clamp_N<ng>N<ng>D / sg13cmos5l_Clamp_N<ng>N0D.
# Reproduces N2N2D, N8N8D, N15N15D and N20N0D exactly; other ng interpolated.
#
#
# ANNOTATED COPY (2026-09-30) of scripts/pcells/Clamp_N_code.py. The code is unchanged: its syntax
# tree is identical to the original's. Only comments were added.
#
# WHERE THIS FILE SITS
#   __init__.py lists 'Clamp_N_code' in moduleNames, imports this file as a submodule of the
#   package that load_clamp_pcells.py builds (hence the relative import below), strips
#   '_code' from the module name to get the class name, and registers
#   PCellWrapper(Clamp_N(), SG13_dev, ...) under the PCell name 'Clamp_N'. So the class name must
#   equal the file name minus '_code', and it is also the PCell name KLayout shows.
#   All code that runs for Clamp_N is in clamp_base_code.py; this file only sets two values.
#
########################################################################

__version__ = "$Revision: #1 $"     # PDK file convention; read by nothing

# clamp_base (clamp_base_code.py) holds the three methods cni PCellWrapper calls:
# defineParamSpecs, setupParams, genLayout.
from .clamp_base_code import clamp_base


class Clamp_N(clamp_base):
    # Key into clamp_engine.FAMILY (per-family rules) and into REFDATA (IHP geometry
    # of the sg13cmos5l_Clamp_N* reference cells in clamp_refdata.py). Read wherever clamp_base_code.py
    # says cls.FAMILY / self.FAMILY.
    FAMILY = 'N'
    # Default of the PCell parameter 'ng' (clamp_base_code.py, defineParamSpecs).
    DEF_NG = 8
