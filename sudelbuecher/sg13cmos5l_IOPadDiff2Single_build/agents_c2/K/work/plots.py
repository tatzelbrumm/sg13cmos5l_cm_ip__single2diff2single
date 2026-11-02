# plots for stage 2 (C(V)) and stage 3 (C along the swing)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
L='/home/user/c2/K/out/logs/'; O='/home/user/c2/K/out/'
col=['#2a78d6','#eb6834','#1baf7a','#eda100','#e87ba4','#008300','#6250d6','#e34948']
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':'#e4e3df','grid.linewidth':0.6})
hv=np.loadtxt(L+'cv1_hvpmos.dat'); sv=np.loadtxt(L+'cv4_svaricap.dat'); mp=np.loadtxt(L+'cv2_moscap_p.dat'); mn=np.loadtxt(L+'cv3_moscap_n.dat'); mo=np.loadtxt(L+'cv5_mom.dat')
fig,ax=plt.subplots(figsize=(7.5,4.6))
ax.plot(hv[:,0],hv[:,1],color=col[0],lw=2,label='hv PMOS 7.96/32.16 (CMA, CMB now), V = V(G)-V(NW)')
ax.plot(sv[:,0],sv[:,2],color=col[1],lw=2,label='S-Varicap Nx10 9.74/0.8, V = V(G)-V(W)')
ax.plot(sv[:,0],sv[:,1],color=col[1],lw=1.2,ls='--',label='S-Varicap Nx10 3.74/0.3 (spec structure)')
m=abs(mp[:,0])<=1.65; ax.plot(mp[m,0],mp[m,1],color=col[2],lw=2,label='moscap_p 10/10 (thin oxide, |V| <= 1.65 V)')
ax.plot(mp[:,0],mp[:,1],color=col[2],lw=0.8,ls=':')
m=abs(mn[:,0])<=1.65; ax.plot(mn[m,0],mn[m,1],color=col[3],lw=2,label='moscap_n 10/10 (thin oxide, G-substrate only)')
ax.plot(mn[:,0],mn[:,1],color=col[3],lw=0.8,ls=':')
ax.plot(mo[:,0],mo[:,1],color=col[4],lw=2,label='cap_cmomf M1-M2 (per footprint)')
ax.plot(mo[:,0],mo[:,4],color=col[6],lw=2,label='cap_cmomi M1-M4 (per footprint)')
ax.axvspan(-0.17,1.78,color='#f0efec',zorder=0); ax.text(0.8,15.6,'V_GW of CMA / CMB\nover the linear swing',ha='center',va='top',fontsize=8,color='#52514e')
ax.set_xlabel('V across the capacitor (V)'); ax.set_ylabel('C (fF per um2 of gate, MOM: of footprint)')
ax.set_title('Small-signal C(V) at 100 kHz, tt 27 C (ngspice, decks 1-5)',fontsize=10,loc='left')
ax.legend(fontsize=7,frameon=False,loc='center left',bbox_to_anchor=(0.0,0.62)); ax.set_xlim(-3.3,3.3); ax.set_ylim(0,16)
fig.tight_layout(); fig.savefig(O+'cv_candidates.png',dpi=150)
# zoom on thick-oxide devices
fig,ax=plt.subplots(figsize=(7.5,3.8))
ax.plot(hv[:,0],hv[:,1],color=col[0],lw=2,label='hv PMOS, CMA connection (gate a, S/D/NW pad)')
ax.plot(hv[:,0],hv[:,2],color=col[0],lw=1.2,ls='--',label='hv PMOS, CMB connection, vs V(NW)-V(G)')
ax.plot(sv[:,0],sv[:,2],color=col[1],lw=2,label='S-Varicap 9.74/0.8')
ax.set_xlabel('V(gate) - V(well) (V)'); ax.set_ylabel('C (fF/um2 of gate)'); ax.set_ylim(0,6.2); ax.set_xlim(-3.3,3.3)
ax.axhline(4.73,color='#52514e',lw=0.8,ls=':'); ax.text(-3.2,4.8,'C_ox at TGOX1NW 7.3 nm',fontsize=7,color='#52514e')
ax.legend(fontsize=7,frameon=False,loc='lower left'); ax.set_title('Thick-oxide capacitors (decks 1, 4)',fontsize=10,loc='left')
fig.tight_layout(); fig.savefig(O+'cv_thick_oxide.png',dpi=150)
# C along the swing
sw=np.loadtxt(L+'swing_vgw.dat'); vd,pad,vA,vB=sw.T
c_hv=lambda v:np.interp(v,hv[:,0],hv[:,1]); c_sv=lambda v:np.interp(v,sv[:,0],sv[:,2])
fig,axs=plt.subplots(1,2,figsize=(8,3.6),sharey=True)
for ax,vg,name in ((axs[0],vA,'CMA (gate a, well pad)'),(axs[1],vB,'CMB (gate pad, well b)')):
    lin=vd<1.4
    ax.plot(pad[lin],256*c_hv(vg[lin]),color=col[0],lw=2,label='hv PMOS 256 um2 (now)')
    ax.plot(pad[lin],171.4*c_sv(vg[lin]),color=col[1],lw=2,label='S-Varicap 171 um2 gate')
    if 'CMB' in name: ax.plot(pad[lin],140.3*c_sv(vg[lin])+77.9*c_sv(-vg[lin]),color=col[2],lw=2,label='S-Varicap Nx9 || Nx5 turned')
    ax.set_title(name,fontsize=10,loc='left'); ax.set_xlabel('pad (V), DC swing deck 6, 1 kOhm to 1.65 V'); ax.set_ylim(0,1250)
    ax.legend(fontsize=7,frameon=False,loc='lower left' if 'CMA' in name else 'lower right')
axs[0].set_ylabel('C (fF)'); fig.tight_layout(); fig.savefig(O+'c_along_swing.png',dpi=150)
