#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
orbit_137.py -- 2026-09-13
「重力の撤廃＝軌道」「電子＝無質量光速粒子の閉じた軌道」「137 = 125 + 12」の検証

Block 1: alpha^-1 は 137 ではない（1.7e6 sigma）。TTT 自身の式との自己矛盾
Block 2: a0 = lambdabar_C / alpha は alpha の定義の書き換え（情報量ゼロ）
Block 3: 137 = 125 + 12 の帰無対照
Block 4: 12 は2回使われて相殺する（自由整数1個）
Block 5: ループ半径は一意でない（量子化条件の選び方で 2 倍動く）
Block 6: 決定的 — 単一ループは g=1 を強制する。実測 g=2.00231930436
Block 7: サイズ — ループ半径 3.86e-13 m は点粒子性の実験限界を 5-7 桁超える
Block 8: 一般相対論は既に重力を幾何にしている（しかも定量予言つき）
"""
import math
from fractions import Fraction as Fr

print("="*74)
print("Block 1  alpha^-1 は 137 か")
print("="*74)
ainv_exp = 137.035999177      # CODATA 2022
ainv_unc = 0.000000021
dev  = ainv_exp - 137.0
sig  = dev/ainv_unc
print(f"  実測      alpha^-1 = {ainv_exp:.9f} ({ainv_unc:.0e})")
print(f"  提案      alpha^-1 = 137 = 125 + 12")
print(f"  ずれ      = {dev:.9f}  = {sig:.3e} sigma")
assert sig > 1e6
print(f"  => 実験誤差の {sig/1e6:.2f} 百万倍。整数 137 は alpha ではない。")

ttt = 137 + Fr(35831, 995328)
ttt_f = float(ttt)
print(f"\n  TTT 自身の式  137 + 35831/995328 = {ttt_f:.9f}")
print(f"    実測との差 = {ttt_f-ainv_exp:+.3e} = {(ttt_f-ainv_exp)/ainv_unc:+.2f} sigma")
assert abs((ttt_f-ainv_exp)/ainv_unc) < 1.0
assert 995328 == 2**12 * 3**5
print("  => TTT の既存の式は 0.6 sigma 以内。**新提案はそれを捨てて 1.7e6 sigma へ戻る**")
print("     alpha の中身は整数部 137 ではなく小数部 0.035999... にある。")
print("     既記録: 約分後は (素数 35831)/(3-smooth 995328)。導出すべきは 35831。")

print()
print("="*74)
print("Block 2  a0 = lambdabar_C / alpha は「発見」か「定義の書き換え」か")
print("="*74)
hbar=1.054571817e-34; c=299792458.0; me=9.1093837015e-31
e=1.602176634e-19; eps0=8.8541878128e-12
alpha = e**2/(4*math.pi*eps0*hbar*c)
lbar  = hbar/(me*c)
a0    = 4*math.pi*eps0*hbar**2/(me*e**2)
print(f"  alpha (e,eps0,hbar,c から)   = {alpha:.12e}   1/alpha = {1/alpha:.9f}")
assert abs(1/alpha - ainv_exp) < 1e-5
print(f"  lambdabar_C = hbar/(me c)    = {lbar:.6e} m")
print(f"  a0          = 4pi eps0 hbar^2/(me e^2) = {a0:.6e} m")
print(f"  a0 * alpha / lambdabar_C     = {a0*alpha/lbar:.15f}")
assert abs(a0*alpha/lbar - 1.0) < 1e-12
print("  => 恒等式。a0 の定義に alpha の定義を代入しただけで、比が 1/alpha なのは自明。")
print("     『原子軌道半径は内部半径の約137倍』は alpha^-1≈137 の言い換えであり、")
print("     新しい情報はゼロ。したがって §1 の全内容は §2 の主張に還元される。")

print()
print("="*74)
print("Block 3  137 = n^3 + g の帰無対照")
print("="*74)
groups = {4:"四面体頂点", 6:"八面体頂点/立方体面", 8:"立方体頂点", 12:"|T| 正四面体回転群/正20面体頂点",
          20:"正12面体頂点", 24:"|O|, 24-cell 頂点", 30:"辺数", 48:"|2O|,|W(T)|", 60:"|I|", 120:"|2I|"}
ns = range(2, 13)
vals = {}
for n in ns:
    for g in groups:
        v = n**3 + g
        if v <= 2000:
            vals.setdefault(v, []).append((n, g))
print(f"  族: n^3 (n=2..12) + g, g in {sorted(groups)}  -> 2000以下に {len(vals)} 値"
      f" = 密度 {len(vals)/2000*100:.2f}%")
print(f"  137 の表現: {vals.get(137)}")
assert 137 in vals
print(f"  比較: 108 のときの族(V x n^3)は密度 1.10%。今回は {len(vals)/2000*100:.2f}% で**より緩い**")
print("  さらに 137 は素数なので分解の族は後から幾らでも書ける。実例:")
for label, expr in [("2^7 + 3^2 (TTT 自身の 128/9)", 128+9),
                    ("11^2 + 4^2 (2平方和・素数なので一意)", 121+16),
                    ("125 + 12 (今回の提案)", 125+12),
                    ("60 + 48 + 24 + 4 + 1", 60+48+24+4+1),
                    ("|2I| + |2O| - 24 - 7", 120+48-24-7)]:
    assert expr == 137
    print(f"    137 = {label}")
print("  => 族が提案の後に書かれている以上、帰無対照を自分で供給できない（108 と同じ構造）")

print()
print("="*74)
print("Block 4  12 は2回使われ、関係式から相殺する")
print("="*74)
print("  提案: 37 = 5^2 + 12,  137 = 5^3 + 12")
assert 5**2 + 12 == 37 and 5**3 + 12 == 137
print(f"  差: 137 - 37 = {137-37} = 5^3 - 5^2 = {5**3-5**2}")
assert 137-37 == 5**3-5**2 == 100
print("  => 12 は両辺から消える。2つの主張を結ぶ関係に 12 は寄与していない。")
print("     自由整数は実質1個（12）で、それを2箇所に置いただけ。")
print("  注: 12 自体には TTT 内に正当な居場所がある（|T|=12、9/13 の『forced な版は12』）。")
print("     しかし 125 と 25 の出所である a=5 には居場所がない。")
print("     群の位数（12）とスケール由来の数（125）を足す操作は、")
print("     9/13 に自分で棄却した『0-セル数と体積を掛ける』と同じ次元不整合。")

print()
print("="*74)
print("Block 5  ループ半径は一意に決まらない")
print("="*74)
R_J   = hbar/(2*me*c)     # 角運動量 J = hbar/2 から
R_w   = hbar/(me*c)       # E = hbar*omega, omega = c/R から
print(f"  条件 J = hbar/2      -> R = lambdabar_C/2 = {R_J:.6e} m")
print(f"  条件 E = hbar c / R  -> R = lambdabar_C   = {R_w:.6e} m")
assert math.isclose(R_w/R_J, 2.0, rel_tol=1e-12)
print(f"  比 = {R_w/R_J:.1f}")
print("  => どちらの量子化条件を課すかで 2 倍動く。ループ描像は半径を一意に決めない。")
print("     『幾何学的に逆算・導出できる』とは言えない（因子 2 が自由）。")

print()
print("="*74)
print("Block 6  決定的 — 単一ループは g=1 を強制する")
print("="*74)
muB = e*hbar/(2*me)
def loop(R):
    I   = e*c/(2*math.pi*R)      # 電流
    mu  = I*math.pi*R**2         # = e c R / 2
    J   = me*c*R                 # (E/c^2) * R * c
    g   = mu/((e/(2*me))*J)
    return mu, J, g
for tag, R in [("R = lambdabar_C/2  (J を合わせる)", R_J),
               ("R = lambdabar_C    (mu を合わせる)", R_w)]:
    mu, J, g = loop(R)
    print(f"  {tag}")
    print(f"     mu = {mu:.6e} J/T  = {mu/muB:.4f} muB     J = {J/hbar:.4f} hbar     g = {g:.4f}")
mu1,J1,g1 = loop(R_J); mu2,J2,g2 = loop(R_w)
assert math.isclose(g1, 1.0, rel_tol=1e-12) and math.isclose(g2, 1.0, rel_tol=1e-12)
assert math.isclose(J1/hbar, 0.5, rel_tol=1e-12)
assert math.isclose(mu2/muB, 1.0, rel_tol=1e-12)
g_exp = 2.00231930436256
print(f"\n  ループ模型の g = 1（半径に依らず恒等的に。R が約分で消える）")
print(f"  実測        g = {g_exp:.14f}   （13桁で確定、物理学最高精度の検証量）")
print(f"  ずれ = 因子 {g_exp/1.0:.5f}")
print("  => 半径を J に合わせると mu が半分、mu に合わせると J が倍。両立しない。")
print("     これは Dirac 方程式が必要になった理由そのもの。古典ループ模型は g=1 で死ぬ。")
print("     TTT が電子ループを主張するなら、g=2 をどう出すかが最初の関門。")

print()
print("="*74)
print("Block 7  サイズ — ループ半径 vs 点粒子性の実験限界")
print("="*74)
r_cl = e**2/(4*math.pi*eps0*me*c**2)
r_lim = 1e-20
print(f"  提案のループ半径 lambdabar_C = {lbar:.4e} m")
print(f"  古典電子半径     r_e         = {r_cl:.4e} m   ({lbar/r_cl:.1f} 倍小さい)")
print(f"  実験上限（LEP 接触相互作用）  < {r_lim:.0e} m")
print(f"  乖離 = {lbar/r_lim:.2e} 倍 = {math.log10(lbar/r_lim):.1f} 桁")
assert lbar/r_lim > 1e7
print("  => 電荷が半径 3.9e-13 m の環を実際に回っているなら、LEP の e+e- 散乱に")
print("     形状因子が見えるはず。見えていない（純粋な点状 QED）。")

print()
print("="*74)
print("Block 8  一般相対論は 1915 年に既に重力を『力』でなくしている")
print("="*74)
rows = [("水星近日点移動", "42.98 arcsec/世紀", "観測 42.98 +/- 0.04"),
        ("太陽縁の光の曲がり", "1.7512 arcsec", "VLBI で 1e-4 精度"),
        ("Shapiro 遅延", "Cassini gamma-1 < 2.3e-5", "確認"),
        ("重力波", "GW150914 以降 100+ 事象", "確認"),
        ("フレームドラッギング", "Gravity Probe B / LAGEOS", "確認")]
print(f"  {'GR の予言':<22s} {'値':<28s} {'状況'}")
for a,b,cc in rows: print(f"  {a:<22s} {b:<28s} {cc}")
print("\n  『引力ではなく軌道に沿った運動』＝GR の測地線そのもの。新しい主張ではない。")
print("  GR が持ち、提案が持たないもの: 場の方程式（軌道を決める式）と上表の定量予言。")
print("  したがって提案は GR より**弱い**（同じ絵で、予言だけがない）。")
print("\n  さらに表の破綻: 提案は「開いた軌道＝質量0＝空間を歪めない」とするが、")
print("  光は重力源であり(応力エネルギーテンソルに入り)、実際に曲がり・曲げる。")
print("  『閉じた軌道だけが重力を作る』は光の重力を説明できない。")

print()
print("="*74)
print("全ブロック assert 通過")
print("="*74)
