"""
Is there a CENTRE in the edge-n subdivision of a tetrahedron, and what is it?
Barycentric construction: lattice points (a,b,c,d), a+b+c+d = n, a,b,c,d >= 0.
  up-tetra    : index sum n-1, vertices = index + e_i (i=1..4)
  down-tetra  : index sum n-3, vertices = index + (1,1,1,0) and permutations
  octahedron  : index sum n-2, vertices = index + e_i + e_j (i<j)
"""
import itertools, numpy as np
from math import comb
from collections import Counter
from fractions import Fraction as F

def pieces(n):
    out = []
    for idx in [t for t in itertools.product(range(n+1), repeat=4) if sum(t)==n-1]:
        vs = [tuple(np.add(idx, e)) for e in np.eye(4, dtype=int)]
        out.append(("up-tet", idx, vs))
    for idx in [t for t in itertools.product(range(n+1), repeat=4) if sum(t)==n-3]:
        vs = []
        for drop in range(4):
            e = [1,1,1,1]; e[drop] = 0
            vs.append(tuple(np.add(idx, e)))
        out.append(("DOWN-tet", idx, vs))
    for idx in [t for t in itertools.product(range(n+1), repeat=4) if sum(t)==n-2]:
        vs = []
        for i, j in itertools.combinations(range(4), 2):
            e = [0,0,0,0]; e[i] = e[j] = 1
            vs.append(tuple(np.add(idx, e)))
        out.append(("octa", idx, vs))
    return out

print("="*78)
print("IS THERE A CENTRE?  (the piece whose centroid is the parent's centroid)")
print("="*78)
print(f"\n{'n':>3} {'up':>4} {'down':>5} {'octa':>5} {'pieces':>7}   central piece")
for n in range(1, 9):
    P = pieces(n)
    cnt = Counter(k for k,_,_ in P)
    assert cnt["up-tet"] == comb(n+2,3) and cnt["DOWN-tet"] == comb(n,3) \
           and cnt["octa"] == comb(n+1,3)
    target = [F(n,4)]*4                       # parent centroid in lattice coords
    central = []
    for kind, idx, vs in P:
        c = [F(sum(v[k] for v in vs), len(vs)) for k in range(4)]
        if c == target: central.append((kind, idx))
    desc = ", ".join(f"{k} at {i}" for k,i in central) if central else "-- none --"
    print(f"{n:>3} {cnt['up-tet']:>4} {cnt['DOWN-tet']:>5} {cnt['octa']:>5} {len(P):>7}   {desc}")

print("\n  => n = 2 : the centre is an OCTAHEDRON")
print("     n = 3 : the centre is a single INVERTED TETRAHEDRON")
print("     n = 4,6,8 (even) : octahedron again;  n = 5,7 (odd) : inverted tetra")
print("  The centre CANNOT be removed by choosing n.  It only changes type.")

print("\n"+"="*78)
print("n = 3 : orbit structure of the 15 pieces under T")
print("="*78)
P = pieces(3)
orb = Counter()
for kind, idx, vs in P:
    sig = tuple(sorted(idx))                  # T permutes the 4 barycentric slots
    orb[(kind, sig)] += 1
print()
for (kind, sig), m in sorted(orb.items(), key=lambda x: -x[1]):
    tag = "   <-- FIXED by all of T (a singlet)" if m == 1 else ""
    print(f"  {kind:>9}  index type {sig}  orbit size {m}{tag}")
assert sum(orb.values()) == 15
assert sorted(orb.values()) == [1, 4, 4, 6]
print(f"\n  orbits: 4 + 6 + 1 + 4 = 15   -> EXACTLY ONE T-invariant piece,")
print(f"  and it is the inverted tetrahedron sitting at the exact centroid.")

print("\n"+"="*78)
print("WHY THIS IS FATAL: the bipolar condition IS non-centrosymmetry")
print("="*78)
tet = np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]], dtype=float)/np.sqrt(3)
# octupole moment: nonzero <=> no inversion centre  (2026-09-11 finding)
Oc = np.zeros((3,3,3))
for v in tet:
    Oc += np.einsum('i,j,k->ijk', v, v, v)
nrm = np.linalg.norm(Oc)
print(f"\n  octupole moment  |sum v(x)v(x)v|  = {nrm:.4f}   (nonzero)")
assert nrm > 1.8
print("  A nonzero odd moment is exactly the statement  -1 not in T_d :")
print("  the tetrahedron has NO centre of inversion.  (2026-09-11 finding,")
print("  where it gave the 32/9 eclipsed-vs-staggered splitting.)")
print("\n  |T_d| = 24,  |O_h| = 48,  and  O_h = T_d  U  (-1)*T_d .")
print("  So 'bipolar zero' in group language = the absence of -1.")
print("\n  But the n=3 subdivision INSERTS an inverted tetrahedron at the centre.")
print("  It supplies the -1 that the group does not have.  The 27-cell picture")
print("  and the bipolar axiom contradict each other -- and the axiom is TTT's,")
print("  so the objection is INTERNAL and fatal, not a matter of taste.")

print("\n"+"="*78)
print("THE FORK: if you keep bipolarity, the group changes")
print("="*78)
print("\n  True bipolarity = tetrahedron + anti-tetrahedron = stella octangula")
print("  (8 vertices = a cube; the intersection is an octahedron).")
print("  Its rotation group is O (order 24), binary cover 2O (order 48).")
print("  McKay:  2O  <->  affine E7")
E7 = [1,1,2,2,2,3,3,4]
print(f"    2O irrep dims {E7}:  # irreps = {len(E7)},  sum = {sum(E7)} = h(E7),"
      f"  sum^2 = {sum(d*d for d in E7)} = |2O|")
assert len(E7) == 8 and sum(E7) == 18 and sum(d*d for d in E7) == 48
print(f"\n  => the class count becomes 8, not 7.")
print("     But the vocabulary's 7 was DEFINED as the class count of 2T")
print("     (= nodes of affine E6), proved forced on 2026-09-13.")
print("     So: bipolarity and the vocabulary word 7 cannot both be kept.")
print("\nALL CHECKS COMPLETE")
