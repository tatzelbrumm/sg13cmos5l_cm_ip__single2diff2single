########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# Metal1 wiring for Clamp_N_M1 with wiring = external (NMOS clamp (pad -> iovss)): gate bus segments over
# the output fingers, jumpers for diode-connected replicas and dummies, and the net names.
# Place it at the origin of the clamp, with the same ng, l and frame (2026-10-27).
#
########################################################################

__version__ = "$Revision: #1 $"

from .clamp_base_code import clamp_m1_wiring_base


class Clamp_N_M1_wiring(clamp_m1_wiring_base):
    FAMILY = 'N'
    DEF_NG = 8
