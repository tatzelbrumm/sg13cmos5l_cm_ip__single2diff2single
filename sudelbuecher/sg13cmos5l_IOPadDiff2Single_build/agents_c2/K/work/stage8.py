# stage 8 evaluation: large steps (deck 15), rail recovery (deck 16), THD (deck 17); plots
import numpy as np, matplotlib, os; matplotlib.use('Agg'); import matplotlib.pyplot as plt
L='/home/user/c2/K/out/logs/'; V=['v0','v8','v9']
lab={'v0':'v0 present','v8':'v8 present orientation + sym 2 kOhm','v9':'v9 both turned + sym 2 kOhm'}; col={'v0':'#2a78d6','v8':'#6250d6','v9':'#eb6834'}
def stepm(t,v,t0,t1):
    m=(t>=t0)&(t<=t1); tt,vv=t[m],v[m]
    va=np.interp(t0-0.01e-6,t,v); vb=vv[-20:].mean(); dv=vb-va; n=(vv-va)/dv
    def cross(x):
        i=np.argmax(n>=x); return tt[i] if n[i]>=x else np.nan
    sr=0.8*abs(dv)/(cross(0.9)-cross(0.1))/1e6
    os_=max(0,(n.max()-1)*100)
    out=np.abs(n-1)>0.01; ts=(tt[np.where(out)[0][-1]]-t0)*1e6 if out.any() else 0
    # ringing: extrema of n-1 after the first crossing of 1 that exceed 0.2 % of |dv|
    i1=np.argmax(n>=1) if (n>=1).any() else len(n)-1; e=n[i1:]-1
    ext=[k for k in range(1,len(e)-1) if (e[k]-e[k-1])*(e[k+1]-e[k])<0 and abs(e[k])>0.002]
    return va,vb,sr,os_,ts,len(ext)
edges=[(2,10,'mid->top'),(10,18,'top->mid'),(18,26,'mid->bottom'),(26,34,'bottom->mid'),(42,50,'bottom->top'),(50,58,'top->bottom')]
out=open(L+'stage8_steps.txt','w')
fig,axs=plt.subplots(2,1,figsize=(9,5.4),sharex=True)
for j,cl in enumerate(('1e-10','3e-10')):
    for v in V:
        f=L+f's15_{v}_{cl}.dat'
        if not os.path.exists(f): continue
        d=np.loadtxt(f); t,y=d[:,0],d[:,1]
        axs[j].plot(t*1e6,y,color=col[v],lw=1.3,label=lab[v])
        for t0,t1,name in edges:
            va,vb,sr,o,ts,nr=stepm(t,y,t0*1e-6,t1*1e-6)
            out.write(f"{v} {cl} {name:12s} {va:.3f}->{vb:.3f} SR {sr:.2f} V/us overshoot {o:.2f} % ts1% {ts:.3f} us ringing-extrema {nr}\n")
    axs[j].set_title('1 kOhm || 100 pF' if cl=='1e-10' else 'unloaded || 300 pF',loc='left',fontsize=9); axs[j].set_ylabel('pad (V)')
axs[1].set_xlabel('t (us)'); axs[0].legend(fontsize=7,frameon=False,loc='lower left')
fig.suptitle('Stage 8: large closed-loop steps mid <-> ends <-> ends (deck 15)',fontsize=9,x=0.01,ha='left'); fig.tight_layout(); fig.savefig('/home/user/c2/K/out/steps_large.png',dpi=150)
out.close()
# rail recovery
o=open(L+'stage8_rail.txt','w'); fig,axs=plt.subplots(2,1,figsize=(9,5),sharex=True)
for v in V:
    f=L+f's16_{v}.dat'
    if not os.path.exists(f): continue
    d=np.loadtxt(f); t,y,a,b=d[:,0],d[:,1],d[:,3],d[:,5]
    axs[0].plot(t*1e6,y,color=col[v],lw=1.3,label=lab[v]); axs[1].plot(t*1e6,a,color=col[v],lw=1.1); axs[1].plot(t*1e6,b,color=col[v],lw=1.1,ls='--')
    for t0,t1,name in ((2,12,'into top rail'),(12,22,'top rail -> mid'),(22,32,'into bottom'),(32,42,'bottom -> mid')):
        m=(t>=t0*1e-6)&(t<=t1*1e-6); tt,yy=t[m],y[m]; vf=yy[-20:].mean(); va=np.interp(t0*1e-6-1e-8,t,y); dv=vf-va
        n=(yy-va)/dv; outb=np.abs(n-1)>0.01; ts=(tt[np.where(outb)[0][-1]]-t0*1e-6)*1e6 if outb.any() else 0
        os_=max(0,(n.max()-1)*100); delay=(tt[np.argmax(np.abs(yy-va)>0.01)]-t0*1e-6)*1e6
        o.write(f"{v} {name:16s} pad {va:.3f} -> {vf:.3f} V; a {np.interp(t1*1e-6-1e-8,t,a):.3f} b {np.interp(t1*1e-6-1e-8,t,b):.3f}; delay(10 mV) {delay:.3f} us; ts1% {ts:.3f} us; overshoot {os_:.2f} %\n")
axs[0].set_ylabel('pad (V)'); axs[1].set_ylabel('a (solid), b (dashed) (V)'); axs[1].set_xlabel('t (us)'); axs[0].legend(fontsize=7,frameon=False)
fig.suptitle('Stage 8: rail drive and recovery, vd 0 -> +3 -> 0 -> -3 -> 0 V, 1 kOhm || 100 pF (deck 16)',fontsize=9,x=0.01,ha='left'); fig.tight_layout(); fig.savefig('/home/user/c2/K/out/rail_recovery.png',dpi=150)
o.close()
