import numpy as np
np.set_printoptions(precision=6, suppress=True)

P = np.array([
 [5, 9, 6, 0.884286376006, 1.369438406005, 0.866025403784],   # D3 triangular bipyramid
 [8,12, 6, 0.551285598433, 1.570796326795, 1.539600717839],   # C6 cube
 [6,12, 8, 1.359347637816, 1.910633236249, 1.333333333333],   # O8 octahedron
 [7,15,10, 1.663999068981, 2.192429488252, 1.585094193825],   # D5 pentagonal bipyramid
], dtype=float)

def build(P):
    Ts, us, vs = [], [], []
    for i in range(3):
        p, d = P[i], P[i+1]-P[i]
        v = p/ (p@p)
        Ts.append(np.eye(6) + np.outer(d, v)); us.append(d); vs.append(v)
    T = Ts[2] @ Ts[1] @ Ts[0]
    return T, np.array(us), np.array(vs)

def algebra_dim(us, vs):
    M = np.array([np.outer(us[i], vs[j]).ravel() for i in range(3) for j in range(3)])
    return np.linalg.matrix_rank(M, tol=1e-9)

def report(tag, P):
    T, us, vs = build(P)
    ev = np.linalg.eigvals(T)
    ones = np.sum(np.abs(ev - 1) < 1e-9)
    C = T[3:, :3]
    s = np.linalg.svd(C, compute_uv=False)
    G = np.array([[vs[j] @ us[i] for j in range(3)] for i in range(3)])
    G0 = G - np.trace(G)/3*np.eye(3)
    W = (G0 - G0.T)/2; S = (G0 + G0.T)/2
    nw = np.linalg.norm(W); ns = np.linalg.norm(S)
    print(f"--- {tag}")
    print("  eigenvalues :", np.sort_complex(ev))
    print(f"  #(lambda=1) : {ones}   algebra dim: {algebra_dim(us,vs)}")
    print(f"  C svd       : {s}   1st-mode energy: {100*s[0]**2/ (s**2).sum():.2f}%")
    print(f"  Tr(G)={np.trace(G):.8f}  ||w||={nw:.8f}  ||s||={ns:.8f}  ratio={ns/nw:.5f}")
    return ev, s, ns/nw

print("========== 1. 論文の数値の再現 ==========")
report("TTT-core の4状態", P)

print()
print("========== 2. 帰無対照：ランダムな4ベクトル ==========")
rng = np.random.default_rng(0)
ratios = []
for k in range(5):
    R = np.column_stack([
        rng.integers(4, 20, 4).astype(float),
        rng.integers(6, 30, 4).astype(float),
        rng.integers(4, 20, 4).astype(float),
        rng.uniform(0.3, 2.0, 4),
        rng.uniform(1.0, 2.5, 4),
        rng.uniform(0.5, 2.0, 4),
    ])
    _, _, r = report(f"random #{k+1}", R)
    ratios.append(r)
print("  ランダム系の 歪み/旋回 比:", np.round(ratios, 4))

print()
print("========== 3. 単位依存性テスト（体積 V を x1000 にするだけ） ==========")
for f in [1.0, 10.0, 1000.0]:
    Q = P.copy(); Q[:, 5] *= f
    report(f"volume scale x{f:g}", Q)

print()
print("========== 4. 可視量 (V,E,F) を 1/100 に正規化 ==========")
Q = P.copy(); Q[:, :3] /= 100.0
report("V,E,F /100", Q)
