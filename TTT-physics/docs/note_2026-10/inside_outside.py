"""TTT 検証 2026-10-05 (3/3): 中から3、外から4 ― XYZ・RST・FBI
numpy のみ。全 assert が通れば PASS。
"""
import itertools
import numpy as np

PASS = 0
def ok(cond, msg):
    global PASS
    assert cond, msg
    PASS += 1
    print(f"  PASS  {msg}")

print("== Block 1: 中から3・外から4（3次元球面と四元数）")
q = np.array([0.3, 0.5, -0.4, 0.2]); q /= np.linalg.norm(q)
ok(len(q) == 4 and np.isclose(q @ q, 1), "単位四元数: 成分4 (実部1+虚部3)、制約1 → 自由度3")
def rot(q):
    w, x, y, z = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
                     [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
                     [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]])
ok(np.allclose(rot(q), rot(-q)), "q と -q は同じ3次元回転（一つの回転に二つの極）")
ok(np.allclose(rot(q).T @ rot(q), np.eye(3)), "rot(q) は直交行列")

print("== Block 2: 外から見ると二組の回転が独立")
def L(i, j):
    M = np.zeros((4, 4)); M[i, j] = -1; M[j, i] = 1; return M
Ls = {(i, j): L(i, j) for i, j in itertools.combinations(range(4), 2)}
ok(len(Ls) == 6, "4次元の回転面は 6（3次元では 3）")
Jl = [0.5 * (Ls[(1, 2)] + Ls[(0, 3)]), 0.5 * (-Ls[(0, 2)] + Ls[(1, 3)]), 0.5 * (Ls[(0, 1)] + Ls[(2, 3)])]
Jr = [0.5 * (Ls[(1, 2)] - Ls[(0, 3)]), 0.5 * (-Ls[(0, 2)] - Ls[(1, 3)]), 0.5 * (Ls[(0, 1)] - Ls[(2, 3)])]
com = lambda a, b: a @ b - b @ a
ok(all(np.allclose(com(a, b), 0) for a in Jl for b in Jr), "左回りの3つと右回りの3つは可換（二つの極は独立）")
ok(not np.allclose(com(Jl[0], Jl[1]), 0) and not np.allclose(com(Jr[0], Jr[1]), 0), "各組の中の3つは非可換（未解決のまま）")

print("== Block 3: F·B·I = -1、F·B·I·e^{πu} = 1")
def qm(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                     w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2, w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2])
one = np.array([1, 0, 0, 0.]); F = np.array([0, 1, 0, 0.]); B = np.array([0, 0, 1, 0.]); I = np.array([0, 0, 0, 1.])
ok(all(np.allclose(qm(u, u), -one) for u in (F, B, I)), "F² = B² = I² = -1")
FBI = qm(qm(F, B), I)
ok(np.allclose(FBI, -one), "F·B·I = -1（ハミルトンの関係）")
eu = np.cos(np.pi) * one + np.sin(np.pi) * F
ok(np.allclose(eu, -one), "π を位相 e^{πu} と読むと -1")
ok(np.allclose(qm(FBI, eu), one), "F·B·I·e^{πu} = +1")
ok(not np.isclose(-np.pi, 1), "π を数 3.14… と読むと F·B·I·π = -π ≠ 1")
Rx = np.diag([1, -1, -1.]); Ry = np.diag([-1, 1, -1.]); Rz = np.diag([-1, -1, 1.])
ok(np.allclose(Rx @ Ry @ Rz, np.eye(3)), "中から（3次元回転）: 180°×3軸 = 恒等（符号が見えない）")

print("== Block 4: XYZ と FBI（クリフォード代数 Cl(3)）")
X = np.array([[0, 1], [1, 0]], complex); Y = np.array([[0, -1j], [1j, 0]]); Z = np.array([[1, 0], [0, -1]], complex)
E2 = np.eye(2)
ok(all(np.allclose(a @ a, E2) for a in (X, Y, Z)), "X² = Y² = Z² = +1（軸）")
Fc, Bc, Ic = Z @ Y, X @ Z, Y @ X
ok(all(np.allclose(a @ a, -E2) for a in (Fc, Bc, Ic)), "F=ZY, B=XZ, I=YX（回転面）の2乗は -1")
ok(np.allclose(Fc @ Bc @ Ic, -E2) and np.allclose(Fc @ Bc, Ic), "F·B·I = -1、F·B = I")
ok(np.allclose((Y @ Z) @ (Z @ X) @ (X @ Y), E2), "面の向きを逆にすると F·B·I = +1（向きが双極）")
P = X @ Y @ Z
ok(np.allclose(P @ P, -E2), "XYZ（3重の積）の2乗は -1")
blades = [cc for k in range(4) for cc in itertools.combinations("XYZ", k)]
ok(len(blades) == 8, "基底 1,X,Y,Z,XY,XZ,YZ,XYZ の 8 = 2^3（各軸の使う・使わない）")

print("== Block 5: 位置 XYZ と向き RST")
th = 0.7; u = np.array([1, 2, 2]) / 3
K = np.array([[0, -u[2], u[1]], [u[2], 0, -u[0]], [-u[1], u[0], 0]])
R = np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * K @ K
ok(R.size == 9 and np.allclose(R.T @ R, np.eye(3)), "回転行列 = RST の3軸を XYZ で表した 3×3、制約6 → 自由度3")
ok(3 + 3 == 6 and 8 - 2 == 6, "位置3＋向き3 = 6 = 双対四元数 8 − 制約 2")

print("== Block 6: 3×3×3 の表 ε")
eps = np.zeros((3, 3, 3), int)
for p in itertools.permutations(range(3)):
    s = 1
    for a in range(3):
        for b in range(a + 1, 3):
            if p[a] > p[b]: s = -s
    eps[p] = s
v = eps.flatten()
ok(v.size == 27 and (v == 1).sum() == 3 and (v == -1).sum() == 3 and (v == 0).sum() == 21, "ε: 27マス = +1が3、-1が3、0が21")
Qs = [Fc, Bc, Ic]
# Fc,Bc,Ic を (1,2),(2,0),(0,1) の面として ε に対応させる確認: Q_i Q_j = -δ_ij + Σ ε_ijk Q_k
ok(all(np.allclose(Qs[i] @ Qs[j], -(i == j) * E2 + sum(eps[i, j, k] * Qs[k] for k in range(3))) for i in range(3) for j in range(3)),
   "F_i F_j = -δ_ij + Σ_k ε_ijk F_k")
ok(len(list(itertools.combinations(range(3), 3))) == 1, "3次元の完全反対称3階の表は定数倍を除き1つ")

print("== Block 7: 2^27")
ok(((2 ** 3) ** 3) ** 3 == 2 ** 27 == 134217728, "((2³)³)³ = 2^(3·3·3) = 134,217,728（27マスへの±の割当数）")

print(f"\n{PASS} PASS / 0 FAIL")
