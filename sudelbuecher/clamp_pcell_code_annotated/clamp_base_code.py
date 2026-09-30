########################################################################
#
# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
#
# Base PyCell for the parametrized sg13cmos5l ESD clamps, written against the
# IHP pycell4klayout (cni) API in the style of the PDK's own *_base_code.py
# (compare sg13cmos5l_pycell_lib/ihp/rfmosfet_base_code.py).
#
########################################################################
#
# ANNOTATED COPY (2026-09-30) of scripts/pcells/clamp_base_code.py. The code is
# unchanged: its syntax tree is identical to the original's. Only comments were added.
#
# Line numbers of files not in this folder: scripts/pcells/ as of 2026-09-30.
# References to other people's code:
#   cni  = IHP-GmbH/pycell4klayout-api @ ad47f5f7, source/python/cni/
#   PDK  = IHP-GmbH/ihp-sg13cmos5l @ 597570ee, libs.tech/klayout/
#   sg13_tech.py, geometry.py, utility_functions.py are under PDK python/sg13cmos5l_pycell_lib/
#
# WHERE THIS FILE SITS
#   This is the only file where the geometry engine (clamp_engine.py: plain integers,
#   no imports) meets IHP's PyCell framework (cni) and KLayout. The batch tools
#   (gen_clamp.py, verify_clamp.py) bypass this file and hand the same engine output to
#   clamp_klayout.write_cell() instead.
#
#   Nobody calls this class by name. __init__.py makes one object of each subclass
#   (Clamp_N_code.py, Clamp_P_code.py) and hands it to cni PCellWrapper (dlo.py:149),
#   which is the object KLayout actually talks to. PCellWrapper then calls the three
#   methods below: defineParamSpecs once, setupParams + genLayout per drawn variant.
#
########################################################################

__version__ = "$Revision: #1 $"     # PDK file convention; read by nothing

# --- names from cni -------------------------------------------------------------------
# cni/dlo.py itself star-imports cni.layer, cni.box, cni.point, cni.pointlist, cni.font,
# cni.dlogen, ... (dlo.py:21-46), so this one line brings in, of the names used below:
#   DloGen            dlogen.py:165     base class of clamp_base
#   ChoiceConstraint  dlo.py:62         turned into a KLayout drop-down by PCellWrapper.__call__
#   Layer             layer.py:19       layer name -> layout layer index (see genLayout)
#   Box, Point        box.py:29, point.py:23      thin wrappers of pya.DBox / pya.DPoint (um)
#   PointList         pointlist.py:24   list of Point with compress()
#   Font              font.py:22        only Font.EURO_STYLE, which dbCreateLabel ignores
from cni.dlo import *
# --- names from the PDK's own PyCell helpers --------------------------------------------
# geometry.py re-exports cni.dlo as well (geometry.py:21). Used from it:
#   dbReplaceProp  :1051    dbCreateRect :283    dbCreatePolygon :293    dbCreateLabel :365
# These are IHP's Cadence-SKILL-named wrappers around the cni shape classes.
from sg13cmos5l_pycell_lib.ihp.geometry import *
# Nothing from utility_functions.py is used in this file. geometry.py imports it itself
# (geometry.py:26) for strToAlignt/strToOrient, which dbCreateLabel needs. Copied PDK style.
from sg13cmos5l_pycell_lib.ihp.utility_functions import *

# --- names from this directory ----------------------------------------------------------
# FAMILY here is the engine's per-family rule dictionary clamp_engine.FAMILY.
# Not the same thing as the class attribute FAMILY below (the letter 'N' or 'P'),
# which is used as the key into it.
from .clamp_engine import FAMILY, generate, cell_name, ClampError
# REFDATA is only passed through to the engine; this file never looks inside it.
from .clamp_refdata import REFDATA

# Keys: the (halign, valign) pairs that occur in engine text tuples, both the computed
# ones (clamp_engine.rule_texts) and the stored ones (REFDATA tie_texts / decor_texts).
# Values: the spellings strToAlignt (utility_functions.py:333) recognises.
# Upper-left is missing because IHP's function spells it 'uperLeft' (utility_functions.py:340).
# Pairs not listed here, including (None, None) from REFDATA, fall back to 'lowerLeft' below.
_ALIGN = {
    ('center', 'center'): 'centerCenter', ('left', 'center'): 'centerLeft', ('right', 'center'): 'centerRight',
    ('center', 'bottom'): 'lowerCenter', ('left', 'bottom'): 'lowerLeft', ('right', 'bottom'): 'lowerRight',
    ('center', 'top'): 'upperCenter', ('right', 'top'): 'upperRight',
}


# The unit boundary: engine and REFDATA are integer nm; the cni shape classes wrap
# KLayout's floating-point D-types in um (box.py:32 pya.DBox, point.py:25 pya.DPoint).
# KLayout rounds back to the layout's database unit when the shape is inserted.
# IN:    v      number, nm
# OUT:   float, um
# CALLS: none
def _um(v):
    return v / 1000.0


# DloGen (dlogen.py:165) contributes no clamp behaviour, only bookkeeping that cni uses:
#   self.props         dlogen.py:172   dict written by dbReplaceProp; read by nothing
#   self.tech          dlogen.py:171   set by PCellWrapper through setTech (dlogen.py:209)
#   addCellContext()   dlogen.py:158   called by PCellWrapper.produce before setupParams
#   addShape()         dlogen.py:147   called by every cni Shape when it is created (shape.py:44-45)
# One object per subclass exists for the whole KLayout session (made in __init__.py,
# kept by PCellWrapper at dlo.py:169); it draws every variant of that PCell in turn.
class clamp_base(DloGen):
    """Common implementation; subclasses set FAMILY ('N' or 'P') and DEF_NG."""

    # Overridden in Clamp_N_code.py / Clamp_P_code.py. FAMILY selects both the engine's
    # rule set FAMILY[...] and the REFDATA branch REFDATA[...]; DEF_NG is the ng default.
    FAMILY = None
    DEF_NG = 8

    # Called once per PCell, by PCellWrapper.__init__ (dlo.py:185) at library registration,
    # before any object method runs; hence a classmethod (gets the class, not the object).
    # `specs` is that PCellWrapper; `specs(...)` runs PCellWrapper.__call__ (dlo.py:190).
    # There the Python type of the default value fixes the KLayout parameter type
    # (int -> TypeInt, str -> TypeString) and a ChoiceConstraint becomes add_choice entries.
    # The order of the specs() calls is the order KLayout stores parameters in, and the
    # order params_as_hash (dlo.py:266) uses to turn them back into names.
    # IN:    cls    the class Clamp_N or Clamp_P
    #        specs  the cni PCellWrapper being built (dlo.py:149)
    # OUT:   None; side effect: five pya.PCellParameterDeclaration objects stored in the wrapper
    # CALLS: specs.tech.getTechParams     PDK sg13_tech.py:95
    #        specs(...) x5                cni PCellWrapper.__call__, dlo.py:190
    #        ChoiceConstraint x2          cni dlo.py:62
    @classmethod
    def defineParamSpecs(cls, specs):
        # specs.tech was set at dlo.py:176, just before this call. getTechParams
        # (sg13_tech.py:95) returns the "techParams" block of sg13cmos5l_tech.json,
        # read when the SG13_dev technology was created (sg13_tech.py:41).
        techparams = specs.tech.getTechParams()
        f = FAMILY[cls.FAMILY]

        # cdf_version, Display, model: stored with every instance, read by nothing
        # (not here, not in the PDK PyCells, not in cni). Cadence CDF heritage.
        specs('cdf_version', techparams['CDFVersion'], 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', f['model'], 'Model name')
        # ng and tie: the only parameters that reach the geometry (setupParams).
        specs('ng', cls.DEF_NG, 'Number of gate fingers')
        specs('tie', 'D', "Gate: D = 'gate' pin + antenna diode, 0D = tied off via rppd",
              ChoiceConstraint(['D', '0D']))

    # Called by PCellWrapper.produce (dlo.py:282) every time KLayout (re)draws a variant.
    # params: {name: value} from params_as_hash (dlo.py:266), names as declared above.
    # IN:    self   the Clamp_N / Clamp_P object
    #        params dict {parameter name: value} from PCellWrapper.params_as_hash (dlo.py:266)
    # OUT:   None; sets self.ng (int) and self.tie (str)
    # CALLS: int (built-in)
    def setupParams(self, params):
        self.ng = int(params['ng'])
        self.tie = params['tie']

    # Called by PCellWrapper.produce (dlo.py:283) right after setupParams, inside
    # `with PyCellContext(tech, cell, impl)` (dlo.py:280). That context object is how the
    # cni constructors used below find their target without being told: the KLayout cell
    # (shape.py:33), the layout and the technology (layer.py:27-30).
    # Any exception ends up at dlo.py:284-285: printed in red on the console, cell left empty.
    # IN:    self   the Clamp_N / Clamp_P object; reads self.FAMILY, self.ng, self.tie and the module-level REFDATA
    # OUT:   None; side effects: shapes and texts in the KLayout cell of the current cni PyCellContext,
    #               seven entries in self.props (never read)
    # CALLS: generate, cell_name                          clamp_engine.py
    #        dbReplaceProp x7                             PDK geometry.py:1051
    #        Layer                                        cni layer.py:24
    #        dbCreateRect, Box                            PDK geometry.py:283, cni box.py:31
    #        dbCreatePolygon, PointList, Point            PDK geometry.py:293, cni pointlist.py:26, point.py:24
    #        dbCreateLabel, Point                         PDK geometry.py:365
    #        _um, _ALIGN.get                              this file
    #        Exception (raised when the engine raises ClampError)
    def genLayout(self):
        # The engine returns plain tuples, format in the clamp_engine.py header. The
        # batch path (clamp_klayout.write_cell) consumes the very same tuples; from here
        # on the PCell path and the batch path write them into KLayout differently.
        try:
            shapes, texts, plan = generate(self.FAMILY, self.ng, self.tie, REFDATA)
        except ClampError as e:
            raise Exception('%s: %s' % (self.__class__.__name__, e))

        # All seven go into DloGen.props (geometry.py:1051-1052) and are never read:
        # no effect on shapes, cell name or netlist. The KLayout cell name is chosen by
        # KLayout (Clamp_N, Clamp_N$1, ...), not by 'cellName'.
        dbReplaceProp(self, 'ivCellType', 'graphic')
        dbReplaceProp(self, 'viewSubType', 'maskLayoutParamCell')
        dbReplaceProp(self, 'instNamePrefix', 'X')
        dbReplaceProp(self, 'function', 'esd')
        dbReplaceProp(self, 'pcellVersion', '$Revision: 1.0 $')
        dbReplaceProp(self, 'pin#', 3 if (self.tie == 'D' or self.FAMILY == 'P') else 2)
        dbReplaceProp(self, 'cellName', cell_name(self.FAMILY, self.ng, self.tie))

        # Layer(name, purpose) (layer.py:24): looks up 'name.purpose' in
        # SG13_Tech.stream_layers() (sg13_tech.py:98). That table is built from the
        # <name>/<source> entries of PDK tech/sg13cmos5l.lyp (sg13_tech.py:49-75), falling
        # back to "Layers" in sg13cmos5l_tech.json only if the .lyp is missing. The result
        # is the layout's layer index for that GDS layer/datatype (created if absent).
        # The same name -> GDS job is done by two other tables in this directory:
        # clamp_klayout.py GDS (batch path) and its inverse extract_clamp_refdata.py LAYERS.
        # A layer/purpose name used by the engine or REFDATA must exist in all three.
        layers = {}
        for lay, pur, kind, d in shapes:
            key = (lay, pur)
            if key not in layers:
                layers[key] = Layer(lay, pur)
            if kind == 'box':
                # geometry.py:283 -> cni Rect (rect.py:28), whose Shape base (shape.py:35)
                # registers it via DloGen.addShape and which inserts a pya.DBox into the
                # PyCellContext cell (rect.py:35).
                dbCreateRect(self, layers[key], Box(_um(d[0]), _um(d[1]), _um(d[2]), _um(d[3])))
            else:
                # geometry.py:293 -> PointList.compress() (pointlist.py:29) removes coincident
                # and collinear points -> cni Polygon (polygon.py:35) -> pya.DSimplePolygon.
                # REFDATA rings arrive here as single polygons with a cut line.
                dbCreatePolygon(self, layers[key], PointList([Point(_um(x), _um(y)) for x, y in d]))

        for lay, pur, s, x, y, size, ha, va, orient in texts:
            key = (lay, pur)
            if key not in layers:
                layers[key] = Layer(lay, pur)
            # geometry.py:365 -> cni Text (text.py:30, a pya.DText of height `size`), then
            # setAlignment(strToAlignt(...)) and setOrientation(strToOrient(...))
            # (utility_functions.py:333 / :305). The font argument is dropped: the code that
            # would use it is commented out in geometry.py.
            dbCreateLabel(self, layers[key], Point(_um(x), _um(y)), s,
                          _ALIGN.get((ha, va), 'lowerLeft'), orient, Font.EURO_STYLE, _um(size))
