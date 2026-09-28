########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# Parametrized NMOS ESD clamp (pad -> iovss), family of sg13cmos5l_io
# sg13cmos5l_Clamp_N<ng>N<ng>D / sg13cmos5l_Clamp_N<ng>N0D.
# Reproduces N2N2D, N8N8D, N15N15D and N20N0D exactly; other ng interpolated.
#
########################################################################

__version__ = "$Revision: #1 $"

from .clamp_base_code import clamp_base


class Clamp_N(clamp_base):
    FAMILY = 'N'
    DEF_NG = 8
