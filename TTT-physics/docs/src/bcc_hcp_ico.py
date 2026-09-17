import numpy as np, itertools
phi=(1+5**.5)/2
def cyc(p):
    out=[]
    for s in itertools.product([1,-1],repeat=3):
        q=np.array(p,float)*s
        for k in range(3): out.append(np.roll(q,k))
    return uniq(out)
def uniq(L): 
    U=[]
    for p in L:
        if not any(np.allclose(p,q) for q in U): U.append(np.array(p,float))
    return U
def nn_edges(P):
    D=sorted({round(np.linalg.norm(a-b),9) for a,b in itertools.combinations(P,2)}); d=D[0]
    return d,sum(1 for a,b in itertools.combinations(P,2) if np.isclose(np.linalg.norm(a-b),d))
cube=[np.array(p,float) for p in itertools.product([1,-1],repeat=3)]
# ---- 1 fcc shell (cuboctahedron) -> icosahedron : P(t)=cyc(0,1,t)
P=lambda t: cyc((0,1,t))
d,n=nn_edges(P(1)); assert len(P(1))==12 and n==24 and np.isclose(d,np.sqrt(2))   # cuboctahedron: 24 edges
# equal-edge condition: |(0,1,t)-(0,-1,t)|=2 and |(0,1,t)-(1,t,0)|=2  ->  t^2-t-1=0
roots=np.roots([1,-1,-1]); assert np.isclose(max(roots),phi)
d,n=nn_edges(P(phi)); assert len(P(phi))==12 and n==30 and np.isclose(d,2)            # regular icosahedron
assert len(P(0))==6                                                                   # t=0: 12 merge pairwise -> octahedron
# ---- 2 bcc 1st+2nd shells (rhombic dodecahedron) -> regular dodecahedron : D(h)
D=lambda h: uniq(cube+cyc((0,1+h,1-h*h)))
bcc=uniq(cube+[s*2*e for e in np.eye(3) for s in (1,-1)])
assert len(D(1))==14 and all(any(np.allclose(p,q) for q in bcc) for p in D(1))        # h=1: exactly bcc 8+6
assert np.isclose(2/np.sqrt(3),1.1547005)                                              # bcc shell ratio
Dg=D(1/phi); d,n=nn_edges(Dg); r=[np.linalg.norm(p) for p in Dg]
assert len(Dg)==20 and n==30 and np.allclose(r,np.sqrt(3))                            # regular dodecahedron
# equal-edge condition for D(h): edge cube-vertex to (0,1+h,1-h^2) equals edge between the two (0,+-(1+h),1-h^2)
hs=np.linspace(0.01,0.99,98001)
f=lambda h: np.linalg.norm(np.array([1,1,1])-np.array([1-h*h,0,1+h]))-2*(1-h*h)
g=[f(h) for h in hs]; i=np.argmin(np.abs(g)); assert abs(hs[i]-1/phi)<1e-4
# ---- 3 duality in common orientation: dodecahedron vertex directions = icosahedron face-centre directions
ico=P(phi)
faces=[f for f in itertools.combinations(range(12),3) if all(np.isclose(np.linalg.norm(ico[a]-ico[b]),2) for a,b in itertools.combinations(f,2))]
fcdir=[sum(ico[k] for k in f)/np.linalg.norm(sum(ico[k] for k in f)) for f in faces]
assert len(faces)==20 and all(any(np.allclose(p/np.linalg.norm(p),q) for q in fcdir) for p in Dg)
# ---- 4 the whole path lives in Th = Oh ∩ Ih ; rotation part T = O ∩ I (order 12)
def close(gens):
    G=[np.eye(3)]; i=0
    while i<len(G):
        for g in gens:
            m=G[i]@g
            if not any(np.allclose(m,x) for x in G): G.append(m)
        i+=1
    return G
from scipy.spatial.transform import Rotation as R
rv=lambda ax,a: R.from_rotvec(np.array(ax,float)/np.linalg.norm(ax)*a).as_matrix()
O=close([rv((0,0,1),np.pi/2),rv((1,1,1),2*np.pi/3)]); Oh=O+[-m for m in O]
I=close([rv((0,1,phi),2*np.pi/5),rv((1,1,1),2*np.pi/3)]); Ih=I+[-m for m in I]
assert (len(O),len(Oh),len(I),len(Ih))==(24,48,60,120)
Th=[m for m in Oh if any(np.allclose(m,x) for x in Ih)]; Trot=[m for m in O if any(np.allclose(m,x) for x in I)]
assert len(Th)==24 and len(Trot)==12 and any(np.allclose(m,-np.eye(3)) for m in Th)
inv=lambda S,G: all(all(any(np.allclose(g@p,q) for q in S) for p in S) for g in G)
for t in (0.5,1,1.3,phi,2.2): assert inv(P(t),Th)
for h in (0.2,1/phi,0.8,1): assert inv(D(h),Th)
assert not inv(P(1.3),Oh) and inv(P(1),Oh) and inv(P(phi),Ih)       # only endpoints gain full symmetry
# ---- 5 Burgers path bcc(110) -> hcp(0001): rhombus angle arccos(1/3)=70.53 must shear to 60
a1=np.array([1,-1,1])/2; a2=np.array([-1,1,1])/2          # nearest-neighbour vectors lying in (110)
assert np.isclose(a1@np.array([1,1,0]),0) and np.isclose(a2@np.array([1,1,0]),0)
ang=np.degrees(np.arccos(a1@a2/np.linalg.norm(a1)/np.linalg.norm(a2)))
assert np.isclose(min(ang,180-ang),np.degrees(np.arccos(1/3)))
shear=min(ang,180-ang)-60; gap5=360-5*np.degrees(np.arccos(1/3))
pack={"bcc":np.pi*np.sqrt(3)/8,"hcp/fcc":np.pi/(3*np.sqrt(2))}
assert np.isclose(pack["bcc"],0.68017) and np.isclose(pack["hcp/fcc"],0.74048)
# 13-atom shells: nearest-neighbour count; icosahedron edges (30) vs cubocta (24) vs anticubocta (24)
hcp12=uniq([np.array([np.cos(k*np.pi/3),np.sin(k*np.pi/3),0]) for k in range(6)]+
           [np.array([np.cos(k*2*np.pi/3+s*np.pi/6)/np.sqrt(3),np.sin(k*2*np.pi/3+s*np.pi/6)/np.sqrt(3),z*np.sqrt(2/3)]) for k in range(3) for z in (1,-1) for s in (1,)])
d,n=nn_edges(hcp12); assert len(hcp12)==12 and np.isclose(d,1) and n==24
print("all 5 blocks PASS")
print(f"bcc(110) angle {min(ang,180-ang):.4f} deg -> shear to 60 = {shear:.4f} deg ; five-around gap {gap5:.4f} deg ; packing {pack}")
