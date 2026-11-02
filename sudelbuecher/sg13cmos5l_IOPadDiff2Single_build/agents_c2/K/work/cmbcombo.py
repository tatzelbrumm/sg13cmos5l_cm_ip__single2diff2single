# CMB: search parallel combinations of MOS-type capacitors whose C(V) complement each other over the V_GW that CMB sees
# (V_GW = pad - b from deck 6, linear range pad 0.95-2.31 V, plus the saturated top point). Basis curves from decks 1 and 4.
import numpy as np, itertools
L='/home/user/c2/K/out/logs/'
hv=np.loadtxt(L+'cv1_hvpmos.dat'); sv=np.loadtxt(L+'cv4_svaricap.dat'); sw=np.loadtxt(L+'swing_vgw.dat')
vd,pad,vB=sw[:,0],sw[:,1],sw[:,3]
lin=(pad>0.95)&(pad<2.31)&(vd<1.4); i0=np.argmin(abs(vd)); top=len(pad)-1
f={'hv':lambda v:np.interp(v,hv[:,0],hv[:,1]),'hvT':lambda v:np.interp(-v,hv[:,0],hv[:,1]),
   'sv':lambda v:np.interp(v,sv[:,0],sv[:,2]),'svT':lambda v:np.interp(-v,sv[:,0],sv[:,2])}
fp={'hv':325.7/256,'hvT':325.7/256,'sv':312.7/171.4,'svT':312.7/171.4}
C0=f['hv'](vB[i0])*256   # present CMB at mid-rail, fF
res=[]
names=list(f); step=0.1
for fr in itertools.product(np.arange(0,1.0001,step),repeat=len(names)):
    if abs(sum(fr)-1)>1e-6: continue
    # fr = share of the mid-rail C; gate area of each part = share*C0/c(V_mid)
    A={n:x*C0/f[n](vB[i0]) for n,x in zip(names,fr)}
    C=sum(A[n]*f[n](vB) for n in names)
    area=sum(A[n]*fp[n] for n in names)
    res.append((C[lin].max()/C[lin].min(), C[top]/C[i0], area, dict(zip(names,np.round(fr,2))), C[lin].min(), C[lin].max()))
res.sort(key=lambda r:r[0])
print(f"present CMB at mid: {C0:.0f} fF; V_GW lin range {vB[lin].min():.2f}..{vB[lin].max():.2f}, saturated top {vB[top]:.2f}")
print("max/min(lin)  C_sat/C_mid  footprint_um2  shares-of-mid-C           Cmin..Cmax fF")
for r in res[:12]: print(f"{r[0]:8.3f}  {r[1]:8.2f}  {r[2]:9.0f}   {r[3]}  {r[4]:.0f}..{r[5]:.0f}")
for name,sh in (('present',{'hv':1,'hvT':0,'sv':0,'svT':0}),('hv+hvT 50/50',{'hv':.5,'hvT':.5,'sv':0,'svT':0}),('S-Varicap',{'hv':0,'hvT':0,'sv':1,'svT':0})):
    r=[x for x in res if x[3]==sh][0]; print(f"{name:14s} {r[0]:.3f} {r[1]:.2f} {r[2]:.0f} {r[4]:.0f}..{r[5]:.0f}")
print(f"MOM cmomf M1-M2 same C: 1.000, footprint {C0/0.677*410/400:.0f} um2 (M1+M2 both occupied)")
print("CMB, no gate on the pad (only hvT, svT: gate on b, well on the pad):")
for r in [x for x in res if x[3]['hv']==0 and x[3]['sv']==0][:4]: print(f"{r[0]:8.3f}  {r[1]:8.2f}  {r[2]:9.0f}   {r[3]}  {r[4]:.0f}..{r[5]:.0f}")
