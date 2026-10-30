import sys
A = "/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent"
sys.path.insert(0, A + "/out/v2")
import drc as _drc
NAME = "gaptest"
PROCESS = A + "/out/v2/process/ihp_sg13cmos5l.py"
SOURCES = {"lib": A + "/inputs/pad_buffer_cells.gds", "pcas_c": A + "/out/v2/oa_pcas_c.gds"}
INSTANCES = {"p": dict(cell="oa_pcas_c"), "n": dict(cell="oa_misc_n")}
FLOORPLAN = """
H gap=auto align=bottom
  cell p
  cell n
"""
NETS = []
DRC = lambda ly, cell: [(r[0], r[3]) for r in _drc.run(ly, cell)]
