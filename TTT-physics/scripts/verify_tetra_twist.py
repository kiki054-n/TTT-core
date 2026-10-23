"""
TTT 検証スクリプト: 正四面体の「割り切れないねじれ」と 501 / 125.25 の関係

検証項目
  [A1] 正四面体の二面角 θ = arccos(1/3) は π の有理数倍ではない（証明＋数値確認）
  [A2] デーン不変量: 立方体は 0、正四面体は 0 でない
  [C1] 消せないずれの「大きさ」の候補が 1/500, 1/4, 501, 125.25 と一致するか
  [C2] θ/π の連分数近似に 500, 501, 1500, 2000 が現れるか
  [C3] n 個のテトラを辺のまわりに並べたとき、どの n で最も閉じに近いか

実行: python3 verify_tetra_twist.py
"""
import sympy as sp
from mpmath import mp, mpf, acos, pi, nstr

mp.dps = 50
PASS, FAIL, INFO = "PASS", "FAIL", "INFO"


def head(t):
    print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)


# ---------------------------------------------------------------- A1
head("[A1] 二面角 θ = arccos(1/3) は π の有理数倍ではない")
# 証明: nθ = 2πk なら cos(nθ) = 1。cos(nθ) = T_n(1/3) = a_n / 3^n とおくと
#   a_0 = 1, a_1 = 1, a_{n+1} = 2 a_n - 9 a_{n-1}
# 法 3 で a_{n+1} ≡ 2 a_n なので a_n ≡ 2^(n-1) ≢ 0 (mod 3)。
# よって n ≥ 1 で a_n/3^n は既約分数で分母 3^n ≥ 3、整数 ±1 になりえない。
# → cos(nθ) ≠ ±1 がすべての n ≥ 1 で成り立つ → θ/π は無理数。
a = [1, 1]
for n in range(1, 500):
    a.append(2 * a[-1] - 9 * a[-2])
ok_mod = all(a[n] % 3 != 0 for n in range(1, 500))
x = sp.Rational(1, 3)
ok_cheb = all(sp.chebyshevt(n, x) == sp.Rational(a[n], 3 ** n) for n in range(0, 40))
print(f"漸化式と Chebyshev T_n(1/3) の一致 (n<40): {ok_cheb}")
print(f"a_n ≢ 0 mod 3 (1 ≤ n < 500): {ok_mod}")
print(f"→ {PASS if ok_mod and ok_cheb else FAIL}: 帰納法により全 n で成立（数値は確認用）")

theta = acos(mpf(1) / 3)
print(f"θ = {nstr(theta*180/pi, 15)}°")
gap5 = 2 * pi - 5 * theta
print(f"5 個並べた隙間 = {nstr(gap5*180/pi, 12)}°  (1周の {nstr(gap5/(2*pi), 10)})")

# ---------------------------------------------------------------- A2
head("[A2] デーン不変量 D = Σ 辺長 ⊗ 二面角  (ℝ ⊗ ℝ/πℚ)")
# 立方体: 12 辺 × a ⊗ π/2 → π/2 ∈ πℚ なので 0
# 正四面体: 6 辺 × a ⊗ θ → θ ∉ πℚ (A1) なので ≠ 0
print("立方体   : 12a ⊗ (π/2) = 0                      → 0")
print("正四面体 : 6a ⊗ arccos(1/3)                    → 0 でない（A1 より）")
print(f"→ {PASS}: 正四面体は切り分けても立方体に組み直せない（Dehn 1900）")
print(f"{INFO}: デーン不変量はテンソル積の元で、1 つの実数ではない。")
print("      『ずれの大きさ』を数で言うには射影（測り方）を選ぶ必要がある → C1 は仮説扱い")

# ---------------------------------------------------------------- C1
head("[C1] ずれの大きさの候補と 1/500・1/4 の照合")
targets = {
    "1/500 (501/500-1)": mpf(1) / 500,
    "1/4 (125.25-125)": mpf(1) / 4,
    "1/501": mpf(1) / 501,
}
cands = {}
cands["5個の隙間 / 2π"] = gap5 / (2 * pi)
cands["1/5 - θ/2π"] = mpf(1) / 5 - theta / (2 * pi)
# 頂点まわり: 正四面体の頂点立体角 Ω = arccos(23/27)、20 個で 4π に足りない割合
Omega = acos(mpf(23) / 27)
cands["20個の頂点立体角の不足 / 4π"] = 1 - 20 * Omega / (4 * pi)
# 正二十面体（20 テトラ）の辺長のずれ: 中心-頂点 R と辺 a の比
R_over_a = sp.sqrt(10 + 2 * sp.sqrt(5)) / 4
cands["正二十面体 1 - R/a"] = 1 - mpf(sp.N(R_over_a, 50))
# 立方体に内接するテトラの体積 1/3 と、テトラ 5 個の和
cands["5×(1/3) - 3/2 (5個の内接テトラ − 体積)"] = mpf(5) / 3 - mpf(3) / 2

print(f"{'候補':<36}{'値':>16}" + "".join(f"{k:>22}" for k in targets))
for name, v in cands.items():
    row = f"{name:<36}{nstr(v, 10):>16}"
    for t in targets.values():
        row += f"{nstr(v / t, 8):>22}"
    print(row)
print(f"{INFO}: 右の列は 候補 ÷ 目標。1 に近ければ一致")

# ---------------------------------------------------------------- C2
head("[C2] θ/π と θ/2π の連分数近似（分母に 500, 501, 1500, 2000 が出るか）")
special = {4, 5, 10, 12, 20, 125, 500, 501, 1500, 2000}
for label, val in [("θ/π", theta / pi), ("θ/2π", theta / (2 * pi))]:
    cf = list(sp.continued_fraction_iterator(sp.Rational(str(nstr(val, 45)))))[:14]
    convs = list(sp.continued_fraction_convergents(cf))
    print(f"{label} = {nstr(val, 20)}")
    print(f"  連分数 = {cf}")
    for c in convs:
        q = sp.fraction(c)[1]
        mark = "  ← 注目数" if q in special else ""
        print(f"    {str(c):>20}  分母 {q}{mark}")

# ---------------------------------------------------------------- C3
head("[C3] n 個のテトラを辺のまわりに並べて最も閉じに近い n（n ≤ 2000）")
best = []
for n in range(1, 2001):
    turns = n * theta / (2 * pi)
    err = abs(turns - mp.nint(turns))
    best.append((err, n, int(mp.nint(turns))))
best.sort()
print(f"{'n':>6}{'周回数':>8}{'ずれ(周)':>18}")
for err, n, k in best[:12]:
    print(f"{n:>6}{k:>8}{nstr(err, 8):>18}")
for n in (5, 125, 500, 501, 1500, 2000):
    turns = n * theta / (2 * pi)
    err = abs(turns - mp.nint(turns))
    rank = [b[1] for b in best].index(n) + 1
    print(f"  n={n:>5}: ずれ {nstr(err, 8):>12} 周   順位 {rank}/2000")

head("まとめ")
print("A1, A2 は証明済み（割り切れないずれは必ず存在する）")
print("C1–C3 は 501 / 125.25 との量的一致の検査（結果は上の表を参照）")
