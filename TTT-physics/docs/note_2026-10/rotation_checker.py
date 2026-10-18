"""
TTT 検証スクリプト 2026-10-19 朝：回転の起源・2×2×2 型・銀河の回転・市松模様
  numpy のみ（標準ライブラリの math, fractions, itertools を併用）。すべての assert が通れば成立。
"""
import math
import itertools as it
import numpy as np
from fractions import Fraction as F

ok = 0
def check(cond, msg):
    global ok
    assert cond, msg
    ok += 1

signs = list(it.product((1, -1), repeat=3))

# ---- Block 1：125 に 2000 を押し込む力 ----
print("Block 1：押し込む力")
# F(N) = c·N/125、距離 1 マス → E = ∫ c N/125 dN
E_total = F(2000**2, 2 * 125)
check(E_total == 16000, "総和 2000²/250 ＝ 16000c")
check(F(1500**2, 250) == 9000, "1500 が先に入る場合 9000c")
check(F(3, 4) * E_total == 12000, "混ざって入る場合 12000c")
check(F(9000, 3) == 3000 and F(12000, 3) == 4000, "π で蓄える（÷3）：3000c / 4000c")

# ---- Block 2：Z が先に決まり、ずれた位置で X が分かれる ----
print("Block 2：ずれから回転")
x, z0, p = 0.7, 0.3, 1.0
L = np.cross([x, 0, z0], [p, 0, 0])
check(np.allclose(L, [0, z0 * p, 0]), "L ＝ (0, z0·p, 0)：Y 軸まわり")
L0 = np.cross([x, 0, 0], [p, 0, 0])
check(np.allclose(L0, 0), "ずれがなければ L ＝ 0")
check(np.allclose(np.cross([x, 0, z0], [p, 0, 0]) + np.cross([x, 0, -z0], [p, 0, 0]), 0), "±z0 の対で合計 0")

# ---- Block 3：2×2×2 型 ----
print("Block 3：2×2×2 型")
Ls = {}
for s in signs:
    r = 0.5 * np.array(s, float)
    pv = np.array([s[0], s[1], 0], float)
    Ls[s] = np.cross(r, pv)
check(all(abs(v[2]) < 1e-12 for v in Ls.values()), "Z まわりの回転は厳密に 0")
check(all(np.allclose(np.abs(v[:2]), 0.5) for v in Ls.values()), "成分はすべて ±1/2 p")
check(np.allclose(sum(Ls.values()), 0), "8 つの合計 0")
check(all(abs(np.dot(Ls[s], 0.5 * np.array(s[:2] + (0,)))) < 1e-12 for s in signs), "回転軸は XY 位置と直交（Z を巡る渦）")
check(abs(np.dot(Ls[(1, 1, 1)], Ls[(1, -1, 1)])) < 1e-12 and abs(np.dot(Ls[(1, 1, 1)], Ls[(-1, 1, 1)])) < 1e-12, "辺を共有する隣：直交")
check(abs(np.dot(Ls[(1, 1, 1)], Ls[(-1, -1, 1)]) + 0.5) < 1e-12, "同じ層の対角：逆向き")
check(abs(np.dot(Ls[(1, 1, 1)], Ls[(1, 1, -1)]) + 0.5) < 1e-12, "上下の層：逆向き")
check(all(np.allclose(Ls[s], -Ls[(s[0], s[1], -s[2])]) for s in signs), "上下の層で逆向きの渦")

# ---- Block 4：正八面体 → 正六面体の隙間と 3 点の回転 ----
print("Block 4：隙間と 3 点")
V_oct, V_cube = F(4, 3), F(8)
check(V_cube - V_oct == F(20, 3) and (V_cube - V_oct) / 8 == F(5, 6), "隙間 20/3、角ごとに 5/6")
check(V_cube / V_oct == 6, "体積比 6（マスを破る条件 6 と同じ）")
for s in signs:
    A = np.array([0, 0, s[2]], float); B = np.array([s[0], 0, 0], float); C = np.array([0, s[1], 0], float)
    corner = np.array(s, float)
    cen = (A + B + C + corner) / 4
    check(np.allclose(cen, 0.5 * corner), f"隙間 {s} の重心 ＝ 2×2×2 の中心")
    orient = np.dot(np.cross(B - A, C - A), corner)
    check(abs(orient - 3 * s[0] * s[1] * s[2]) < 1e-12, f"Z→X→Y の向き ＝ 3·sx·sy·sz {s}")
check(sum(s[0] * s[1] * s[2] for s in signs) == 0, "右回り 4・左回り 4、合計 0")

# ---- Block 5：XYZπ=1 ----
print("Block 5：XYZπ=1")
check(F(1, 1 * 1 * 1) == 1, "±1 の正八面体で π ＝ 1")
check(F(1, 2 * 2 * 2) == F(1, 8), "±2 で π ＝ 1/8（8 つの中心に分かれる）")

# ---- Block 6：衝突で止まっても回転は残る ----
print("Block 6：衝突")
m, v, b, k = 1.0, 1.0, 0.8, 0.4
Lc, K = m * v * b, m * v**2
Rmin = b / (2 * math.sqrt(k))
I = k * 2 * m * Rmin**2
check(abs(Lc**2 / (2 * I) - K) < 1e-12, "R_min ＝ b/(2√k) で回転エネルギー ＝ K")
check(Lc**2 / (2 * k * 2 * m * (2 * Rmin) ** 2) < K, "R_min より大きければ蓄えに回る分が残る")

# ---- 市松模様の数え方（細分割）----
def board(n, dim, shape, sub):
    R = n / 2
    xs = (np.arange(sub) + 0.5) / sub
    w = [0.0, 0.0]; full = cut = 0
    for idx in it.product(range(n), repeat=dim):
        g = np.meshgrid(*[i + xs - R for i in idx], indexing="ij")
        if shape == "cube":
            f = 1.0
        elif shape == "ball":
            f = (sum(c * c for c in g) <= R * R + 1e-9).mean()
        else:
            f = (sum(np.abs(c) for c in g) <= R + 1e-9).mean()
        if f > 0.99999: full += 1
        elif f > 0: cut += 1
        w[sum(idx) % 2] += f
    c0 = (n // 2) * dim % 2 if n % 2 else 0  # 中心のマスの色
    return full, cut, w[c0] - w[1 - c0]

# ---- Block 7：平面（四角・円・菱形）----
print("Block 7：平面")
check(abs(F(2) / 4 - 0.5) < 1e-12 and abs(math.pi / 4 - 0.785398) < 1e-6, "菱形：円：四角 ＝ 2 : π : 4")
f, c, d = board(5, 2, "ball", 200)
check((f, c) == (9, 16) and abs(abs(d) - 0.674) < 0.01, "5×5 の円：完全 9・切れ 16、白黒の差 0.67")
f, c, d = board(5, 2, "octa", 200)
check((f, c) == (5, 16) and abs(abs(d) - 2.5) < 0.01, "5×5 の菱形：差 2.5")
for sh in ("ball", "octa"):
    check(abs(board(6, 2, sh, 200)[2]) < 1e-9, f"6×6 の {sh}：差 0")

# ---- Block 8：立体（正六面体・球・正八面体）----
print("Block 8：立体")
expect5 = {"cube": (125, 0, 1.0), "ball": (19, 98, -0.32), "octa": (7, 50, 25 / 6)}
for sh, (ef, ec, ed) in expect5.items():
    f, c, d = board(5, 3, sh, 40)
    check((f, c) == (ef, ec) and abs(d - ed) < 0.02, f"5×5×5 の {sh}：{ef}・{ec}・差 {ed:.2f}")
expect6 = {"cube": (216, 0), "ball": (56, 128), "octa": (8, 72)}
for sh, (ef, ec) in expect6.items():
    f, c, d = board(6, 3, sh, 40)
    check((f, c) == (ef, ec) and abs(d) < 1e-9, f"6×6×6 の {sh}：{ef}・{ec}・差 0")
check(F(25, 2) + F(25, 3) == F(4, 3) * F(5, 2) ** 3, "5×5×5 の正八面体：12.5 ＋ 25/3 ＝ 体積 125/6")
check(F(25, 2) / F(25, 3) == F(3, 2) and F(25, 2) - F(25, 3) == F(25, 6), "中心の色：反対の色 ＝ 3 : 2、差 25/6")

# ---- Block 9：偶数なら鏡映で白黒が入れ替わる ----
print("Block 9：偶奇")
for n in range(2, 9):
    swaps = all((n - 1 - i + j + k) % 2 != (i + j + k) % 2 for i, j, k in it.product(range(n), repeat=3))
    check(swaps == (n % 2 == 0), f"n＝{n}：X の鏡映で色が{'入れ替わる' if n % 2 == 0 else '変わらない'}")

# ---- Block 10：回転軸に垂直な切り口 ----
print("Block 10：ハニカム")
cube_hex = [np.array(q, float) for q in set(it.permutations((1, -1, 0)))]
oct_hex = [0.5 * h for h in cube_hex]
check(len(cube_hex) == 6 and all(abs(h.sum()) < 1e-12 for h in cube_hex), "正六面体の切り口：6 頂点、x＋y＋z＝0")
check(all(abs(np.abs(h).max() - 1) < 1e-12 for h in cube_hex), "頂点は立方体の辺の上")
check(all(abs(np.abs(h).sum() - 1) < 1e-12 for h in oct_hex), "正八面体の切り口も同じ向きの正六角形")
check(len({round(np.linalg.norm(h), 12) for h in cube_hex}) == 1, "正六角形（中心から等距離）")
check(abs(np.linalg.norm(cube_hex[0]) / np.linalg.norm(oct_hex[0]) - 2) < 1e-12, "大きさ 2 : 1")

print(f"\n{ok} assert 全通過")
