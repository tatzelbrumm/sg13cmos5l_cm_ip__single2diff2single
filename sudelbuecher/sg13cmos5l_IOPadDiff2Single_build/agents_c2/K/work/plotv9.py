# stage 7: PM / fc / GM over the swing, v0 and v8 (deck 13) against v9 (deck 14)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
L='/home/user/c2/K/out/logs/'
rows=[l.split() for f in ('loop13.dat','loop14.dat') for l in open(L+f) if l.split()[0] in ('v0','v8','v9')]
col={'v0':'#2a78d6','v8':'#6250d6','v9':'#eb6834'}; lab={'v0':'v0 present','v8':'v8 present orientation, sym 2 kOhm','v9':'v9 both turned, sym 2 kOhm'}
plt.rcParams.update({'font.size':8,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':'#e4e3df'})
fig,axs=plt.subplots(2,3,figsize=(10,5.6),sharex=True)
for j,cl in enumerate(('1e-10','3e-10')):
    for i,(k,yl,sc) in enumerate(((8,'PM (deg)',1),(7,'fc (MHz)',1e-6),(9,'GM (dB)',1))):
        ax=axs[j,i]
        for v in col:
            d=sorted([(float(r[3]),float(r[k])*sc) for r in rows if r[0]==v and r[1]==cl]); x,y=np.array(d).T
            ax.plot(x,y,'-o',ms=3,lw=1.6,color=col[v],label=lab[v])
        ax.set_ylabel(yl); ax.axvline(1.65,color='#52514e',lw=0.6,ls=':')
        ax.set_title(('1 kOhm || 100 pF' if cl=='1e-10' else 'unloaded || 300 pF')+': '+yl.split()[0],loc='left',fontsize=9)
for ax in axs[1]: ax.set_xlabel('pad (V)')
axs[0,1].legend(fontsize=7,frameon=False,loc='upper center')
fig.suptitle('Stage 7: both capacitors turned behind symmetric 2 kOhm stages (v9) vs v0 / v8, decks 13 / 14',fontsize=9,x=0.01,ha='left')
fig.tight_layout(); fig.savefig('/home/user/c2/K/out/pm_fc_gm_v9.png',dpi=150)
for v in col:
    for cl in ('1e-10','3e-10'):
        q=[r for r in rows if r[0]==v and r[1]==cl]; pm=[float(r[8]) for r in q]; gm=[float(r[9]) for r in q]; fc=[float(r[7])/1e6 for r in q]
        k=int(np.argmin(pm)); print(v,cl,'PMmin',min(pm),'@',q[k][3],'PMmax',max(pm),'GMmin',min(gm),'fc',round(min(fc),3),round(max(fc),3))
