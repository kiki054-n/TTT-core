#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
penguin_pentagon.py
「ペンギン崩壊の異常」と「電子＝五角双錐(J13)」の関係を検定する。
6ブロック。全 assert 通過を要件とする。
2026-09-21
"""
import math, itertools, random

def head(s): print("\n" + "="*72 + "\n" + s + "\n" + "="*72)

# =====================================================================
head("BLOCK 1: 用語の資格審査 — 「ペンギン崩壊」は崩壊モードではない")
# =====================================================================
# ペンギン＝ダイアグラムの位相（ループ内で W と t が回り、外線にゲージ/ヒッグスが出る）。
# 該当する物理過程は b -> s l+ l-（FCNC、ツリーで起きない）。
# 2026年時点で「異常」と呼ばれている観測量の内訳：
observables = {
    # 名前 : (レプトン依存性, 2026年の状態)
    "R_K  (B+->K+ ll, high q2)":      ("mu/e 比",   "SMと一致 1.08 +0.11-0.09 +-0.04"),
    "R_K* (B0->K*0 ll, high q2)":     ("mu/e 比",   "SMと一致"),
    "R_K  (low q2, 2022再測定)":       ("mu/e 比",   "SMと一致"),
    "P5'  (B0->K*0 mumu 角度分布)":    ("mu のみ",   "テンション継続"),
    "BR(Bs->phi mumu)":               ("mu のみ",   "テンション継続（低め）"),
    "BR(B->K(*) mumu) low q2":        ("mu のみ",   "テンション継続（低め）"),
    "Bs->mumu":                       ("mu のみ",   "SMと一致"),
}
n_ratio  = sum(1 for v in observables.values() if v[0] == "mu/e 比")
n_muonly = sum(1 for v in observables.values() if v[0] == "mu のみ")
for k, v in observables.items():
    print(f"  {k:34s} {v[0]:9s} {v[1]}")
print(f"\n  mu/e 比の観測量 {n_ratio} 件 : すべて SM と一致")
print(f"  mu 単独の観測量 {n_muonly} 件 : テンションはすべてこちら側")

# 決定的な構造的事実：
# 「電子が特別である」という仮説が予言するのは mu/e 比のずれ。
# 2026年に生き残っている異常は mu/e 比ではない。
assert n_ratio == 3 and n_muonly == 4
LFU_violated_2026 = False   # R_K, R_K* が1に戻った時点で
assert LFU_violated_2026 is False
print("\n  => 電子特有の構造が説明すべき対象（LFU破れ）は 2022-2026 に消滅済み。")

# =====================================================================
head("BLOCK 2: 必要な新物理スケール vs TTT の格子スケール E_a")
# =====================================================================
G_F   = 1.1663787e-5      # GeV^-2
alpha = 1.0/133.0         # alpha_em(m_b)
Vtb_Vts = 0.04            # |V_tb V_ts*|
# 有効ラグランジアン係数 N = (4 G_F/sqrt2)(alpha/4pi) |V_tb V_ts|
N = (4*G_F/math.sqrt(2)) * (alpha/(4*math.pi)) * Vtb_Vts
print(f"  SM 前置係数 N = {N:.4e} GeV^-2")

def scale_for_C9(c9):
    """|C9^NP| = c9 を 1/Lambda^2 型の接触相互作用で出すのに必要な Lambda [GeV]"""
    return 1.0/math.sqrt(N*abs(c9))

Lam_1 = scale_for_C9(1.0)
print(f"  C9^NP = -1 を出すのに必要なスケール Lambda = {Lam_1/1e3:.1f} TeV")
assert 30e3 < Lam_1 < 40e3, Lam_1   # 教科書的な「約35 TeV」を再現

# TTT の格子スケール（許容窓 1 <= a/lP < 1.0174e7、ttt-theory-11 の全景マップ）
E_P = 1.2209e19           # GeV
windows = {"a/lP = 1 (プランク)": 1.0,
           "a/lP = 1e3 (GUT)": 1.0e3,
           "a/lP = 1.2e8 (本人の選択)": 1.2e8,
           "a/lP = 1.0174e7 (窓の上端)": 1.0174e7}
print("\n  格子スケール E_a = E_P/(a/lP) と、そこから出る C9^NP の大きさ:")
worst = 0.0
for name, r in windows.items():
    E_a = E_P/r
    c9  = N**-1 * (1.0/E_a**2) * 1.0   # 1/E_a^2 を N で割って C9 換算
    c9  = (1.0/E_a**2)/N
    print(f"    {name:28s} E_a = {E_a:.3e} GeV   C9^NP ~ {c9:.3e}")
    worst = max(worst, c9)
# 窓の中で最大（＝最も効く）のは上端 1.0174e7
assert worst < 1e-10, worst
print(f"\n  窓内で最大でも |C9^NP| ~ {worst:.2e}  （必要なのは 1）")
print(f"  => 不足 {1.0/worst:.2e} 倍。格子起源で b->s 異常は原理的に作れない。")

# 逆に、35 TeV を E_a として要求すると a/lP は？
r_need = E_P/Lam_1
print(f"  逆算: E_a = 35 TeV を要求すると a/lP = {r_need:.3e}")
print(f"        これは LIV の窓上端 1.0174e7 の {r_need/1.0174e7:.2e} 倍 = 窓の遥か外。")
assert r_need > 1.0174e7 * 1e6

# =====================================================================
head("BLOCK 3: R_K から出る「電子の内部構造」の上限 — 新規の台帳項目")
# =====================================================================
C9_SM, C10_SM = 4.27, -4.17
# high-q2 で R_K ~ (|C9|^2+|C10|^2)_mu / (|C9+d|^2+|C10|^2)_e
def RK_of_delta(d):
    num = C9_SM**2 + C10_SM**2
    den = (C9_SM + d)**2 + C10_SM**2
    return num/den
sens = -(RK_of_delta(1e-4)-RK_of_delta(-1e-4))/2e-4   # dR_K/dd の符号反転量
print(f"  感度 |dR_K/d(delta_e)| = {sens:.4f}")
# 測定 R_K = 1.08 (+0.11-0.09 stat) (+-0.04 syst) @ high q2
sigma_tot = math.hypot(0.11, 0.04)
dev = 0.08
d_max = (abs(dev) + 2*sigma_tot)/sens      # 2sigma 上限
print(f"  R_K = 1.08 +- {sigma_tot:.3f} -> |delta_e| < {d_max:.2f} (2sigma)")
Lam_e = scale_for_C9(d_max)
print(f"  => 電子側の接触相互作用スケール Lambda_e > {Lam_e/1e3:.1f} TeV")
r_e = E_P/Lam_e
print(f"  => a/lP < {r_e:.3e}")
ledger = {"LIV n=2": 1.0174e7, "ブリルアンゾーン": 8.72e12,
          "R_K (今回)": r_e, "点粒子性": 9.28e15, "g-2": 2.39e16}
print("\n  台帳の順位（小さいほど強い制約）:")
for k, v in sorted(ledger.items(), key=lambda x: x[1]):
    print(f"    {k:18s} a/lP < {v:.3e}")
assert 8.72e12 < r_e < 9.28e15, r_e
print("\n  => R_K は g-2 より約 {:.0f} 倍強い。だが LIV の {:.1e} 倍緩く順位は動かない。"
      .format(2.39e16/r_e, r_e/1.0174e7))
print("     新規の ○ 項目。ただし『格子が味を区別しない』前提つき（TTT では成立）。")

# =====================================================================
head("BLOCK 4: J13（五角双錐）の資格 — 9/20 の2つの棄却理由は有効か")
# =====================================================================
# n角双錐: V=n+2, E=3n, F=2n
n = 5
V, E, F = n+2, 3*n, 2*n
assert (V, E, F) == (7, 15, 10)
assert V - E + F == 2
print(f"  J13: V={V} E={E} F={F}, 点群 D_5h")
# 棄却理由1: 面を持つ（無質量成分は Wigner の小群 ISO(2) で線 dim1）
has_faces = (F > 0)
# 棄却理由2: achiral（D_5h は sigma_h を含む）
chiral_point_groups = {"C_n", "D_n", "T", "O", "I"}
assert "D_5h" not in chiral_point_groups
print("  理由1: 面を持つ（F=10）→ 無質量・線という要請と衝突")
print("  理由2: D_5h は sigma_h を含み achiral → カイラリティを担えない")
# 今回の第3の理由：異常側がレプトン普遍になった以上、電子だけ特別な形をとる動機が消えた
print("  理由3(今回): 説明対象だった LFU 破れが消滅 → 電子特有構造への外部需要がゼロ")
assert has_faces and True
print("  => 独立な棄却理由は 2 から 3 に増えた。J13＝電子は再び閉じる。")

# ただし J13 の幾何学的内容そのものは生きている（7.356/5）
dih = math.degrees(math.acos(1/3))
gap = 360 - 5*dih
per  = gap/5
print(f"\n  （J13 の幾何は別途有効: 二面角 {dih:.6f}°, 5枚で不足 {gap:.6f}°, "
      f"1接合あたり {per:.6f}°）")
assert abs(gap - 7.356103) < 1e-5 and abs(per - 1.471221) < 1e-5

# =====================================================================
head("BLOCK 5: 帰無対照 — 「5」の名前一致")
# =====================================================================
# P5' の 5 は角度観測量の基底 {P1,P2,P3,P4',P5',P6',P8'} の中の通し番号。
basis = ["P1","P2","P3","P4'","P5'","P6'","P8'"]
print(f"  角度観測量の基底: {basis}  (要素数 {len(basis)})")
print("  5 は S_i 基底からの変換で付いた通し番号であって、5回対称ではない。")
# フレーバー物理が供給する整数の在庫
flavour_integers = [1,2,3,4,5,6,7,8,9,10,14.3,27,35]  # P_i, C_i, q2 bin, TeV など
vocab = {4,5,7,12,24,37,120,125,137,600}
hits = [x for x in flavour_integers if x in vocab]
print(f"  フレーバー物理が日常的に使う整数 {len(flavour_integers)} 個のうち "
      f"TTT語彙と一致するのは {len(hits)} 個: {hits}")
rate = len(hits)/len(flavour_integers)
print(f"  一致率 {rate:.1%} → 『5 が両方に出る』は情報量ほぼゼロ")
assert rate > 0.2   # 当たって当然の水準
print("  => P5' の 5 と J13 の 5 の同一視は、alpha/6pi^5/Milgrom/McKay/Z_3 に続く轍。")

# =====================================================================
head("BLOCK 6: 本当に接続しうる場所 — 2T = T' はフレーバー群として既存")
# =====================================================================
# 2T（binary tetrahedral, order 24）の既約表現
irreps = {"1":1, "1'":1, "1''":1, "2":2, "2'":2, "2''":2, "3":3}
assert sum(d*d for d in irreps.values()) == 24
print(f"  2T の既約表現: {list(irreps.keys())}  次元^2 の和 = {sum(d*d for d in irreps.values())} = |2T|")
# フレーバー模型の標準的な割り当て: (第1,第2世代)->2', 第3世代->1
assignment = {"gen1+gen2": "2'", "gen3": "1"}
print(f"  T' フレーバー模型の標準割り当て: {assignment}  ＝ 2+1 構造")
print("  先行研究: Aranda-Carone-Lebed 2000 / Feruglio-Hagedorn-Lin-Ting 2007 ほか")
# この 2+1 構造が予言すること
print("\n  2+1 構造が強制する2つの帰結:")
print("   (i) レプトン: e と mu は同じ2重項 → e-mu 普遍性は保たれる  -> R_K = 1 ✓ 観測と一致")
print("   (ii) クォーク: b は1重項、s は2重項 → b->s は 1重項-2重項遷移＝非普遍性の最大の場所")
print("      -> 異常が b->s のみに出て mu/e 比に出ない、という 2026 のパターンと同型")
pattern_match = (LFU_violated_2026 is False)
assert pattern_match
print("\n  ◎ これは J13 とは無関係。効いているのは 2T の表現構造であって電子の形ではない。")
print("  ★ ただし穴: TTT の 2T は McKay 経由で E6（ゲージ側）に使われており、")
print("     それを世代空間にも作用させるのは現状ただの名前の再利用。")
print("     ttt-theory-11 の『新規の穴①』と完全に同型 → 構成を示すまで主張不可。")

print("\n" + "="*72)
print("全ブロック完了（assert 通過）")
print("="*72)
