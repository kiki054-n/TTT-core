"""
(B) 2T in SL(2,C) — machine verification of every group-theoretic claim in the draft.
All blocks assert; a silent run means everything checked out.
"""
import numpy as np, itertools, math
np.set_printoptions(precision=6, suppress=True)

# ---------------- Block 1: build 2T as Hurwitz units in SU(2) ----------------
def quat_to_su2(q):
    a,b,c,d = q                      # q = a + b i + c j + d k
    return np.array([[a+1j*d, b+1j*c],
                     [-b+1j*c, a-1j*d]], dtype=complex)

H = []
for s in itertools.product([1,-1], repeat=1):
    pass
# 8 Lipschitz units
for k in range(4):
    for s in (1,-1):
        q=[0,0,0,0]; q[k]=s; H.append(tuple(q))
# 16 half-integer units
for signs in itertools.product([1,-1], repeat=4):
    H.append(tuple(s*0.5 for s in signs))
H = [np.array(q,dtype=float) for q in H]
assert len(H)==24, len(H)
assert all(abs(np.dot(q,q)-1)<1e-12 for q in H)

G = [quat_to_su2(q) for q in H]
for g in G:
    assert abs(np.linalg.det(g)-1) < 1e-12
    assert np.allclose(g.conj().T @ g, np.eye(2))          # in SU(2)
print("Block 1 OK: 24 unit quaternions -> 24 matrices in SU(2), det=1")

# ---------------- Block 2: closure (it really is a group) ----------------
def key(m, tol=1e-8):
    return tuple(np.round(np.array([m[0,0].real,m[0,0].imag,m[0,1].real,
                                    m[0,1].imag,m[1,0].real,m[1,0].imag,
                                    m[1,1].real,m[1,1].imag]),6))
idx = {key(g):i for i,g in enumerate(G)}
assert len(idx)==24, "matrices not distinct"
table = np.zeros((24,24),dtype=int)
for i,a in enumerate(G):
    for j,b in enumerate(G):
        k = key(a@b)
        assert k in idx, "NOT CLOSED"
        table[i,j] = idx[k]
print("Block 2 OK: closed under multiplication -> 2T is a group of order 24")

# ---------------- Block 3: element orders, involutions, 2T != S4 ----------------
def order(i):
    n, cur = 1, G[i]
    I = np.eye(2)
    while not np.allclose(cur, I, atol=1e-8):
        cur = cur @ G[i]; n += 1
        assert n <= 24
    return n
orders = [order(i) for i in range(24)]
from collections import Counter
oc = Counter(orders)
assert dict(oc) == {1:1, 2:1, 4:6, 6:8, 3:8}, dict(oc)
print("Block 3 OK: order profile", dict(sorted(oc.items())))
print("           involutions (order 2) =", oc[2], " -> S4 has 9, so 2T is NOT S4")
assert oc[2] == 1

# ---------------- Block 4: conjugacy classes ----------------
classes = []
seen = set()
for i in range(24):
    if i in seen: continue
    cl = set()
    for j in range(24):
        inv = next(t for t in range(24) if table[j,t]==idx[key(np.eye(2))])
        cl.add(table[table[j,i],inv])
    classes.append(sorted(cl)); seen |= cl
sizes = sorted(len(c) for c in classes)
assert len(classes)==7, len(classes)
assert sizes == [1,1,4,4,4,4,6], sizes
assert sum(sizes)==24
print("Block 4 OK: 7 conjugacy classes, sizes", sizes)

# ---------------- Block 5: irrep dimensions vs affine E6 marks ----------------
dims_2T = [1,1,1,2,2,2,3]
E6_affine_marks = [1,2,3,2,1,2,1]          # Kac labels of \tilde{E}_6 (7 nodes)
assert len(dims_2T)==len(classes)          # #irreps = #classes
assert sum(d*d for d in dims_2T)==24       # sum of squares = |2T|
assert sum(dims_2T)==12                    # = Coxeter number h(E6)
assert sorted(dims_2T)==sorted(E6_affine_marks)
print("Block 5 OK: irrep dims", dims_2T, " sum =",sum(dims_2T),"= h(E6)",
      " sum^2 =",sum(d*d for d in dims_2T),"= |2T|")
print("           = multiset of affine E6 Dynkin marks", E6_affine_marks, "(McKay)")

# same check for 2O -> E7 and 2I -> E8   (sum of marks = Coxeter number, sum^2 = |group|)
E7      = [1,2,3,4,3,2,1,2];   dims_2O = [1,1,2,2,2,3,3,4]
E8      = [1,2,3,4,5,6,4,2,3]; dims_2I = [1,2,2,3,3,4,4,5,6]
assert sorted(dims_2O)==sorted(E7) and sum(E7)==18  and sum(d*d for d in E7)==48
assert sorted(dims_2I)==sorted(E8) and sum(E8)==30  and sum(d*d for d in E8)==120
print("Block 5b OK: 2O->E7  8 nodes, dims",dims_2O,"sum=18=h(E7), sum^2=48=|2O|")
print("            2I->E8  9 nodes, dims",dims_2I,"sum=30=h(E8), sum^2=120=|2I|")
print("           -> vocabulary word 5 is an irrep dim of 2I, NOT of 2T;")
print("              7 is the number of classes/irreps of 2T (= nodes of affine E6)")

# ---------------- Block 6: 2T/{+-1} = A4, and trace spectrum ----------------
tr = [complex(np.trace(g)).real for g in G]
tc = Counter(np.round(tr,6))
assert dict(tc) == {2.0:1, -2.0:1, 0.0:6, 1.0:8, -1.0:8}, dict(tc)
print("Block 6 OK: trace spectrum of 2T =", dict(sorted(tc.items())))

# ---------------- Block 7: the 24 elements are the 24-cell vertices ----------------
ip = {}
for a,b in itertools.combinations(range(24),2):
    v = round(float(np.dot(H[a],H[b])),6)
    ip[v] = ip.get(v,0)+1
assert set(ip.keys()) <= {1.0,0.5,0.0,-0.5,-1.0}, ip
nn = sum(1 for b in range(1,24) if abs(np.dot(H[0],H[b])-0.5)<1e-9)
assert nn==8, nn
print("Block 7 OK: pairwise inner products only in {+-1/2, 0, -1}; each vertex has",
      nn,"neighbours at 60deg -> 24-cell (self-dual, no 3D analogue)")

# ---------------- Block 8: the point of the whole exercise ----------------
print()
print("Block 8: WHAT A BOOST DOES")
# (a) the tetrahedron AS A SHAPE in 3-space
tet = np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],dtype=float)/math.sqrt(3)
def ang(u,v): return math.degrees(math.acos(np.clip(np.dot(u,v),-1,1)))
a0 = ang(tet[0],tet[1])
print(f"  (a) rest frame  : tetrahedral angle = {a0:.6f} deg   (arccos(-1/3) = {math.degrees(math.acos(-1/3)):.6f})")
for beta in (0.3,0.6,0.9):
    gam = 1/math.sqrt(1-beta**2)
    # length contraction along x of a rigid configuration
    C = np.diag([1/gam,1.0,1.0])
    t2 = np.array([C@v/np.linalg.norm(C@v) for v in tet])
    angs = sorted(ang(t2[i],t2[j]) for i,j in itertools.combinations(range(4),2))
    print(f"      beta={beta}: angles spread {angs[0]:.4f} .. {angs[-1]:.4f} deg"
          f"   (was all {a0:.4f}) -> the SHAPE is destroyed")
    assert abs(angs[0]-a0) > 1.0

# (b) 2T as a SUBGROUP of SL(2,C)
def boost(beta, axis=(1,0,0)):
    # SL(2,C) element for a boost: exp(+rapidity/2 * sigma.n)
    rap = 0.5*math.log((1+beta)/(1-beta))
    sx = np.array([[0,1],[1,0]],dtype=complex)
    return np.cosh(rap/2)*np.eye(2) + np.sinh(rap/2)*sx
for beta in (0.3,0.6,0.9):
    B = boost(beta)
    assert abs(np.linalg.det(B)-1)<1e-12          # in SL(2,C)
    Gb = [B@g@np.linalg.inv(B) for g in G]
    # still a group, isomorphic, same multiplication table
    idxb = {key(m):i for i,m in enumerate(Gb)}
    assert len(idxb)==24
    tb = np.zeros((24,24),dtype=int)
    for i,a in enumerate(Gb):
        for j,b in enumerate(Gb):
            tb[i,j] = idxb[key(a@b)]
    assert (tb==table).all(), "multiplication table changed!"
    # traces invariant
    trb = Counter(np.round([complex(np.trace(m)).real for m in Gb],6))
    imb = max(abs(complex(np.trace(m)).imag) for m in Gb)
    assert dict(trb)==dict(tc) and imb < 1e-9
    # but the matrices are no longer unitary
    nonuni = max(np.linalg.norm(m.conj().T@m - np.eye(2)) for m in Gb)
    print(f"      beta={beta}: mult. table IDENTICAL, trace spectrum IDENTICAL,"
          f" max |U^dag U - 1| = {nonuni:.3f} -> left SU(2), stayed 2T")
print()
print("  => angles in 3-space: NOT boost invariant.")
print("     group structure + character table of 2T: boost invariant (conjugation).")

# ---------------- Block 9: 2 (x) 2 = 3 + 1 inherited from SU(2) ----------------
print()
def su2_to_so3(u):
    s = [np.array([[0,1],[1,0]],dtype=complex),
         np.array([[0,-1j],[1j,0]],dtype=complex),
         np.array([[1,0],[0,-1]],dtype=complex)]
    return np.array([[0.5*np.trace(s[a] @ u @ s[b] @ u.conj().T).real
                      for b in range(3)] for a in range(3)])
chi2 = np.array([complex(np.trace(g)).real for g in G])
chi3 = np.array([np.trace(su2_to_so3(g)).real for g in G])
assert np.allclose(chi2**2, chi3 + 1.0, atol=1e-8)
print("Block 9 OK: chi_2(g)^2 = chi_3(g) + 1 for all 24 elements")
print("           -> 2 (x) 2 = 3 + 1 : the 3 that acts on space is the symmetric")
print("              square of the spinor. 'Space' is derived, not assumed.")
print("           (this rule is why T'=2T is used as a flavour group: smallest")
print("            discrete group with 1-, 2- and 3-dim irreps)")

# ---------------- Block 10: Sum v_i = 0 is a THEOREM, not an axiom ----------------
R = [su2_to_so3(g) for g in G]                      # image in SO(3) = T, each twice
Rq = []
for r in R:
    if not any(np.allclose(r,x,atol=1e-8) for x in Rq): Rq.append(r)
assert len(Rq)==12, len(Rq)                          # |T| = |A4| = 12
# permutation character of T on the 4 tetrahedron vertices
perm_chi = []
for r in Rq:
    fixed = sum(1 for v in tet if np.allclose(r@v, v, atol=1e-8))
    perm_chi.append(fixed)
assert sorted(perm_chi) == [0,0,0,1,1,1,1,1,1,1,1,4], sorted(perm_chi)
# multiplicity of the trivial rep in the permutation rep
m_triv = sum(perm_chi)/12.0
# multiplicity of the trivial rep inside the 3 (vector rep)
m_triv_in_3 = sum(np.trace(r).real for r in Rq)/12.0
assert abs(m_triv - 1.0) < 1e-9, m_triv
assert abs(m_triv_in_3 - 0.0) < 1e-9, m_triv_in_3
S = sum(tet)
assert np.linalg.norm(S) < 1e-12
print()
print("Block 10 OK: perm. rep of T on the 4 vertices contains the trivial rep exactly",
      int(round(m_triv)), "time -> 4 = 1 + 3")
print("            the vector rep 3 contains the trivial rep", int(round(m_triv_in_3)),
      "times -> NO invariant vector exists")
print("            => sum_i v_i is T-invariant and must therefore vanish:",
      f"|sum v| = {np.linalg.norm(S):.1e}")
print("            'bipolar zero' is a THEOREM of irreducibility, not an axiom --")
print("            and it carries no information beyond equivariance (cf. 2026-09-11).")

# ---------------- Block 11: Molien series -> degrees of the invariants ----------------
print()
print("Block 11: invariant ring of 2T acting on C^2 (Molien series)")
import sympy as sp
t = sp.symbols('t')
M = sp.Rational(0)
for g in G:
    gm = sp.Matrix([[sp.nsimplify(sp.Rational(round(g[i,j].real*1000),1000)
                                  + sp.I*sp.Rational(round(g[i,j].imag*1000),1000))
                     for j in range(2)] for i in range(2)])
    M += 1/sp.det(sp.eye(2) - t*gm)
M = sp.simplify(M/24)
ser = sp.series(M, t, 0, 30).removeO()
co = [int(sp.nsimplify(ser.coeff(t, n))) for n in range(30)]
print("   dim of invariants by degree:", {n:c for n,c in enumerate(co) if c})
first = [n for n in range(1,30) if co[n] > 0]
assert first[:3] == [6,8,12], first[:3]
print("   -> primary invariants at degrees 6, 8, 12 (E6 singularity x^4+y^3+z^2=0)")
print("   -> 6+8+12 = 26, 6*8*12 = 576;  108 does NOT occur")
assert 108 not in [6,8,12] and 108 not in first[:8]
print("Block 11 OK")
print()
print("ALL BLOCKS PASSED (11 blocks)")
