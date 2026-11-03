# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""F2 stage B: reference netlists of d2s_block and of the pad candidate, from the cells' own CDLs.

    python3 compose_cdl.py <p2.cdl> <f2b_p.cdl> <f2b_n.cdl> <f2b_sp.cdl> <out_block.cdl> <out_pad.cdl>

d2s_block = d2s_mpdda_pd (inputs, tails, rhigh, sinks, cascodes, loads, class AB + the folded-in switches) +
bias_tree_pd (bias_tree_p_f2, bias_tree_n_f2, the transmission gate TGN / TGP and TDN, written flat here: TGP's bulk
is the shared iovdd well) + the two 2 kOhm stages. Pad level: as rejected F's compose_pad_cdl.py (clamp frames, CMA /
CMB, DCN / DCP as IHP's LVS extracts them), with CMA / CMB as in the sheet (v8) but behind their stages:
CMA source / drain / well on pa, gate on a; CMB gate on pb, source / drain / well on b.
vdd = vddo = iovdd and vss = iovss inside the pad; vsso (SB's source, own path to the P frame's p+ ring) is a block port tied to iovss at the pad level (Xd's ports in the sheet); vfb = pad (Kelvin line).
"""
import sys

p2, fp, fn, fsp, ob, op = sys.argv[1:7]


def body(path, skip=()):
    out, keep = [], True
    for line in open(path):
        t = line.split()
        if t and t[0].upper() == ".SUBCKT":
            keep = t[1] not in skip
        if keep and not line.startswith("* SPDX"):
            out.append(line.rstrip("\n"))
        if t and t[0].upper() == ".ENDS":
            keep = True
    return "\n".join(out) + "\n"


BLOCK = """
* d2s_block (agent F2, C2 stage B): d2s_mpdda_pd + bias_tree_pd + the 2 kOhm stages of CMA / CMB
.SUBCKT d2s_block iovdd iovss vinp vinn vref vfb a b dabp dabn iref en_3v3 en_3v3_b pa pb pad vsso
XSPA pa iovdd iovss pad d2s_sp2k_f2
XSPB pb iovdd iovss pad d2s_sp2k_f2
XIN sa_A sa_B sa_C1 sa_C2 sb_A sb_B sb_C1 sb_C2 iovdd vfb vinn vinp vref x y d2s_inputs_c2
XTL sa_A sa_B sa_C1 sa_C2 sb_A sb_B sb_C1 sb_C2 vbp iovdd d2s_tails_c2
XRH sa_A sa_B sa_C1 sa_C2 sb_A sb_B sb_C1 sb_C2 iovss d2s_rhigh_f2
XSK vbn iovss x y sinks_6x6_f2
XCN b l1 vbnc iovss x y d2s_casc_n_f2
XLD l2 pl pr iovdd d2s_loads_c2
XCP a l2 pl pr vbpc iovdd d2s_casc_p_c2
XABP a b dabp en_3v3 l1 l2 vabp iovdd iovdd d2s_ab_p_f2
XABN a b dabn en_3v3_b l1 l2 vabn iovss vsso d2s_ab_n_f2
XBP vabn vbn vbnc vbp iovdd bias_tree_p_f2
XBN ni vabp vbp vbpc iovss bias_tree_n_f2
MTGP ni en_3v3_b iref iovdd sg13_hv_pmos w=1u l=0.45u ng=1 m=1
MTGN ni en_3v3 iref iovss sg13_hv_nmos w=1u l=0.45u ng=1 m=1
MTDN ni en_3v3_b iovss iovss sg13_hv_nmos w=1u l=0.45u ng=1 m=1
.ENDS d2s_block
"""
PAD = """
* sg13cmos5l_IOPadDiff2Single as partitioned in C2 phase 1 (1.7), stage B of F2: d2s_block, the output stage of
* d2s_out.spice (OP / RP1 / RPD in the P frame, ON / RN1 in the N frames), CMA / CMB behind their 2 kOhm stages,
* DCN / DCP (as IHP's LVS extracts the DCNDiode / DCPDiode PCells, A and P as drawn by A1).
.SUBCKT sg13cmos5l_IOPadDiff2Single iovdd iovss vdd vss pad vinp vinn vref iref en_3v3 en_3v3_b
XBLK iovdd iovss vinp vinn vref pad a b dabp dabn iref en_3v3 en_3v3_b pa pb pad iovss d2s_block
MOP pad a iovdd iovdd sg13_hv_pmos w=546.12u l=0.6u ng=82 m=1
MRP1 dabp dabp iovdd iovdd sg13_hv_pmos w=13.32u l=0.6u ng=2 m=1
MRPD dabp iovdd iovdd iovdd sg13_hv_pmos w=13.32u l=0.6u ng=2 m=1
MON pad b iovss iovss sg13_hv_nmos w=299.2u l=1u ng=68 m=1
MRN1 dabn dabn iovss iovss sg13_hv_nmos w=8.8u l=1u ng=2 m=1
MCMA pa a pa pa sg13_hv_pmos w=7.96u l=32.16u ng=1 m=1
MCMB b pb b b sg13_hv_pmos w=7.96u l=32.16u ng=1 m=1
DDN iovss pad dantenna A=85.176p P=137.72u m=2
DDP pad iovdd dpantenna A=82.908p P=134.12u m=2
.ENDS sg13cmos5l_IOPadDiff2Single
"""
HEAD = "* SPDX-FileCopyrightText: 2026 Christoph Maier\n* SPDX-License-Identifier: Apache-2.0\n"
cells = body(p2) + body(fp) + body(fn, skip=("d2s_tgsw_f2",)) + body(fsp)
open(ob, "w").write(HEAD + cells + BLOCK)
open(op, "w").write(HEAD + cells + BLOCK + PAD)
