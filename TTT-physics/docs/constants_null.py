#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants_null.py -- 2026-09-13
「alpha^-1・ヒッグス質量・陽子電子質量比が語彙 {4,5,7,17,108,...} から精密に導出される」
という主張の検証

Block 1: 3つの標的の資格審査（次元を持つ量は標的になれない）
Block 2: ヒッグス質量 125 は GeV でしか現れない
Block 3: PDG 値は動いている（125.25 -> 125.20）
Block 4: 1836 = 108 x 17 は成立する。しかし mu = 1836.15267343(11)
Block 5: mu の帰無対照 — 語彙から整数 1836 に当たる確率
Block 6: 6 pi^5 = 1836.118（Lenz 1951）という先行例
Block 7: 内部矛盾 — Core=108 は今朝「出所なし」と自分で確定させた
"""
import math, itertools
from fractions import Fraction as Fr

print("="*78)
print("Block 1  3つの標的の資格審査")
print("="*78)
rows = [("alpha^-1",      "137.035999177(21)",  "無次元", "○ 標的になれる"),
        ("m_p/m_e",       "1836.15267343(11)",  "無次元", "○ 標的になれる"),
        ("ヒッグス質量",   "125.20(11) GeV",     "次元あり", "× 標的になれない")]
print(f"  {'量':<12s} {'値':<22s} {'次元':<8s} 判定")
for a,b,c,d in rows: print(f"  {a:<12s} {b:<22s} {c:<8s} {d}")
print("\n  9/13 に自分で確立した規律: 単位系は反証不能で、反証可能性は無次元量にしか宿らない。")
print("  次元を持つ量が『整数に見える』のは単位の選び方の結果であって、幾何学の結果ではない。")

print()
print("="*78)
print("Block 2  ヒッグス質量 125 は GeV でしか現れない")
print("="*78)
mH_GeV = 125.20
conv = [("GeV",           mH_GeV,                       ""),
        ("MeV",           mH_GeV*1e3,                   ""),
        ("eV",            mH_GeV*1e9,                   ""),
        ("kg",            mH_GeV*1.78266192e-27,        "1 GeV/c^2 = 1.78266192e-27 kg"),
        ("電子質量 m_e",   mH_GeV*1e9/0.51099895e6,      ""),
        ("陽子質量 m_p",   mH_GeV/0.93827208816,         ""),
        ("プランク質量",   mH_GeV/1.220890e19,           "m_Pl = 1.220890e19 GeV")]
print(f"  {'単位':<14s} {'ヒッグス質量の値':>20s}   備考")
for u,v,note in conv:
    print(f"  {u:<14s} {v:20.6g}   {note}")
print("\n  『125』が現れるのは GeV のときだけ。そして GeV は")
print("  ボルト（2019年以降 e, h, Delta_nu_Cs, c で固定）から作られた人間の約束であり、")
print("  セシウム原子の超微細遷移周波数を内部に抱えている。")
print("  => 『ヒッグス質量 = 125 = 5^3』は幾何学の主張ではなく、単位の偶然。")

print()
print("="*78)
print("Block 3  PDG 値は動いている")
print("="*78)
vals = [("PDG 2022", 125.25, 0.17), ("PDG 2024", 125.20, 0.11)]
for tag,v,u in vals: print(f"  {tag}: m_H = {v} +/- {u} GeV")
print(f"  中心値の移動 = {125.25-125.20:.2f} GeV")
print(f"  整数 125 とのずれ（PDG2024）= {125.20-125:.2f} GeV = {(125.20-125)/0.11:.1f} sigma")
print("  => 提示された 125.25 は既に旧値。動いている測定値に整数を当てるのは、")
print("     測定が精密化するたびに主張が壊れる構造。alpha のとき（0.6 sigma の式を持っている）")
print("     と正反対の作法になっている。")

print()
print("="*78)
print("Block 4  1836 = 108 x 17 は成立する。しかし mu は 1836 ではない")
print("="*78)
assert 108*17 == 1836
assert 1836 == 2**2 * 3**3 * 17
mu, mu_u = 1836.15267343, 0.00000011
print(f"  108 x 17 = {108*17}   （1836 = 2^2 x 3^3 x 17、算術は正確）")
print(f"  実測 m_p/m_e = {mu} ({mu_u})")
dev = mu-1836
print(f"  ずれ = {dev:.8f} = {dev/mu_u:.3e} sigma")
assert dev/mu_u > 1e6
print(f"  => {dev/mu_u/1e6:.2f} 百万 sigma。**137 = 125+12 と完全に同じ失敗の型**。")
print("     整数部（4桁）を当てても、11桁の定数のうち残り7桁には触れていない。")
print("     alpha のときに自分で書いた通り『中身は整数部でなく小数部にある』。")

print()
print("="*78)
print("Block 5  帰無対照 — 語彙から整数 1836 に当たる確率")
print("="*78)
V = [2,3,4,5,7,12,17,24,60,108,120,137]
hits = set()
# 2因子・3因子の積、および小さい有理係数倍
for r in (2,3):
    for combo in itertools.combinations_with_replacement(V, r):
        p = 1
        for x in combo: p *= x
        for num in range(1,13):
            for den in range(1,13):
                v = Fr(p*num, den)
                if v.denominator == 1 and 1000 <= v <= 3000:
                    hits.add(int(v))
print(f"  語彙 V = {V}")
print(f"  族: V の 2-3 個の積 x (p/q), p,q <= 12")
print(f"  [1000,3000] の 2001 整数のうち到達可能 = {len(hits)} = 密度 {len(hits)/2001*100:.1f}%")
assert 1836 in hits
reps = []
for r in (2,3):
    for combo in itertools.combinations_with_replacement(V, r):
        p=1
        for x in combo: p*=x
        for num in range(1,13):
            for den in range(1,13):
                if Fr(p*num,den) == 1836: reps.append((combo,num,den))
print(f"  1836 の表現数 = {len(reps)} 通り。例: " +
      ", ".join(f"{'x'.join(map(str,c))}" + (f" x{n}/{d}" if (n,d)!=(1,1) else "") for c,n,d in reps[:6]))
print(f"\n  => 密度 {len(hits)/2001*100:.1f}% の族で特定の整数に当たっても情報にならない。")
print("     108 のとき(1.10%)・137 のとき(5.45%) と比べても**桁違いに緩い**。")

print()
print("="*78)
print("Block 6  先行例 — 6 pi^5 = 1836.118（Lenz 1951, Phys. Rev. 82, 554）")
print("="*78)
lenz = 6*math.pi**5
print(f"  6 pi^5 = {lenz:.6f}   実測 {mu}")
print(f"  ずれ = {lenz-mu:+.6f} = {abs(lenz-mu)/mu_u:.2e} sigma  （相対 {abs(lenz-mu)/mu:.2e}）")
print(f"  比較: 108 x 17 = 1836 のずれ = {dev/mu_u:.2e} sigma  （相対 {dev/mu:.2e}）")
assert abs(lenz-mu) < dev
print(f"\n  => **Lenz の 6 pi^5 の方が 108x17 より {dev/abs(lenz-mu):.1f} 倍精度が高い**。")
print("     そして 6 pi^5 は m_p/m_e 数秘術の教科書的な失敗例として1951年から知られている。")
print("     より粗い一致を新規の導出として出すと、この系譜に即座に分類される。")

print()
print("="*78)
print("Block 7  内部矛盾 — Core=108 は今朝『出所なし』と自分で確定させた")
print("="*78)
print("  9/13 の記録（v0.2 §9「108 の三重の閉鎖」）:")
print("   (a) 24 は 108 を割らず、Klein 分類にも 2T の数え上げ不変量にも 108 は無い")
print("   (b) 3-smooth 骨格: 108=2^2 3^3 も 972 も 110592 も 995328 も等しく『説明』でき区別しない")
print("       -> 群論が実際に制約しているのは 35=5x7 だけ")
print("   (c) 27 分割の中心に反転四面体が座り、双極公理と矛盾する")
print("  さらに v0.2 §0 の未達成5点に『108 は出所なし』を明記済み。")
print("\n  => 『Core=108 を含む完全固定語彙から諸定数が精密に導出される』は、")
print("     **今朝の自分の結論と正面から矛盾する**。108 自体が導出されていない。")
print("     導出されていない語で書いた導出は導出ではない。")

print()
print("="*78)
print("全ブロック assert 通過")
print("="*78)
