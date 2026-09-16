import numpy as np, itertools
from scipy.special import sph_harm_y
from scipy.spatial.transform import Rotation as Rot
def close(gens):
    G=[np.eye(3)]
    while True:
        new=[a@b for a in G for b in gens]
        added=[m for m in new if not any(np.allclose(m,x) for x in G)]
        if not added: return G
        for m in added:
            if not any(np.allclose(m,x) for x in G): G.append(m)
rv=lambda ax,ang: Rot.from_rotvec(np.array(ax,float)/np.linalg.norm(ax)*ang).as_matrix()
T=close([rv((1,1,1),2*np.pi/3),rv((0,0,1),np.pi)])
O=close([rv((1,1,1),2*np.pi/3),rv((0,0,1),np.pi/2)])
D3=close([rv((0,0,1),2*np.pi/3),rv((1,0,0),np.pi)])
assert (len(T),len(O),len(D3))==(12,24,6)
def chi(J,R):
    th=np.arccos(np.clip((np.trace(R)-1)/2,-1,1))
    return 2*J+1 if np.isclose(th,0) else np.sin((2*J+1)*th/2)/np.sin(th/2)
nJ=lambda G,J: round(sum(chi(J,R) for R in G)/len(G),9)
Js=range(0,9)
tab={"pair(D_inf,exchange)":[1 if J%2==0 else 0 for J in Js],
     "triangle D3":[nJ(D3,J) for J in Js],"tetra T":[nJ(T,J) for J in Js],"octa O":[nJ(O,J) for J in Js]}
assert tab["tetra T"][:7]==[1,0,0,1,1,0,2]
assert tab["octa O"][:7]==[1,0,0,0,1,0,1]
assert tab["triangle D3"][:5]==[1,0,1,1,2]
# block2: multipole moments of point sets; lowest l>=1 that is nonzero
def lowest(P,w):
    P=np.array(P,float); r=np.linalg.norm(P,axis=1); th=np.arccos(P[:,2]/r); ph=np.arctan2(P[:,1],P[:,0])
    for l in range(1,9):
        if sum(abs(np.sum(w*sph_harm_y(l,m,th,ph))) for m in range(-l,l+1))>1e-9: return l
cube=list(itertools.product([1,-1],repeat=3))
tet=[v for v in cube if np.prod(v)==1]
octa=[s*e for e in np.eye(3) for s in (1,-1)]
tri=[(np.cos(a),np.sin(a),0) for a in (0,2*np.pi/3,4*np.pi/3)]
L={"pair":lowest([(0,0,1),(0,0,-1)],np.ones(2)),"triangle":lowest(tri,np.ones(3)),
   "tetra(+x4)":lowest(tet,np.ones(4)),"cube bipolar sign(xyz)":lowest(cube,np.array([np.prod(v) for v in cube],float)),
   "octa":lowest(octa,np.ones(6)),"cube(+x8)":lowest(cube,np.ones(8))}
assert L=={"pair":2,"triangle":2,"tetra(+x4)":3,"cube bipolar sign(xyz)":3,"octa":4,"cube(+x8)":4}
# block3: xyz is a pure l=3 harmonic (Laplacian 0, degree 3) -> numeric Laplacian
f=lambda x,y,z:x*y*z; h=1e-3
for _ in range(10):
    x,y,z=np.random.randn(3)
    lap=sum((f(*(np.array([x,y,z])+h*e))-2*f(x,y,z)+f(*(np.array([x,y,z])-h*e)))/h**2 for e in np.eye(3))
    assert abs(lap)<1e-6
# block4: Landau-Yang: every rotation-covariant vector amplitude bilinear in transverse e1,e2 is odd under photon exchange
rng=np.random.default_rng(3)
amps=[lambda e1,e2,k:(e1@e2)*k, lambda e1,e2,k:np.cross(e1,e2), lambda e1,e2,k:(np.cross(e1,e2)@k)*k,
      lambda e1,e2,k:e1*(e2@k)+e2*(e1@k)]
for _ in range(50):
    k=rng.normal(size=3);k/=np.linalg.norm(k)
    e1=np.cross(k,rng.normal(size=3)); e2=np.cross(k,rng.normal(size=3))
    for A in amps: assert np.allclose(A(e2,e1,-k),-A(e1,e2,k))
# block5: integer-spin constituents -> integer total J (all couplings)
def couple(js):
    S={js[0]}
    for j in js[1:]: S={J for a in S for J in np.arange(abs(a-j),a+j+1)}
    return S
assert all(float(J).is_integer() for J in couple([1,1,1,1]))
assert 0.5 in couple([0.5,1,1,1]) and not any(float(J).is_integer() for J in couple([0.5,1,1,1]))
# block6: binary tetrahedral 2T in SU(2): 24 elements, contains -1 (2pi rotation = sign flip)
q=lambda R: Rot.from_matrix(R).as_quat()
def qmul(a,b): return (Rot.from_quat(a)*Rot.from_quat(b)).as_quat()  # SO(3) loses sign -> use explicit Hamilton product
def ham(a,b):
    x1,y1,z1,w1=a;x2,y2,z2,w2=b
    return np.array([w1*x2+x1*w2+y1*z2-z1*y2,w1*y2-x1*z2+y1*w2+z1*x2,w1*z2+x1*y2-y1*x2+z1*w2,w1*w2-x1*x2-y1*y2-z1*z2])
g1=np.array([*(np.ones(3)/np.sqrt(3)*np.sin(np.pi/3)),np.cos(np.pi/3)]); g2=np.array([0,0,1.,0])
G=[np.array([0,0,0,1.])]
while True:
    add=[ham(a,b) for a in G for b in (g1,g2)]; add=[m for m in add if not any(np.allclose(m,x) for x in G)]
    if not add: break
    for m in add:
        if not any(np.allclose(m,x) for x in G): G.append(m)
assert len(G)==24 and any(np.allclose(x,[0,0,0,-1]) for x in G)
print("all 6 blocks PASS")
for k,v in tab.items(): print(f"{k:24s}", dict(zip(Js,[int(x) for x in v])))
print(L)
