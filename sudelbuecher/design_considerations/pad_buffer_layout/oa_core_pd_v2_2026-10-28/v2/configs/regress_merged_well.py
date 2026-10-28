# Test C for generator.py: old primitives + oa_pcas_c (no ring, NWell to the edge) in a slicing floorplan with
# auto gaps, one merged vdd NWell, tie stripes under both rails. Must give DRC 0 / LVS MATCH vs out/oa_core_pd.cdl.
import sys

A = "/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent"
sys.path.insert(0, A + "/out/v2")
import drc as _drc

NAME = "oa_core_pd"
PROCESS = A + "/out/v2/process/ihp_sg13cmos5l.py"
SOURCES = {"lib": A + "/inputs/pad_buffer_cells.gds", "pcas_c": A + "/out/v2/oa_pcas_c.gds"}
INSTANCES = {
    "pmir": dict(cell="oa_pmir", o="M0"), "pcas": dict(cell="oa_pcas_c", o="M0"),
    "misc_p": dict(cell="oa_misc_p", o="R180"), "nmir": dict(cell="oa_nmir", o="R0"),
    "misc_n": dict(cell="oa_misc_n", o="R0"), "mcs": dict(cell="oa_mcs", o="R0"),
}
FLOORPLAN = """
V gap=-1.34,auto,-0.72
  rail vdd h=1.50 tap=n
  H align=top gap=auto
    cell pmir
    V align=left gap=auto
      H align=top gap=auto
        V align=left gap=0
          space h=1.90
          cell pcas
        cell misc_p
      H align=top gap=auto
        cell nmir
        cell misc_n
  cell mcs
  rail vss h=1.42 tap=p
"""
NETS = ["vdd", "vss", "iout", "en_3v3", "en_3v3_b", "vpg", "vpc", "vnc", "vbr", "ks", "d10", "vres", "co", "c8",
        "c2"]
PORTS = {"iout": ("top", None), "en_3v3": ("top", None), "en_3v3_b": ("right", None)}
PIN_OVERRIDES = {"oa_nmir": [("M1", "vnc", (15.0, 10.50, 15.3, 10.70)), ("M1", "d10", (31.05, 4.75, 31.29, 5.25)),
                             ("M2", "d10", (29.0, 0.38, 29.5, 0.62)), ("M2", "vres", (27.0, -4.14, 27.6, -3.90)),
                             ("M1", "vss", (30.0, -1.70, 30.5, -1.12))]}
MERGE_WELLS = True
DRC = lambda ly, cell: [(r[0], r[3]) for r in _drc.run(ly, cell)]
