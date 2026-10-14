########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# IHP sg13cmos5l_DCPDiode with the diode length l as parameter: p+ stripes
# (anode) in an NWell with an n+ frame (cathode), p+ substrate-tap guard ring
# (guard).
# l = 27.78u reproduces IHP's cell.
#
########################################################################

__version__ = "$Revision: #1 $"

from .clamp_base_code import dcdiode_base


class DCPDiode(dcdiode_base):
    FAMILY = 'P'
