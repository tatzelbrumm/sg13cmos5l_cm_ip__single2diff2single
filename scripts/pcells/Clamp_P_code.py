########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# Parametrized PMOS ESD clamp (pad -> iovdd, two stacked device rows), family of
# sg13cmos5l_io sg13cmos5l_Clamp_P<ng>N<ng>D / sg13cmos5l_Clamp_P<ng>N0D.
# Reproduces P2N2D, P8N8D, P15N15D and P20N0D exactly; other ng interpolated.
#
########################################################################

__version__ = "$Revision: #1 $"

from .clamp_base_code import clamp_base


class Clamp_P(clamp_base):
    FAMILY = 'P'
    DEF_NG = 8
