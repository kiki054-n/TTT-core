"""
The 2T vs 2O fork.
Step 0: the two different "-1"s -- spinorial vs spatial. They are NOT the same.
Step 1: build 2O, verify order 48, 8 classes, 2T normal of index 2.
Step 2: the lattice: 2T < 2O, 2T < 2I, but 2O and 2I are INCOMPARABLE.
Step 3: 2T = 2O (intersect) 2I   <- the decisive fact.
Step 4: what each choice costs.
"""
import itertools, math, numpy as np
from collections import Counter

def qmul(p,q):
    a1,b1,c1,d1=p; a2,b2,c2,d2=q
    return (a1*a2-b1*b2-c1*c2-d1*d2, a1*b2+b1*a2+c1*d2-d1*c2,
            a1*c2-b1*d2+c1*a2+d1*b2, a1*d2+b1*c2-c1*b2+d1*a2)
def rnd(q,n=6): return tuple(round(x,n)+0.0 for x in q)
def qinv(q): return (q[0],-q[1],-q[2],-q[3])

print("="*78)
print("STEP 0 — I conflated two different '-1's last time.  Correcting.")
print("="*78)
print("""
  (a) SPATIAL inversion  -I in O(3) = parity.
      det(-I) = (-1)^3 = -1  =>  -I is NOT in SO(3),
      therefore -I is in NO rotation group and in NO binary group.
      The tetrahedron's non-centrosymmetry is  -I not in T_d.
      That is what the nonzero octupole moment measures.

  (b) SPINORIAL -1 in SU(2) = the 2*pi rotation, the kernel of SU(2)->SO(3).
      This IS in 2T (its unique involution, verified 2026-09-13).

  Last message I wrote "bipolar zero = the absence of -1" without saying which.
  It is (a) that the tetrahedron lacks.  2T HAS (b).  These are different
  statements and the fork looks completely different once they are separated.
""")

# ---------- 2T ----------
TT=[]
for k in range(4):
    for s in (1,-1):
        q=[0.,0.,0.,0.]; q[k]=float(s); TT.append(tuple(q))
for sg in itertools.product([1,-1],repeat=4): TT.append(tuple(0.5*s for s in sg))
TT=[rnd(q) for q in TT]
assert len(set(TT))==24
one, minus = (1.,0.,0.,0.), (-1.,0.,0.,0.)
def order_of(q):
    n, cur = 1, q
    while rnd(cur) != one:
        cur = rnd(qmul(cur,q)); n += 1; assert n<=48
    return n
invol = [q for q in TT if order_of(q)==2]
print(f"  check: involutions in 2T = {len(invol)} -> {invol}")
assert invol == [minus]
print("         the spinorial -1 is in 2T, and it is the ONLY involution.")
oct_m = np.zeros((3,3,3))
tet = np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],dtype=float)/math.sqrt(3)
for v in tet: oct_m += np.einsum('i,j,k->ijk',v,v,v)
print(f"  check: octupole |sum v(x)v(x)v| = {np.linalg.norm(oct_m):.4f} != 0")
print("         -> spatial parity absent.  Both statements true simultaneously.")

print("\n"+"="*78)
print("STEP 1 — build 2O (binary octahedral), order 48")
print("="*78)
r2 = 1/math.sqrt(2)
OO = set(TT)
for i,j in itertools.combinations(range(4),2):
    for si,sj in itertools.product([1,-1],repeat=2):
        q=[0.,0.,0.,0.]; q[i]=si*r2; q[j]=sj*r2
        OO.add(rnd(tuple(q)))
OO = sorted(OO)
print(f"\n  |2O| = {len(OO)}")
assert len(OO)==48
A = np.array(OO)
def member(q, S=A, tol=1e-6):
    return bool((np.abs(S-np.array(q)).max(axis=1) < tol).any())
bad = sum(0 if member(qmul(a,b)) else 1 for a in OO for b in OO)
assert bad==0
print(f"  all {len(OO)**2} products close -> it is a group")
print(f"  all unit norm: {all(abs(sum(x*x for x in q)-1)<1e-5 for q in OO)}" + "  (1e-5: the 1/sqrt2 entries are stored rounded to 6 dp)")
# conjugacy classes
cls=[]; seen=set()
for i,q in enumerate(OO):
    if i in seen: continue
    c=set()
    for g in OO:
        p=rnd(qmul(qmul(g,q),qinv(g)))
        for k,x in enumerate(OO):
            if max(abs(x[t]-p[t]) for t in range(4))<1e-6: c.add(k); break
    cls.append(sorted(c)); seen|=c
sizes=sorted(len(c) for c in cls)
print(f"  conjugacy classes: {len(cls)}, sizes {sizes}, total {sum(sizes)}")
assert len(cls)==8 and sum(sizes)==48
dims_2O=[1,1,2,2,2,3,3,4]
assert len(dims_2O)==len(cls) and sum(d*d for d in dims_2O)==48 and sum(dims_2O)==18
print(f"  => 8 classes = 8 irreps, dims {dims_2O}, sum^2 = 48, sum = 18 = h(E7)")
print(f"  McKay: 2O <-> affine E7 (8 nodes)")
# 2T normal of index 2
print(f"\n  2T subset 2O ? {all(member(q) for q in TT)}   index = {len(OO)//len(TT)}")
normal = all(member(rnd(qmul(qmul(g,h),qinv(g))), np.array(TT)) for g in OO for h in TT)
print(f"  2T normal in 2O ? {normal}")
assert normal

print("\n"+"="*78)
print("STEP 2 — the subgroup lattice: 2O and 2I are INCOMPARABLE")
print("="*78)
phi=(1+math.sqrt(5))/2
EVEN=[(0,1,2,3),(0,2,3,1),(0,3,1,2),(1,0,3,2),(1,2,0,3),(1,3,2,0),
      (2,0,1,3),(2,1,3,0),(2,3,0,1),(3,0,2,1),(3,1,0,2),(3,2,1,0)]
II=set(TT)
for perm in EVEN:
    for s in itertools.product([1,-1],repeat=3):
        base=[0.0,0.5*s[0],0.5*s[1]/phi,0.5*s[2]*phi]
        q=[0.0]*4
        for slot,v in zip(perm,base): q[slot]=v
        II.add(rnd(tuple(q)))
II=sorted(II); AI=np.array(II)
assert len(II)==120
print(f"\n  |2T| = 24, |2O| = 48, |2I| = 120")
print(f"  24 | 48 : {48%24==0}      24 | 120 : {120%24==0}")
print(f"  48 | 120: {120%48==0}   <-- so 2O cannot sit inside 2I (Lagrange)")
assert 120%48 != 0
in_I = sum(1 for q in OO if member(q, AI))
print(f"  elements of 2O that lie in 2I: {in_I} of 48")
print(f"  elements of 2I that lie in 2O: {sum(1 for q in II if member(q, A))} of 120")

print("\n"+"="*78)
print("STEP 3 — the decisive fact:  2T = 2O (intersect) 2I")
print("="*78)
inter = [q for q in OO if member(q, AI)]
print(f"\n  |2O ∩ 2I| = {len(inter)}")
same = (len(inter)==24) and all(member(q, np.array(inter)) for q in TT)
print(f"  is it exactly 2T ? {same}")
assert same
print("""
  This is the 3D fact  O ∩ I = T  (recorded 2026-09-11 as T_d ∩ I_h = T),
  lifted to the spin groups.  In words:

      2T is the LARGEST group compatible with BOTH the octahedral
      (crystalline / cubic / diamond) and the icosahedral
      (5-fold twinning / decahedral / Mackay) worlds.
""")

print("="*78)
print("STEP 4 — what each choice costs")
print("="*78)
print(f"""
  CHOOSE 2T  (order 24, 7 classes, affine E6, Molien degrees 6,8,12)
    keeps : the 5-fold line (2I side) AND the cubic line (2O side)
    keeps : vocabulary 7 = # classes (forced, proved 2026-09-13)
    keeps : 5 = [2I:2T] (forced, proved 2026-09-13)
    keeps : diamond -- a carbon atom in diamond sits on a T_d SITE, so the
            local group really is tetrahedral even though the crystal is O_h
    bipolar: supplied by the spinorial +-1, i.e. Z(2T) = {{+-1}} = Z_2, which
            forces the Z_2 grading (integer j / half-integer j) verified
            2026-09-13, which is what gives the j = 3/2 selection rule
    costs : nothing found

  CHOOSE 2O  (order 48, 8 classes, affine E7)
    gains : the stella octangula as ONE object -- and note the swap of the
            two tetrahedra is a PROPER C4 rotation, so no parity is needed
    costs : 7 -> 8.  The vocabulary word 7 dies.
    costs : 2I is no longer reachable (48 does not divide 120), so the whole
            5-fold twinning programme -- 7.356 deg, LJ7, Cheng et al. 2025,
            the diamond disclination numbers -- is cut off from the base group.
            That is TTT's strongest and most defensible body of work.
    costs : 5 = [2I:2T] loses its home.
""")
print("="*78)
print("STEP 5 — the McKay images, stated precisely (a place people gloss)")
print("="*78)
print("""
  2T < 2O  and  2T < 2I  are both true.
  E6 < E7  and  E6 < E8  are both true.
  So McKay preserves the inclusions FROM THE BASE.

  BUT  2O and 2I are incomparable (48 does not divide 120), while
  E7 < E8 holds in the Lie world.  So the sentence
      "the group chain IS the exceptional chain"
  is FALSE at the top.  The correspondence is a bijection on ADE data,
  not a functor on subgroup lattices.  Only the two inclusions out of
  2T transfer; the E7 < E8 inclusion has no counterpart in the groups.
""")
print("="*78)
print("  => 2T.  The fork does not survive contact with the lattice.")
print("\nALL CHECKS COMPLETE")
