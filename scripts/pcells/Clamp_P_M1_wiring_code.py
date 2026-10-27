########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# Metal1 wiring for Clamp_P_M1 with wiring = external (PMOS clamp (pad -> iovdd)): gate bus segments over
# the output fingers, jumpers for diode-connected replicas and dummies, and the net names.
# Place it at the origin of the clamp, with the same ng, l and frame (2026-10-27).
#
########################################################################

__version__ = "$Revision: #1 $"

from .clamp_base_code import clamp_m1_wiring_base


class Clamp_P_M1_wiring(clamp_m1_wiring_base):
    FAMILY = 'P'
    DEF_NG = 8
