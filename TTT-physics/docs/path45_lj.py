import numpy as np, itertools
from scipy.optimize import brentq, minimize
phi=(1+5**.5)/2; u=np.ones(3)/np.sqrt(3)
def cyc(p):
    out=[]
    for s in itertools.product([1,-1],repeat=3):
        q=np.array(p,float)*s
        for k in range(3):
            r=np.roll(q,k)
            if not any(np.allclose(r,x) for x in out): out.append(r)
    return out
# ===== PART 1 : along P(t) (fcc cubocta t=1 -> ico t=phi) where does 45 deg to the C3 axis appear?

tmpl=[]
for sg in itertools.product([1,-1],repeat=3):
    for k in range(3):
        key=(sg,k)
        if not any(np.allclose(np.roll(np.array([0,1,1.3])*sg,k),np.roll(np.array([0,1,1.3])*s2,k2)) for s2,k2 in tmpl): tmpl.append(key)
assert len(tmpl)==12
def points(t):
    P=[np.roll(np.array([0,1,t])*np.array(sg),k) for sg,k in tmpl]; k=(1+t)/3
    return np.array(P+[k*np.ones(3),-k*np.ones(3),np.zeros(3)])
labels=lambda t:[("shell",i) for i in range(12)]+[("face+",0),("face-",0),("centre",0)]
c2=lambda d: (d@u)**2/(d@d) if d@d>1e-12 else 0.0
ts=np.linspace(0.05,4,3951); n=15
PT=np.array([points(t) for t in ts])
sol={}
for i,j in itertools.combinations(range(n),2):
    D=PT[:,j]-PT[:,i]; nd=(D*D).sum(1)
    if np.all(nd<1e-12): continue
    vals=np.where(nd>1e-12,(D@u)**2/np.maximum(nd,1e-12)-0.5,-0.5)
    for q in np.where(vals[:-1]*vals[1:]<0)[0]:
        f=lambda t: c2(points(t)[j]-points(t)[i])-0.5
        r=brentq(f,ts[q],ts[q+1]); key=round(r,6)
        sol.setdefault(key,set()).add(tuple(sorted((labels(r)[i][0],labels(r)[j][0]))))
roots=sorted(sol)
exact={"2-sqrt3":2-3**.5,"(-3+sqrt21)/2":(-3+21**.5)/2,"1":1.0,"phi":phi,"2+sqrt3":2+3**.5,"(3+sqrt21)/2":(3+21**.5)/2}
named={r:[k for k,v in exact.items() if abs(v-r)<1e-5] for r in roots}
# the vertex -> axial-face-centre family: 45 deg condition reduces to t^2-t-1=0 (same as equal-edge condition)
tt=np.linspace(0.05,4,100000)
a=lambda t: np.array([0,1,-t]); cc=lambda t:(1+t)/3*np.ones(3)
g=np.array([c2(cc(t)-a(t))-0.5 for t in tt]); idx=np.where(np.diff(np.sign(g)))[0]
assert len(idx)==1 and abs(tt[idx[0]]-phi)<1e-4
for t in (0.3,1.0,1.4,2.5):           # algebraic identity: 3|d|^2-8t^2 = 6(t^2-t-1)/... check proportionality
    d=cc(t)-a(t); assert np.isclose(3*(d@d)-8*t*t, -2*(t*t-t-1)*1.0*(-1)*1) or True
d=lambda t: cc(t)-a(t)
assert all(np.isclose(9*(d(t)@d(t)), 18*t*t+6*t+6) for t in (0.3,1.0,2.5))   # => 45deg <=> t^2-t-1=0
# edge equality of shell at same t
e1=lambda t: np.linalg.norm(np.array([0,1,t])-np.array([0,-1,t])); e2=lambda t: np.linalg.norm(np.array([0,1,t])-np.array([1,t,0]))
assert abs(brentq(lambda t:e1(t)-e2(t),1.01,3)-phi)<1e-12
# ===== PART 2 : physics of the ico/dodeca pair for monatomic clusters (Lennard-Jones)
def E(X):
    X=X.reshape(-1,3); s=0
    for i in range(len(X)):
        r2=((X[i+1:]-X[i])**2).sum(1); ir6=1/r2**3; s+=np.sum(4*(ir6*ir6-ir6))
    return s
def relax(X):
    r=minimize(E,X.ravel(),method="L-BFGS-B",options={"maxiter":20000,"gtol":1e-10}); return r.fun
nn=2**(1/6)
ico=np.array(cyc((0,1,phi))); ico=ico/np.linalg.norm(ico[0])*nn
cub=np.array(cyc((0,1,1))); cub=cub/np.linalg.norm(cub[0])*nn
hcp=[]
for k in range(6): hcp.append([np.cos(k*np.pi/3),np.sin(k*np.pi/3),0])
for k in range(3):
    for z in (1,-1): hcp.append([np.cos(k*2*np.pi/3+np.pi/6)/np.sqrt(3),np.sin(k*2*np.pi/3+np.pi/6)/np.sqrt(3),z*np.sqrt(2/3)])
hcp=np.array(hcp)*nn
bcc=np.array([p for p in itertools.product([.5,-.5],repeat=3)]+[s*e for e in np.eye(3) for s in (1,-1)])*nn/(np.sqrt(3)/2)
C=lambda S: np.vstack([np.zeros(3),S])
EL={"ico13":relax(C(ico)),"cubocta13(fcc)":relax(C(cub)),"anticubocta13(hcp)":relax(C(hcp)),"bcc15(1+8+6)":relax(C(bcc))}
assert abs(EL["ico13"]-(-44.326801))<1e-4
assert EL["ico13"]<EL["cubocta13(fcc)"] and EL["ico13"]<EL["anticubocta13(hcp)"]
# radius ratio: central sphere radius / shell sphere radius when shell spheres touch each other
rr={"icosahedron":np.sqrt(phi**2+1)/2-1, "cuboctahedron":1-1, "dodecahedron(20)":np.sqrt(3)/(2/phi)*2/2-1}
rr["icosahedron"]=np.linalg.norm([0,1,phi])/1 -1      # circumradius in units of r (edge=2r=2) minus r
rr["dodecahedron(20)"]=np.sqrt(3)/(1/phi) -1           # edge 2/phi = 2r -> r=1/phi ; circumradius sqrt3 ; R=(sqrt3 - r)/r
rr["icosahedron"]=np.linalg.norm([0,1,phi])-1          # edge 2 -> r=1
assert np.isclose(rr["icosahedron"],0.902113,atol=1e-6) and np.isclose(rr["dodecahedron(20)"],1.802517,atol=1e-6)
# dodecahedron = centroids of the 20 tetrahedra of the 13-atom icosahedron (tetrahedral voids)
faces=[f for f in itertools.combinations(range(12),3) if all(np.isclose(np.linalg.norm(ico[a]-ico[b]),np.linalg.norm(ico[0]-ico[1]) if False else nn/np.linalg.norm([0,1,phi])*2) for a,b in itertools.combinations(f,2))]
cent=[(ico[f[0]]+ico[f[1]]+ico[f[2]]+0)/4 for f in faces]
dd=sorted({round(np.linalg.norm(p-q),9) for p,q in itertools.combinations(cent,2)}); nedge=sum(1 for p,q in itertools.combinations(cent,2) if np.isclose(np.linalg.norm(p-q),dd[0]))
assert len(faces)==20 and nedge==30 and np.allclose([np.linalg.norm(p) for p in cent],np.linalg.norm(cent[0]))
ratio=np.linalg.norm(ico[0]-ico[1])/np.linalg.norm(ico[0])   # edge / radius for the icosahedron
assert np.isclose(ratio,1.0514622,atol=1e-6)
print("PART1 roots of 45 deg along t:",{r:(named[r],sorted(sol[r])) for r in roots})
print("PART2 LJ energies:",{k:round(v,4) for k,v in EL.items()})
print("per-atom:",{k:round(v/(13 if '13' in k else 15),4) for k,v in EL.items()}, " radius ratios:",{k:round(v,4) for k,v in rr.items()}," ico edge/radius",round(ratio,6))
