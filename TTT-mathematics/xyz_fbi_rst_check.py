"""
xyz_fbi_rst_check.py
XYZ（位置）・FBI（力）・RST（回転）の関係式の機械検証。
対応文書: xyz_fbi_rst_relations.md
依存: numpy のみ。実行: python3 xyz_fbi_rst_check.py
"""
import itertools
import numpy as np

rng = np.random.default_rng(20261017)
TOL = 1e-10
results = []


def check(label, cond):
    results.append((label, bool(cond)))
    print(("PASS " if cond else "FAIL ") + label)


# ---------------------------------------------------------------
# 定理1: 回転による位置の変化 dX = dR × X に対し、力の仕事は
#        F·dX = (X × F)·dR  （トルク×回転角）
# ---------------------------------------------------------------
ok = True
for _ in range(1000):
    X, F, dR = rng.normal(size=(3, 3))
    lhs = F @ np.cross(dR, X)
    rhs = np.cross(X, F) @ dR
    ok &= abs(lhs - rhs) < TOL
check("定理1: F·(dR×X) = (X×F)·dR", ok)

# P6 = F·dX + (X×F)·dR は、並進 dX と回転 dR を合わせた変位の仕事
ok = True
for _ in range(1000):
    X, F, dX, dR = rng.normal(size=(4, 3))
    P6 = F @ dX + np.cross(X, F) @ dR
    total_disp = dX + np.cross(dR, X)
    ok &= abs(P6 - F @ total_disp) < TOL
check("定理1': P6 = F·(dX + dR×X)", ok)

# ---------------------------------------------------------------
# 定理2: 3⊗3⊗3 (27成分) の回転不変成分は1つだけで、ε_abc
# ---------------------------------------------------------------
def so3_generators():
    L = np.zeros((3, 3, 3))
    for a, b, c in itertools.permutations(range(3)):
        L[a, b, c] = np.linalg.det(np.eye(3)[[a, b, c]])
    return [-L[k] for k in range(3)]  # (L_k)_{bc} = -ε_kbc


def rep3(gen):
    I = np.eye(3)
    return (np.kron(np.kron(gen, I), I)
            + np.kron(np.kron(I, gen), I)
            + np.kron(np.kron(I, I), gen))


G = so3_generators()
M = np.vstack([rep3(g) for g in G])           # 81×27
_, s, Vt = np.linalg.svd(M)
null_dim = int(np.sum(s < 1e-9)) + (27 - len(s))
check(f"定理2: 回転不変な成分の数 = {null_dim}（期待値 1）", null_dim == 1)

eps = np.zeros((3, 3, 3))
for a, b, c in itertools.permutations(range(3)):
    eps[a, b, c] = np.linalg.det(np.eye(3)[[a, b, c]])
inv = Vt[-1].reshape(3, 3, 3)
inv = inv / inv[0, 1, 2]
check("定理2: その成分は ε_abc（完全反対称）", np.allclose(inv, eps))

# 27 = 1+3+3+3+5+5+7 : カシミール演算子 J² の固有値 l(l+1) の重複度
J2 = sum(rep3(g) @ rep3(g) for g in G)
ev = np.round(-np.linalg.eigvalsh(J2), 6)
counts = {l: int(np.sum(np.isclose(ev, l * (l + 1)))) // (2 * l + 1)
          for l in range(4)}
check(f"定理2: 27 の分解 l=0,1,2,3 の個数 = {counts}（期待値 1,3,2,1）",
      counts == {0: 1, 1: 3, 2: 2, 3: 1})

# 不変量 (X×F)·R と ε_abc X_a F_b R_c の一致
ok = True
for _ in range(1000):
    X, F, R = rng.normal(size=(3, 3))
    T = np.einsum("a,b,c->abc", X, F, R)
    ok &= abs(np.einsum("abc,abc", eps, T) - np.cross(X, F) @ R) < TOL
check("定理2: ε_abc X_a F_b R_c = (X×F)·R", ok)

# 回転で不変・鏡映で符号反転
ok_rot, ok_mir = True, True
for _ in range(200):
    X, F, R = rng.normal(size=(3, 3))
    Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    e0 = np.cross(X, F) @ R
    e_rot = np.cross(Q @ X, Q @ F) @ (Q @ R)
    P = Q @ np.diag([-1, 1, 1])                 # 鏡映（det = -1）
    e_mir = np.cross(P @ X, P @ F) @ (P @ R)
    ok_rot &= abs(e_rot - e0) < 1e-9
    ok_mir &= abs(e_mir + e0) < 1e-9
check("定理2: 不変量は回転で不変", ok_rot)
check("定理2: 不変量は鏡映で符号反転（右手系/左手系）", ok_mir)

# ---------------------------------------------------------------
# 定理3: 四元数 q = (1+i+j+k)/2
# ---------------------------------------------------------------
def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return np.array([a1*a2 - b1*b2 - c1*c2 - d1*d2,
                     a1*b2 + b1*a2 + c1*d2 - d1*c2,
                     a1*c2 - b1*d2 + c1*a2 + d1*b2,
                     a1*d2 + b1*c2 - c1*b2 + d1*a2])


def rotate(q, v):
    qc = q * np.array([1, -1, -1, -1])
    return qmul(qmul(q, np.r_[0.0, v]), qc)[1:]


q = np.array([1, 1, 1, 1]) / 2
w = (1 + np.sqrt(3) * 1j) / 2
check("定理3: |w|=1, arg w = 60°", abs(abs(w) - 1) < TOL
      and abs(np.degrees(np.angle(w)) - 60) < 1e-9)
check("定理3: Re q = Re w = 1/2 かつ |Im q| = Im w = √3/2",
      abs(q[0] - w.real) < TOL and abs(np.linalg.norm(q[1:]) - w.imag) < TOL)
qq = np.array([1.0, 0, 0, 0])
for _ in range(6):
    qq = qmul(qq, q)
check("定理3: q^6 = 1（w^6 = 1 と同じ）", np.allclose(qq, [1, 0, 0, 0])
      and abs(w**6 - 1) < 1e-12)
tetra = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
img = np.array([rotate(q, v) for v in tetra])
perm = [int(np.argmin(np.linalg.norm(tetra - p, axis=1))) for p in img]
check(f"定理3: q は正四面体の頂点を写す 置換 {perm}",
      sorted(perm) == [0, 1, 2, 3] and np.allclose(img, tetra[perm]))
check("定理3: 軸 (1,1,1) は固定、残り3頂点を巡回", perm[0] == 0
      and perm[1:] in ([2, 3, 1], [3, 1, 2]))
v = np.array([1.0, -1.0, 0.0])                # 軸に垂直なベクトル
ang = np.degrees(np.arccos(v @ rotate(q, v) / (v @ v)))
check(f"定理3: 回転角 = {ang:.6f}°（半角 60° の2倍 = 120°）",
      abs(ang - 120) < 1e-9)

# ---------------------------------------------------------------
# 定理4: 3軸の組の向き（行列式）と、向きを反転させる操作
# ---------------------------------------------------------------
E = np.eye(3)
left = E[[0, 2, 1]]                           # 左手系の組
check("定理4: 右手系の組 det = +1", abs(np.linalg.det(E) - 1) < TOL)
check("定理4: 左手系の組 det = -1", abs(np.linalg.det(left) + 1) < TOL)
check("定理4: 反転操作を1回作用させると -1 → +1",
      abs(np.linalg.det(np.diag([-1, 1, 1]) @ left) - 1) < TOL)

# ---------------------------------------------------------------
# 定理5: 双極 Ψ⁺ + Ψ⁻ = 0 のとき Ψ⁺ − Ψ⁻ = ±2Ψ
# ---------------------------------------------------------------
ok = True
for _ in range(100):
    psi = rng.normal(size=9)
    pp, pm = psi, -psi
    ok &= np.allclose(pp + pm, 0) and np.allclose(pp - pm, 2 * psi) \
        and np.allclose(pm - pp, -2 * psi)
check("定理5: Ψ⁺+Ψ⁻=0 ⇒ Ψ⁺−Ψ⁻ = ±2Ψ（9成分）", ok)

# ---------------------------------------------------------------
n_pass = sum(r for _, r in results)
print(f"\n{n_pass} PASS / {len(results) - n_pass} FAIL")
raise SystemExit(0 if n_pass == len(results) else 1)
