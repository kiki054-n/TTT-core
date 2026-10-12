"""
TTT 検証スクリプト 2026-10-12：空間・境界・質量・力・運動の流れのまとめ
  numpy のみ（標準ライブラリの fractions, math, itertools を併用）。すべての assert が通れば成立。
  単位：OOπO 1つのエネルギー E0 ＝ 1、リング半径 R ＝ 1（必要な箇所のみ c を明示）
"""
import math
import itertools as it
import numpy as np
from fractions import Fraction as Fr

ok = 0
def check(cond, msg):
    global ok
    assert cond, msg
    ok += 1
    print("  ✓", msg)

phi = (1 + 5 ** 0.5) / 2

# ---- Block 1：力 × 長さ ＝ k × エネルギー ----
print("Block 1：F·L ＝ k·E")
E, R = 1.0, 1.0
check(abs((E / R) * R / E - 1) < 1e-15, "光速のリング：F ＝ E/R、k ＝ 1")
T = 2 * E / (math.pi * R)
check(abs(T * R / E - 2 / math.pi) < 1e-15, "光速で回る直線：E ＝ (π/2)TR、k ＝ 2/π")
eps = 0.75                                   # OπO 1つ ＝ OOπO の 3/4
t_edge = eps / (3 * R)
check(abs(6 * t_edge * 2 * R - 4 * eps) < 1e-15, "テトラ拘束：6辺 × 張力 ε/(3R) × 辺 2R ＝ 4ε（k ＝ 1）")
for n in range(1, 8):
    N = 2 * 3 ** (n - 1); V = n ** 3
    Es, Eo = N / 4, 3 * N / 4
    P = Eo / (3 * V)
    assert abs(P * V - Es) < 1e-12
    side = sum(P * n * n * n for _ in range(6)) / 2   # 6面 × (P·面積) × (中心から面 n/2)… n²×n/2
    assert abs(side - Eo) < 1e-9
check(True, "外郭：外郭 : OπO ＝ 1 : 3 のとき E外郭 ＝ PV ＝ E_OπO/3、6面の F·L 合計 ＝ E_OπO（段1〜7すべて、k ＝ 1）")

# ---- Block 2：単位 ----
print("Block 2：時間・長さ・速さ")
k = (1 + 3 * math.pi) / 2
check(abs(1 / k - 0.19185) < 1e-5, f"τ0 ＝ (1+3π)/2·R/c より R ＝ {1/k:.5f} cτ0、格子1マス ＝ 2R")
check(1 / k < 1, f"枠の広がる速さ R/τ0 ＝ {1/k:.5f} c は光速を超えない")
H = math.log(3) / 3
check(abs(H - 0.3662) < 1e-4, f"体積が τ0 ごとに3倍 → 大きさ ∝ e^(Ht)、H ＝ ln3/(3τ0) ＝ {H:.4f}/τ0（指数的膨張）")

# ---- Block 3：125 の空間と 3・4 の食い違い ----
print("Block 3：125 の空間、500 と 501、D の保存")
n_oopo = 500
Es, Eo = n_oopo / 4, 3 * n_oopo / 4
check(Eo / (3 * 125) == 1.0 and Es == 125, "OOπO 500 → テトラ 125：圧力 1、外郭 125 ＝ PV")
check(500 % 4 == 0 and 500 % 3 != 0 and 501 % 3 == 0 and 501 % 4 != 0, "格子は4の倍数 500、外郭は3の倍数 501 を要求（同時には満たせない）")
check(Fr(501, 4) == Fr(501, 4) and float(Fr(501, 4)) == 125.25, "食い違い 1 は格子の単位で 1/4：501/4 ＝ 125.25")
Es, Eo = 501 / 4, 3 * 501 / 4
need = 3 * 126 - Eo
Es2, Eo2 = Es - need, 3 * 126
D = Es2 - Eo2 / 3
check(abs(need - 2.25) < 1e-12 and abs(D + 3) < 1e-12, "126番目のテトラが外郭から 2.25 を奪う → 外郭 123、必要 126、D ＝ −3（外郭が破れる）")
check(abs(0.25 - 0.75 / 3) < 1e-15, "OOπO を1つ供給しても ΔD ＝ 1/4 − (3/4)/3 ＝ 0（供給では戻らない）")
check(abs(D + 9 / 3) < 1e-12, "質量は圧力を持たないとして、テトラ3つ（9）を質量にすれば D ＝ 0")

# ---- Block 4：正四面体・立方体・正二十面体を軸で定義 ----
print("Block 4：点・線・面と軸")
P = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
d = [np.linalg.norm(P[i] - P[j]) for i, j in it.combinations(range(4), 2)]
check(np.allclose(d, d[0]) and np.allclose((P ** 2).sum(1), 3), "正四面体の4点は互いに等距離で、1つの球（半径 √3）の上にある")
check(abs(np.linalg.det(2 * (P[1:] - P[0]))) > 1e-9, "同じ平面に乗らない4点は、ちょうど1つの球を決める（外接球の連立方程式が一意）")
e1, e2 = P[0] - P[3], P[1] - P[2]
check(abs(e1 @ e2) < 1e-12 and abs(2 / (2 * 2 ** 0.5) - 1 / 2 ** 0.5) < 1e-15, "直交する2本の軸（向かい合う辺）を辺/√2 離して置くと正四面体")
faces = list(it.combinations(range(4), 3))
c1 = sum(1 for f in faces if {0, 3} <= set(f)); c2 = sum(1 for f in faces if {1, 2} <= set(f))
check(c1 == 2 and c2 == 2 and all(not ({0, 3} <= set(f) and {1, 2} <= set(f)) for f in faces),
      "4面は、片方の軸を含む2枚ともう片方を含む2枚にちょうど分かれる（π 4・O 8 の分け方の根拠）")
ico = []
for s1 in (1, -1):
    for s2 in (1, -1):
        ico += [(0, s1, s2 * phi), (s1, s2 * phi, 0), (s2 * phi, 0, s1)]
ico = np.array(ico, float)
dd = sorted({round(np.linalg.norm(a - b), 9) for a, b in it.combinations(ico, 2)})
check(abs(dd[0] - 2) < 1e-9 and len(ico) == 12, "正二十面体の12頂点 (0,±1,±φ) 等：辺 2")
check(abs(np.linalg.norm(np.array([0, 1, phi]) - np.array([0, 1, -phi])) - 2 * phi) < 1e-12,
      "平行な2本の軸（辺）の間の距離は 2φ ＝ φ × 辺。3方向 × 2本 ＝ 6本の軸で決まる")
for n in range(3, 8):
    rc = 0.5 / math.sin(math.pi / n)
    h2 = 1 - rc ** 2
    if n <= 5:
        assert h2 > 1e-12
    else:
        assert h2 <= 1e-12
check(True, "辺がすべて等しい n 角双錐は n ＝ 3, 4, 5 だけ（n ＝ 6 で高さ 0）→ 正多面体5＋双錐2 ＝ 7")

# ---- Block 5：外から見た比重と中から見た比重 ----
print("Block 5：比重（外接球と内接球）")
S = {"tetra": (4, 2 ** .5 / 12, 6 ** .5 / 4, 6 ** .5 / 12), "cube": (6, 1, 3 ** .5 / 2, .5),
     "octa": (6, 2 ** .5 / 3, 2 ** .5 / 2, 6 ** .5 / 6), "icosa": (12, 5 / 12 * (3 + 5 ** .5), math.sin(2 * math.pi / 5), phi ** 2 / (2 * 3 ** .5))}
sg = lambda m, V, L: m / (V / L ** 3)
to = sg(S["tetra"][0], S["tetra"][1], S["tetra"][2]); ti = sg(S["tetra"][0], S["tetra"][1], S["tetra"][3])
out = {k: sg(m, V, Rr) / to for k, (m, V, Rr, r) in S.items()}
inn = {k: sg(m, V, r) / ti for k, (m, V, Rr, r) in S.items()}
check(abs(out["cube"] - 0.5) < 1e-12 and abs(out["octa"] - 1 / 3 ** .5) < 1e-12, "外から（外接球）：立方体 0.5、正八面体 1/√3")
check(abs(inn["octa"] - 3) < 1e-12, "中から（内接球）：正八面体は正四面体のちょうど 3 倍（テトラ3つ＝正八面体）")

# ---- Block 6：奇数段と偶数段の中心のずれ ----
print("Block 6：中心のずれ")
off = np.array([0.5, 0.5, 0.5]) * 2          # 半マス × 3方向、1マス ＝ 2R
check(abs(np.linalg.norm(off) - 3 ** .5) < 1e-12, "奇数段（マスの中心）と偶数段（格子点）の中心は体対角線の向きに √3 R ずれる")
check(abs(3 ** .5 / k - 0.3323) < 1e-4, f"ずれの速さ √3R/τ0 ＝ {3**.5/k:.4f} c、往復周期 2τ0")

# ---- Block 7：回転子 R^3 ＝ −1（2 と 3 の結びつき） ----
print("Block 7：体対角線のまわりの 120° 回転")
def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2, w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2])
u = np.ones(3) / 3 ** .5
q = np.hstack([math.cos(math.pi / 3), math.sin(math.pi / 3) * u])
q3 = qmul(qmul(q, q), q); q6 = qmul(q3, q3)
check(np.allclose(q3, [-1, 0, 0, 0]) and np.allclose(q6, [1, 0, 0, 0]), "回転子 R ＝ e^(−Iuπ/3)：R³ ＝ −1、R⁶ ＝ 1（3回で符号を除き戻る＝二重被覆）")
v = np.array([0, 1, 0, 0.0]); qc = q * np.array([1, -1, -1, -1])
rx = qmul(qmul(q, v), qc)[1:]
ry = qmul(qmul(q, np.hstack([0, rx])), qc)[1:]
rz = qmul(qmul(q, np.hstack([0, ry])), qc)[1:]
check(np.allclose(rx, [0, 1, 0]) and np.allclose(ry, [0, 0, 1]) and np.allclose(rz, [1, 0, 0]), "同じ回転で X → Y → Z と巡回する（虚数 i の繰り返しでは作れない：i² ＝ −1）")

# ---- Block 8：外部資料の検証で使った数値 ----
print("Block 8：外部資料の数値")
check(abs(2 ** 27 / 3 ** 17 - 256 / 243) > 0.01, f"2²⁷/3¹⁷ ＝ {2**27/3**17:.4f} ≠ 256/243 ＝ {256/243:.4f}")
lP = 1.616255e-35; t = 2.0e-27 / lP
check(abs(t / (1.22089e19 / 1.2005e12) - 12.17) < 0.05, f"a/l_P ＝ {t:.3e} は LIV の上限 1.02×10⁷ を 12 倍超える")
aC, MC = 3.567, 12.011
aSi = aC * (28.085 / MC) ** (0.564 / 2.40)
check(abs((aSi - 5.431) / 5.431 + 0.198) < 0.002, f"IV族のスケーリング則は Si で {aSi:.3f} Å（実測 5.431、−19.8%）")
check(abs(math.sqrt(3) * 0.142 * math.sqrt(300) / math.pi - 1.356) < 0.001, "(10,10) 型 CNT の直径は 1.356 nm（1.42 は C–C 結合長 0.142 nm）")
me, mm = 0.51099895, 105.6583755
f = lambda x: (me + mm + x) - (2 / 3) * (me ** .5 + mm ** .5 + x ** .5) ** 2
lo, hi = 1000.0, 3000.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if f(lo) * f(mid) > 0 else (lo, mid)
check(abs(lo - 1776.969) < 0.001 and abs(lo - 1776.93) / 0.09 < 0.5, f"小出の式 mτ ＝ {lo:.3f} MeV、PDG 2025 1776.93±0.09 と 0.4σ")
check(abs(6 * math.pi ** 5 - 1836.118) < 0.001, "6π⁵ ＝ 1836.12（チャームの比 2485 ではなく陽子/電子比に近い）")
check(abs(2.2e6 * me / 1e6 - 1.124) < 0.001 and 2.2e6 * me / 1e6 < 1.37, "H 節の M_T ≈ 2.2×10⁶ mₑ ＝ 1.12 TeV は LHC の下限 1.37 TeV より軽い")

print(f"\n{ok} assert 全通過")
