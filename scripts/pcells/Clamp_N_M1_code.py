########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# NMOS ESD clamp (pad -> iovss), M1 only, derived from Clamp_N: no Metal2/Metal3,
# no gate tie-off, gate length l, guard rings wrapped around the finger array.
#
########################################################################

__version__ = "$Revision: #1 $"

from .clamp_base_code import clamp_m1_base


class Clamp_N_M1(clamp_m1_base):
    FAMILY = 'N'
    DEF_NG = 8
