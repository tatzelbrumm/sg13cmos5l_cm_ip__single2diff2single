# pole-zero fit of the loop gain T(jw) from deck 13's AC data (ngspice .pz does not converge on this circuit):
# vector fitting (Gustavsen & Semlyen 1999) in the real formulation, 1 Hz ... fmax, order N, relative weighting.
# Zeros = eig(A - b c^T / d) of the fitted state-space model. Units Hz; real part < 0 = LHP.
import numpy as np, sys
def basis(s,poles):
    cols=[];
    for p in poles:
        if abs(p.imag)<1e-12*abs(p): cols.append(1/(s-p.real))
        else: cols+= [1/(s-p)+1/(s-p.conjugate()), 1j/(s-p)-1j/(s-p.conjugate())]
    return np.array(cols).T
def ss(poles):
    n=sum(1 if abs(p.imag)<1e-12*abs(p) else 2 for p in poles); A=np.zeros((n,n)); b=np.zeros(n); k=0
    for p in poles:
        if abs(p.imag)<1e-12*abs(p): A[k,k]=p.real; b[k]=1; k+=1
        else: A[k:k+2,k:k+2]=[[p.real,p.imag],[-p.imag,p.real]]; b[k]=2; k+=2
    return A,b
def topoles(ev):
    ev=np.where(ev.real>0,-ev.real+1j*ev.imag,ev); out=[]
    for e in ev:
        if abs(e.imag)<1e-9*abs(e): out.append(complex(e.real,0))
        elif e.imag>0: out.append(e)
    return out
def vf(s,H,N,it=15):
    w0=np.logspace(np.log10(abs(s[0])),np.log10(abs(s[-1])),N//2)
    poles=[complex(-x/100,x) for x in w0]
    W=1/np.abs(H)
    for _ in range(it):
        P=basis(s,poles); M=np.hstack([P,np.ones((len(s),1)),-H[:,None]*P])*W[:,None]
        Mr=np.vstack([M.real,M.imag]); rhs=np.concatenate([(H*W).real,(H*W).imag])
        x=np.linalg.lstsq(Mr,rhs,rcond=None)[0]; ct=x[P.shape[1]+1:]
        A,b=ss(poles); poles=topoles(np.linalg.eigvals(A-np.outer(b,ct)))
    P=basis(s,poles); M=np.hstack([P,np.ones((len(s),1))])*W[:,None]
    x=np.linalg.lstsq(np.vstack([M.real,M.imag]),np.concatenate([(H*W).real,(H*W).imag]),rcond=None)[0]
    c,d=x[:-1],x[-1]; Hf=(P@c)+d; A,b=ss(poles)
    allp=np.linalg.eigvals(A); z=np.linalg.eigvals(A-np.outer(b,c)/d) if abs(d)>0 else np.array([])
    return allp,z,Hf
def fit(f,N=6,fmax=3e8):
    d=np.loadtxt(f); fr=d[:,0]; T=10**(d[:,1]/20)*np.exp(1j*np.deg2rad(d[:,3]))
    m=(fr>=1)&(fr<=fmax); s=2j*np.pi*fr[m]; H=T[m]
    p,z,Hf=vf(s/(2*np.pi*1e6),H,N)           # frequency scaled to MHz for conditioning
    edb=np.sqrt(np.mean((20*np.log10(abs(Hf)/abs(H)))**2)); eph=np.sqrt(np.mean(np.rad2deg(np.angle(Hf/H))**2))
    return p*1e6,z*1e6,edb,eph
fmt=lambda v:' '.join(f"{x.real:+.3g}{x.imag:+.3g}j" for x in sorted(v,key=abs))
if __name__=='__main__':
    for f in sys.argv[1:]:
        for N in (4,6,8,10):
            p,z,edb,eph=fit(f,N)
            print(f.split('/')[-1],N,f"err {edb:.3f} dB {eph:.2f} deg\n  poles {fmt(p)}\n  zeros {fmt(z)}")
