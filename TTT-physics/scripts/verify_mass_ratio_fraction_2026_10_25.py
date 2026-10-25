"""
2026-10-24〜25 の議論の機械検証
  - 電子 125 の構成（1 + 4×31、π 120 + O 5）
  - 正二十面体（双極 2 + 五角反柱 10）の頂点・辺の分け方
  - 陽子／電子質量比の小数部の式と帰無対照

実行: python TTT-physics/scripts/verify_mass_ratio_fraction_2026_10_25.py
"""
import itertools
import math
import random
from fractions import Fraction

n_assert = 0


def check(cond, msg):
    global n_assert
    assert cond, msg
    n_assert += 1


# ---------------------------------------------------------------
# 1. 電子 125 の構成
# ---------------------------------------------------------------
check(1 + 4 * 31 == 125, "125 = 1 + 4x31")
check(31 == 1 + 2 * 3 * 5, "31 = 1 + 2x3x5")
check(1 + 4 == 5 and 4 * 30 == 120 and 5 + 120 == 125, "芯 5 + 殻 120")
check(30 * 4 + 5 == 125, "π 30x4 + O 5 = 125")
check(480 + 20 == 500 and 4 * 120 == 480 and 4 * 5 == 20, "テトラで π480 + O20 = 500")
# 原子全体（電子 π480・O20、陽子を数の鏡像 O1480・π20 とした場合）
check(480 + 20 == 500 and 1480 + 20 == 1500, "π 500 / O 1500")
# OπO は 3 要素 → 1500 要素は OπO 500 個 → π 500
check(1500 // 3 == 500, "1500 要素中の π = 500")

# ---------------------------------------------------------------
# 2. 正二十面体 = 双極 2 + 五角反柱 10
# ---------------------------------------------------------------
s5 = math.sqrt(5)
verts = [(0.0, 0.0, 1.0), (0.0, 0.0, -1.0)]
r = 2 / s5
for k in range(5):
    a = 2 * math.pi * k / 5
    verts.append((r * math.cos(a), r * math.sin(a), 1 / s5))      # 上の環
for k in range(5):
    a = 2 * math.pi * k / 5 + math.pi / 5                           # 36° ねじれ
    verts.append((r * math.cos(a), r * math.sin(a), -1 / s5))     # 下の環

def dist(p, q):
    return math.dist(p, q)

d = [dist(p, q) for p, q in itertools.combinations(verts, 2)]
dmin = min(d)
edges = [(i, j) for i, j in itertools.combinations(range(12), 2)
         if abs(dist(verts[i], verts[j]) - dmin) < 1e-9]
check(len(verts) == 12 and len(edges) == 30, "正二十面体 V12 E30")

POLE = {0, 1}
UP = set(range(2, 7))
LO = set(range(7, 12))
cap = [e for e in edges if POLE & set(e)]
ring = [e for e in edges if set(e) <= UP or set(e) <= LO]
zig = [e for e in edges if (e[0] in UP and e[1] in LO) or (e[0] in LO and e[1] in UP)]
check(len(cap) == 10 and len(ring) == 10 and len(zig) == 10, "辺 30 = 10 + 10 + 10")
check(sum(1 for e in cap if 0 in e) == 5 and sum(1 for e in cap if 1 in e) == 5, "キャップ 5+5")
check(sum(1 for e in ring if set(e) <= UP) == 5, "環 5+5")
# 五角反柱だけの辺は 20（環 10 + ジグザグ 10）
check(len(ring) + len(zig) == 20, "五角反柱の辺 20")
# 頂点 12 = 中（反柱）10 + 外（双極）2
check(len(UP | LO) == 10 and len(POLE) == 2, "頂点 12 = 中 10 + 外 2")
# 五角双錐 = 双極 2 + 五角形 5 = 7
check(2 + 5 == 7, "五角双錐 V7")

# ---------------------------------------------------------------
# 3. 中心あり／なし の 4 要素（工 と T・⊥）
# ---------------------------------------------------------------
h = 1.0
L = math.sqrt(2) * h
tet = [(L, 0, h), (-L, 0, h), (0, L, -h), (0, -L, -h)]
dd = [dist(p, q) for p, q in itertools.combinations(tet, 2)]
check(max(dd) - min(dd) < 1e-12, "直交する 2 本の線（半長 L = √2 h）の端点は正四面体")

# ---------------------------------------------------------------
# 4. 標準理論の照合値
# ---------------------------------------------------------------
alpha = 1 / 137.035999177
check(abs((1 / math.sqrt(1 - alpha**2) - 1) / (alpha**2 / 2) - 1) < 1e-4, "基底状態の γ-1 ≈ α²/2")
Ry = 13.605693
check(abs(Ry * (1 - 1 / 4) - 10.204) < 1e-2, "n=1→2 は 10.2 eV")
check(abs(Ry * (1 / 4 - 1 / 9) - 1.890) < 1e-2, "n=2→3 は 1.89 eV")
check(abs(Ry * (1 / 9 - 1 / 16) - 0.661) < 1e-2, "n=3→4 は 0.66 eV")
kB = 8.617333262e-5
check(110000 < 10.204 / kB < 125000, "kT = 10.2 eV は約 12 万 K")

# ---------------------------------------------------------------
# 5. 陽子／電子質量比の小数部
# ---------------------------------------------------------------
R = 1836.152673426            # CODATA 2022
SIG = 0.000000032

D_need = 1836 / (R - 1836)
check(abs(D_need - 12025.6684) < 1e-3, "必要な分母 12025.668")

six_base = 3 * 2              # 3 要素が 2 つ
six_share = Fraction(12, 2)   # 共有する接続 12 を 2 粒子で分ける
check(six_base == six_share == 6, "二つの 6 は同じ値")

D = Fraction(six_base * 2000) + 2 * 12 + Fraction(10) / six_share
check(D == Fraction(36077, 3), "D = 6x2000 + 2x12 + 10/(12/2) = 12025 2/3")
pred = 1836 * (1 + 1 / float(D))
z = (pred - R) / SIG
check(abs(z) < 1.0, f"小数部の式は 1σ 以内（{z:.2f}σ）")
check(abs(pred - 1836.15267345) < 1e-8, "予測値 1836.15267345")
check(Fraction(10) / six_share == Fraction(2 * 10, 12), "10/(12/2) = (2x10)/12")

# 合わない数え方
def zz(den):
    return (1836 * (1 + 1 / den) - R) / SIG

check(abs(zz(12000)) > 1e4, "1/2000÷6 のみ（12000）は約 1 万σ")
check(abs(zz(12000 + 12 + 10 / 6)) > 4000, "共有 12 を 1 回だけ数えると約 4800σ")
check(abs(zz(12000 + 24 + 20 / 24)) > 300, "中 20 を 24 で割ると約 330σ")
check(abs(zz(12025.6)) > 20, "逆算値 25.6 は 27σ")
check(abs(zz(12000 * 2001 / 2000 / 1)) > 1e3, "2001/2000 をそのまま使うと合わない")

# 陽子の大きさ（電子を 1）
size = float(D) / (float(D) + 1)
check(0.99991 < size < 0.99992, "陽子の大きさ 0.999917（1 より小さい）")

# 整数部の分解
check(17 * 108 == 1836 and 12 * 153 == 1836 and 153 == 9 * 17 and 1500 // 125 == 12,
      "1836 = 17x108 = 12x153、12 = 1500/125")

# ---------------------------------------------------------------
# 6. 帰無対照：小さな数で作る a ± b/c の形が偶然に精度内に入る確率
# ---------------------------------------------------------------
vals = [2, 4, 6, 8, 10, 12, 24]
forms = set()
for a in vals:
    for b in vals:
        for c in vals:
            forms.add(a + b / c)
            forms.add(a - b / c)
forms = [f for f in forms if 0 < f < 60]
tol = SIG / (1836 / D_need**2)          # 1σ に相当する分母の幅
hits_target = [f for f in forms if abs((D_need - 12000) - f) < tol]
check(len(hits_target) == 1 and abs(hits_target[0] - (24 + 5 / 3)) < 1e-9, "目標に当たるのは 24 + 10/6 のみ")
random.seed(20261025)
N = 20000
rate = sum(any(abs(x - f) < tol for f in forms)
           for x in (random.uniform(0, 60) for _ in range(N))) / N
check(0.01 < rate < 0.03, f"偶然に当たる確率 約 {rate:.1%}")

print(f"all {n_assert} asserts passed")
print(f"needed D = {D_need:.6f}, D = {float(D):.6f}")
print(f"prediction = {pred:.10f}, CODATA 2022 = {R}, z = {z:.2f} sigma")
print(f"null-control hit rate = {rate:.3%} ({len(forms)} forms)")
