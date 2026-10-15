CACE mismatch histogram setup
=============================

Put these files under:

  JanteStroemSpejl/
    JanteStroemSpejl.sch
    JanteStroemSpejl.sym
    xschemrc
    cace/
      JanteStroemSpejl.yaml
      templates/
        JanteStroemSpejl_cace_mm.sch
        xschemrc
      scripts/
        pool_mismatch.py

Run from the JanteStroemSpejl project directory:

  cace cace/JanteStroemSpejl.yaml --source schematic -j 8

CACE performs 500 independent mismatch simulations, collates them by the
'iterations' condition, pools the ten mirror-output errors into 5000 samples,
and generates the SVG histogram requested in the datasheet.

If your existing project uses xschem/ rather than the project root for
schematics, change paths.schematic and the template xschemrc accordingly.
