########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# Base PyCell for the parametrized sg13cmos5l ESD clamps, written against the
# IHP pycell4klayout (cni) API in the style of the PDK's own *_base_code.py
# (compare sg13cmos5l_pycell_lib/ihp/rfmosfet_base_code.py).
#
# clamp_base     -> Clamp_N, Clamp_P        (IHP cells, parameters ng, tie)
# clamp_m1_base  -> Clamp_N_M1, Clamp_P_M1  (M1 only, no tie block, parameters ng, l, frame)
# dcdiode_base   -> DCNDiode, DCPDiode       (IHP's DC diodes, parameter l = diode length)
#
########################################################################

__version__ = "$Revision: #1 $"

from cni.dlo import *
from sg13cmos5l_pycell_lib.ihp.geometry import *
from sg13cmos5l_pycell_lib.ihp.utility_functions import *

from .clamp_engine import FAMILY, generate, generate_m1, generate_diode, cell_name, ClampError
from .clamp_refdata import REFDATA

_ALIGN = {
    ('center', 'center'): 'centerCenter', ('left', 'center'): 'centerLeft', ('right', 'center'): 'centerRight',
    ('center', 'bottom'): 'lowerCenter', ('left', 'bottom'): 'lowerLeft', ('right', 'bottom'): 'lowerRight',
    ('center', 'top'): 'upperCenter', ('right', 'top'): 'upperRight',
}


def _um(v):
    return v / 1000.0


class clamp_base(DloGen):
    """Common implementation; subclasses set FAMILY ('N' or 'P') and DEF_NG."""

    FAMILY = None
    DEF_NG = 8

    @classmethod
    def defineParamSpecs(cls, specs):
        techparams = specs.tech.getTechParams()
        f = FAMILY[cls.FAMILY]

        specs('cdf_version', techparams['CDFVersion'], 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', f['model'], 'Model name')
        specs('ng', cls.DEF_NG, 'Number of gate fingers')
        specs('tie', 'D', "Gate: D = 'gate' pin + antenna diode, 0D = tied off via rppd",
              ChoiceConstraint(['D', '0D']))

    def setupParams(self, params):
        self.ng = int(params['ng'])
        self.tie = params['tie']

    def genLayout(self):
        try:
            shapes, texts, plan = generate(self.FAMILY, self.ng, self.tie, REFDATA)
        except ClampError as e:
            raise Exception('%s: %s' % (self.__class__.__name__, e))

        dbReplaceProp(self, 'ivCellType', 'graphic')
        dbReplaceProp(self, 'viewSubType', 'maskLayoutParamCell')
        dbReplaceProp(self, 'instNamePrefix', 'X')
        dbReplaceProp(self, 'function', 'esd')
        dbReplaceProp(self, 'pcellVersion', '$Revision: 1.0 $')
        dbReplaceProp(self, 'pin#', 3 if (self.tie == 'D' or self.FAMILY == 'P') else 2)
        dbReplaceProp(self, 'cellName', cell_name(self.FAMILY, self.ng, self.tie))
        self.draw(shapes, texts)

    def draw(self, shapes, texts):
        """Engine shapes/texts (nm) -> cni shapes (um)."""
        layers = {}
        for lay, pur, kind, d in shapes:
            key = (lay, pur)
            if key not in layers:
                layers[key] = Layer(lay, pur)
            if kind == 'box':
                dbCreateRect(self, layers[key], Box(_um(d[0]), _um(d[1]), _um(d[2]), _um(d[3])))
            else:
                dbCreatePolygon(self, layers[key], PointList([Point(_um(x), _um(y)) for x, y in d]))

        for lay, pur, s, x, y, size, ha, va, orient in texts:
            key = (lay, pur)
            if key not in layers:
                layers[key] = Layer(lay, pur)
            dbCreateLabel(self, layers[key], Point(_um(x), _um(y)), s,
                          _ALIGN.get((ha, va), 'lowerLeft'), orient, Font.EURO_STYLE, _um(size))


class clamp_m1_base(clamp_base):
    """M1-only clamp: no Metal2/Metal3, no gate tie-off, gate length l."""

    MIN_L = {'N': 'nmosHV_minL', 'P': 'pmosHV_minL'}

    @classmethod
    def defineParamSpecs(cls, specs):
        techparams = specs.tech.getTechParams()
        f = FAMILY[cls.FAMILY]

        specs('cdf_version', techparams['CDFVersion'], 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', f['model'], 'Model name')
        specs('ng', cls.DEF_NG, 'Number of gate fingers')
        specs('l', '0.6u', 'Gate length')
        specs('frame', 'fit', "Guard rings: fit = wrap the array, 80u = IHP's fixed 80 um frame, array centred",
              ChoiceConstraint(['fit', '80u']))
        specs('Lmin', techparams[cls.MIN_L[cls.FAMILY]], 'Lmin')

    def setupParams(self, params):
        self.ng = int(params['ng'])
        self.l = int(round(Numeric(params['l']) * 1e9))        # nm
        self.lmin = int(round(Numeric(params['Lmin']) * 1e9))
        self.frame = params['frame']

    def genLayout(self):
        try:
            if self.l < self.lmin:
                raise ClampError('l = %d nm < Lmin = %d nm' % (self.l, self.lmin))
            shapes, texts = generate_m1(self.FAMILY, self.ng, self.l, 80000 if self.frame == '80u' else None)
        except ClampError as e:
            raise Exception('%s: %s' % (self.__class__.__name__, e))

        dbReplaceProp(self, 'ivCellType', 'graphic')
        dbReplaceProp(self, 'viewSubType', 'maskLayoutParamCell')
        dbReplaceProp(self, 'instNamePrefix', 'X')
        dbReplaceProp(self, 'function', 'esd')
        dbReplaceProp(self, 'pcellVersion', '$Revision: 1.0 $')
        dbReplaceProp(self, 'pin#', 3 if self.FAMILY == 'N' else 4)   # gate pad iovss [iovdd]
        dbReplaceProp(self, 'cellName', self.__class__.__name__)
        self.draw(shapes, texts)


class dcdiode_base(clamp_base):
    """DC diode pair with tap frame and guard ring; subclasses set FAMILY ('N' or 'P')."""

    MODEL = {'N': 'dantenna', 'P': 'dpantenna'}

    @classmethod
    def defineParamSpecs(cls, specs):
        techparams = specs.tech.getTechParams()

        specs('cdf_version', techparams['CDFVersion'], 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', cls.MODEL[cls.FAMILY], 'Model name')
        specs('l', '27.78u', 'Diode length (stripe length in x; w = 1.26u fixed)')

    def setupParams(self, params):
        self.l = int(round(Numeric(params['l']) * 1e9))        # nm

    def genLayout(self):
        try:
            shapes, texts = generate_diode(self.FAMILY, self.l)
        except ClampError as e:
            raise Exception('%s: %s' % (self.__class__.__name__, e))

        dbReplaceProp(self, 'ivCellType', 'graphic')
        dbReplaceProp(self, 'viewSubType', 'maskLayoutParamCell')
        dbReplaceProp(self, 'instNamePrefix', 'X')
        dbReplaceProp(self, 'function', 'esd')
        dbReplaceProp(self, 'pcellVersion', '$Revision: 1.0 $')
        dbReplaceProp(self, 'pin#', 3)                               # anode cathode guard
        dbReplaceProp(self, 'cellName', self.__class__.__name__)
        self.draw(shapes, texts)
