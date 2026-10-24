import itertools, math
import numpy as np

n = 0
def check(c, m):
    global n
    assert c, m
    n += 1
    print("ok:", m)

# 1. 直交 3 軸を (1,1,1) 方向に投影 → 120°、和 0
u = np.ones(3) / math.sqrt(3)
E = np.eye(3)
P = [e - e.dot(u) * u for e in E]
ang = [math.degrees(math.acos(P[i].dot(P[j]) / np.linalg.norm(P[i]) / np.linalg.norm(P[j])))
       for i, j in [(0, 1), (1, 2), (0, 2)]]
check(all(abs(a - 120) < 1e-9 for a in ang), f"投影した3方向の角度 {ang}")
check(np.allclose(sum(P), 0), "3方向の和 = 0（色の中和）")

# 2. SU(3) のウェイト（ゲルマン行列 λ3, λ8 の固有値）と一致するか
l3 = np.diag([1, -1, 0]) / 2
l8 = np.diag([1, 1, -2]) / (2 * math.sqrt(3))
W = [np.array([l3[i, i], l8[i, i]]) for i in range(3)]
# 平面上の正規直交基底で P を座標化
b1 = (E[0] - E[1]) / math.sqrt(2)
b2 = np.cross(u, b1)
Q = [np.array([p.dot(b1), p.dot(b2)]) for p in P]
# 長さの比と角度が一致（相似）
lenW = [np.linalg.norm(w) for w in W]; lenQ = [np.linalg.norm(q) for q in Q]
check(np.allclose(np.array(lenW) / lenW[0], np.array(lenQ) / lenQ[0]), "3色のウェイトと投影の長さ比が一致")
angW = [math.degrees(math.acos(W[i].dot(W[j]) / lenW[i] / lenW[j])) for i, j in [(0, 1), (1, 2), (0, 2)]]
check(all(abs(a - 120) < 1e-9 for a in angW), "SU(3) の3色ウェイトも 120°")
scale = lenW[0] / lenQ[0]
# 回転＋拡大で一致するか（Kabsch）
A = np.array(Q) * scale; B = np.array(W)
U, S, Vt = np.linalg.svd(A.T @ B); R = U @ Vt
check(np.allclose(A @ R, B, atol=1e-12), "投影した XYZ は回転と拡大で SU(3) の3色ウェイトに一致")

# 3. グルーオン 8 種 = 随伴表現のウェイト：6 本（差 e_i - e_j）＋ 中心 2
lam = [np.zeros((3, 3), complex) for _ in range(8)]
lam[0][0,1]=lam[0][1,0]=1
lam[1][0,1]=-1j; lam[1][1,0]=1j
lam[2][0,0]=1; lam[2][1,1]=-1
lam[3][0,2]=lam[3][2,0]=1
lam[4][0,2]=-1j; lam[4][2,0]=1j
lam[5][1,2]=lam[5][2,1]=1
lam[6][1,2]=-1j; lam[6][2,1]=1j
lam[7]=np.diag([1,1,-2])/math.sqrt(3)
T = [l / 2 for l in lam]
def ad(X):
    M = np.zeros((8, 8), complex)
    for b in range(8):
        C = X @ T[b] - T[b] @ X
        for a in range(8):
            M[a, b] = 2 * np.trace(T[a] @ C)
    return M
H3, H8 = ad(T[2]), ad(T[7])
ev, vec = np.linalg.eig(H3 + 0.123 * H8)  # 同時対角化
roots = []
for k in range(8):
    v = vec[:, k]
    r3 = (v.conj() @ H3 @ v) / (v.conj() @ v)
    r8 = (v.conj() @ H8 @ v) / (v.conj() @ v)
    roots.append((round(r3.real, 9), round(r8.real, 9)))
zero = [r for r in roots if abs(r[0]) < 1e-9 and abs(r[1]) < 1e-9]
nonzero = [r for r in roots if r not in zero]
check(len(zero) == 2 and len(nonzero) == 6, "グルーオン 8 = 中心 2 + 6 本")
diffs = sorted({(round(W[i][0]-W[j][0], 9), round(W[i][1]-W[j][1], 9)) for i in range(3) for j in range(3) if i != j})
check(sorted(nonzero) == diffs, "6 本は3色ウェイトの差（Δ の辺を両向きにたどったもの）")
L6 = [math.hypot(*r) for r in nonzero]
check(max(L6) - min(L6) < 1e-9, "6 本は同じ長さ（正六角形）")

# 4. 正四面体を3回軸から見ると、三角形＋中心（Y と Δ）
tet = np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]], float)  # 立方体の交互の頂点
axis = tet[0] / np.linalg.norm(tet[0])                            # 立方体の対角線
proj = [t - t.dot(axis) * axis for t in tet]
check(np.allclose(proj[0], 0), "頂点 1 は中心に重なる（Y の接合点）")
d = [np.linalg.norm(proj[i] - proj[j]) for i, j in [(1,2),(2,3),(1,3)]]
check(max(d) - min(d) < 1e-12, "残り 3 頂点は正三角形（Δ）")
check(abs(axis.dot(np.ones(3) / math.sqrt(3)) - 1) < 1e-12, "正四面体の3回軸 = 立方体の対角線 (1,1,1)")

# 5. ビリアル：H = |p| + σ|x|（相対論的）で <T> = <V>、H = p²/2 + σ|x| で <T> = <V>/2
N, Lbox = 4096, 60.0
x = np.linspace(-Lbox/2, Lbox/2, N, endpoint=False); dx = x[1]-x[0]
p = 2*np.pi*np.fft.fftfreq(N, dx)
F = np.fft.fft(np.eye(N), axis=0); Fi = np.conj(F).T / N
def ground(Tp):
    Tm = (Fi @ np.diag(Tp) @ F).real
    H = Tm + np.diag(np.abs(x))
    w, v = np.linalg.eigh(H); g = v[:, 0]
    return g @ Tm @ g, g @ (np.abs(x) * g)
N = 1024; Lbox = 40.0
x = np.linspace(-Lbox/2, Lbox/2, N, endpoint=False); dx = x[1]-x[0]
p = 2*np.pi*np.fft.fftfreq(N, dx)
F = np.fft.fft(np.eye(N), axis=0); Fi = np.conj(F).T / N
Tr, Vr = ground(np.abs(p))
Tn, Vn = ground(p**2 / 2)
check(abs(Tr / Vr - 1) < 0.02, f"相対論的（質量0）: <T>/<V> = {Tr/Vr:.4f}")
check(abs(Tn / Vn - 0.5) < 0.02, f"非相対論的: <T>/<V> = {Tn/Vn:.4f}")

# 6. 格子QCD の 33% と 37% の比
T_, sT = 33, math.hypot(4, 4); V_, sV = 37, math.hypot(5, 4)
r = T_ / V_; sr = r * math.hypot(sT / T_, sV / V_)
z1 = (1 - r) / sr; z05 = (r - 0.5) / sr
print(f"T/V = {r:.3f} ± {sr:.3f}; 1:1 から {z1:.2f}σ, 1:2 から {z05:.2f}σ")
check(abs(z1) < 1 and z05 > 1.5, "格子QCD は 1:1（相対論的）と合い、1:2（非相対論的）とは約 1.8σ ずれる")

# 7. 数え方：Y の腕 3 と クォーク 3 → 1:1、Δ 張力半分 → 1.5:3
check(3 / 3 == 1 and (3 * 0.5) / 3 == 0.5, "要素あたり等配分なら Y は 1:1、Δ（張力半分）は 1:2")
check(3 / 8 != 1, "クォーク 3 : グルーオン 8 の数をそのまま使うと 1:1 にならない")

# 8. Δ と Y の幾何（正三角形の一辺 a = 1）
a = 1.0
LD, LY = 3 * a, math.sqrt(3) * a
arm = math.sqrt((a / math.sqrt(3))**2 + (a * math.sqrt(2 / 3))**2)
check(abs(arm - a) < 1e-12 and abs(3 * arm - LD) < 1e-12, "Y を持ち上げた正四面体の3本 = Δ の3辺 = 3a（辺 6 = 3 + 3）")
check(abs(LY / (LD / 2) - 2 / math.sqrt(3)) < 1e-12, "Y / Δ(張力半分) = 2/√3 = 1.155（正三角形）")

# 9. 張力 0.9 GeV/fm と 5×5×5 の 1 マス（三角形の一辺 = 1 マス）
s, M, rp = 0.9, 0.93827208816, 0.8409
cells = {"A": 2 * rp / 5, "B": rp * (4 * math.pi / 3) ** (1 / 3) / 5, "C": (2 * rp / math.sqrt(3)) / 5}
pct = {k: {"Y": 100 * s * math.sqrt(3) * c / M, "D": 100 * s * 1.5 * c / M, "T": 100 * s * 3 * c / M}
       for k, c in cells.items()}
for k in pct:
    print(k, round(cells[k], 4), {q: round(v, 1) for q, v in pct[k].items()})
lo, hi = 37 - math.hypot(5, 4), 37 + math.hypot(5, 4)
inside = [(k, q) for k in pct for q in pct[k] if lo <= pct[k][q] <= hi]
check(sorted(inside) == [("B", "D"), ("C", "Y")], f"37±6.4% に入るのは B×Δ と C×Y のみ {inside}")
Er = s * math.sqrt(3) * (math.sqrt(3) * rp)
check(Er / M > 2.4, "クォークを陽子半径に置くと Y の力線だけで陽子質量の 2.4 倍")

# 10. 双対：正二十面体と正十二面体
for V, Ed, Fc in [(12, 30, 20), (20, 30, 12), (8, 12, 6), (6, 12, 8), (4, 6, 4)]:
    check(V - Ed + Fc == 2, f"オイラー V-E+F=2: {V},{Ed},{Fc}（合計 {V+Ed+Fc}）")

# 11. 77/12 と球・立方体・黄金比の定数
t = 77 / 12; tol = 0.0025 / 4
phi = (1 + 5 ** 0.5) / 2
for name, v in [("2π", 2 * math.pi), ("4(4π/3)^(1/3)", 4 * (4 * math.pi / 3) ** (1 / 3)), ("√41", 41 ** 0.5), ("4φ", 4 * phi)]:
    check(abs(v - t) > 10 * tol, f"{name} = {v:.4f} は 77/12 から許容幅の 10 倍以上離れる")
check(abs((24 + 10 / 6) / 4 - t) < 1e-12, "(24 + 10/6)/4 = 77/12 = 6 + 5/12")
print(f"\nall {n} checks passed")
