import sys, runpy
for m in [m for m in sys.modules if m.startswith('sg13cmos5l_cm_clamps')]:
    del sys.modules[m]
runpy.run_path('/foss/designs/sg13cmos5l_cm_ip__single2diff2single/scripts/pcells/load_clamp_pcells.py')
