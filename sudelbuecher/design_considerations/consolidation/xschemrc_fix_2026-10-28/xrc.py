"""xschemrc fixes 2026-10-28: BOM removed; pin_netlist_dir falls back to schematic/xschem/simulations when the macro has
no testbenches/xschem, and creates the folder; macros/xschemrc re-reads the macro list on every load. usage: xrc.py <root>"""
import sys, os, glob
R = sys.argv[1]
OLD = '''    if {[string match */schematic/xschem $dir]} {
      set dir [file join $dir ../../testbenches/xschem]
    } elseif {![string match */testbenches/xschem $dir] && ![string match */cace/templates $dir]} {
      return
    }
    set ::netlist_dir [file normalize [file join $dir simulations]]
  }'''
NEW = '''    if {[string match */schematic/xschem $dir]} {
      # testbenches/xschem/simulations if the macro has testbenches, else schematic/xschem/simulations (both gitignored)
      set tb [file normalize [file join $dir ../../testbenches/xschem]]
      if {[file isdir $tb]} {set dir $tb}
    } elseif {![string match */testbenches/xschem $dir] && ![string match */cace/templates $dir]} {
      return
    }
    set ::netlist_dir [file normalize [file join $dir simulations]]
    # xschem does not create a netlist_dir set this way; without the folder netlisting fails
    catch {file mkdir $::netlist_dir}
  }'''
changed = []
for f in sorted(glob.glob(os.path.join(R, 'macros/**/xschemrc'), recursive=True)):
    if '/simulations/' in f: continue
    b = open(f, 'rb').read(); t0 = b
    if b.startswith(b'\xef\xbb\xbf'): b = b[3:]
    t = b.decode()
    if t.count(OLD) != 1: print('NO MATCH', f); continue
    t = t.replace(OLD, NEW)
    if f.endswith('macros/xschemrc'):
        old = '''set macros_root [file dirname [file normalize [info script]]]
foreach sub {schematic/xschem testbenches/xschem} {
  foreach d [lsort [glob -nocomplain -type d [file join $macros_root * $sub]]] {
    append_xschem_library_path_unique $d
  }
}
'''
        new = '''set macros_root [file dirname [file normalize [info script]]]
# The macro list is read again on every file load (load_file_postprocess below), so a macro created while xschem runs
# is found without a restart (2026-10-28).
proc add_macro_paths {} {
  foreach sub {schematic/xschem testbenches/xschem} {
    foreach d [lsort [glob -nocomplain -type d [file join $::macros_root * $sub]]] {
      append_xschem_library_path_unique $d
    }
  }
}
add_macro_paths
'''
        assert t.count(old) == 1; t = t.replace(old, new)
        old = 'set load_file_postprocess {pin_netlist_dir [xschem get current_dirname]}'
        assert t.count(old) == 1; t = t.replace(old, 'set load_file_postprocess {add_macro_paths; pin_netlist_dir [xschem get current_dirname]}')
        t = t.replace('# New macros are picked up automatically (glob below); nothing to edit when one is added.',
                      '# New macros are picked up automatically (glob below, repeated on every file load); nothing to edit when one is added.')
    open(f, 'w').write(t); changed.append(os.path.relpath(f, R) + (' (BOM removed)' if t0.startswith(b'\xef\xbb\xbf') else ''))
print(len(changed)); print('\n'.join(c for c in changed if 'BOM' in c or c.startswith('macros/xschemrc')))
