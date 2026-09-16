import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(1)
Z=np.zeros((2,2));I2=np.eye(2)
p=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.array([[1,0],[0,-1]],complex)]
g0=np.block([[I2,Z],[Z,-I2]]).astype(complex)
g=[g0]+[np.block([[Z,pk],[-pk,Z]]) for pk in p]
eta=np.diag([1,-1,-1,-1]); Id=np.eye(4)
I=g[0]@g[1]@g[2]@g[3]
sig=[g[k+1]@g0 for k in range(3)]
V=lambda a: sum(a[k]*sig[k] for k in range(3))
F_of=lambda E,B: V(E)+I@V(B)
sc=lambda M: np.trace(M).real/4
def split(M):  # E and B components of a bivector
    E=np.array([np.trace(M@s).real/4 for s in sig]); B=np.array([-np.trace(M@I@s).real/4 for s in sig]); return E,B
# 1 metric, pseudoscalar
for m in range(4):
    for n in range(4): assert np.allclose((g[m]@g[n]+g[n]@g[m])/2, eta[m,n]*Id)
assert np.allclose(I@I,-Id); assert np.allclose(I@(-I),Id)
assert all(np.allclose(I@gm,-gm@I) for gm in g)          # I anticommutes with vectors
assert all(np.allclose(I@s,s@I) for s in sig)             # commutes with bivectors
# 2 relative vectors = Pauli algebra; sigma1 sigma2 sigma3 = I (same I as Cl(3))
assert all(np.allclose(s@s,Id) for s in sig); assert np.allclose(sig[0]@sig[1]@sig[2],I)
# 3 F^2 = (E^2-B^2) + 2 I (E.B): two invariants as one "complex" number
for _ in range(50):
    E,B=rng.normal(size=3),rng.normal(size=3); F=F_of(E,B)
    assert np.allclose(F@F,(E@E-B@B)*Id+2*(E@B)*I)
    E2,B2=split(F); assert np.allclose(E2,E) and np.allclose(B2,B)
# 4 duality: I F -> (E,B)=(-B,E), I^2 F=-F ; e^{I th} rotation keeps F^2? (F^2 -> e^{2I th}F^2), energy/momentum invariant
for _ in range(20):
    E,B=rng.normal(size=3),rng.normal(size=3); F=F_of(E,B)
    E2,B2=split(I@F); assert np.allclose(E2,-B) and np.allclose(B2,E)
    th=rng.normal(); Fr=expm(I*th)@F; Er,Br=split(Fr)
    assert np.isclose(E@E+B@B,Er@Er+Br@Br) and np.allclose(np.cross(E,B),np.cross(Er,Br))
# 5 Lorentz force: q F.u (dot = antisym part) vs tensor form
for _ in range(50):
    E,B=rng.normal(size=3),rng.normal(size=3); v=rng.normal(size=3); v=0.9*v/np.linalg.norm(v)*rng.random()
    gam=1/np.sqrt(1-v@v); u=gam*(g0+sum(v[k]*g[k+1] for k in range(3))); q=1.3
    F=F_of(E,B); f=q*(F@u-u@F)/2
    comp=np.array([np.trace(f@g[m]).real/4*eta[m,m] for m in range(4)])
    assert np.isclose(comp[0],q*gam*(E@v))                         # power: B absent
    assert np.allclose(comp[1:],q*gam*(E+np.cross(v,B)))           # Lorentz force
# 6 boost rotor: F' = R F R~ gives standard field transformation
for _ in range(30):
    E,B=rng.normal(size=3),rng.normal(size=3); n=rng.normal(size=3); n/=np.linalg.norm(n); ph=rng.random()*2
    v=np.tanh(ph)*n; gam=np.cosh(ph)
    R=expm(-ph/2*V(n)); Rr=expm(ph/2*V(n))
    Ep,Bp=split(R@F_of(E,B)@Rr)
    par=lambda x: (x@n)*n
    Ee=par(E)+gam*((E-par(E))+np.cross(v,B)); Be=par(B)+gam*((B-par(B))-np.cross(v,E))
    assert np.allclose(Ep,Ee) and np.allclose(Bp,Be)
    Fp=R@F_of(E,B)@Rr; assert np.allclose(Fp@Fp,F_of(E,B)@F_of(E,B))
# 7 null field (light): E.B=0,|E|=|B| -> F^2=0 but F!=0 ; plane-wave form F=(1+k)E
for _ in range(20):
    k=rng.normal(size=3);k/=np.linalg.norm(k); E=np.cross(k,rng.normal(size=3)); B=np.cross(k,E)
    F=F_of(E,B); assert np.allclose(F@F,0) and not np.allclose(F,0)
    assert np.allclose(F,(Id+V(k))@V(E))
# 8 parity (g0->g0, gk->-gk): I->-I, E->-E, B->+B
P=[g0]+[-gk for gk in g[1:]]; IP=P[0]@P[1]@P[2]@P[3]; assert np.allclose(IP,-I)
sigP=[P[k+1]@P[0] for k in range(3)]; assert all(np.allclose(a,-b) for a,b in zip(sigP,sig))
E,B=rng.normal(size=3),rng.normal(size=3)
FP=sum(E[k]*sigP[k] for k in range(3))+IP@sum(B[k]*sigP[k] for k in range(3))
Ex,Bx=split(FP); assert np.allclose(Ex,-E) and np.allclose(Bx,B)
print("all 8 blocks PASS")
