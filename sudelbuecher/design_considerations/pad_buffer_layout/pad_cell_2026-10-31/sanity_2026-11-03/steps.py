# step metrics as K's stage8.py (stepm): 10-90 % slew, overshoot, 1 % settling, ringing extrema > 0.2 %
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def stepm(t,v,t0,t1):
    m=(t>=t0)&(t<=t1); tt,vv=t[m],v[m]
    va=np.interp(t0-0.01e-6,t,v); vb=vv[-20:].mean(); dv=vb-va; n=(vv-va)/dv
    def cross(x):
        i=np.argmax(n>=x); return tt[i] if n[i]>=x else np.nan
    sr=0.8*abs(dv)/(cross(0.9)-cross(0.1))/1e6
    os_=max(0,(n.max()-1)*100)
    out=np.abs(n-1)>0.01; ts=(tt[np.where(out)[0][-1]]-t0)*1e6 if out.any() else 0
    i1=np.argmax(n>=1) if (n>=1).any() else len(n)-1; e=n[i1:]-1
    ext=[k for k in range(1,len(e)-1) if (e[k]-e[k-1])*(e[k+1]-e[k])<0 and abs(e[k])>0.002]
    return va,vb,sr,os_,ts,len(ext)
edges=[(2,10,'mid +0.1 V'),(10,18,'back to mid'),(18,26,'mid->bottom'),(26,34,'bottom->top'),(34,42,'top->mid')]
fig,axs=plt.subplots(2,1,figsize=(9,5.4),sharex=True)
with open('steps.txt','w') as o:
    for j,cl in enumerate(('1e-10','3e-10')):
        d=np.loadtxt(f'step_{cl}.dat'); t,y=d[:,0],d[:,1]
        axs[j].plot(t*1e6,y,lw=1.2,color='#2a78d6')
        axs[j].set_title('1 kOhm to 1.65 V || 100 pF' if cl=='1e-10' else 'unloaded || 300 pF',loc='left',fontsize=9); axs[j].set_ylabel('pad (V)')
        for t0,t1,name in edges:
            va,vb,sr,os_,ts,nr=stepm(t,y,t0*1e-6,t1*1e-6)
            line=f"{cl} {name:12s} {va:.3f}->{vb:.3f} V  SR {sr:.2f} V/us  overshoot {os_:.2f} %  ts1% {ts:.3f} us  ringing extrema {nr}"
            print(line); o.write(line+'\n')
axs[1].set_xlabel('t (us)')
fig.suptitle('Sanity run 2026-11-03: closed-loop steps of the backannotated pad cell (sheet netlist, tt, 27 C)',fontsize=9,x=0.01,ha='left')
fig.tight_layout(); fig.savefig('steps.png',dpi=150)
