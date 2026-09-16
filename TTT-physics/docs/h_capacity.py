import numpy as np, itertools, time
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
phi=(1+5**.5)/2
RHH=2.1   # Switendick minimum H-H distance (Angstrom) at ambient pressure
def mis(P,box,thr):
    """max independent set fraction: sites P (N,3) in periodic box (3,), no two closer than thr"""
    N=len(P); edges=[]
    for i in range(N):
        d=P[i+1:]-P[i]
        if box is not None: d-=box*np.round(d/box)
        r=np.linalg.norm(d,axis=1)
        for j in np.where(r<thr-1e-9)[0]: edges.append((i,i+1+j))
    if not edges: return N
    A=lil_matrix((len(edges),N))
    for k,(i,j) in enumerate(edges): A[k,i]=1; A[k,j]=1
    res=milp(c=-np.ones(N),constraints=LinearConstraint(A.tocsr(),-np.inf,1),integrality=np.ones(N),bounds=Bounds(0,1),options={"time_limit":15})
    return round(-res.fun)
def lattice(kind,d,n):
    if kind=="fcc":
        a=d*np.sqrt(2); atoms=[(0,0,0),(0,.5,.5),(.5,0,.5),(.5,.5,0)]
        tet=[(x,y,z) for x in (.25,.75) for y in (.25,.75) for z in (.25,.75)]
        octs=[(.5,.5,.5),(.5,0,0),(0,.5,0),(0,0,.5)]
    else:
        a=d*2/np.sqrt(3); atoms=[(0,0,0),(.5,.5,.5)]
        tet=[]
        for p in itertools.permutations((.5,.25,0)): tet.append(p)
        for p in itertools.permutations((.5,.75,0)): tet.append(p)
        tet=list({tuple(np.round(t,3)) for t in tet}); assert len(tet)==12
        octs=[(.5,.5,0),(.5,0,.5),(0,.5,.5),(.5,0,0),(0,.5,0),(0,0,.5)]
    cells=np.array(list(itertools.product(range(n),repeat=3)))
    rep=lambda B: (np.array([c+np.array(b) for c in cells for b in B]))*a
    return rep(atoms),rep(tet),rep(octs),np.array([n*a]*3)
def cap_lattice(kind,d,n=2):
    at,te,oc,box=lattice(kind,d,n); M=len(at)
    allsites=np.vstack([te,oc])
    return {"tet only":mis(te,box,RHH)/M,"oct only":mis(oc,box,RHH)/M,"tet+oct":mis(allsites,box,RHH)/M}
# ---- block 1 : site counts per metal atom (no exclusion)
at,te,oc,_=lattice("fcc",1,1); assert (len(te)/len(at),len(oc)/len(at))==(2,1)
at,te,oc,_=lattice("bcc",1,1); assert (len(te)/len(at),len(oc)/len(at))==(6,3)
# ---- block 2 : ideal icosahedral order = 600-cell (vertices = 2I, 120 atoms, 600 tetrahedra, Z=12)
V=[]
for s in itertools.product([.5,-.5],repeat=4): V.append(np.array(s))
for i in range(4):
    for s in (1,-1):
        v=np.zeros(4); v[i]=s; V.append(v)
evenperm=[p for p in itertools.permutations(range(4)) if sum(1 for i in range(4) for j in range(i+1,4) if p[i]>p[j])%2==0]
for p in evenperm:
    for s in itertools.product([1,-1],repeat=3):
        base=np.array([phi/2*s[0],.5*s[1],1/(2*phi)*s[2],0.0]); v=np.zeros(4)
        for k in range(4): v[p[k]]=base[k]
        if not any(np.allclose(v,w) for w in V): V.append(v)
V=np.array(V); assert len(V)==120
G=V@V.T; E=np.isclose(G,phi/2)
assert all(E[i].sum()==12 for i in range(120))                 # Z = 12 for every atom
cells=[]
for i in range(120):
    nb=np.where(E[i])[0]
    for j,k,l in itertools.combinations(nb,3):
        if i<j<k<l and E[j,k] and E[j,l] and E[k,l]: cells.append((i,j,k,l))
assert len(cells)==600                                          # 5 tetrahedral sites per atom
C=np.array([V[list(c)].mean(0) for c in cells])
edge=1/phi                                                      # chord edge of 600-cell on unit S^3
def cap600(d):
    P=C*(d/edge)                                                # scale so metal-metal edge = d
    return mis(P,None,RHH)/120
# ---- block 3 : scan metal-metal distance
ds=[2.75,2.9,3.05,3.2,3.4,3.7,4.0]
t0=time.time(); table=[]
for d in ds:
    f=cap_lattice("fcc",d); b=cap_lattice("bcc",d); i=cap600(d)
    table.append((d,f,b,i)); print(d,max(f.values()),max(b.values()),i,flush=True)
# ---- block 4 : sanity versus known hydrides (metal sublattice d from representative lattice constants)
known={"PdH (fcc, d~2.85)":2.85,"TiH2 (fcc, d~3.15)":3.15,"ZrH2 (d~3.38)":3.38,"YH3/YH2 (fcc, d~3.68)":3.68,"LaH3 (fcc, d~3.96)":3.96}
res_known={k:cap_lattice("fcc",d) for k,d in known.items()}
assert max(res_known["PdH (fcc, d~2.85)"].values())==1.0
assert max(res_known["TiH2 (fcc, d~3.15)"].values())==2.0
assert max(res_known["ZrH2 (d~3.38)"].values())==2.0
assert max(res_known["LaH3 (fcc, d~3.96)"].values())==3.0
print("blocks PASS  (time %.0fs)"%(time.time()-t0))
print("d(A) | fcc best | bcc best | icosahedral(600-cell)")
for d,f,b,i in table: print(f"{d:4.2f} | {max(f.values()):.2f} {f} | {max(b.values()):.2f} {b} | {i:.2f}")
for k,v in res_known.items(): print(k,v)
