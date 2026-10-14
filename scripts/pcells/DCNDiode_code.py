########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# IHP sg13cmos5l_DCNDiode with the diode length l as parameter: n+ stripes in
# the p substrate (cathode), p+ substrate-tap frame (anode), n+ guard ring in an
# NWell ring (guard).
# l = 27.78u reproduces IHP's cell.
#
########################################################################

__version__ = "$Revision: #1 $"

from .clamp_base_code import dcdiode_base


class DCNDiode(dcdiode_base):
    FAMILY = 'N'
