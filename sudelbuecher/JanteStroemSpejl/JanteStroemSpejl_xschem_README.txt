JanteStroemSpejl Xschem + mismatch testbench
================================================

Files
-----
JanteStroemSpejl.sch
    22 explicit sg13_lv_nmos devices: 11 left + 11 right.
    No use of m/ng for arraying; every physical device is instantiated once.
    m=1, ng=1 are explicit.
    mm_ok=1 is explicit on every device.

JanteStroemSpejl.sym
    Pins: IREF, S, B, OUT01..OUT10.

JanteStroemSpejl_tb_mismatch.sch
    Local mismatch testbench using:
        .lib cornerMOSlv.lib mos_tt_mismatch
    IREF = 100 uA.
    S=B=0.
    Each OUTxx is independently clamped to V(IREF) with a unity-gain
    dependent voltage source followed by a 0-V current-sense source.
    This makes VDS(output) = VGS(reference) without loading IREF.

    500 Monte-Carlo mismatch runs are executed.  On every reset the
    mismatch model is re-evaluated.  The file
        JanteStroemSpejl_mismatch.dat
    contains fractional current error for OUT01..OUT10:
        e_k = IOUT_k / 100u - 1

Geometry:
    contact = 2 lambda = 0.16 um
    lambda  = 0.08 um
    W       = 4 lambda  = 0.32 um
    L       = 64 lambda = 5.12 um

PDK notes
---------
Run under the SG13CMOS5L xschemrc / IIC-OSIC-TOOLS environment so that
cornerMOSlv.lib and the sg13g2_pr symbols resolve through the PDK setup.

The current IHP mismatch models use per-instance mm_ok.  Selecting
mos_tt_mismatch plus mm_ok=1 enables local device mismatch.
