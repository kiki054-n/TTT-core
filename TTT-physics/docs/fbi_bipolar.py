import numpy as np, itertools
s1=np.array([[0,1],[1,0]],complex); s2=np.array([[0,-1j],[1j,0]]); s3=np.array([[1,0],[0,-1]],complex)
E=[s1,s2,s3]; Id=np.eye(2)
vec=lambda a: sum(a[k]*E[k] for k in range(3))
I=s1@s2@s3
# 1: pseudoscalar I = i*identity, I^2=-1, I*(-I)=+1  (bipolar: -I = 1/I)
assert np.allclose(I,1j*Id); assert np.allclose(I@I,-Id); assert np.allclose(I@(-I),Id)
assert np.allclose(np.linalg.inv(I),-I)
# 2: cross product = -I (a^b), wedge = antisym part of geometric product
rng=np.random.default_rng(0)
for _ in range(100):
    a,b=rng.normal(size=3),rng.normal(size=3)
    wedge=(vec(a)@vec(b)-vec(b)@vec(a))/2
    assert np.allclose(vec(np.cross(a,b)), -I@wedge)
# 3: twice rotation -> -1 : (v x B) x B = -B^2 v_perp  (Lenz sign)
for _ in range(100):
    v,B=rng.normal(size=3),rng.normal(size=3)
    vperp=v-np.dot(v,B)/np.dot(B,B)*B
    assert np.allclose(np.cross(np.cross(v,B),B), -np.dot(B,B)*vperp)
# 4: 8 cube vertices split by sign of xyz into two tetrahedra; inversion swaps them
V=np.array(list(itertools.product([1,-1],repeat=3)))
Tp=[tuple(p) for p in V if np.prod(p)==1]; Tm=[tuple(p) for p in V if np.prod(p)==-1]
d=lambda T:{round(np.linalg.norm(np.subtract(p,q)),9) for p,q in itertools.combinations(T,2)}
assert len(Tp)==len(Tm)==4 and d(Tp)==d(Tm)=={round(2*np.sqrt(2),9)}  # regular tetrahedra
assert {tuple(-np.array(p)) for p in Tp}==set(Tm)
assert all(np.isclose(np.sum(Tp,axis=0),0)) and all(np.isclose(np.sum(Tm,axis=0),0))
# 5: under inversion a->-a: bivector a^b invariant, I=e1e2e3 -> -I
a,b=rng.normal(size=3),rng.normal(size=3)
w=lambda a,b:(vec(a)@vec(b)-vec(b)@vec(a))/2
assert np.allclose(w(-a,-b),w(a,b)); assert np.allclose((-s1)@(-s2)@(-s3),-I)
# 6: handedness of (F,B,I): F = I x B  -> det[I,B,F]>0 ; det[F,B,I]<0
for _ in range(50):
    Ic,B=rng.normal(size=3),rng.normal(size=3); F=np.cross(Ic,B)
    assert np.linalg.det(np.array([Ic,B,F]))>0 and np.linalg.det(np.array([F,B,Ic]))<0
print("all 6 blocks PASS")
