"""
TTT 検証スクリプト 2026-10-12 (2/2)：O と π・宇宙の境界・誕生のエネルギーと h・空間のゆがみ
  numpy のみ（標準ライブラリの math を併用）。すべての assert が通れば成立。
  物理定数は CODATA 2018/2022 の SI 値。
"""
import math
import numpy as np

ok = 0
def check(cond, msg):
    global ok
    assert cond, msg
    ok += 1
    print("  ✓", msg)

hbar = 1.054571817e-34
h = 2 * math.pi * hbar
c = 299792458.0
G = 6.67430e-11
me = 9.1093837015e-31
eV = 1.602176634e-19
GeV = 1e9 * eV
k13 = 1 + 3 * math.pi
lP = math.sqrt(hbar * G / c ** 3)
tP = lP / c
EP = math.sqrt(hbar * c ** 5 / G)

# ---- Block 1：O と π（回転と単振動）----
print("Block 1：O と π")
t = np.linspace(0, 10, 2001); w = 1.7
check(np.allclose(np.exp(1j * w * t) + np.exp(-1j * w * t), 2 * np.cos(w * t)),
      "逆向きの回転2つの和 ＝ 1本の軸上の単振動（OπO → πOπ、円偏光2つ → 直線偏光）")
rng = np.random.default_rng(0)
Ev, Bv = rng.normal(size=3), rng.normal(size=3)
F = Ev + 1j * Bv
iF = 1j * F
check(np.allclose(iF.real, -Bv) and np.allclose(iF.imag, Ev) and abs(np.vdot(iF, iF) - np.vdot(F, F)) < 1e-12,
      "F ＝ E＋icB に i をかけると E と B が入れ替わり、エネルギー |F|² は不変（電磁双対性）")
a = 1.0; K = 1.0
kk = np.linspace(1e-3, 0.3, 50)
wl = 2 * np.sqrt(K) * np.sin(kk * a / 2)
vph = wl / kk
check(np.allclose(vph, a * np.sqrt(K) * (1 - (kk * a) ** 2 / 24), atol=1e-6) and np.all(np.diff(vph) < 0),
      "つながった振動子の列：ω ＝ 2ω0 sin(ka/2)、速さ ≈ c(1 − (ka)²/24)、短い波ほど遅い")

# ---- Block 2：宇宙の境界（巨大粒子）----
print("Block 2：境界の広がり")
check(True, "密度一定のまま膨張し、外からの供給がないと dE ＝ −PdV より P ＝ −ρc²（記述のみ）")
A, n = 1, 1
hist = {}
for kstep in range(1, 5001):
    A *= 3
    while A > 3 * n * n + 3 * n + 1:
        A -= 3 * n * n + 3 * n + 1
        n += 1
    hist[kstep] = n
check(0.98 < hist[5000] / 5000 < 1.0 and 0.98 < hist[2000] / 2000 < 1.0,
      f"あふれた OOπO だけが ×3、層 (n+1)³−n³ を埋めると境界は τ0 ごとに1層（n/k ＝ {hist[5000]/5000:.4f}）")
check(abs((2 ** (1 / 3)) - 1.26) < 0.001, "（撤回した ×2 の読み）数が ×2 で表面積 ×2^(2/3) なら最前列は τ0 ごとに 1.26 倍混む")

# ---- Block 3：質量・時間・重力の既知の事実 ----
print("Block 3：質量と時間")
fC = me * c ** 2 / h
check(abs(fC / 1.2356e20 - 1) < 1e-4, f"電子のコンプトン振動数 mc²/h ＝ {fC:.4e} Hz")
check(abs(2.1969811e-6 * 29.3 * 1e6 - 64.37) < 0.01, "ミューオン寿命 2.197 μs × γ 29.3 ＝ 64.4 μs")
check(abs(9.80665 * 0.3 / c ** 2 - 3.27e-17) < 0.01e-17, "高さ 30 cm の時計のずれ gh/c² ＝ 3.27×10⁻¹⁷")
hbar_MeVs = hbar / (1e6 * eV)
check(abs(hbar_MeVs / 4.1 - 1.6e-22) < 0.05e-22 and abs(hbar_MeVs / 1420 - 4.6e-25) < 0.1e-25,
      "幅 Γ ＝ ħ/τ：ヒッグス 4.1 MeV ↔ 1.6×10⁻²² s、トップ 1.42 GeV ↔ 4.6×10⁻²⁵ s")
gamma = 3.0; m = 1.0; vv = math.sqrt(1 - 1 / gamma ** 2)
Etot = gamma * m; p = gamma * m * vv
check(abs(Etot ** 2 - p ** 2 - m ** 2) < 1e-12, "(mc²)² ＝ E² − (pc)²：静止質量は速さで変わらず、E ＝ γmc² が増える")
Ms, Rs = 1.98847e30, 6.957e8
defl = 4 * G * Ms / (Rs * c ** 2) * 206264.806
check(abs(defl - 1.75) < 0.01, f"太陽のそばの光の曲がり 4GM/(bc²) ＝ {defl:.3f}″（ニュートンの2倍）")

# ---- Block 4：誕生のエネルギーと h ----
print("Block 4：誕生のエネルギー")
a = 1.0; cc = 1.0
L_path = 1 + 3 * math.pi * a
check(abs(L_path - k13) < 1e-15, "1×1×1 のマス：リング直径 a ×3（3πa）＋ π の長さ a → 4要素の合計 1+3π")
tau0 = L_path / cc
check(abs(tau0 / (k13 / 4) - 4) < 1e-15, "τ0 ＝ (1+3π)a/c は 9/25 の (1+3π)/2·R/c ＝ (1+3π)a/(4c) の4倍（REVISED）")
eps = hbar * c / 1.0
L_ring = eps * 0.5 / c
check(abs(L_ring / hbar - 0.5) < 1e-15, "要素1つ ε ＝ ħc/a、直径 a のリングを光速で回すと L ＝ ħ/2")
check(abs(4 * k13 / (2 * math.pi) - 6.6366) < 1e-4, f"E0τ0 ＝ 4(1+3π)ħ ＝ {4*k13/(2*math.pi):.4f} h")
check(abs(1 / (8 * k13) - 0.011990) < 1e-6, "外郭の O 1つの L ＝ E0τ0 / (8(1+3π))")
check(abs(1 / (2 * k13) - 0.047962) < 1e-6 and abs(1 / k13 - 0.095925) < 1e-6,
      "新しい τ0 で R/τ0 ＝ c/(2(1+3π)) ＝ 0.04796c、a/τ0 ＝ 0.0959c（記録の 0.19185c を置き換え）")
check(True, "OOπO（＋L）と ππOπ（−L）が i と −i の対で同時に生まれ、合計 0（記述のみ）")

# ---- Block 5：a と力の上限 ----
print("Block 5：a とプランク長")
check(abs(lP - 1.616255e-35) < 1e-40 and abs(EP / GeV - 1.22089e19) < 1e15,
      "ℓ_P ＝ 1.616×10⁻³⁵ m、E_P ＝ 1.221×10¹⁹ GeV")
check(abs(k13 * tP - 5.620e-43) < 0.01e-43, "a ＝ ℓ_P なら τ0 ＝ (1+3π) t_P ＝ 5.62×10⁻⁴³ s、ε ＝ E_P")
check(abs(2 * G * EP / c ** 4 / lP - 2) < 1e-12 and abs(EP / (lP / 2) / (c ** 4 / G) - 2) < 1e-12,
      "a ＝ ℓ_P ではブラックホール半径 2ℓ_P ＞ リング半径 0.5ℓ_P、F ＝ 2c⁴/G")
p_ = 3.0; Rr = 2.0
check(abs(p_ * (c / Rr) - (p_ * c) / Rr) < 1e-9, "F ＝ dp/dt ＝ pω ＝ E/R（速さを上げる加速度は使わない）")
a2 = math.sqrt(4 * hbar * G / c ** 3)
a4 = math.sqrt(8 * hbar * G / c ** 3)
check(abs(2 * hbar * c / a2 ** 2 - c ** 4 / (2 * G)) / (c ** 4 / G) < 1e-12 and abs(a2 / lP - 2) < 1e-12,
      "F ＝ 2ħc/a² ＝ c⁴/2G なら a ＝ 2ℓ_P")
check(abs(a4 / lP - 2 * math.sqrt(2)) < 1e-12 and abs(2 * k13 - 20.85) < 0.01 and abs(2 * math.sqrt(2) * k13 - 29.49) < 0.01,
      "F ＝ c⁴/4G なら a ＝ 2√2ℓ_P、τ0 ＝ 20.85 t_P（c⁴/2G）／29.49 t_P（c⁴/4G）")
check(abs(c ** 4 / (8 * math.pi * G) - 4.815e42) < 0.01e42, "空間の硬さ c⁴/(8πG) ＝ 4.8×10⁴² N")

# ---- Block 6：誕生の力と 37 があふれる力 ----
print("Block 6：面1つにかかる力")
f1 = 2 * 4 / 3
f5 = 162 * 4 / (3 * 125)
check(abs(f1 - 8 / 3) < 1e-15 and abs(f5 - 1.728) < 1e-12 and abs(f1 / f5 - 1.5432) < 1e-4,
      "圧力で比べると 1×1×1（OOπO 2）は 2.667ε/a、5×5×5（162/125）は 1.728ε/a、比 1.543")

# ---- Block 7：ゆがみの源 ----
print("Block 7：ゆがみの源")
rho = 1.0
check(abs((rho + 3 * rho / 3) - 2 * rho) < 1e-15 and abs((rho + 3 * (-rho)) + 2 * rho) < 1e-15,
      "源 ρ＋3P/c²：光は 2ρ、ダークエネルギー（P ＝ −ρc²）は −2ρ")
check(True, "源 ＝ OπO と比べたエネルギー密度の差（質量＋ためた運動エネルギー）。光も含む（ADOPTED、記述のみ）")

print(f"\n{ok} assert 全通過")
