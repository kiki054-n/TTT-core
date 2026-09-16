import numpy as np, itertools
from scipy.optimize import minimize
me,mmu=0.51099895,105.6583755
for mtau,dt in [(1776.93,0.09),(1776.86,0.12)]:
    pass
mtau,dt=1776.93,0.09
R_mu,R_tau=mmu/me,mtau/me
# ---- 1 spring network: pentagonal bipyramid + axis edge (5 regular tetrahedra), rest length 1
Rr=1/(2*np.sin(np.pi/5))
def build(R,h):
    ring=[np.array([R*np.cos(2*np.pi*k/5),R*np.sin(2*np.pi*k/5),0]) for k in range(5)]
    return [np.array([0,0,h]),np.array([0,0,-h])]+ring
edges=[(0,1)]+[(p,2+k) for p in (0,1) for k in range(5)]+[(2+k,2+(k+1)%5) for k in range(5)]
assert len(edges)==16
E=lambda X: 0.5*sum((np.linalg.norm(X[i]-X[j])-1)**2 for i,j in edges)
h_nat=np.sqrt(1-Rr**2)
modes={
 "A axis stretch":E(build(Rr,h_nat)),                               # ring & lateral exact, axis 1.0515
 "B ring stretch":E(build(np.sqrt(0.75),0.5)),                      # axis & lateral exact
 "C lateral compress":E(build(Rr,0.5)),                             # axis & ring exact
}
res=minimize(lambda v:E(build(np.sqrt(1)*v[0],v[1])),[Rr,0.5]); modes["D relaxed (sym)"]=res.fun
X0=np.array(build(Rr,0.5))+1e-3*np.random.default_rng(0).normal(size=(7,3))
res2=minimize(lambda v:E(list(v.reshape(7,3))),X0.ravel(),method="BFGS")
assert res2.fun<=modes["D relaxed (sym)"]+1e-9
vals=sorted(modes.values()); r1,r2=vals[1]/vals[0],vals[2]/vals[0]
assert r2<5                                     # all modes within a factor of a few
# exponent needed to turn energy ratios into lepton mass ratios: must be one p for both
p1=np.log(R_mu)/np.log(r1); p2=np.log(R_tau)/np.log(r2)
# ---- 2 Koide
sq=np.sqrt([me,mmu,mtau]); Q=sum([me,mmu,mtau])/sq.sum()**2
dQ=(lambda m:(sum([me,mmu,m])/(np.sqrt([me,mmu,m]).sum())**2))
sQ=abs(dQ(mtau+dt)-dQ(mtau-dt))/2
# Brannen form sqrt(m_k)=mu(1+sqrt2 cos(delta+2pi k/3)): fit delta
mu=sq.sum()/3
cosk=(sq/mu-1)/np.sqrt(2)
def dfit(m):
    s=np.sqrt([me,mmu,m]); u=s.sum()/3; c=(s/u-1)/np.sqrt(2)
    best=None
    for d in np.linspace(0,2*np.pi/3,200001):
        pred=np.cos(d+2*np.pi*np.arange(3)/3)
        err=np.min([np.sum((np.sort(pred)-np.sort(c))**2)])
        if best is None or err<best[0]: best=(err,d)
    return best[1]
delta=dfit(mtau); sd=abs(dfit(mtau+dt)-dfit(mtau-dt))/2
gap=np.radians(360-5*np.degrees(np.arccos(1/3)))
ratio=delta/gap
# ---- 3 null control for "delta = (simple factor) x (TTT angle)"
factors={"1":1,"2":2,"3":3,"4":4,"5":5,"1/2":.5,"1/3":1/3,"2/3":2/3,"3/2":1.5,"sqrt2":2**.5,"sqrt3":3**.5,"sqrt5":5**.5,
         "phi":(1+5**.5)/2,"1/phi":2/(1+5**.5),"pi":np.pi,"1/pi":1/np.pi,"sqrt2/2":2**-.5,"sqrt3/2":3**.5/2,"2/9":2/9}
angles={"gap":gap,"2pi/5":2*np.pi/5,"pi/5":np.pi/5,"tet":np.arccos(1/3),"magic":np.arccos(1/np.sqrt(3)),"pi/3":np.pi/3,"1rad":1.0}
cands=[(f"{fn}*{an}",fv*av) for fn,fv in factors.items() for an,av in angles.items()]
tol=max(3*sd,abs(delta)*1e-4)
hits=[n for n,v in cands if abs(v-delta)<tol]
lo,hi=0.05,1.5
dens=sum(1 for _,v in cands if lo<v<hi)*2*tol/(hi-lo)   # expected chance hits
print("PASS blocks 1-3")
print("mode energies",{k:f"{v:.3e}" for k,v in modes.items()})
print(f"ratios r1={r1:.3f} r2={r2:.3f} ; needed p: mu {p1:.2f}, tau {p2:.2f}")
print(f"Koide Q={Q:.7f} +/- {sQ:.7f}  (2/3 diff = {(Q-2/3)/sQ:.2f} sigma)")
print(f"delta={delta:.6f} +/- {sd:.6f} rad ; 2/9={2/9:.6f} ; delta/gap={ratio:.5f} ; sqrt3={3**.5:.5f}")
print("hits:",hits," candidates:",len(cands)," expected chance hits:",round(dens,3))
