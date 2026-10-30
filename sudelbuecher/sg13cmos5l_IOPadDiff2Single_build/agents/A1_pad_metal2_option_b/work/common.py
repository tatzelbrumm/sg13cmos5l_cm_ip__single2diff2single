"""shared helpers for the m2 rework (loading with the PCell library registered)."""
import os, sys, runpy
sys.dont_write_bytecode = True
W = '/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/pcw'
os.environ['PDKPATH'] = W + '/pdk/ihp-sg13cmos5l'
PC = W + '/new/pcells'
if PC not in sys.path: sys.path.insert(0, PC)
_loaded = False
def load_lib():
    global _loaded
    if not _loaded:
        runpy.run_path(os.path.join(PC, 'load_clamp_pcells.py')); _loaded = True
import klayout.db as db
