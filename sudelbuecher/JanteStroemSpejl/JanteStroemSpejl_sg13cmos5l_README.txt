JanteStroemSpejl -> Xschem / IHP SG13CMOS5L
=================================================

Interpretation
--------------
The artwork is not LVS-complete, so this is the electrically coherent
interpretation suggested by its title and repeated left/right geometry:
an NMOS current mirror with 11 identical rows on each side.

Geometry extracted from the SVG
-------------------------------
The square contact marker is 14.173228 SVG units.
The horizontal diffusion stripe is 28.34647 units = 2 contact widths.
The poly-over-diffusion overlap in the current-flow direction is
453.5433 units = 32 contact widths.

Using the usual lambda normalization contact = 2 lambda:
    contact side = 2 lambda
    transistor W = 4 lambda
    transistor L = 64 lambda

Absolute SG13CMOS5L scaling used here
-------------------------------------
Assumption: square Cont side = 0.16 um.
Therefore:
    lambda = 0.08 um
    W = 0.32 um
    L = 5.12 um
    m = 11
    effective W per mirror side = 3.52 um

The Xschem schematic uses:
    sg13g2_pr/sg13_lv_nmos.sym
    model=sg13_lv_nmos

This library/model naming is the one used by the current IHP/Xschem
examples and remains applicable to the SG13CMOS5L PDK frontend.
