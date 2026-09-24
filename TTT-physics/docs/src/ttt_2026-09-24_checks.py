"""
TTT 検証記録 2026-09-24 — 【A】項目の機械検証スクリプト
依存: numpy のみ。  実行: python3 ttt_2026-09-24_checks.py
各ブロックは assert で停止する。最後まで走れば全項目 PASS。
"""
import itertools, math
from collections import Counter
from fractions import Fraction as F
import numpy as np

PASS = []
def ok(tag, msg):
    PASS.append(tag); print(f"[PASS] {tag}: {msg}")

# ---------------------------------------------------------------- A1
# SO(18) スピノル（9個の二値モード）→ SO(10)×SO(8) 分岐と正味世代数
W = list(itertools.product([1, -1], repeat=9))
weyl = [s for s in W if s.count(-1) % 2 == 0]
blk = Counter((s[:5].count(-1) % 2, s[5:].count(-1) % 2) for s in weyl)
assert len(W) == 512 and len(weyl) == 256
assert blk[(0, 0)] == 128 and blk[(1, 1)] == 128          # (16,8s)+(16bar,8c)
ok("A1", "2^9=512, Weyl 256 = (16,8s)+(16bar,8c) → 16が8個・16barが8個、正味0世代")

# ---------------------------------------------------------------- A2
# SO(8) 内のアーベル群 Z_N による射影：正味世代数 (#16 − #16bar) は常に偶数
S4 = list(itertools.product([1, -1], repeat=4))
s8 = [s for s in S4 if s.count(-1) % 2 == 0]
c8 = [s for s in S4 if s.count(-1) % 2 == 1]
def kept(Wt, t):
    return sum(1 for w in Wt if (sum(F(x, 2) * t[j] for j, x in enumerate(w))) % 1 == 0)
nets_all = {}
for N in (2, 3, 4, 6):
    nets = set()
    for m in itertools.product(range(2 * N), repeat=4):
        t = [F(x, N) for x in m]
        if any((N * sum(F(x, 2) * t[j] for j, x in enumerate(w))) % 1 for w in S4):
            continue
        nets.add(kept(s8, t) - kept(c8, t))
    nets_all[N] = sorted(nets)
    assert all(n % 2 == 0 for n in nets)
assert nets_all[3] == [-6, 0, 6]
ok("A2", f"Z_N 射影の正味世代数は常に偶数（Z3 は {nets_all[3]}）→ 3 は出ない")

# ---------------------------------------------------------------- 共通：有理写像
def sph(z):
    r2 = abs(z) ** 2
    return np.array([2 * z.real, 2 * z.imag, r2 - 1]) / (1 + r2)
def zeta(v):
    return (v[0] + 1j * v[1]) / (1 - v[2])
def kabsch(A, B):
    U, _, Vt = np.linalg.svd(A.T @ B)
    D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
    R = Vt.T @ D @ U.T
    return R, np.abs(A @ R.T - B).max()

s3 = math.sqrt(3); I = 1j
maps = {
    3: (np.poly1d([I * s3, 0, -1]), np.poly1d([1, 0, -I * s3, 0])),
    4: (np.poly1d([1, 0, 2 * s3 * I, 0, 1]), np.poly1d([1, 0, -2 * s3 * I, 0, 1])),
    7: (np.poly1d([1, 0, -7, 0, 0, -7, 0, -1]), np.poly1d([1, 0, 7, 0, 0, -7, 0, 1])),
}
def holes(B):
    p, q = maps[B]
    Wr = np.polyder(p) * q - p * np.polyder(q)
    pts = [sph(r) for r in Wr.r]
    while len(pts) < 2 * B - 2:
        pts.append(np.array([0, 0, 1.0]))
    return np.array(pts)

# ---------------------------------------------------------------- A3
# B=3 スカーミオン（有理写像）の対称群を SU(2) に持ち上げると 2T
H3 = holes(3)
rots = []
for perm in itertools.permutations(range(4)):
    R, err = kabsch(H3, H3[list(perm)])
    if err < 1e-8 and np.linalg.det(R) > 0:
        rots.append(R)
assert len(rots) == 12
rng = np.random.default_rng(1)
Z = [complex(*rng.normal(size=2)) for _ in range(40)]
p3, q3 = maps[3]; R3 = lambda z: p3(z) / q3(z)
Vt_ = np.array([sph(R3(z)) for z in Z])
for g in rots:
    Wt = np.array([sph(R3(zeta(g @ sph(z)))) for z in Z])
    _, err = kabsch(Vt_, Wt)
    assert err < 1e-7
def su2(R):
    ang = math.acos(max(-1, min(1, (np.trace(R) - 1) / 2)))
    if ang < 1e-9:
        return np.eye(2, dtype=complex)
    w, v = np.linalg.eig(R)
    ax = np.real(v[:, np.argmin(abs(w - 1))]); ax /= np.linalg.norm(ax)
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    if not np.allclose(np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K, R, atol=1e-7):
        ax = -ax
    sx = np.array([[0, 1], [1, 0]]); sy = np.array([[0, -1j], [1j, 0]]); sz = np.array([[1, 0], [0, -1]])
    return math.cos(ang / 2) * np.eye(2) - 1j * math.sin(ang / 2) * (ax[0] * sx + ax[1] * sy + ax[2] * sz)
G = []
for g in rots:
    for U in (su2(g), -su2(g)):
        if not any(np.allclose(U, V) for V in G):
            G.append(U)
assert len(G) == 24 and all(any(np.allclose(A @ B, C) for C in G) for A in G for B in G)
tr = Counter(round(float(np.trace(U).real), 4) for U in G)
assert tr[2.0] == 1 and tr[-2.0] == 1 and tr[1.0] == 8 and tr[-1.0] == 8 and tr[0.0] == 6
ok("A3", "B=3 の対称回転 12 個はすべて写像の対称性、SU(2) 持ち上げは位数24で閉じ、跡の分布が 2T と一致")

# ---------------------------------------------------------------- A4
# 殻の穴の配置：B=3 正四面体 / B=4 正八面体 / B=7 正二十面体（殻はそれぞれ 正四面体・立方体・正十二面体）
expect = {3: (4, 109.4712, 3), 4: (6, 90.0, 4), 7: (12, 63.4349, 5)}
for B, (n, ang, nb) in expect.items():
    P = holes(B); Gm = np.clip(P @ P.T, -1, 1); np.fill_diagonal(Gm, -2)
    nn = np.degrees(np.arccos(Gm.max(axis=1)))
    assert len(P) == n and np.ptp(nn) < 1e-4 and abs(nn.mean() - ang) < 1e-3
    cnt = {int(np.isclose(np.degrees(np.arccos(np.clip(Gm[i], -1, 1))), nn[i], atol=1e-4).sum()) for i in range(n)}
    assert cnt == {nb}
ok("A4", "穴の配置 B=3→正四面体, B=4→正八面体, B=7→正二十面体（殻は双対：正四面体・立方体・正十二面体）")

# ---------------------------------------------------------------- A5
Fc = lambda B: 2 * B - 2
for k in range(1, 5):
    for Bs in itertools.product(range(1, 12), repeat=k):
        assert Fc(sum(Bs)) == sum(Fc(b) for b in Bs) + 2 * (k - 1)
plat = {'正四面体': (4, 4, 3), '立方体': (6, 8, 3), '正八面体': (8, 6, 4), '正十二面体': (12, 20, 3), '正二十面体': (20, 12, 5)}
shell_ok = [n for n, (Fn, V, val) in plat.items() if val == 3 and V == 4 * ((Fn + 2) // 2) - 8]
assert shell_ok == ['正四面体', '立方体', '正十二面体']
ok("A5", "F(ΣB)=ΣF(B)+2(k−1)（+2 は合体ごと）／殻になれる正多面体は 正四面体・立方体・正十二面体 のみ")

# ---------------------------------------------------------------- A6
# 正二十面体回転群 I で不変な球面調和関数の次数 → l=2 なし → 固有四重極 0
clsI = [(0, 1), (2 * math.pi / 5, 12), (4 * math.pi / 5, 12), (2 * math.pi / 3, 20), (math.pi, 15)]
chiL = lambda l, t: 2 * l + 1 if t == 0 else math.sin((2 * l + 1) * t / 2) / math.sin(t / 2)
inv = [l for l in range(17) if round(sum(c * chiL(l, t) for t, c in clsI) / 60) > 0]
assert inv == [0, 6, 10, 12, 15, 16]
ok("A6", f"I 不変な l = {inv} → l=2 なし：正二十面体対称の固有四重極モーメントは厳密に 0")

# ---------------------------------------------------------------- A7
# 二重被覆 2I での半整数スピンの既約性と、アイソスピン T との表現共有
cls2I = [(0, 1), (math.pi, 1), (math.pi / 5, 12), (2 * math.pi / 5, 12), (3 * math.pi / 5, 12),
         (4 * math.pi / 5, 12), (math.pi / 3, 20), (2 * math.pi / 3, 20), (math.pi / 2, 30)]
def chiJ(j, p):
    s = math.sin(p)
    if abs(s) < 1e-12:
        return (2 * j + 1) * (1 if p < 1 else (-1) ** int(round(2 * j)))
    return math.sin((2 * j + 1) * p) / s
ov = lambda a, b: round(sum(c * chiJ(a, p) * chiJ(b, p) for p, c in cls2I) / 120, 6)
assert [ov(j, j) for j in (0.5, 1.5, 2.5, 3.5)] == [1, 1, 1, 2]
share = lambda T: [j2 / 2 for j2 in range(1, 12, 2) if ov(j2 / 2, T) > 0]
assert share(1.5)[0] == 1.5 and share(3.5)[0] == 2.5 and share(6.5)[0] == 0.5
ok("A7", "2I で J=1/2,3/2,5/2 は既約・7/2 から可約／T と表現を共有する最低 J："
         f"T=3/2→{share(1.5)[0]}, T=7/2→{share(3.5)[0]}, T=13/2→{share(6.5)[0]}")

# ---------------------------------------------------------------- A8
# 二十面体フラーレン殻：B = 5(h²+hk+k²)+2 と (h,k)・キラル性
sols = {}
for h in range(8):
    for k in range(h + 1):
        T = h * h + h * k + k * k
        if T:
            sols.setdefault(5 * T + 2, []).append((h, k))
lab = {B: sols[B] for B in (7, 17, 22, 37, 47, 67, 97, 137)}
assert lab == {7: [(1, 0)], 17: [(1, 1)], 22: [(2, 0)], 37: [(2, 1)], 47: [(3, 0)],
               67: [(3, 1)], 97: [(3, 2)], 137: [(3, 3)]}
chiral = [B for B in (7, 17, 37, 67, 97) if any(k and h != k for h, k in sols[B])]
assert chiral == [37, 67, 97]
between = sorted(b for b in sols if 97 < b < 137)
assert between == [107, 127]
ok("A8", f"(h,k): {lab}；BHS列のうちキラルは {chiral}；97 と 137 の間にも {between} がある")

# ---------------------------------------------------------------- A9
# 剛体の正四面体回転子（群 T）で完全対称な基底から許される J
clsT = [(0, 1), (2 * math.pi / 3, 8), (math.pi, 3)]
multT = {J: round(sum(c * chiL(J, t) for t, c in clsT) / 12) for J in range(11)}
assert [J for J, m in multT.items() if m] [:6] == [0, 3, 4, 6, 7, 8] and multT[6] == 2
assert multT[1] == multT[2] == multT[5] == 0
ok("A9", "正四面体回転子の許容 J = 0,3,4,6(×2),7,8,… ／ 1,2,5 は禁止")

# ---------------------------------------------------------------- A10
# 正二十面体の上下五角形のねじれ π/5、帯（D5d）は軸方向の磁気モーメントを禁止
phi = (1 + 5 ** .5) / 2
Vx = []
for a, b in itertools.product([1, -1], repeat=2):
    Vx += [(0, a, b * phi), (a, b * phi, 0), (b * phi, 0, a)]
Vx = np.array(Vx, float); ax = Vx[0] / np.linalg.norm(Vx[0]); hgt = Vx @ ax
up = Vx[(hgt > 0) & ~np.isclose(hgt, hgt.max())]; dn = Vx[(hgt < 0) & ~np.isclose(hgt, hgt.min())]
e1 = np.cross(ax, [1, 0, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(ax, e1)
az = lambda P: [math.degrees(math.atan2(p @ e2, p @ e1)) % 360 for p in P]
twist = min((d - u) % 72 for u in az(up) for d in az(dn))
assert abs(twist - 36) < 1e-9
ops = []
for tri in itertools.permutations(range(12), 3):
    try:
        M = np.linalg.solve(Vx[[0, 1, 2]], Vx[list(tri)]).T
    except np.linalg.LinAlgError:
        continue
    if not np.allclose(M @ M.T, np.eye(3), atol=1e-9):
        continue
    if all(np.isclose(np.linalg.norm((M @ Vx.T).T - v, axis=1), 0, atol=1e-9).any() for v in Vx) \
            and np.isclose(abs((M @ ax) @ ax), 1) and not any(np.allclose(M, O) for O in ops):
        ops.append(M)
flip = [O for O in ops if not np.allclose(np.linalg.det(O) * O @ ax, ax)]
assert len(ops) == 20 and len(flip) == 10
ok("A10", "上下五角形のねじれ = 36° = π/5 ／ 軸を保つ20操作のうち10が軸性ベクトルを反転 → 静止した帯は磁石になれない")

# ---------------------------------------------------------------- B-Q（既知の照合・数値の再現）
# 単一 j 殻の四重極モーメント：Q = Q_sp·(2j+1−2n)/(2j−1)，Q_sp = −(2j−1)/(2j+2)<r²>  (j によらず負)
def Qshell(A, Nosc, j, n, e):
    b2 = 41.47 / (41 * A ** (-1 / 3)); r2 = (Nosc + 1.5) * b2
    return -(2 * j - 1) / (2 * j + 2) * r2 * (2 * j + 1 - 2 * n) / (2 * j - 1) * e * 10   # mb
data = [("7Li", 7, 1, 1.5, 1, 1.5, -40.0), ("17O", 17, 2, 2.5, 1, 0.5, -25.6),
        ("37Cl", 37, 2, 1.5, 1, 1.5, -64.2), ("67Zn", 67, 3, 2.5, 5, 0.5, 150.0),
        ("97Mo", 97, 4, 2.5, 5, 0.5, 255.0), ("137Ba", 137, 4, 1.5, 3, 0.5, 236.0)]
rows = []
for name, A, No, j, n, e, meas in data:
    q = Qshell(A, No, j, n, e)
    assert (q < 0) == (meas < 0), name
    rows.append(f"{name}:{q:+.0f}/{meas:+.0f}")
assert Qshell(97, 4, 2.5, 1, 1) < 0 and Qshell(97, 4, 1.5, 1, 1) < 0     # 単一粒子は j=l±1/2 どちらでも負
ok("B-Q", "符号 6/6 一致（計算/実測 mb）: " + ", ".join(rows))

# 単位の確認：1 mb = 0.1 fm²、β2 は資料値の約 1/10
b2 = lambda Qmb, Z, A: abs(Qmb * 0.1) / (3 / math.sqrt(5 * math.pi) * Z * (1.2 * A ** (1 / 3)) ** 2)
assert b2(64.2, 17, 37) < 0.04 and b2(150, 30, 67) < 0.04
ok("B-U", f"β2(Q_spec): 37Cl={b2(64.2,17,37):.3f}, 67Zn={b2(150,30,67):.3f}（0.33/0.29 は単位の誤り）")

print(f"\nALL PASS: {len(PASS)} blocks -> {', '.join(PASS)}")
