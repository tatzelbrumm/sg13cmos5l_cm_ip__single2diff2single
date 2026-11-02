# step responses of deck 8 (all variants)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
col=['#2a78d6','#eb6834','#1baf7a','#eda100','#6250d6']
lab={'v0':'v0 present','v1':'v1 S-Varicap both','v2':'v2 S-Varicap 70 / hv PMOS 30 both','v3':'v3 CMB hv PMOS turned','v4':'v4 CMB S-Varicap 80/20 pair'}
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':'#e4e3df'})
fig,axs=plt.subplots(1,2,figsize=(8,3.4))
for i,v in enumerate(lab):
    d=np.loadtxt(f'/home/user/c2/K/out/logs/step8_{v}.dat'); t=d[:,0]*1e6
    for ax,(a,b) in zip(axs,((0.8,2.0),(12.8,14.0))):
        m=(t>=a)&(t<=b); ax.plot(t[m],d[m,1],color=col[i],lw=1.6,label=lab[v])
axs[0].set_title('step 1: pad 1.40 -> 1.90 V',loc='left',fontsize=10); axs[1].set_title('step 2: pad 2.05 -> 2.29 V',loc='left',fontsize=10)
for ax in axs: ax.set_xlabel('t (us)')
axs[0].set_ylabel('pad (V)'); axs[0].legend(fontsize=7,frameon=False,loc='lower right')
fig.suptitle('Closed-loop steps, 1 kOhm || 100 pF, tt 27 C (deck 8)',fontsize=10,x=0.01,ha='left'); fig.tight_layout(); fig.savefig('/home/user/c2/K/out/step_response.png',dpi=150)
