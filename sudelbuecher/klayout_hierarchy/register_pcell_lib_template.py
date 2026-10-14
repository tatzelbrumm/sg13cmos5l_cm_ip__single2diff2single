# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""
Template: register a KLayout PCell library (own PyCells) so that interactive
`klayout -e` and batch scripts can place its cells.

Copy and rename, then replace the placeholders:
  MY_LIB        -> library name shown in the Library Selector
  MyCell        -> PCell name passed to register_pcell
  MyCellDecl    -> your PCellDeclarationHelper subclass (module imported below)

Interactive (after `source .designinit` in the container, from the repo root):
    klayout -e -rm register_pcell_lib.py <file.klay.gds>

Batch / scripts (klayout -b skips autorun, so this file must register itself):
    import runpy; runpy.run_path('register_pcell_lib.py')
"""

import pya


class MyPCellLib(pya.Library):
    def __init__(self):
        self.description = "MY_LIB: own PyCells"
        # replace MyCellDecl with your PCellDeclarationHelper subclass
        self.layout().register_pcell("MyCell", MyCellDecl())
        self.register("MY_LIB")


# Register once per KLayout session.
if pya.Library.library_by_name("MY_LIB", "sg13cmos5l") is None:
    MyPCellLib()


# Placing an instance from a script (example):
#   lib  = pya.Library.library_by_name("MY_LIB", "sg13cmos5l")
#   cell = ly.create_cell("MyCell", "MY_LIB", {"ng": 4})
