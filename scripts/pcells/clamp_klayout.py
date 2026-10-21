# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Write clamp_engine output into a klayout.db / pya Layout (batch use, no PyCell framework)."""

try:
    import klayout.db as db
except ImportError:          # inside the KLayout application
    import pya as db

# (layer, purpose) -> GDS layer/datatype, from sg13cmos5l.lyp
GDS = {
    ('Activ', 'drawing'): (1, 0), ('GatPoly', 'drawing'): (5, 0), ('Cont', 'drawing'): (6, 0),
    ('Metal1', 'drawing'): (8, 0), ('Metal1', 'pin'): (8, 2), ('Metal1', 'text'): (8, 25),
    ('Metal2', 'drawing'): (10, 0), ('Metal2', 'pin'): (10, 2), ('Metal2', 'text'): (10, 25),
    ('pSD', 'drawing'): (14, 0), ('Via1', 'drawing'): (19, 0), ('SalBlock', 'drawing'): (28, 0),
    ('Via2', 'drawing'): (29, 0), ('Metal3', 'drawing'): (30, 0), ('NWell', 'drawing'): (31, 0),
    ('Substrate', 'drawing'): (40, 0), ('ThickGateOx', 'drawing'): (44, 0), ('HeatRes', 'drawing'): (52, 0),
    ('TEXT', 'drawing'): (63, 0), ('Recog', 'diode'): (99, 31), ('EXTBlock', 'drawing'): (111, 0),
    ('PolyRes', 'drawing'): (128, 0),
}
_HA = {'left': db.HAlign.HAlignLeft, 'center': db.HAlign.HAlignCenter, 'right': db.HAlign.HAlignRight}
_VA = {'bottom': db.VAlign.VAlignBottom, 'center': db.VAlign.VAlignCenter, 'top': db.VAlign.VAlignTop}


def layer_index(layout, key):
    l, d = GDS[key]
    return layout.layer(l, d)


def write_cell(layout, cell, shapes, texts):
    """Insert engine shapes/texts (nm) into cell. layout.dbu must be 0.001."""
    if abs(layout.dbu - 0.001) > 1e-12:
        raise ValueError('layout dbu must be 0.001')
    for lay, pur, kind, d in shapes:
        li = layer_index(layout, (lay, pur))
        if kind == 'box':
            cell.shapes(li).insert(db.Box(*d))
        else:
            cell.shapes(li).insert(db.Polygon([db.Point(x, y) for x, y in d]))
    for lay, pur, s, x, y, size, ha, va, orient in texts:
        li = layer_index(layout, (lay, pur))
        t = db.Text(s, db.Trans(int(orient[1:]) // 90, False, x, y))
        t.size = size
        if ha in _HA:
            t.halign = _HA[ha]
        if va in _VA:
            t.valign = _VA[va]
        cell.shapes(li).insert(t)
    return cell
