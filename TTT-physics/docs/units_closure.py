#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
units_closure.py  --  2026-09-13
「電子＝質量ゼロで軌道エネルギーを持つ電荷」という描像のもとで
絶対単位系 (M, L, T) が定義できるか、を機械検証する。

Block 1: 次元計数 — (c, rho) だけでは M,L,T は固定されない
Block 2: 残存する 1 パラメータ・スケーリング群を明示
Block 3: (c, hbar, rho) なら閉じる。L=(hbar/(c*rho))^{1/4} と数値
Block 4: 質量ゼロ電荷の円運動 + J=hbar/2 -> R = lambdabar_C/2
Block 5: 古典電子半径 vs 電子サイズの実験上限（自己エネルギー模型の死）
Block 6: 中性子 vs 陽子 — 電荷ゼロでも質量はほぼ同じ
Block 7: 陽子質量収支 — 質量ゼロ構成子の描像はハドロンでは正しいが、糊は色であって電荷ではない
"""
from fractions import Fraction as F
import math, itertools

def solve_exponents(cols, target):
    """cols: list of (M,L,T) exponent triples. target: (M,L,T).
    Solve sum a_i * cols[i] = target over rationals. Return list or None."""
    n = len(cols)
    # build 3 x n matrix, augmented
    A = [[F(cols[j][i]) for j in range(n)] + [F(target[i])] for i in range(3)]
    # gaussian elimination
    row = 0; piv = []
    for col in range(n):
        sel = None
        for r in range(row, 3):
            if A[r][col] != 0: sel = r; break
        if sel is None: continue
        A[row], A[sel] = A[sel], A[row]
        pv = A[row][col]
        A[row] = [x/pv for x in A[row]]
        for r in range(3):
            if r != row and A[r][col] != 0:
                f = A[r][col]
                A[r] = [a - f*b for a, b in zip(A[r], A[row])]
        piv.append(col); row += 1
        if row == 3: break
    # inconsistency?
    for r in range(3):
        if all(A[r][c] == 0 for c in range(n)) and A[r][n] != 0:
            return None
    sol = [F(0)]*n
    for i, c in enumerate(piv):
        sol[c] = A[i][n]
    return sol

# ---- dimension triples (M, L, T) -------------------------------------------
DIM = {
    "c":    (0, 1, -1),     # L T^-1
    "rho":  (1, -3, 0),     # M L^-3   <- 37/125 は「無次元」ではなく密度
    "hbar": (1, 2, -1),     # M L^2 T^-1
    "G":    (-1, 3, -2),
    "e_g":  (F(1,2), F(3,2), -1),   # ガウス系の電荷
}
LEN  = (0, 1, 0)
MASS = (1, 0, 0)
TIME = (0, 0, 1)

print("="*72)
print("Block 1  次元計数: (c, rho) から長さ・質量・時間は作れるか")
print("="*72)
base2 = [DIM["c"], DIM["rho"]]
for name, tgt in [("length", LEN), ("mass", MASS), ("time", TIME)]:
    s = solve_exponents(base2, tgt)
    print(f"  {name:7s}: {'解なし' if s is None else s}")
    assert s is None, f"{name} が (c,rho) だけから作れてしまった"
print("  => 3つの基本次元に対し独立な次元定数が2つしかない。1自由度が残る。")
print("  注: rho=37/125 を『無次元』と呼ぶなら定数は c ひとつだけで、事態はさらに悪い。")

print()
print("="*72)
print("Block 2  残る自由度の正体: 1パラメータ・スケーリング群")
print("="*72)
lam = 3.7  # 任意
for L0, T0, M0 in [(1.0, 1.0, 1.0), (2.5, 0.3, 7.1)]:
    c0   = L0/T0
    rho0 = M0/L0**3
    Ls, Ts, Ms = lam*L0, lam*T0, lam**3*M0
    cs, rhos = Ls/Ts, Ms/Ls**3
    assert math.isclose(c0, cs, rel_tol=1e-12)
    assert math.isclose(rho0, rhos, rel_tol=1e-12)
    # 力の式 F = rho c^2 L^2 と F = M a が同じ倍率で動く（共変）ことを確認
    F1 = rho0*c0**2*L0**2 ; F2 = M0*(L0/T0**2)
    G1 = rhos*cs**2*Ls**2 ; G2 = Ms*(Ls/Ts**2)
    assert math.isclose(F1, F2, rel_tol=1e-12)
    assert math.isclose(G1, G2, rel_tol=1e-12)
    assert math.isclose(G1/F1, lam**2, rel_tol=1e-12)
print(f"  (L,T,M) -> ({lam}L, {lam}T, {lam}^3 M) で c も rho も不変、全式は共変。")
print("  => 『絶対単位系』は絶対ではなく、1パラメータ族。尺度は決まっていない。")

print()
print("="*72)
print("Block 3  (c, hbar, rho) なら閉じる")
print("="*72)
base3 = [DIM["c"], DIM["hbar"], DIM["rho"]]
sol = solve_exponents(base3, LEN)
print(f"  length = c^{sol[0]} * hbar^{sol[1]} * rho^{sol[2]}")
assert sol == [F(-1,4), F(1,4), F(-1,4)], sol
print("  => L = (hbar / (c*rho))^(1/4)   ... 長さが存在する")
for tgt, nm in [(MASS,"mass"), (TIME,"time")]:
    s = solve_exponents(base3, tgt)
    assert s is not None
    print(f"  {nm:6s} = c^{s[0]} * hbar^{s[1]} * rho^{s[2]}")

hbar = 1.054571817e-34   # J s
c    = 299792458.0       # m/s
print("\n  数値: rho の『単位の読み方』を変えると L がどう動くか")
print(f"  {'rho [kg/m^3]':>16s}  {'読み方':<22s}  {'L = (hbar/c rho)^1/4 [m]':>26s}")
rows = [(0.296,        "0.296 kg/m^3"),
        (296.0,        "0.296 g/cm^3"),
        (2.96e5,       "0.296 g/mm^3"),
        (0.296*2.3e17, "0.296 x 核密度")]
Ls = []
for r, tag in rows:
    Lv = (hbar/(c*r))**0.25
    Ls.append(Lv)
    print(f"  {r:16.4g}  {tag:<22s}  {Lv:26.4e}")
assert Ls[0] > Ls[1] > Ls[2] > Ls[3]
span_rho = rows[-1][0]/rows[0][0]
span_L   = Ls[0]/Ls[-1]
print(f"\n  rho を {span_rho:.3e} 倍動かすと L は {span_L:.4g} 倍しか動かない")
assert math.isclose(span_L, span_rho**0.25, rel_tol=1e-9)
print("  4乗根なので圧縮は効く(有利な点)。だが 5.9 pm と 33 pm は別の物理的主張であり、")
print("  『0.296 が何あたり何なのか』を言わない限り尺度は決まらない = 循環。")

print()
print("="*72)
print("Block 4  質量ゼロ電荷の円運動 + 角運動量量子化")
print("="*72)
m_e   = 9.1093837015e-31           # kg
lbar  = hbar/(m_e*c)               # reduced Compton wavelength
R_zbw = hbar/(2*m_e*c)
print(f"  E = M c^2, 速さ c で半径 R を回る -> J = (E/c^2) R c = M c R")
print(f"  J = hbar/2  =>  R = hbar/(2 M c) = lambdabar_C / 2")
print(f"  lambdabar_C(e) = {lbar:.6e} m")
print(f"  R_zbw(e)       = {R_zbw:.6e} m")
assert math.isclose(R_zbw, lbar/2, rel_tol=1e-12)
lbar_ref = 3.8615926796e-13
assert math.isclose(lbar, lbar_ref, rel_tol=1e-8), (lbar, lbar_ref)
T_orb = 2*math.pi*R_zbw/c
print(f"  周期 T = 2 pi R / c = {T_orb:.6e} s   (振動数 {1/T_orb:.6e} Hz)")
print("  => 質量が決まれば長さも時間も決まる。ただしこの関係式は hbar を必要とする。")
print("     すなわち軌道描像が供給する第3の定数は 37/125 ではなく hbar。")

print()
print("="*72)
print("Block 5  自己エネルギー模型は既に死んでいる（1881-1950s）")
print("="*72)
e     = 1.602176634e-19
eps0  = 8.8541878128e-12
r_cl  = e**2/(4*math.pi*eps0*m_e*c**2)
print(f"  古典電子半径 r_e = e^2/(4 pi eps0 m_e c^2) = {r_cl:.6e} m")
assert math.isclose(r_cl, 2.8179403262e-15, rel_tol=1e-8)
r_exp = 1e-20   # LEP 接触相互作用 Lambda > ~10 TeV から保守的に
print(f"  実験上限（LEP 接触相互作用 Lambda>10 TeV 相当）  r < ~{r_exp:.0e} m")
print(f"  乖離: {r_cl/r_exp:.3e} 倍 = {math.log10(r_cl/r_exp):.1f} 桁")
assert r_cl/r_exp > 1e5
print("  『電子の質量＝電荷の自己/軌道エネルギー』なら r ~ r_e でなければならない。")
print("  Abraham-Lorentz-Poincare のプログラムはここと 4/3 問題で破綻した。")

print()
print("="*72)
print("Block 6  決定的検証: 中性子は電荷ゼロなのに質量はほぼ同じ")
print("="*72)
m_p = 938.27208816   # MeV
m_n = 939.56542052   # MeV
d   = (m_n-m_p)/m_p
print(f"  m_p = {m_p} MeV, m_n = {m_n} MeV")
print(f"  差 = {m_n-m_p:.5f} MeV = {d*100:.4f} %")
assert abs(d) < 0.002
print(f"  中性子の正味電荷 = 0 (実験上限 |q_n|/e < 1e-21)")
print("  => 質量が『電荷の軌道エネルギー』なら中性子は質量を持てない。0.14% しか違わない。")
print("     電荷は質量の担い手ではない。")

print()
print("="*72)
print("Block 7  ただし『質量ゼロ構成子の閉じ込めエネルギー＝質量』自体は正しい")
print("="*72)
m_u, m_d = 2.16, 4.67          # PDG current quark masses [MeV]
sum_q = 2*m_u + m_d
print(f"  陽子(uud) のカレントクォーク質量和 = 2*{m_u} + {m_d} = {sum_q:.2f} MeV")
print(f"  陽子質量に占める割合 = {sum_q/m_p*100:.2f} %")
assert sum_q/m_p < 0.02
print(f"  => 陽子質量の {100-sum_q/m_p*100:.1f}% は構成子の静止質量ではない（グルーオン場＋運動エネルギー）")
print("  この描像が成り立っているのはハドロンであり、糊は色荷であって電荷ではない。")
print("  電子は逆に、質量が湯川結合由来の点粒子で、この描像に最も向かない粒子。")
y_e = math.sqrt(2)*0.51099895e-3/246.0   # m_e[GeV]/v[GeV]
assert 2.9e-6 < y_e < 3.0e-6
print(f"  電子の湯川結合 y_e = sqrt(2)*m_e/v, v=246 GeV -> y_e = {y_e:.3e}")

print()
print("="*72)
print("全ブロック assert 通過")
print("="*72)
