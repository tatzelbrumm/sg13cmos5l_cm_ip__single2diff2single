# stage 6: per variant / load / vd: fc, PM, GM (deck 13) and the fitted dominant poles / zeros (vfit.py, N = 6); plots
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import sys; sys.path.insert(0, "/home/user/c2/K/work"); from vfit import fit
L='/home/user/c2/K/out/logs/loop13.dat'
rows=[l.split() for l in open(L) if l.split()[0][0]=='v' and len(l.split())==10]
V=['v0','v5','v6','v7','v8','v7d']; loads=['1e-10','3e-10']
res={}
for r in rows:
    v,cl,vd,vo,va,vb,T0,fc,PM,GM=r; vd=float(vd)
    for N in (6,8,10,5,7):   # first order whose roots classify sanely (p1 1 Hz-1 kHz, p2 and LHP zero > 1 MHz)
        p,z,edb,eph=fit(f'/home/user/c2/K/work/T13/T_{v}_{cl}_{r[2]}.dat',N)
        # drop pole-zero doublets above 10 kHz (zero within 5 % of the pole)
        P=[x for x in p if abs(x)>=1]; Z=[x for x in z if abs(x)>=1]   # roots below the 1 Hz fit band are artefacts (flat there)
        for pp in list(P):
            if not Z: break
            k=int(np.argmin([abs(zz-pp) for zz in Z]))
            if abs(pp)>1e4 and abs(Z[k]-pp)<0.05*abs(pp): P.remove(pp); Z.pop(k)   # never the dominant pole
        P=sorted([x for x in P if x.imag>=0],key=abs); Zl=sorted([x for x in Z if x.real<0 and x.imag>=0],key=abs); Zr=sorted([x for x in Z if x.real>0 and x.imag>=0],key=abs)
        p2=P[1] if len(P)>1 else np.nan
        ok=(1<=abs(P[0])<=1e3) and len(P)>1 and abs(P[1])>1e6 and Zl and abs(Zl[0])>1e6
        if ok: break
    order=N if ok else -N
    res[(v,cl,vd)]=dict(pad=float(vo),fc=float(fc)/1e6,PM=float(PM),GM=float(GM),T0=float(T0),p1=abs(P[0]),p2=abs(p2),z2=abs(p2.real)/abs(p2) if p2==p2 else np.nan,
                        p3=abs(P[2]) if len(P)>2 else np.nan,zl=abs(Zl[0]) if Zl else np.nan,zr=abs(Zr[0]) if Zr else np.nan,err=(edb,eph),N=order)
vds=sorted({k[2] for k in res})
with open('/home/user/c2/K/out/logs/stage6_table.txt','w') as o:
    o.write("variant load vd pad T0dB fcMHz PM GM | p1Hz |p2|MHz zeta2 |p3|MHz zLHP_MHz zRHP_MHz fit_err_dB/deg order(neg=no sane fit)\n")
    for v in V:
        for cl in loads:
            for vd in vds:
                if (v,cl,vd) not in res: continue
                q=res[(v,cl,vd)]
                o.write(f"{v} {cl} {vd:+.2f} {q['pad']:.3f} {q['T0']:.1f} {q['fc']:.3f} {q['PM']:.1f} {q['GM']:.1f} | {q['p1']:.0f} {q['p2']/1e6:.2f} {q['z2']:.2f} {q['p3']/1e6:.1f} {q['zl']/1e6:.1f} {q['zr']/1e6:.0f} {q['err'][0]:.3f}/{q['err'][1]:.2f} N{q['N']}\n")
col={'v0':'#2a78d6','v5':'#eb6834','v6':'#1baf7a','v7':'#eda100','v8':'#6250d6','v7d':'#e87ba4'}
lab={'v0':'v0 present','v5':'v5 CMB 587 Ohm','v6':'v6 CMB 2 kOhm','v7':'v7 sym 587 Ohm','v8':'v8 sym 2 kOhm','v7d':'v7d sym 587 + dummy diodes'}
plt.rcParams.update({'font.size':8,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':'#e4e3df'})
def series(v,cl,key):
    pts=[(res[(v,cl,vd)]['pad'],res[(v,cl,vd)][key]) for vd in vds if (v,cl,vd) in res]; return np.array(pts).T
fig,axs=plt.subplots(2,3,figsize=(10,5.6),sharex=True)
for j,cl in enumerate(loads):
    for i,(key,yl) in enumerate((('PM','PM (deg)'),('fc','fc (MHz)'),('GM','GM (dB)'))):
        ax=axs[j,i]
        for v in V:
            x,y=series(v,cl,key); ax.plot(x,y,'-o',ms=3,lw=1.4,color=col[v],label=lab[v])
        ax.set_ylabel(yl); ax.set_title(('1 kOhm || 100 pF' if cl=='1e-10' else 'unloaded || 300 pF')+f': {key}',loc='left',fontsize=9)
        ax.axvline(1.65,color='#52514e',lw=0.6,ls=':')
for ax in axs[1]: ax.set_xlabel('pad (V)')
axs[0,0].legend(fontsize=6.5,frameon=False); fig.tight_layout(); fig.savefig('/home/user/c2/K/out/pm_fc_gm_vs_pad.png',dpi=150)
fig,axs=plt.subplots(2,3,figsize=(10,5.6),sharex=True)
for j,cl in enumerate(loads):
    for i,(key,yl,sc) in enumerate((('p1','p1 (Hz)',1),('p2','|p2| non-dominant pair (MHz)',1e-6),('zr','lowest RHP zero (MHz)',1e-6))):
        ax=axs[j,i]
        for v in V:
            x,y=series(v,cl,key); ax.plot(x,y*sc,'-o',ms=3,lw=1.4,color=col[v],label=lab[v])
        ax.set_ylabel(yl); ax.set_title(('1 kOhm || 100 pF' if cl=='1e-10' else 'unloaded || 300 pF')+f': {key}',loc='left',fontsize=9); ax.axvline(1.65,color='#52514e',lw=0.6,ls=':')
        if key!='p2': ax.set_yscale('log')
for ax in axs[1]: ax.set_xlabel('pad (V)')
axs[0,0].legend(fontsize=6.5,frameon=False,loc='lower left'); fig.suptitle('Loop-gain poles / zeros fitted from the AC response (vector fitting, order 6; 5-10 where 6 did not classify), deck 13. Scatter of 10-30 % between neighbouring points = fit ambiguity of pole-zero doublets',fontsize=9,x=0.01,ha='left')
fig.tight_layout(); fig.savefig('/home/user/c2/K/out/pz_vs_pad.png',dpi=150)
# summary: worst PM and symmetry (PM and fc at mirrored vd = +-x, x = 0.35 0.7 1.05; and the ends -1.4 / +1.3)
print("variant load PMmin@pad PMmax  fc max/min  |dPM| mirrored (0.35/0.7/1.05/ends)  fc ratio hi/lo (same)  GMmin")
for v in V:
    for cl in loads:
        q=[res[(v,cl,vd)] for vd in vds if (v,cl,vd) in res]
        if len(q)<len(vds): print(v,cl,'incomplete',len(q)); continue
        pm=[x['PM'] for x in q]; fc=[x['fc'] for x in q]; k=int(np.argmin(pm))
        g=lambda vd:res[(v,cl,vd)]
        dpm=[abs(g(a)['PM']-g(-a)['PM']) for a in (0.35,0.7,1.05)]+[abs(g(1.3)['PM']-g(-1.4)['PM'])]
        fr=[g(a)['fc']/g(-a)['fc'] for a in (0.35,0.7,1.05)]+[g(1.3)['fc']/g(-1.4)['fc']]
        print(f"{v:4s} {cl} {min(pm):5.1f}@{q[k]['pad']:.2f} {max(pm):5.1f} {max(fc)/min(fc):5.2f}  " + "/".join(f"{x:.1f}" for x in dpm) + "  " + "/".join(f"{x:.2f}" for x in fr) + f"  {min(x['GM'] for x in q):.1f}")
