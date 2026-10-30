<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Reference sheets, as delivered 2026-10-20

Snapshot of every xschem sheet and symbol in `macros/*/schematic/xschem`, `macros/*/testbenches/xschem`,
`schematic/xschem`, `testbenches/xschem` and the CACE templates `macros/*/verification/cace/templates` of `sg13cmos5l_cm_ip__single2diff2single`: the versions the
consolidation session delivered and verified on 2026-10-20 (CACE runs, sheet-against-netlist comparisons).
Files that session did not deliver (template examples, `IOPad`, `OgueyAebischerBias`, top cell) are in
their state of 2026-10-22 01:06. Same folder layout as the repository, so the folder works as the
reference root of `scripts/xschem/sheet_equiv.py`:

    cd /foss/designs/sg13cmos5l_cm_ip__single2diff2single
    source .designinit
    python3 scripts/xschem/sheet_equiv.py \
      ../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/consolidation/reference_sheets_2026-10-20 .

Do not edit these files; they are the comparison baseline. Once the working tree passes, a commit of it
is the better reference. The container has no git, so export the commit on the host into `~/EDA`, which
the container sees as `/foss/designs` (only the three folders the script reads):

    # host
    mkdir ~/EDA/ref_<commit>
    git -C ~/EDA/sg13cmos5l_cm_ip__single2diff2single archive <commit> macros schematic testbenches | tar -x -C ~/EDA/ref_<commit>
    # container
    python3 scripts/xschem/sheet_equiv.py ../ref_<commit> .
    # host, afterwards
    rm -r ~/EDA/ref_<commit>

Record: `../log.md`, entries of 22 and 24 Oct.
