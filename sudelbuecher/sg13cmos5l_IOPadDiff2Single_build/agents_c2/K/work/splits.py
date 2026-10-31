# C of CMA / CMB along the DC swing (deck 6) for each option, from the C(V) curves (decks 1, 4, 5).
# Options are sized for the same C as the present device at mid-rail (vd = 0). Prints a table; writes swing_c.dat.
import numpy as np
L='/home/user/c2/K/out/logs/'
hv=np.loadtxt(L+'cv1_hvpmos.dat'); sv=np.loadtxt(L+'cv4_svaricap.dat'); mom=np.loadtxt(L+'cv5_mom.dat')
V=hv[:,0]
c_hv=lambda v: np.interp(v,V,hv[:,1])          # fF/um2 gate, V = V(gate) - V(well)
c_sv=lambda v: np.interp(v,sv[:,0],sv[:,2])    # S-Varicap Nx10 9.74/0.8, fF/um2 gate, V = V(gate) - V(well)
c_mom=mom[0,1]                                 # cmomf M1-M2, fF/um2
dc=np.loadtxt(L+'dc6_swing.dat'); vd=dc[:,0]; pad,a,b=dc[:,1],dc[:,3],dc[:,5]
vA=a-pad; vB=pad-b                              # V_GW of CMA (gate a, well pad) and CMB (gate pad, well b)
i0=np.argmin(abs(vd)); lin=(pad>0.95)&(pad<2.31)&(vd<1.4)
FP_HV=325.7/256; FP_SV=312.7/171.4; FP_MOM=410/400   # footprint um2 per um2 of gate / model area (PCell boxes, NWell of drawn caps)
def opt(name, parts, vgw):
    # parts: list of (kind, fraction of mid C, sign) ; sign -1 = device turned around (sees -V_GW)
    C=np.zeros_like(pad); area=0; gate=0
    for kind,fr,sg in parts:
        f={'hv':c_hv,'sv':c_sv,'mom':(lambda v: c_mom+0*v)}[kind]
        Cnom=c_hv(vgw[i0])*256*fr; A=Cnom/f(sg*vgw[i0])
        C+=A*f(sg*vgw); gate+=A if kind!='mom' else 0
        area+=A*{'hv':FP_HV,'sv':FP_SV,'mom':FP_MOM}[kind]
    return name,C,gate,area
opts=[]
for cap,vgw in (('CMA',vA),('CMB',vB)):
    opts+=[(cap,)+opt('present hv PMOS',[('hv',1,1)],vgw),
           (cap,)+opt('hv PMOS turned',[('hv',1,-1)],vgw),
           (cap,)+opt('anti-parallel hv PMOS 50/50',[('hv',.5,1),('hv',.5,-1)],vgw),
           (cap,)+opt('S-Varicap',[('sv',1,1)],vgw),
           (cap,)+opt('S-Varicap turned',[('sv',1,-1)],vgw),
           (cap,)+opt('S-Varicap 50 + hv PMOS 50',[('sv',.5,1),('hv',.5,1)],vgw),
           (cap,)+opt('S-Varicap 70 + hv PMOS 30',[('sv',.7,1),('hv',.3,1)],vgw),
           (cap,)+opt('hv PMOS 50 + MOM M1-M2 50',[('hv',.5,1),('mom',.5,1)],vgw),
           (cap,)+opt('S-Varicap 50 + MOM M1-M2 50',[('sv',.5,1),('mom',.5,1)],vgw),
           (cap,)+opt('MOM M1-M2 only',[('mom',1,1)],vgw)]
k={p:np.argmin(abs(pad-p)) for p in (1.0,1.65,2.3)}; ks=len(pad)-1
print("V_GW at pad 0.90 / 1.00 / 1.65 / 2.30 / 3.28 (sat):")
for cap,vgw in (('CMA',vA),('CMB',vB)): print(cap, [round(vgw[j],2) for j in (0,k[1.0],i0,k[2.3],ks)])
print(f"{'cap':4s} {'option':30s} {'C@0.90':>7s} {'C@1.00':>7s} {'C@1.65':>7s} {'C@2.30':>7s} {'C@3.28':>7s} {'min/mid lin':>11s} {'gate um2':>8s} {'area um2':>8s}")
for cap,n,C,g,A in opts:
    print(f"{cap:4s} {n:30s} " + " ".join(f"{C[j]:7.0f}" for j in (0,k[1.0],i0,k[2.3],ks)) + f" {C[lin].min()/C[i0]:11.2f} {g:8.0f} {A:8.0f}")
np.savetxt('/home/user/c2/K/out/logs/swing_vgw.dat', np.c_[vd,pad,vA,vB], header='vd pad VGW_CMA VGW_CMB (loaded pad, deck 6)')
