# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Write the Makefiles of vcm_rb and vref_s2d_rb from macros/oa_core_pd/Makefile: TOP and CACE_GROUPS changed, sim-cace
exports the macro library path as the pads' sim-cace does, new targets check-sheet and sim-char.
usage: python3 -I gen_makefiles.py"""
import re
from pathlib import Path

MAC = Path(__file__).resolve().parents[1]
src = (MAC / "oa_core_pd/Makefile").read_text()
CLEAN = "rm -rf _runs _docs netlist .xschem_library_path"
new_cace = """sim-cace: ## Run CACE (-s schematic) and collect plots, summaries and CSV in verification/cace/results/<TOP>/
\tcd $(CACE_DIR) && mkdir -p results/$(TOP) && status=0 && \\
\txschem -x -q -r --rcfile $(MAKEFILE_DIR)/$(XSCHEM_SCH_DIR)/xschemrc \\
\t  --command "set fp [open .xschem_library_path w]; puts \\$$fp \\$$XSCHEM_LIBRARY_PATH; close \\$$fp" > /dev/null 2>&1 ; \\
\texport XSCHEM_USER_LIBRARY_PATH=$$(tr ':' '\\n' < .xschem_library_path | grep '/macros/' | grep -v '^$(MAKEFILE_DIR)/' | paste -sd: -) ; \\
\tfor g in $(CACE_GROUPS); do \\
\t  rm -rf _runs/RUN_* ; \\
\t  cace $(TOP).yaml -s schematic -p $$g -j $(CACE_JOBS) --no-progress-bar || status=1 ; \\
\t  cp _runs/RUN_*/parameters/$$g/*.png results/$(TOP)/ 2>/dev/null ; \\
\t  cp _runs/RUN_*/summary.md results/$(TOP)/summary_$$g.md ; \\
\t  python3 $(CACE_SCRIPTS)/cace_to_csv.py $(TOP).yaml $$g _runs/RUN_* results/$(TOP)/$$g.csv || status=1 ; \\
\t  rm -rf _runs/RUN_* ; \\
\tdone ; \\
\t""" + CLEAN + """ ; exit $$status
.PHONY: sim-cace

check-sheet: ## Netlist each sheet (SHEET_CELLS) with xschem and compare it with netlist/source/<TOP>.spice (devices, instances)
\tcd $(XSCHEM_SCH_DIR) && mkdir -p simulations && status=0 && \\
\tfor c in $(SHEET_CELLS); do \\
\t  xschem -q -x -n -s --tcl 'set top_subckt 1' --rcfile xschemrc -o simulations --netlist_filename $$c.spice $$c.sch > /dev/null 2>&1 ; \\
\t  python3 $(MAKEFILE_DIR)/../vcm_rb/schematic/gen_sheet.py --check $(MAKEFILE_DIR)/netlist/source/$(TOP).spice $$c simulations/$$c.spice || status=1 ; \\
\tdone ; exit $$status
.PHONY: check-sheet

sim-char: ## Block and closed-loop characterization decks of pad_ref_rb (macros/vcm_rb/testbenches/rb_char/run_rb.py)
\tpython3 -I $(MAKEFILE_DIR)/../vcm_rb/testbenches/rb_char/run_rb.py rb_dc rb_z rb_mm rb_en rb_up -j 4
.PHONY: sim-char
"""
i = src.index("sim-cace: ##")
j = src.index(".PHONY: sim-cace") + len(".PHONY: sim-cace\n")
# Since 2026-11-07 vcm_rb and vref_s2d_rb hang on the shared tree bias_tree_rb: their CACE suite is pad_ref_rb's.
CELLS = (("vcm_rb", "", "vcm_rb"), ("vref_s2d_rb", "", "vref_s2d_rb"),
         ("pad_ref_rb", "vcm_dc_params vcm_dc_3v0_params vcm_sel_params vref_room_params vref_hot_params "
                        "vref_cold_params pd_params mm_params", "pad_ref_rb bias_tree_rb bypass_rb"))
DELEGATE = """sim-cace: ## CACE suite of pad_ref_rb (this block hangs on its shared tree bias_tree_rb since 2026-11-07)
\t$(MAKE) -C $(MAKEFILE_DIR)/../pad_ref_rb sim-cace
.PHONY: sim-cace
"""
for top, groups, cells in CELLS:
    cace = new_cace if groups else DELEGATE + new_cace[new_cace.index("\ncheck-sheet:"):]
    s = src[:i] + cace + src[j:]
    s = s.replace("TOP = oa_core_pd", f"TOP = {top}")
    s = re.sub(r"^CACE_GROUPS \?= .*$", f"CACE_GROUPS ?= {groups}\nSHEET_CELLS ?= {cells}", s, flags=re.M)
    s = s.replace("# oa_core_pd: copied 2026-10-27", f"# {top}: copied {'2026-11-07' if top == 'pad_ref_rb' else '2026-11-06'} from macros/oa_core_pd/Makefile (replica bias task;"
                  " changed: TOP, CACE_GROUPS, SHEET_CELLS, sim-cace exports the macro library path, targets check-sheet and\n"
                  "# sim-char).\n"
                  "# oa_core_pd: copied 2026-10-27", 1)
    (MAC / top / "Makefile").write_text(s)
    print(top, "Makefile written")
