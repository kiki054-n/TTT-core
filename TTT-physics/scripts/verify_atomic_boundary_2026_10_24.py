"""原子の境界・核分裂と双極空間（2026-10-24）の数値検証。

対応ノート: TTT-physics/原子の境界・核分裂と双極空間の整理（2026-10-24）.md
依存: numpy のみ。全ブロックが assert を通れば最後に件数を表示する。
"""
import itertools
import math

import numpy as np

N = 0


def ok(cond, msg):
    global N
    assert cond, msg
    N += 1


hc = 1239.84198  # MeV·fm
hbarc = 197.326980  # MeV·fm
aS, aC, aV = 17.8, 0.711, 15.8  # MeV（液滴模型の代表値）

# --- Block 1: 液滴模型による U-236 → A=95 + A=141 ---
A, Z = 236, 92
A1, A2 = 95, 141
Z1, Z2 = Z * A1 / A, Z * A2 / A  # 電荷は質量数に比例して分配
ES0 = aS * A ** (2 / 3)
ES1 = aS * (A1 ** (2 / 3) + A2 ** (2 / 3))
EC0 = aC * Z ** 2 / A ** (1 / 3)
EC1 = aC * (Z1 ** 2 / A1 ** (1 / 3) + Z2 ** 2 / A2 ** (1 / 3))
dS, dC = ES1 - ES0, EC1 - EC0
print(f"表面 {ES0:.0f}→{ES1:.0f} ({dS:+.0f}) / クーロン {EC0:.0f}→{EC1:.0f} ({dC:+.0f}) / 差 {dS + dC:+.0f} MeV")
ok(160 < dS < 185, "表面エネルギーは約+170 MeV 増える")
ok(dC < -330, "クーロンエネルギーは大きく減る")
ok(-160 > dS + dC > -200, "差し引きで放出（約-174 MeV、対分裂の会話中の概算 -190 を訂正）")
ok(abs(Z ** 2 / A - 35.86) < 0.01, "Z²/A(U-236)")
ok(abs((dS + dC) / 931.494 + 0.2) < 0.06, "質量欠損 約0.2 u")

# --- Block 2: 表面張力と OπO の長さ ---
sigma = aS / (4 * math.pi * 1.2 ** 2)
ok(abs(sigma - 0.98) < 0.01, "σ ≈ 0.98 MeV/fm²")
for a_s in (17.0, 18.3):
    s = a_s / (4 * math.pi * 1.44)
    ok(0.93 < s < 1.02, "σ の幅 0.94〜1.01")
d_2000 = (hc / (2000 * sigma)) ** (1 / 3)  # σ = n·hc/d³, n = 1/2000
ok(abs(d_2000 - 0.86) < 0.01, "n=1/2000 なら d≈0.86 fm")
cell = 0.16 ** (-1 / 3)
lam_p = hc / 938.272
ok(abs(cell - 1.842) < 0.002 and abs(lam_p - 1.3214) < 0.0005, "核子セル一辺・陽子コンプトン波長")
ok(1.36 < 0.17 ** (-1 / 3) / lam_p < 0.15 ** (-1 / 3) / lam_p < 1.43, "比は密度の不確かさで 1.37〜1.42")

# --- Block 3: 2000 と誕生則 ---
ok(3 ** 6 < 2000 < 3 ** 7 and 3 ** 7 - 2000 == 187, "2000 は第7世代の途中、187 はみ出す")
ok(2000 % 3 == 2 and all(3 ** k % 3 == 0 for k in range(1, 12)), "累積 3^k は 2000 に一致しない")
ok(125 * 8 * 2 == 2000, "125×8×2")
e_min = hc / 1.68
ok(abs(e_min - 738) < 1 and abs(2000 * e_min / 1e6 - 1.476) < 0.002, "e≥738 MeV, E0≥1.48 TeV")
ok(hc / (2 * 938.272 / 2000) > 1000, "陽子対生成では d≈1320 fm で核より大きい")

# --- Block 4: 尺度 ---
G, h, c = 6.67430e-11, 6.62607015e-34, 2.99792458e8
d_pl = math.sqrt(2 * G * h / c ** 3)
ok(5.6e-35 < d_pl < 5.8e-35, "重力で閉じる条件 d≈5.7e-35 m")

# --- Block 5: 正8面体・立方体・XY=1 ---
r = 1.0
ok(math.isclose((math.sqrt(2) * r / r) ** 2, 2), "読みB: 破るエネルギーは単振動で2倍")
xs = np.linspace(0.05, 20, 200001)
ok(abs(np.min(np.hypot(xs, 1 / xs)) - math.sqrt(2)) < 1e-6, "XY=1 の原点最近点は √2")
# 定在波: 直径=1波長なら中心が節
ok(abs(math.sin(2 * math.pi * 0.5)) < 1e-12, "中心が節")

# --- Block 6: 切頂八面体（正8面体∩立方体） ---
t = 1.0  # 立方体の中心から面まで
R = 1.5 * t  # 正8面体の中心から頂点まで
sq_edge = math.sqrt(2) * (R - t)
hex_edge = math.dist((t, R - t, 0), (R - t, t, 0))
ok(math.isclose(sq_edge, hex_edge), "R=3t/2 で正方形と六角形の辺が等しい")
ok(6 + 8 == 14, "面 6+8")
# bcc の第1・第2近接が 8 と 6
pts = [p for p in itertools.product(range(-2, 3), repeat=3)] + \
      [tuple(x + 0.5 for x in p) for p in itertools.product(range(-2, 2), repeat=3)]
dists = sorted(round(math.dist(p, (0, 0, 0)), 6) for p in pts if p != (0, 0, 0))
ok(dists.count(dists[0]) == 8 and dists.count(1.0) == 6, "bcc 近接 8 と 6")
# 正四面体と立方体の二面角で 360° は 4×90° のみ
dt, dc = math.degrees(math.acos(-1 / 3)), 90.0  # 正8面体の二面角 109.47°
combos = [(i, j) for i in range(5) for j in range(5) if i + j and abs(i * dc + j * dt - 360) < 1e-6]
ok(combos == [(4, 0)], "正8面体と立方体の混合では辺を閉じられない")

# --- Block 7: 立方体の5分割と星型八面体 ---
a = 1.0
ok(math.isclose(4 * a ** 3 / 6 + a ** 3 / 3, a ** 3), "4角+中心1=立方体")
ok(math.isclose(4 * a ** 3 / 6 + 2 * a ** 3 / 3 - a ** 3, a ** 3 / 3), "4+2 で a³/3 はみ出す")
tet_area = math.sqrt(3) * (a * math.sqrt(2)) ** 2
small = math.sqrt(3) / 4 * (a / math.sqrt(2)) ** 2
ok(math.isclose(24 * small / (2 * tet_area), 0.75), "重ねると表面積 3/4")
ok(math.isclose(2 * tet_area - 24 * small, 8 * small), "隠れる面積 = 正8面体の表面 √3a²")
ok(math.isclose(8 * small, math.sqrt(3) * a ** 2), "√3 a²")

# --- Block 8: 一筆書き（奇数次数の頂点数） ---
def odd(deg):
    return sum(d % 2 for d in deg)


ok(odd([3, 3]) == 2, "OπO: 奇数点2 → 開いた一筆書き")
ok(odd([4] * 6) == 0, "正8面体: 閉じた一筆書き")
ok(odd([3] * 8) == 8 and odd([3] * 4) == 4, "立方体・正四面体は不可")

# --- Block 9: 双錐と 7.36° ---
for n in (3, 4, 5):
    V, E, F = n + 2, 3 * n, 2 * n
    ok(V - E + F == 2, "オイラー")
    ok((V % 2, E % 2, F % 2) == ((n % 2), (n % 2), 0), "奇数nで頂点・辺が奇数、面は偶数")
    eq = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)]
    has_inv = all(any(math.isclose(-x, u, abs_tol=1e-9) and math.isclose(-y, v, abs_tol=1e-9) for u, v in eq) for x, y in eq)
    ok(has_inv == (n % 2 == 0), "反転中心は偶数nのみ")
gap = 360 - 5 * math.degrees(math.acos(1 / 3))
ok(abs(gap - 7.356) < 0.001, "正四面体5個のすき間 7.36°")

print(f"{N} assert 全通過")
