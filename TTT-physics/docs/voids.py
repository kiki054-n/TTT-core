import numpy as np, itertools
phi=(1+5**.5)/2
def uniq(L,tol=1e-7):
    U=[]
    for p in L:
        if not any(np.linalg.norm(p-q)<tol for q in U): U.append(np.array(p,float))
    return U
def cyc(p):
    out=[]
    for s in itertools.product([1,-1],repeat=3):
        for k in range(3): out.append(np.roll(np.array(p,float)*s,k))
    return uniq(out)
def voro(N,tol=1e-8):
    """Voronoi vertices of the central atom (origin) with neighbours N; returns list of (vertex, degree)"""
    N=[np.array(n,float) for n in N]; V=[]
    for i,j,k in itertools.combinations(range(len(N)),3):
        A=np.array([N[i],N[j],N[k]]); b=np.array([N[i]@N[i],N[j]@N[j],N[k]@N[k]])/2
        if abs(np.linalg.det(A))<1e-10: continue
        x=np.linalg.solve(A,b)
        if all(x@n<=n@n/2+tol for n in N): V.append(x)
    V=uniq(V,1e-6)
    return [(v,sum(1 for n in N if abs(v@n-n@n/2)<1e-6)) for v in V]
def summary(N):
    vs=voro(N); deg={}
    for v,d in vs: deg[d]=deg.get(d,0)+1
    return len(vs),deg,vs
# ---- 1 cluster shells
cub=cyc((0,1,1)); ico=cyc((0,1,phi))
hcp=[np.array([np.cos(k*np.pi/3),np.sin(k*np.pi/3),0]) for k in range(6)]+\
    [np.array([np.cos(k*2*np.pi/3+s)/np.sqrt(3),np.sin(k*2*np.pi/3+s)/np.sqrt(3),z*np.sqrt(2/3)]) for k in range(3) for z,s in ((1,np.pi/6),(-1,np.pi/6))]
bcc14=[np.array(p)/2 for p in itertools.product([1,-1],repeat=3)]+[s*e for e in np.eye(3) for s in (1,-1)]
R={}
for name,N in {"fcc(cubocta)":cub,"hcp(anticubocta)":hcp,"ico":ico,"bcc(8+6)":bcc14}.items():
    n,deg,_=summary(N); R[name]=(n,deg)
assert R["fcc(cubocta)"]==(14,{3:8,4:6})
assert R["hcp(anticubocta)"]==(14,{3:8,4:6})
assert R["ico"]==(20,{3:20})
assert R["bcc(8+6)"]==(24,{3:24})
# ---- 2 bulk check of site types: fcc tet(8)+oct(6) = Voronoi vertices ; bcc tet(24) = vertices, oct(6) = square-face centres
fccN=[np.array(p)/2 for p in itertools.product([0,1,-1],repeat=3) if sum(abs(x) for x in p)==2]
_,_,vs=summary(fccN); d=sorted({round(np.linalg.norm(v),6) for v,_ in vs})
assert d==[round(np.sqrt(3)/4,6),0.5]                       # tet sqrt3/4 a , oct a/2
bccN=bcc14; _,_,vb=summary(bccN)
assert {round(np.linalg.norm(v),6) for v,_ in vb}=={round(np.sqrt(5)/4,6)}    # all 24 are tetrahedral sites
tet_bcc=uniq([np.roll(np.array([.5*s1,.25*s2,0]),k) for s1 in (1,-1) for s2 in (1,-1) for k in range(3)]+
             [np.roll(np.array([.5*s1,0,.25*s2]),k) for s1 in (1,-1) for s2 in (1,-1) for k in range(3)])
assert len(tet_bcc)==24 and all(any(np.allclose(v,t) for t in tet_bcc) for v,_ in vb)
# ---- 3 bcc ATOM shell (8+6) == fcc VOID shell (8 tet + 6 oct): same point set up to scale
scale=0.5/1.0      # bcc14 2nd-shell radius 1 ; fcc oct radius 1/2
fccvoid=[v for v,_ in vs]
assert all(any(np.allclose(p*scale,q) for q in fccvoid) for p in bcc14)
# ---- 4 along fcc->ico path P(t): 6 four-fold (octahedral) vertices split into 12 three-fold ones
path={}
for t in (1.0,1.001,1.01,1.1,1.3,phi,2.0):
    n,deg,vv=summary(cyc((0,1,t))); path[t]=(n,deg)
assert path[1.0]==(14,{3:8,4:6}) and all(path[t]==(20,{3:20}) for t in (1.001,1.01,1.1,1.3,phi,2.0))
# splitting distance -> 0 linearly as t->1 ; each pair straddles an old octahedral site
_,_,v0=summary(cub); oct0=[v for v,dg in v0 if dg==4]
seps=[]
for eps in (1e-2,1e-3,1e-4):
    _,_,vv=summary(cyc((0,1,1+eps))); pts=[v for v,_ in vv]
    s=[]
    for o in oct0:
        near=sorted(pts,key=lambda p:np.linalg.norm(p-o))[:2]
        assert np.allclose((near[0]+near[1])/2,o,atol=10*eps); s.append(np.linalg.norm(near[0]-near[1]))
    seps.append(np.mean(s))
assert 8<seps[0]/seps[1]<12 and 8<seps[1]/seps[2]<12      # linear in eps
# ---- 5 at t=phi the 20 voids form a regular dodecahedron of D(h) form with h=1/phi; generic t fits D(h) family
def fitD(pts):
    cubepart=[p for p in pts if np.allclose(np.abs(p),np.abs(p)[0])]
    k=np.abs(cubepart[0][0]); other=[p for p in pts if not np.allclose(np.abs(p),np.abs(p)[0])][0]
    a,b=sorted(np.abs(other))[1:]; # a<b ; D(h) pattern (0,1+h,1-h^2)*k -> larger=k(1+h), smaller=k(1-h^2)
    h=b/k-1; return len(cubepart),h,abs(a-k*(1-h*h))
for t in (1.3,phi,2.0):
    _,_,vv=summary(cyc((0,1,t))); pts=[v for v,_ in vv]
    nc,h,res=fitD(pts); assert nc==8 and res<1e-9
    if np.isclose(t,phi): assert np.isclose(h,1/phi)
    edges=sorted(np.linalg.norm(p-q) for p,q in itertools.combinations(pts,2))[:30]
    if np.isclose(t,phi): assert np.allclose(edges,edges[0])
print("all 5 blocks PASS"); print(R); print(path)
print("split distance ratios",seps)
for t in (1.1,1.3,phi,2.0):
    _,_,vv=summary(cyc((0,1,t))); print("t",round(t,4),"h",round(fitD([v for v,_ in vv])[1],6))
# ---- 6 atom parameter t and void parameter h obey t*h = 1  (Y = 1/X)
for t in (1.05,1.1,1.3,1.5,phi,2.0,3.0,5.0):
    n,deg,vv=summary(cyc((0,1,t)))
    if n==20:
        assert np.isclose(fitD([v for v,_ in vv])[1]*t,1.0)
print("block 6 PASS: t*h=1")
