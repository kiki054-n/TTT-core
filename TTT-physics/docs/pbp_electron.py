import numpy as np
from fractions import Fraction as Fr
phi=(1+5**.5)/2
# 1 bipyramids with all faces equilateral exist only for n=3,4,5 ; V=n+2 parity
exist={}
for n in range(3,9):
    R=1/(2*np.sin(np.pi/n)); exist[n]=R<1-1e-12   # lateral edge sqrt(R^2+h^2)=1 needs R<1
    V,E,F=n+2,3*n,2*n; assert V-E+F==2
assert [n for n,ok in exist.items() if ok]==[3,4,5]
parity={n:("odd" if (n+2)%2 else "even") for n in (3,4,5)}
assert parity=={3:"odd",4:"even",5:"odd"}
# 2 five regular tetrahedra around an edge leave 7.356 deg
gap=360-5*np.degrees(np.arccos(1/3)); assert abs(gap-7.3561)<1e-3
# 3 N spin-1/2 : half-integer total J iff N odd
def couple(js):
    S={Fr(js[0])}
    for j in js[1:]:
        j=Fr(j); S={a+b for a in S for b in [0]} if False else {J for a in S for J in [abs(a-j)+k for k in range(int(a+j-abs(a-j))+1)]}
    return S
for N in range(2,9):
    S=couple([Fr(1,2)]*N)
    assert all((J.denominator==2)==(N%2==1) for J in S)
assert couple([Fr(1,2)]*7)=={Fr(1,2),Fr(3,2),Fr(5,2),Fr(7,2)}
assert couple([Fr(1,2)]*5)=={Fr(1,2),Fr(3,2),Fr(5,2)}
# 4 binary groups in SU(2): is j=1/2, j=3/2 irreducible?
def ham(a,b):
    w1,x1,y1,z1=a;w2,x2,y2,z2=b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2,w1*x2+x1*w2+y1*z2-z1*y2,w1*y2-x1*z2+y1*w2+z1*x2,w1*z2+x1*y2-y1*x2+z1*w2])
rq=lambda ax,ang: np.array([np.cos(ang/2),*(np.array(ax,float)/np.linalg.norm(ax)*np.sin(ang/2))])
def close(gens):
    G=[np.array([1.,0,0,0])]; i=0
    while i<len(G):
        for g in gens:
            m=ham(G[i],g)
            if not any(np.allclose(m,x) for x in G): G.append(m)
        i+=1
    return G
groups={"2D5":close([rq((0,0,1),2*np.pi/5),rq((1,0,0),np.pi)]),
        "2T":close([rq((1,1,1),2*np.pi/3),rq((0,0,1),np.pi)]),
        "2O":close([rq((1,1,1),2*np.pi/3),rq((0,0,1),np.pi/2)]),
        "2I":close([rq((0,1,phi),2*np.pi/5),rq((1,1,1),2*np.pi/3)])}
assert {k:len(v) for k,v in groups.items()}=={"2D5":20,"2T":24,"2O":48,"2I":120}
def chi(j,q):
    th=2*np.arccos(np.clip(q[0],-1,1))
    if np.isclose(np.sin(th/2),0): return (2*j+1)*(1 if np.isclose(q[0],1) else (-1)**int(2*j))
    return np.sin((2*j+1)*th/2)/np.sin(th/2)
irr={k:{j:round(sum(chi(j,q)**2 for q in G)/len(G)) for j in (0.5,1.5,2.5)} for k,G in groups.items()}
assert all(irr[k][0.5]==1 for k in irr)                    # spin-1/2 stays a doublet everywhere
assert irr["2D5"][1.5]==2 and irr["2T"][1.5]==2 and irr["2O"][1.5]==1 and irr["2I"][1.5]==1
# 5 classical g-factor of a rigidly rotating pentagonal bipyramid (axis through apices)
def gfac(m_apex,m_ring,q_apex,q_ring,R=1.0,w=1.0):
    J=5*m_ring*R**2*w                     # apices on axis carry no L
    mu=5*q_ring*R**2*w/2
    M=2*m_apex+5*m_ring; Q=2*q_apex+5*q_ring
    return mu/(Q/(2*M)*J)
assert np.isclose(gfac(1,1,1,1),1.0)          # same q/m everywhere -> g=1 (any geometry)
assert np.isclose(gfac(1,1,0,1),1.4)          # charge on ring only, equal masses -> 14/10
assert np.isclose(gfac(2.5,1,0,1),2.0)        # g=2 iff total apex mass = total ring mass (2*2.5=5*1)
assert np.isclose(gfac(1,1,0.5,0.5),1.0)
print("all 5 blocks PASS"); print(irr)
