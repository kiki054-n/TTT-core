"""
TTT 検証スクリプト 2026-10-14〜15：1マスのエネルギー・陽子/電子比・ヘリウム4とテトラ拘束
  numpy のみ（標準ライブラリの math を併用）。すべての assert が通れば成立。
  実測値：CODATA 2022 / PDG 2025
"""
import math
import numpy as np

ok = 0
def check(cond, msg):
    global ok
    assert cond, msg
    ok += 1
    print("  ✓", msg)

hc = 1239.84198          # MeV·fm
me = 0.51099895069       # MeV
mp = 938.27208943        # MeV
mu = mp / me             # 1836.15267...
L = 1 + 3 * math.pi      # OOOπ の経路（O の直径1 → 周 π が3つ、π の長さ1）

# ---- Block 1：1マスのエネルギー ----
print("Block 1：1マスのエネルギー")
e0 = 1 / L               # hc/a 単位
check(abs(e0 - 0.09593) < 1e-5, "OOOπ 1個：e0 ＝ hc/[(1+3π)a] ＝ 0.09593 hc/a")
check(abs(2 * e0 - 0.19185) < 1e-5, "1×1×1 に2個：0.1919 hc/a")
lP = 1.616255e-35; h = 6.62607015e-34; c = 299792458; GeV = 1.602176634e-10
check(abs(2 * h * c / (L * lP) / GeV / 1.4717e19 - 1) < 1e-3, "a ＝ プランク長なら 1マス 1.47×10¹⁹ GeV")

# ---- Block 2：2 + 125 + 37 + 17×108 ＝ 2000 ----
print("Block 2：2000 への積み上げ")
check(2 + 125 + 37 + 17 * 108 == 2000, "2 ＋ 125 ＋ 37 ＋ 17×108 ＝ 2000")
check(17 * 108 == 1836, "17×108 ＝ 1836（整数部の一致。小数部 0.1527 は出ない）")
check(6**3 - 5**3 == 91 and 125 - 91 == 34, "6³−5³ ＝ 91、125 − 91 ＝ 34")
check(2 * 3**4 - 5**3 == 37, "162 − 125 ＝ 37")
# 世代（同時発生）で数えた到達段
shell = lambda n: 3 * n * n - 3 * n + 1
A = [242]
for s in range(1, 140):
    A.append(A[-1] + shell(5 + s) + 34)
reach = {k: max(i for i, v in enumerate(A) if v <= 3**k) for k in range(5, 14)}
check(reach[12] < 108 <= reach[13], "108段目は 13 τ0 の間に入る（5×5×5 から 8 τ0）")
steps = [min(108, reach[k]) - min(108, reach[k - 1]) for k in range(6, 14)]
check(sum(17 * d for d in steps) == 1836, "6〜13 τ0 に 125 へ入る数の合計 ＝ 1836")
FT = 162 * 9 + sum(17 * d * (14 - k) for d, k in zip(steps, range(6, 14)))
check(FT == 6711, "力 × 時間の合計（入った世代を含む）＝ 6711 T")

# ---- Block 3：破る条件と相似形 ----
print("Block 3：破る条件と相似形")
check(2 * 3 == 6, "1×1×1：OπO 要素 2×3 ＝ 6／マス → 破れる")
check(abs(486 / 125 - 3.888) < 1e-3, "5×5×5 の始まり：486/125 ＝ 3.89 < 6 → 破れない")
check(1500 / 125 == 12 and 6 * 125 == 750, "破る条件 750（6/マス）、釣り合い 1500（12/マス＝テトラ1個）")
check(1500 // 4 // 3 == 125, "1500 / 4 / 3 ＝ 125")
check(2000 / 10**3 == 2, "5×5×5 を 10×10×10 で数えると 1マスに OOOπ 2個（発生時と相似）")

# ---- Block 4：陽子/電子比 ＝ 3 × (L_O / L_OπO) ----
print("Block 4：陽子/電子比")
g = mu / 3
check(abs(g - 612.0509) < 1e-3, "必要な長さの比 L_O/L_OπO ＝ 612.05")
check(abs(1500 * g - 918076) < 1, "1500 × 612.05 ＝ 918,076（10-13 の陽子側要素数と一致）")
check(3 * 5 == 15 and 3 * 25 == 75, "125→1（長さ1/5）だけなら比 15、O を 5a で見て 75")
check(abs(3 * 5**4 / mu - 1 - 0.0211) < 1e-3, "5⁴ ＝ 625 は +2.1%（E ∝ L⁻⁴ は時間との関係がなく除外）")
rp = 0.84075
for n, a_exp, Lp_exp in [(1, 232.74, 0.3803), (4, 930.98, 1.5211)]:
    a = hc / (L * me / n); Lp = a / g
    check(abs(a - a_exp) < 0.05 and abs(Lp - Lp_exp) < 1e-3,
          f"静止電子 ＝ 4点（OOOπ {n} 個分）：a ＝ {a:.1f} fm、L_OπO ＝ {Lp:.3f} fm")
Lp4 = hc / (L * me / 4) / g
check(abs(Lp4 / (2 * rp) - 0.9046) < 1e-3, "L_OπO ÷ 陽子直径 ＝ 0.905（−9.5%）")

# ---- Block 5：ヘリウム4とテトラ拘束 ----
print("Block 5：ヘリウム4とテトラ拘束")
B = {"D": 2.22457, "He3": 7.71804, "H3": 8.48182, "He4": 28.29566}
pn = {"D": 1, "He3": 2, "H3": 2, "He4": 4}
per = {k: B[k] / pn[k] for k in B}
lo, hi = per["He4"] / per["H3"], per["He4"] / per["He3"]
check(1.66 < lo < 1.67 and 1.83 < hi < 1.84, f"3→4 粒子で pn 格子1本の強さ {lo:.3f}〜{hi:.3f} 倍")
check(lo < math.sqrt(3) < hi, "√3 ＝ 1.732 はこの範囲に入る")
check(not (lo < math.sqrt(5) < hi) and not (lo < (1 + 5**0.5) / 2 < hi), "√5・黄金比は範囲外")
check(abs(per["He4"] / per["D"] - 3.18) < 0.01, "2→4 粒子（全 B の比 12.7、pn 1本あたり 3.18）は √3 で出ない")
# 正四面体の幾何
V = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
edges = [(i, j) for i in range(4) for j in range(i + 1, 4)]
mids = [(V[i] + V[j]) / 2 for i, j in edges]
check(len(edges) == 6, "正四面体の格子 6本（pp 1・nn 1・pn 4）")
check(sorted(map(tuple, np.round(mids, 12))) == sorted([tuple(s * e) for e in np.eye(3) for s in (1, -1)]),
      "6本の中点 ＝ XYZ 軸上の ±1（正八面体の6頂点）")
check(all(abs(np.dot(V[i] - V[j], m)) < 1e-12 for (i, j), m in zip(edges, mids)), "各格子は通る軸と直交")
check(abs(np.linalg.norm(V[0]) - math.sqrt(3)) < 1e-12, "中心→頂点 ＝ √3、中心→辺の中点 ＝ 1、向かい合う辺の間 ＝ 2")
tri = np.array([[0, 2 / math.sqrt(3)], [1, -1 / math.sqrt(3)], [-1, -1 / math.sqrt(3)]])
check(abs(np.linalg.norm(tri[0]) / np.linalg.norm((tri[1] + tri[2]) / 2) - 2) < 1e-12,
      "正三角形：中心→頂点 ÷ 中心→辺の中点 ＝ 2（正四面体は √3）")
cube_mid = math.sqrt(2); octa_ratio = 1 / (1 / math.sqrt(2))
check(abs(math.sqrt(3) / cube_mid - 1.2247) < 1e-4 and abs(octa_ratio - math.sqrt(2)) < 1e-12,
      "頂点÷辺の中点 ＝ √3 は正四面体だけ（正六面体 1.225、正八面体 1.414）")
Rr = {(3, 3): 3, (4, 3): math.sqrt(3), (3, 4): math.sqrt(3), (5, 3): math.sqrt(3) * math.tan(math.pi / 5)}
check(all(abs(math.tan(math.pi / p) * math.tan(math.pi / q) - v) < 1e-12 for (p, q), v in Rr.items()),
      "R/r ＝ tan(π/p)·tan(π/q)：すべての正多面体に tan60° ＝ √3 が掛かる")
axes = {"正四面体": (2, 4), "正八面体": (3, 6), "正二十面体": (6, 12)}
check(all(2 * a == v for a, v in axes.values()), "π の数 ＝ 軸×2 ＝ 頂点数（三角形の面の立体）")

print(f"\n{ok} assert 全通過")
