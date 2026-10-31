crashbackups stop
drc off
gds read d2s_rhigh.gds
if {[lsearch [cellname list topcells] {d2s_rhigh}] < 0} {
    set _fp [open {/home/user/c2/F/work/runs/pex_rhigh/pex_d2s_rhigh.cellmismatch} w]
    puts $_fp [cellname list topcells]
    close $_fp
    quit -noprompt
}
load d2s_rhigh
select top cell
flatten d2s_rhigh_flat
load d2s_rhigh_flat
cellname delete d2s_rhigh
cellname rename d2s_rhigh_flat d2s_rhigh_pex
select top cell
extract path /home/user/c2/F/work/runs/pex_rhigh
ext2spice lvs
extract all
ext2spice cthresh 0.01
ext2spice -p /home/user/c2/F/work/runs/pex_rhigh -o /home/user/c2/F/work/runs/pex_rhigh/d2s_rhigh.pex.spice.tmp
quit -noprompt
