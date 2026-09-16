import numpy as np, itertools
from scipy.linalg import expm
from scipy.optimize import linprog
rng=np.random.default_rng(2)
Z=np.zeros((2,2));I2=np.eye(2)
p=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.array([[1,0],[0,-1]],complex)]
g0=np.block([[I2,Z],[Z,-I2]]).astype(complex)
g=[g0]+[np.block([[Z,pk],[-pk,Z]]) for pk in p]
Id=np.eye(4); I=g[0]@g[1]@g[2]@g[3]; sig=[g[k+1]@g0 for k in range(3)]
V=lambda a: sum(a[k]*sig[k] for k in range(3))
def split(M):
    return (np.array([np.trace(M@s).real/4 for s in sig]), np.array([-np.trace(M@I@s).real/4 for s in sig]))
unit=lambda x:x/np.linalg.norm(x)
# 1 two kinds of bipolar pair: A=(+I,-I): sum 0, product 1 ; B=(P+,P-): sum 1, product 0
for _ in range(20):
    k=unit(rng.normal(size=3)); Pp=(Id+V(k))/2; Pm=(Id-V(k))/2
    assert np.allclose(Pp@Pp,Pp) and np.allclose(Pm@Pm,Pm)
    assert np.allclose(Pp+Pm,Id) and np.allclose(Pp@Pm,0) and np.allclose(Pm@Pp,0)
assert np.allclose(I+(-I),0) and np.allclose(I@(-I),Id)
# 2 single plane wave: E(1+k)=(1-k)E  => F^2=(1+k)(1-k)E^2=0 : null because it carries both poles
for _ in range(20):
    k=unit(rng.normal(size=3)); E=np.cross(k,rng.normal(size=3))
    assert np.allclose(V(E)@(Id+V(k)),(Id-V(k))@V(E))
    F=(Id+V(k))@V(E); assert np.allclose(F@F,0)
    Ef,Bf=split(F); assert np.allclose(Ef,E) and np.allclose(Bf,np.cross(k,E))
# 3 helicity = sign of I : F(th)=exp(-/+ I th) F0 rotates E one way or the other about k
e1,e2,e3=np.eye(3); F0=(Id+V(e3))@V(e1)
for th in np.linspace(0,2*np.pi,13):
    Em,_=split(expm(-I*th)@F0); Ep,_=split(expm(I*th)@F0)
    assert np.allclose(Em,np.cos(th)*e1+np.sin(th)*e2) and np.allclose(Ep,np.cos(th)*e1-np.sin(th)*e2)
# 4 invariant mass of photon sets (each energy 1, momentum = unit direction)
def mass(D): D=np.array(D,float); P=D.sum(0); return np.sqrt(max(len(D)**2-P@P,0))
tet=[unit(np.array(v)) for v in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]]
octa=[s*e for e in np.eye(3) for s in (1,-1)]
tri=[np.array([np.cos(a),np.sin(a),0]) for a in (0,2*np.pi/3,4*np.pi/3)]
cases={"same dir x2":[e3,e3],"opposite x2":[e3,-e3],"triangle x3":tri,"tetra x4":tet,"octa x6":octa}
M={n:mass(D) for n,D in cases.items()}
assert np.isclose(M["same dir x2"],0) and np.isclose(M["opposite x2"],2) and np.isclose(M["triangle x3"],3)
assert np.isclose(M["tetra x4"],4) and np.isclose(M["octa x6"],6)
# 5 positive spanning of R^3 (every direction reachable by non-negative combination)
def posspan(D):
    A=np.array(D).T
    for t in list(np.eye(3))+list(-np.eye(3)):
        r=linprog(np.zeros(len(D)),A_eq=A,b_eq=t,bounds=[(0,None)]*len(D))
        if r.status!=0: return False
    return True
PS={n:posspan(D) for n,D in cases.items()}
assert PS=={"same dir x2":False,"opposite x2":False,"triangle x3":False,"tetra x4":True,"octa x6":True}
for _ in range(300):   # no 3 vectors ever positively span R^3 (theorem: minimum is d+1=4)
    assert not posspan([unit(rng.normal(size=3)) for _ in range(3)])
# 6 superposition is no longer null: opposite pair -> pure standing E field, F^2>0
F=(Id+V(e3))@V(e1)+(Id-V(e3))@V(e1); assert np.allclose(F,2*V(e1)) and np.allclose(F@F,4*Id)
Ft=sum((Id+V(d))@V(unit(np.cross(d,rng.normal(size=3)))) for d in tet)
assert not np.allclose(Ft@Ft,0)
print("all 6 blocks PASS"); print(M); print(PS)
