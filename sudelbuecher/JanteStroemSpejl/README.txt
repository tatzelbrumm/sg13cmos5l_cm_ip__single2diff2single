CACE-only files for JanteStroemSpejl
====================================

These files do NOT replace or modify:
  JanteStroemSpejl.sch
  JanteStroemSpejl.sym
  JanteStroemSpejl_tb_mismatch.sch

The dedicated CACE testbench is:
  cace/templates/JanteStroemSpejl_cace_mismatch.sch

It intentionally contains exactly one operating-point run.
CACE performs the 500-run outer loop.

The `iterations` placeholder is attached to an electrically isolated voltage
source VDUMMY:
  value=CACE{iterations}

That is deliberate: it puts the condition in a normal Xschem component value
instead of hiding it inside a code_shown block.  VDUMMY is disconnected from
the DUT, so it has no electrical effect.

This package is intended for:
  cace cace/JanteStroemSpejl.yaml --source schematic -j 8
