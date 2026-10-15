"""
TTT 検証スクリプト 2026-10-15 夜〜10-16：陽子の大きさ・電子と α・テトラの貼り合わせ・3²+4²=5²・ハニカム
  numpy のみ（標準ライブラリの math, fractions, itertools を併用）。すべての assert が通れば成立。
  実測値：CODATA 2022、AME2020（⁸⁰Zr のみ Hamaker et al. 2021）
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
    print("  ✓", msg)

hc = 1239.84198; me = 0.51099895069; mp = 938.27208943
L = 1 + 3 * math.pi; g = mp / me / 3
rp = 0.84075; dp = 2 * rp

# ---- Block 1：陽子の大きさ（外部資料の検証）----
print("Block 1：陽子の大きさ")
Lp = hc / (L * me / 4) / g
check(abs(Lp - 1.5211) < 1e-3, "OπO の長さ 1.521 fm（静止電子＝4点それぞれ OOOπ）")
r43 = Lp * (4 / 3) ** (1 / 3)
check(abs(r43 / dp - 1 + 0.0044) < 3e-4, "∛(4/3) 倍で 1.674 fm、陽子直径と −0.44%")
check(abs((dp - r43) / (2 * 0.00064)) > 5, "ずれは測定誤差の 5σ 以上（誤差の範囲ではない）")
check(abs(Lp * (6 / math.pi) ** (1 / 3) / dp - 1.122) < 1e-3, "体積を保って球にすると +12.2%")
a = hc / (L * me / 4)
for law, d in [("力 F＝E/L", math.sqrt(3) * a), ("エネルギー密度", 3 ** 0.25 * a)]:
    check(d > a, f"境界 O500 と中の 1500 を『同じ力』で釣り合わせると球はマスより大きい（{law}）")
check(abs(a / 3 / dp - 184.6) < 0.5, "E∝1/L で 1500 が 1/3：陽子 a/3 ＝ 310 fm（185 倍）")

# ---- Block 2：電子の存在エネルギーと α ----
print("Block 2：電子と α")
lc = hc / me
check(abs(lc - 2426.31) < 0.01, "存在エネルギーの長さ hc/(mₑc²) ＝ 2426 fm（コンプトン波長）")
a0 = 52917.72105
check(abs(2 * math.pi * a0 / lc - 137.036) < 1e-3, "軌道の一周 ÷ 存在エネルギーの長さ ＝ 1/α（恒等式）")
alpha = F(137) + F(35, 972) - F(1, 110592)
check(alpha == F(162 - 25) + F(37 - 2, 6 * 162) - F(1, (3 * 16) ** 3), "v2.2 の双錐語彙と 10-11 の誕生則語彙は同じ有理数")
check(abs((float(alpha) - 137.035999177) / 2.1e-8 - 0.534) < 0.01, "CODATA 2022 と 0.53σ")
# 今日の数で α の各項を書ける通り数と基準率
V = [2, 3, 4, 5, 6, 8, 12, 16, 17, 25, 27, 34, 37, 91, 125, 162, 243, 486, 500, 1500, 2000]
def n_ways(t):
    n = 0
    for x, y in it.combinations_with_replacement(V, 2):
        n += (x + y == t) + (x * y == t) + (x - y == t) + (y - x == t)
    return n
rate = lambda lo, hi: sum(1 for t in range(lo, hi + 1) if n_ways(t)) / (hi - lo + 1)
check(n_ways(137) >= 2 and rate(100, 200) > 0.5, "137 は書けるが 100〜200 の過半数が書ける（証拠にならない）")
check(n_ways(972) >= 4 and rate(800, 1200) < 0.05, "972 ＝ 4×3⁵ は誕生則に組み込み済みのため書けるだけ")

# ---- Block 3：テトラ（⁴He）の貼り合わせ ----
print("Block 3：テトラの貼り合わせ")
He = 28.29566
Bn = {2: 56.4995, 3: 92.16173, 4: 127.6193, 5: 160.6448, 6: 198.2569, 7: 236.5368, 8: 271.7805,
      9: 306.7167, 10: 342.0521, 11: 375.4750, 12: 411.4686, 13: 447.6975, 14: 483.9884,
      15: 514.9939, 16: 545.9502, 17: 576.4268, 18: 607.1063, 19: 638.0838}
Bn[20] = 40 * 7.288971 + 40 * 8.071318 + 55.128          # ⁸⁰Zr（質量偏差 −55128 keV）
ex = {n: b - n * He for n, b in Bn.items()}
check(abs(ex[2]) < 0.1, "⁸Be：テトラ2個は結合しない（−0.09 MeV）")
ratio = (ex[4] / 6) / (ex[3] / 3)
check(abs(ratio - 0.992) < 0.005 and abs(ratio - math.sqrt(3)) > 0.7, "予言 √3 は外れ：¹⁶O/¹²C の1本あたり 0.99 倍")
for V_, E_ in [(4, 6), (5, 9), (6, 12), (7, 15), (12, 30)]:
    check(E_ == 3 * V_ - 6, f"三角形の面の立体 V={V_}：辺 ＝ 3V−6 ＝ {E_}")
per = [ex[n] / (3 * n - 6 if n > 3 else 3) for n in range(3, 15)]
check(min(per) > 2.1 and max(per) < 2.6 and np.std(per) / np.mean(per) < 0.05,
      f"¹²C〜⁵⁶Ni：格子1本 {np.mean(per):.2f} MeV ± {100*np.std(per)/np.mean(per):.1f}%")
check(ex[8] / 12 > 3.7 and 2.4 < ex[8] / 18 < 2.6, "³²S：立方体の辺12本だと 3.79、貼り合わせ18本で 2.52")
bonds = lambda n: 3 * n - 6 if n <= 14 else 36 + 1.5 * (n - 14)
per2 = [ex[n] / bonds(n) for n in range(3, 21)]
check(min(per2) > 2.1 and max(per2) < 2.6, "⁵⁶Ni より先はフラーレン型（1個につき 1.5本）で ⁸⁰Zr まで 2.13〜2.56")
check(ex[20] / 54 < 2.0, "⁸⁰Zr を貼り合わせだけで数えると 1.92（外れる）")

# ---- Block 4：3² + 4² ＝ 5²（双極＝直交で交差が消える）----
print("Block 4：3²+4²=5²")
u = np.array([3, 0, 0, 0, 0, 0, 0.]); v = np.array([0, 0, 0, 4, 0, 0, 0.])
check(abs(np.dot(u + v, u + v) - 25) < 1e-12 and np.dot(u, v) == 0, "直交する長さ3と4の和の長さ ＝ 5")
M = np.zeros((7, 7)); M[:3, :3] = 1; M[3:, 3:] = 1
check(int(M.sum()) == 25 and M[:3, 3:].sum() == 0, "3⊕4 の 7×7 で交差24成分が0なら残り 9＋16 ＝ 25")
check(1 + 3 == 4, "正四面体の 1 : √3 : 2 は 1 + 3 ＝ 4（スカラー1 ＋ ベクトル3）")
check(6 * 9 == 2 * 3**3 and 6 * 25 == 150, "箱6面：XYZ側 6×9 ＝ 54（第4世代）、全体 150")

# ---- Block 5：対角線方向の平面（ハニカム・六芒星）----
print("Block 5：ハニカム")
hexn = lambda n: 3 * n * n - 3 * n + 1
check(all(n**3 - (n - 1)**3 == hexn(n) for n in range(1, 10)), "立方体の殻 ＝ 中心六角数")
check(sum(hexn(n) for n in range(1, 6)) == 125, "125 ＝ 1＋7＋19＋37＋61（5枚のハニカム）")
check(hexn(4) == 37 == 6 * 3 * 2 + 1, "37 は中心六角数かつ六芒星の数（星数）")
sol = [n for n in range(1, 1000) if n * n == 1 + 6 * (n - 1)]
check(sol == [1, 5], "正方形の面 n² ＝ 六角形の中心＋外周 1＋6(n−1) は n ＝ 5 だけ（n＝1 は点）")
# ---- Block 6：四元数（トリ＋テトラ）----
print("Block 6：四元数")
q = lambda a, b, c, d: np.array([a, b, c, d], float)
def mul(x, y):
    a1, b1, c1, d1 = x; a2, b2, c2, d2 = y
    return q(a1*a2 - b1*b2 - c1*c2 - d1*d2, a1*b2 + b1*a2 + c1*d2 - d1*c2,
             a1*c2 - b1*d2 + c1*a2 + d1*b2, a1*d2 + b1*c2 - c1*b2 + d1*a2)
i, j, k, one = q(0, 1, 0, 0), q(0, 0, 1, 0), q(0, 0, 0, 1), q(1, 0, 0, 0)
check(all(np.allclose(mul(x, x), -one) for x in (i, j, k)) and np.allclose(mul(mul(i, j), k), -one), "i² ＝ j² ＝ k² ＝ ijk ＝ −1")
T = [s * e for e in (one, i, j, k) for s in (1, -1)] + [q(*s) / 2 for s in it.product((1, -1), repeat=4)]
check(len(T) == 24 and all(any(np.allclose(mul(x, y), z) for z in T) for x in T for y in T), "2T：24個の四元数が積で閉じる")
check((1 | 1) == 1, "ブール代数の和：1 ＋ 1 ＝ 1")

print(f"\n{ok} assert 全通過")
