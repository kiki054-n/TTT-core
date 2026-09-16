import numpy as np, itertools
from scipy.spatial import Delaunay
def periodic_voids(frac_atoms,n_rep=3):
    """Delaunay tetrahedra of a cubic lattice (a=1); returns atoms, circumcentres in the home cell, per-atom void lists"""
    A=np.array(frac_atoms,float)
    shifts=np.array(list(itertools.product(range(-1,n_rep-1),repeat=3)))
    P=np.array([a+s for s in shifts for a in A]); idx=np.array([i for s in shifts for i in range(len(A))])
    tri=Delaunay(P); cents=[]
    for simp in tri.simplices:
        X=P[simp]; M=2*(X[1:]-X[0]); b=(X[1:]**2).sum(1)-(X[0]**2).sum()
        if abs(np.linalg.det(M))<1e-12: continue
        c=np.linalg.solve(M,b)
        if np.all(c>=-1e-9) and np.all(c<1-1e-9): cents.append(c)
    U=[]
    for c in cents:
        if not any(np.linalg.norm(c-u)<1e-6 for u in U): U.append(c)
    return A,np.array(U)
def around(atom,voids,rcut):
    out=[]
    for s in itertools.product((-1,0,1),repeat=3):
        d=voids+np.array(s)-atom; r=np.linalg.norm(d,axis=1)
        out+=list(r[r<rcut])
    return sorted(out)
def coord(atom,atoms):
    ds=[]
    for s in itertools.product((-1,0,1),repeat=3):
        for a in atoms:
            r=np.linalg.norm(a+np.array(s)-atom)
            if r>1e-9: ds.append(r)
    return np.array(sorted(ds))
# ---- A15 (Pm-3n): B at 2a, A at 6c
B=[(0,0,0),(.5,.5,.5)]; Aat=[(.25,0,.5),(.75,0,.5),(.5,.25,0),(.5,.75,0),(0,.5,.25),(0,.5,.75)]
atoms,voids=periodic_voids(B+Aat)
assert len(atoms)==8 and len(voids)==46            # 46 tetrahedral voids per 8 atoms  -> 5.75 per atom
# coordination: B -> 12 , A -> 14 (Frank-Kasper)
cB=coord(np.array(B[0]),atoms); cA=coord(np.array(Aat[0]),atoms)
ZB=int((cB<0.5*1.2).sum()) ; 
# use first coordination shell by gap
def Z(c):
    for k in range(10,17):
        if c[k]-c[k-1]>0.05 and k>=12: return k
ZB,ZA=Z(cB),Z(cA); assert (ZB,ZA)==(12,14)
Zbar=(2*ZB+6*ZA)/8; assert np.isclose((Zbar-2)/2,46/8)
# voids around each atom = 2Z-4 (pentagonal dodecahedron 20 around B, 24 around A)
nvB=len([r for r in around(np.array(B[0]),voids,0.6)]); nvA=len([r for r in around(np.array(Aat[0]),voids,0.6)])
# pick shell by distance clustering
def shell_count(atom):
    rs=np.array(around(atom,voids,0.9))
    # first shell: voids that are circumcentres of tetrahedra containing the atom == closest cluster
    gaps=np.diff(rs); k=np.argmax(gaps[:40]>0.04)+1
    return k
nB,nA=shell_count(np.array(B[0])),shell_count(np.array(Aat[0]))
assert (nB,nA)==(20,24)
# framework of voids is 4-connected (clathrate I = sp3 network)
Dv=[]
for i,v in enumerate(voids):
    ds=[]
    for s in itertools.product((-1,0,1),repeat=3):
        d=np.linalg.norm(voids+np.array(s)-v,axis=1); ds+=list(d[d>1e-9])
    Dv.append(sorted(ds)[:5])
Dv=np.array(Dv)
# ---- bcc: 24 tetrahedral voids around atom (sodalite H24), per atom 6 ; Z=14
atb,vb=periodic_voids([(0,0,0),(.5,.5,.5)])
# bcc Delaunay is degenerate-free? tetrahedral sites count 12 per cell
assert len(vb)==12 and np.isclose((14-2)/2,len(vb)/2)
# CaH6 consistency: nearest 12d-12d distance = a*sqrt2/4 ; PNAS gives 1.24 A at 150 GPa
a_CaH6=1.24/(np.sqrt(2)/4); dCaCa=a_CaH6*np.sqrt(3)/2
# ---- counts rules
rules={"ico (Z=12, not space-filling)":(12-2)/2,"A15 (Zbar=13.5)":5.75,"C15 Laves (Zbar=40/3)":(40/3-2)/2,"bcc (Z=14, 8+6)":6.0}
assert np.isclose(rules["C15 Laves (Zbar=40/3)"],136/24)       # type-II clathrate 136 framework / 24 cages
# ---- clathrate cage free space estimate (5^12 cage)
bond=2.50; r_cage=bond*np.sqrt(3)/(2/((1+5**.5)/2))*1   # circumradius/edge of dodecahedron = sqrt3*phi/2 = 1.401
r_cage=bond*1.4012585; free=r_cage-1.22
sp3_def=np.degrees(np.arccos(-1/3))-108
print("all blocks PASS")
print("A15: voids/cell",len(voids)," Z(B,A)",(ZB,ZA)," voids around B,A",(nB,nA)," void-void nearest distances (a units):",np.round(np.unique(np.round(Dv[:,:4],4)),4))
print("rule H/M=(Zbar-2)/2:",rules)
print(f"CaH6: a={a_CaH6:.3f} A, Ca-Ca={dCaCa:.3f} A (from H-H 1.24 A)")
print(f"5^12 cage: radius {r_cage:.2f} A for bond {bond} A; free radius ~{free:.2f} A ; sp3 vs pentagon angle deficit {sp3_def:.3f} deg")
