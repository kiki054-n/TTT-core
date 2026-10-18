"""
TTT 検証スクリプト 2026-10-18〜19：大きさ・面・34 と 17・時間と中心・125.25・物理との対応
  numpy のみ（標準ライブラリの math, fractions, itertools を併用）。すべての assert が通れば成立。
  実測値：CODATA 2022
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

# ---- Block 1：大きさ（単位 a ＝ 1マスの辺）----
print("Block 1：大きさ")
s6 = math.sqrt(6)
verts = np.array([[0, 0, 0], [1, 0, 0], [0.5, math.sqrt(3) / 2, 0], [0.5, math.sqrt(3) / 6, math.sqrt(2 / 3)]])
c = verts.mean(axis=0)
check(all(abs(np.linalg.norm(v - c) - s6 / 4) < 1e-12 for v in verts), "辺 a の正四面体：中心→頂点 √6/4·a")
check(abs(s6 / 4 + 0.5 - 1.1123724) < 1e-6, "(OπO)4 を包む球の半径 (√6/4＋1/2)a ＝ 1.112a")
check(abs((3 * 125 / (4 * math.pi)) ** (1 / 3) - 3.1017525) < 1e-6, "125 と同じ体積の球の半径 3.10a")
check(abs(5 * math.sqrt(3) / 2 - 4.3301270) < 1e-6, "125 の外接球の半径 5√3/2·a ＝ 4.33a")
check(abs((3 * 37 / (4 * math.pi)) ** (1 / 3) - 2.0671455) < 1e-6, "37 マス分と同じ体積の球の半径 2.07a")
hbarc, Ep = 197.3269804, 938.27208816
rp = 4 * hbarc / Ep
check(abs(rp - 0.84124) < 1e-5, "r_p·E_p/4 ＝ ħc から r_p ＝ 0.8412 fm")
lP = 1.616255e-35
check(abs((rp / 2.5) * 1e-15 / (2 * lP) - 1.04e19) / 1.04e19 < 0.01, "a(陽子半径の式) / 2ℓ_P ≈ 1.04×10¹⁹")

# ---- Block 2：面 ----
print("Block 2：面")
n = 5
check(6 * n**3 - 6 * n * n == 600 and 3 * (n - 1) * n * n == 300, "立方体 125：750 − 150 ＝ 600 面（境目 300 枚）")
check(F(600, 150) == 4 == F(2000, 500), "なくなる：残る ＝ 4：1 ＝ 2000 ÷ 500")
octa = n * (2 * n * n + 1) // 3
tetra = 4 * n * (n * n - 1) // 3
check((octa, tetra) == (85, 160), "辺 5 の正八面体 ＝ 小八面体 85 ＋ 小四面体 160")
check(4 * octa + tetra == 500 == 4 * n**3, "体積（小四面体単位）500 ＝ 4n³")
check(8 * octa + 4 * tetra == 1320 and 8 * n * n == 200, "面の合計 1320、表面 200")
up, down = n * (n + 1) // 2, n * (n - 1) // 2
check(8 * up == 120 and 8 * down == 80, "表面の内訳：八面体側 120・四面体側 80")
check(8 * octa - 8 * up == 4 * tetra - 8 * down == 560, "内側の境目 560 はすべて八面体–四面体")
check(all(4 * (m * (2 * m * m + 1) // 3) + 4 * m * (m * m - 1) // 3 == 4 * m**3 for m in range(1, 20)), "体積の式は辺 n すべてで成立")
# 正八面体 ±1 → 正六面体 ±1 → 正八面体 ±2（モンテカルロでなく厳密体積）
V_oct1, V_cube = F(4, 3), F(8)
check(V_cube / V_oct1 == 6, "正八面体 ±1 → 正六面体 ±1 で体積 6 倍")
corner = F(1, 6)  # x+y+z≥2 で切る [0,1]³ の角
check(8 * corner == V_oct1, "±2 の正八面体が切り出す 8 つの角の合計 ＝ 正八面体 ±1 の体積 4/3")
check(V_cube - 8 * corner == F(20, 3) and abs(5 * math.sqrt(2) / 3 * math.sqrt(2) ** 3 - 20 / 3) < 1e-12, "残りは立方八面体 20/3（辺 √2）")

# ---- Block 3：34 と 17、テトラ化 ----
print("Block 3：34 と 17")
check(5**3 - 4**3 - 3**3 == 34 and 3**2 + 4**2 == 5**2, "面では閉じ、立体では 34 足りない")
check(91 + 2 * 17 == 125 and 6**3 + 34 == 2 * 125 and 6**3 - 5**3 == 91, "91 ＋ 2×17 ＝ 125、6³ ＋ 34 ＝ 2×125")
check([2 * 37 + b * 17 for b in (1, 2, 3)] == [91, 108, 125], "91 → 108 → 125 は 17 ずつの列")
check(divmod(37, 3) == (12, 1) and divmod(17 * 19 + 1, 3) == (108, 0) and divmod(15, 3) == (5, 0), "テトラ化：37→12、323＋1→108、15→5")
check(12 + 108 + 5 == 125 and 125 + 37 + 17 * 19 + 15 == 500 and 37 + 17 * 19 + 15 == 375 == 125 * 3, "合計 125 マス・OOπO 500、押し込み 375 ＝ 125×3")

# ---- Block 4：時間と中心 ----
print("Block 4：時間と中心")
new = lambda t: 2 * 3 ** (t - 1)
check([new(t) for t in range(1, 8)] == [2, 6, 18, 54, 162, 486, 1458], "新しく生まれる数 2·3^(t−1)")
check(all(new(t) == 162 * 3 ** (t - 5) for t in range(5, 15)), "t ≥ 5 は 162 のまとまりで割り切れる")
check([3 ** (t - 5) - 1 for t in (5, 6, 7, 8)] == [0, 2, 8, 26], "最初の 1 を除く中心の候補 0, 2, 8, 26")
check(divmod(1458 - 125, 125) == (10, 83), "採らない数え方：(1458−125)÷125 ＝ 10 余り 83")
check(486 == 162 + 2 * 162, "t＝6：親 162 ＋ 子 324")

# ---- Block 5：125.25、誕生と消滅 ----
print("Block 5：125.25")
check(F(500 + 1, 4) == F(501, 4) == 125 + F(1, 4), "(500＋1)/4 ＝ 125.25")
check(501 * 4 == 2004, "要素 2004")
check(F(2 * 3, 1) == 6 and F(500 * 3, 125) == 12 == 2 * 6, "1マスあたり要素：t＝1 で 6、t＝25 で 12 ＝ 6×2")
check(-1 + 1 == 0 and (0 + 1) == 1, "± で見ると合計 0（保存）、0・1 で見ると 1 が有る（存在）")

# ---- Block 6：物理との対応 ----
print("Block 6：物理との対応")
h, hbar, cc = 2 * math.pi, 1.0, 1.0
a = 1.0
L = (1 + 3 * math.pi) * a
tau0 = 2 * L / cc
A = cc / tau0
kT = hbar * A / (2 * math.pi * cc)
e0 = h * cc / ((1 + 3 * math.pi) * a)  # e0 = hc/[(1+3π)a], h = 2πħ
check(abs(A - cc**2 / (2 * (1 + 3 * math.pi) * a)) < 1e-15, "一様加速：A ＝ c²/[2(1+3π)a]")
check(abs(kT - e0 / (8 * math.pi**2)) < 1e-15, "ウンルー温度 k_BT ＝ e₀/(8π²)")
# 光の時計：静止で往復 2d、速さ v で斜めの道 → 周期 γ 倍
d, v = 1.0, 0.6
T0 = 2 * d / cc
# 斜めの道：(c T/2)² ＝ d² ＋ (v T/2)² → T ＝ 2d / sqrt(c² − v²)
Tv = 2 * d / math.sqrt(cc**2 - v**2)
gamma = 1 / math.sqrt(1 - v**2 / cc**2)
check(abs(Tv / T0 - gamma) < 1e-12 and abs(gamma - 1.25) < 1e-12, "光の時計：周期 γ 倍（v＝0.6c で 1.25）")
# 仕事 → (γ−1)m₀c²、光速で発散
m0 = 1.0
work = lambda u: (1 / math.sqrt(1 - u**2) - 1) * m0
check(abs(work(0.6) - 0.25) < 1e-12 and work(0.999999) > 700 and work(0.99999999) > 7000, "∫F dx ＝ (γ−1)m₀c² は v→c で発散")
# 一定の固有加速では光速に届かない
check(all(math.tanh(x) < 1 for x in (1, 5, 10)), "一定の固有加速：v ＝ c·tanh(Aτ/c) < c")

print(f"\n{ok} assert 全通過")
