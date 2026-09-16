import numpy as np, itertools
me,mmu,mtau,dt=0.51099895,105.6583755,1776.93,0.09
u=np.ones(3)/np.sqrt(3)
def ang(v): return np.degrees(np.arccos(np.clip(abs(v@u)/np.linalg.norm(v),0,1)))
# 1 equivalences: Q = 1/(3 cos^2 th); Q=2/3 <=> th=45 <=> |v_par|=|v_perp| <=> amplitude sqrt2
v=np.sqrt([me,mmu,mtau]); Q=np.sum(v**2)/v.sum()**2
th=ang(v); assert np.isclose(Q,1/(3*np.cos(np.radians(th))**2))
vp=(v@u)*u; vq=v-vp; w2w1=(vq@vq)/(vp@vp)
thp=ang(np.sqrt([me,mmu,mtau+dt])); sth=abs(thp-th)
for d in np.linspace(0,2,9):   # Brannen form with amplitude A: Q=(1+A^2/2)/3 -> A=sqrt2 gives 2/3
    for A in (1.0,np.sqrt(2),1.5):
        s=1+A*np.cos(d+2*np.pi*np.arange(3)/3)
        assert np.isclose(np.sum(s**2)/s.sum()**2,(1+A**2/2)/3)
# 2 no nonzero rational direction on the 45-degree cone:  a^2+b^2+c^2 = 4(ab+bc+ca)
N=60; sols=[(a,b,c) for a in range(-N,N+1) for b in range(-N,N+1) for c in range(-N,N+1)
            if (a,b,c)!=(0,0,0) and a*a+b*b+c*c==4*(a*b+b*c+c*a)]
assert sols==[]
M=400; assert not any(3*X*X+Y*Y==2*Z*Z for X in range(M) for Y in range(M) for Z in range(1,M))  # descent form
# 3 all directions built from tetrahedron/cube points: angles to the C3 axis ; 45 never occurs
V=[np.array(p,float) for p in itertools.product([1,-1],repeat=3) if np.prod(p)==1]
pts=V+[(a+b)/2 for a,b in itertools.combinations(V,2)]+[sum(f)/3 for f in itertools.combinations(V,3)]+[np.zeros(3)]
pts+=[np.array(p,float) for p in itertools.product([1,-1],repeat=3)]+[s*e for e in np.eye(3) for s in (1,-1)]
angles=set()
for a,b in itertools.combinations(pts,2):
    d=b-a
    if np.linalg.norm(d)>1e-9: angles.add(round(ang(d),4))
assert all(abs(x-45)>1e-3 for x in angles)
Qset=sorted({round(1/(3*np.cos(np.radians(x))**2),4) for x in angles if x<89.99})
assert 0.6667 not in Qset
# 4 the "2/3" of the tetrahedron sits at the wrong place: sin^2(magic)=2/3 gives Q=1, not 2/3
magic=np.degrees(np.arccos(1/np.sqrt(3))); assert np.isclose(np.sin(np.radians(magic))**2,2/3)
assert np.isclose(1/(3*np.cos(np.radians(magic))**2),1.0)
# 5 the 120-degree part IS natural: base triangle of the tetrahedron projected along C3
axis=V[0]/np.linalg.norm(V[0]); base=[p-(p@axis)*axis for p in V[1:]]
cosang=[b1@b2/np.linalg.norm(b1)/np.linalg.norm(b2) for b1,b2 in itertools.combinations(base,2)]
assert np.allclose(cosang,-0.5)
print("all 5 blocks PASS")
print(f"theta={th:.4f} +/- {sth:.4f} deg ; Q={Q:.7f} ; |v_perp|^2/|v_par|^2={w2w1:.5f}")
print("angles to C3 from tetra/cube points:",sorted(angles))
print("Q values reachable:",Qset)
