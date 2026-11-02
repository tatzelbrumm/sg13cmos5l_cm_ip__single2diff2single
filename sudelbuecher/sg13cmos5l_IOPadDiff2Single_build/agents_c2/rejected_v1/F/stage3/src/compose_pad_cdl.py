# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Reference netlist of the pad candidate: d2s_block.cdl + the pad level (C2 phase 1 §1.7 partition, d2s_out.spice).
python3 compose_pad_cdl.py <d2s_block.cdl> <out.cdl>"""
import sys
PAD = """
* sg13cmos5l_IOPadDiff2Single as partitioned in C2 phase 1 (1.7): Xt + Xd = d2s_block, the output stage of
* d2s_out.spice (OP / RP1 / RPD in the P frame, ON / RN1 in the N frames), CMA / CMB, DCN / DCP. vfb = pad (Kelvin).
* The diodes as IHP's LVS extracts the DCNDiode / DCPDiode PCells (dantenna / dpantenna, A and P as drawn by A1).
.SUBCKT sg13cmos5l_IOPadDiff2Single iovdd iovss vdd vss pad vinp vinn vref iref en_3v3 en_3v3_b
XBLK iovdd iovss vinp vinn vref pad a b dabp dabn iref en_3v3 en_3v3_b d2s_block
MOP pad a iovdd iovdd sg13_hv_pmos w=546.12u l=0.6u ng=82 m=1
MRP1 dabp dabp iovdd iovdd sg13_hv_pmos w=13.32u l=0.6u ng=2 m=1
MRPD dabp iovdd iovdd iovdd sg13_hv_pmos w=13.32u l=0.6u ng=2 m=1
MON pad b iovss iovss sg13_hv_nmos w=299.2u l=1u ng=68 m=1
MRN1 dabn dabn iovss iovss sg13_hv_nmos w=8.8u l=1u ng=2 m=1
MCMA pad a pad pad sg13_hv_pmos w=7.96u l=32.16u ng=1 m=1
MCMB b pad b b sg13_hv_pmos w=7.96u l=32.16u ng=1 m=1
DDN iovss pad dantenna A=85.176p P=137.72u m=2
DDP pad iovdd dpantenna A=82.908p P=134.12u m=2
.ENDS sg13cmos5l_IOPadDiff2Single
"""
open(sys.argv[2], "w").write(open(sys.argv[1]).read() + PAD)
