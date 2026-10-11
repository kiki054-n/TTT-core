"""
TTT 検証スクリプト 2026-10-11：力と質量・テトラ拘束のねじれ・α の式の書き直し
  numpy のみ（標準ライブラリの fractions, itertools, math を併用）。すべての assert が通れば成立。
  単位：c ＝ 1（Block 1 の時間単位の換算のみ c を R/τ0 で表す）
"""
import numpy as np
import itertools as it
import math
from fractions import Fraction as Fr

ok = 0
def check(cond, msg):
    global ok
    assert cond, msg
    ok += 1
    print("  ✓", msg)

# ---- Block 1：力と質量 ----
print("Block 1：F ＝ E/R と m ＝ FR/c²")
c, R, E = 1.0, 1.7, 3.2
m = E / c**2
F = m * c**2 / R
check(abs(F - E / R) < 1e-15, "光速の円運動で F ＝ mA ＝ (E/c²)(c²/R) ＝ E/R")
check(abs(F * R / c**2 - m) < 1e-15, "並べ替えると m ＝ FR/c²（質量は閉じ込める力 × 半径 / c²）")
# 電子：R ＝ ħ/(2mc) を入れると F ＝ 2m²c³/ħ
hbar, me, cs = 1.054571817e-34, 9.1093837015e-31, 299792458.0
Fe = me * cs**2 / (hbar / (2 * me * cs))
check(abs(Fe - 2 * me**2 * cs**3 / hbar) / Fe < 1e-12 and 0.42 < Fe < 0.43,
      f"電子（R ＝ ħ/2mc）で F ＝ 2m²c³/ħ ＝ {Fe:.3f} N")
G = 6.67430e-11
for mm in (1.0, 1e30):
    Rs = 2 * G * mm / cs**2
    check(abs(mm * cs**2 / Rs - cs**4 / (2 * G)) / (cs**4 / (2 * G)) < 1e-12,
          f"R をブラックホール半径 2Gm/c² にすると F ＝ c⁴/2G（m ＝ {mm:g} kg でも同じ）")
k = (1 + 3 * np.pi) / 2
check(abs(k - 5.21239) < 1e-5, f"時間単位 τ0 ＝ (1+3π)/2 · R/c で c ＝ {k:.5f} R/τ0（9/25 の定義）")

# ---- Block 2：テトラ拘束の力 ----
print("Block 2：4つの OπO（半径 R、接触）を正四面体に拘束")
R, eps = 1.0, 1.0
a = 2 * R
r = a * np.sqrt(6) / 4
check(abs(r - np.sqrt(6) / 2) < 1e-15, f"中心から各 OπO まで r ＝ √6/2 R ＝ {r:.4f} R")
f = eps / r
check(abs(4 * f - 3.26599) < 1e-5, f"中心へ押す力：1つ {f:.4f} ε/R、4つ合計 {4*f:.4f} ε/R")
t = f / (3 * np.sqrt(2 / 3))
check(abs(t - 1 / 3) < 1e-14, "辺1本の張力は厳密に ε/(3R)")
check(abs(4 * eps / k**2 - 0.14722) < 1e-5, "質量 m ＝ 4ε/c² ＝ 0.14722 ε τ0²/R²（OπO 自体は質量を持たない）")

# ---- Block 3：ねじれ ----
print("Block 3：正四面体は空間を埋めない（ねじれの発生点）")
d = np.arccos(1 / 3)
gap = 2 * np.pi - 5 * d
check(abs(np.degrees(gap) - 7.3561) < 1e-4, f"辺のまわりに5つ並べると隙間 {np.degrees(gap):.4f}°")
check(abs(np.degrees(gap / 5) - 1.471221) < 1e-6, f"1つあたり {np.degrees(gap/5):.6f}°（以前の 1.471221° と一致）、角ひずみ {gap/5/d*100:.3f}%")
q = np.sin(2 * np.pi / 5)
s_i = 1 - q
check(abs(s_i - 0.048943) < 1e-6, f"正二十面体：外接半径/辺 ＝ sin72° → 中心向きの辺は {s_i*100:.3f}% 短い")
Ns, Nr = 30, 12
U = lambda aa: t * (Ns * abs(aa - a) + Nr * abs(q * aa - a))
grid = np.linspace(a, a / q, 20001)
amin = grid[np.argmin([U(x) for x in grid])]
check(abs(amin - a) < 1e-3, "張力型では、表面は元の長さのまま中心向きの12本だけが縮むのがエネルギー最小")
Uico = U(a)
check(abs(Uico - 0.39155) < 1e-4, f"ねじれを閉じるエネルギー：全体 {Uico:.4f} ε、テトラ1つあたり {Uico/20:.4f} ε（4ε の {Uico/80*100:.2f}%）")

# ---- Block 4：0.296 ＝ 37/125 は数え方の産物（REJECTED） ----
print("Block 4：ねじれ ÷ 圧縮 の比")
s_c = 1 - (125 / 162) ** (1 / 3)
iso = (3 * t * s_i * a) / (6 * t * s_c * a)
check(abs(iso - 37 / 125) / (37 / 125) < 2e-3, f"孤立テトラ（3辺 vs 6辺）では {iso:.4f} ≈ 37/125 ＝ 0.296")
harm = 0.5 * (s_i / s_c) ** 2
check(abs(harm - 37 / 125) > 0.1, f"ばね型にすると {harm:.3f}（外れる）")
for n_, name in ((42, "全42本"), (30, "表面30本"), (12, "中心向き12本")):
    ratio = Uico / (t * n_ * s_c * a)
    check(abs(ratio - 0.296) > 0.05, f"正二十面体で辺を重複なく数えると {name}：{ratio:.3f}（0.296 にならない）")

# ---- Block 5：5つの立体と充填 ----
print("Block 5：四面体＋八面体ハニカムと 162/125 の充填率")
Vt, Vo = np.sqrt(2) / 12, np.sqrt(2) / 3
check(abs(Vo / Vt - 4) < 1e-14, "同じ辺で正八面体の体積は正四面体の4倍")
check(abs(2 * Vt / (2 * Vt + Vo) - 1 / 3) < 1e-14, "ハニカム（四面体2：八面体1）の体積比は 1/3 : 2/3")
phi = 162 / 125 * np.pi / 6
check(0.64 < phi < np.pi / (3 * np.sqrt(2)), f"162/125 の充填率 {phi:.4f} はランダム最密 0.64 と面心立方 0.7405 の間（整列が強制され、つぶさずに入る）")

# ---- Block 6：3×3×3 の面心立方格子（Core の候補として REJECTED） ----
print("Block 6：3×3×3 面心立方の数え上げ")
n = 3
A = [(0, 0, 0), (.5, .5, 0), (.5, 0, .5), (0, .5, .5)]
O = [(.5, .5, .5), (.5, 0, 0), (0, .5, 0), (0, 0, .5)]
T = [(x, y, z) for x in (.25, .75) for y in (.25, .75) for z in (.25, .75)]
def opn(B):
    S = set()
    for i, j, kk in it.product(range(-1, n + 1), repeat=3):
        for b in B:
            p = (i + b[0], j + b[1], kk + b[2])
            if all(0 <= cc <= n for cc in p):
                S.add(p)
    return len(S)
check((27 * len(A), 27 * len(O), 27 * len(T)) == (108, 108, 216), "周期的（境界なし）：格子点108・八面体位置108・四面体位置216")
check((opn(A), opn(O), opn(T)) == (172, 171, 216), "境界あり：172・171・216（108 は出ない）")
nat = sorted({27, 108, 216, 4, 8, 12, 6, 3, 9, 172, 171, 64, 13, 14, 2})
reach = set(nat)
for x, y in it.product(nat, repeat=2):
    reach |= {x + y, x * y, abs(x - y)}
check(all(v in reach for v in range(1, 31)), "帰無対照：格子の数の和・差・積で 1〜30 はすべて作れる（9 に重みなし）")

# ---- Block 7：α の式の書き直し ----
print("Block 7：1/α ＝ 137 ＋ 35/972 − 1/110592 の読み")
orig = Fr(137) + Fr(7 * 5, 108 * (5 + 4)) - Fr(1, 108 * 2**7 * (7 + 1))
check(orig == Fr(136395767, 995328), "記録の式 ＝ 136,395,767/995,328")
check(Fr(91 + 17) == Fr(6**3, 2) and 2 * 125 - 216 == 34, "Core ＝ 91＋17 ＝ (216−125)＋(2·125−216)/2 ＝ 6³/2（125 は消える）")
check(162 - 5**2 == 137 and 125 + 12 == 137 and 2**9 - 3 * 5**3 == 137, "137 ＝ 162−5²（B、採用）＝ 125＋12 ＝ 2⁹−3·5³")
Sx = sorted({1, 8, 27, 64, 125, 216, 512, 2, 6, 18, 54, 162, 37, 34, 17, 16, 3, 4, 5, 7, 9, 12, 25, 36, 91, 108})
pairs = [(x, y, '+') for x, y in it.combinations_with_replacement(Sx, 2) if x + y == 137] + \
        [(x, y, '-') for x in Sx for y in Sx if x - y == 137]
check(len(pairs) == 2, "帰無対照：TTT の数2つの和・差で 137 になるのは 125＋12 と 162−25 の2通り")
hits = sum(1 for v in range(100, 201) if any(x + y == v or x - y == v for x in Sx for y in Sx))
check(hits == 77, f"同じ数の組で 100〜200 のうち {hits}/101 が作れる（137 の分解に重みなし）")
check(Fr(37 - 2, 6 * 162) == Fr(35, 972), "第1項 35/972 ＝ (37−2)/(6×162)（段5の球とはみ出しで書ける）")
check(108 * 2**7 * 8 == 48**3 == (3 * 16)**3, "第2項の分母 110592 ＝ 48³ ＝ (3軸 × 角の欠陥16)³（読み②）")
new = Fr(162 - 25) + Fr(37 - 2, 6 * 162) - Fr(1, (3 * 16)**3)
check(new == orig, f"書き直した式 (162−5²) ＋ (37−2)/(6·162) − 1/(3·16)³ ＝ {float(new):.13f}（記録と厳密に一致）")

# ---- Block 8：測定との比較と第2項の決まり方 ----
print("Block 8：測定との比較（CODATA 2022 / Rb 2020 / g−2 2023 / Cs 2018）")
meas = {"CODATA 2022": (137.035999177, 21e-9), "Rb 2020": (137.035999206, 11e-9),
        "g−2 2023": (137.035999166, 15e-9), "Cs 2018": (137.035999046, 27e-9)}
v = float(new)
sig = {kk: (v - mm) / u for kk, (mm, u) in meas.items()}
for kk, s in sig.items():
    print(f"     {kk}: {s:+.2f}σ")
check(abs(sig["CODATA 2022"]) < 1 and abs(sig["Rb 2020"]) < 2 and abs(sig["g−2 2023"]) < 2, "CODATA・Rb・g−2 とは 2σ 以内")
check(sig["Cs 2018"] > 5, "Cs 2018 とは 5σ 以上離れる（Cs と Rb の食い違いの判定に使える）")
base = Fr(137) + Fr(35, 972)
gap_cs = (v - 137.035999046) / (1 / 110592)
check(0.015 < gap_cs < 0.017, f"Cs に合わせるには第2項を {gap_cs*100:.1f}% 動かす必要がある（分母の細かい形では判定は変わらない）")
win = [D for D in range(100000, 125000) if abs(float(base - Fr(1, D)) - 137.035999177) <= 21e-9]
lo, hi = win[0], win[-1]
check((lo, hi) == (110200, 110711), f"CODATA 2022 の 1σ に入る分母は {lo}〜{hi}（幅 {(hi-lo)/110592*100:.2f}%）")
Sp = [2, 3, 4, 5, 6, 7, 8, 9, 12, 16, 17, 18, 24, 25, 27, 34, 36, 37, 48, 54, 64, 91, 108, 125, 162, 216, 512]
cand = set()
for rr in (2, 3):
    for comb in it.combinations_with_replacement(Sp, rr):
        p = math.prod(comb)
        if lo <= p <= hi:
            cand.add(p)
for x in Sp:
    for e in (2, 3):
        if lo <= x**e <= hi:
            cand.add(x**e)
check(cand == {110592}, "その窓の中で TTT の数の積・累乗で作れる分母は 48³ ＝ 110592 だけ")

print(f"\n{ok} assert 全通過")
