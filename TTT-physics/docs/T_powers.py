#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T_powers.py -- 2026-09-13
「すべては時間 T の冪に還元される」という一元化主張の検証

Block 1: 指数の帳尻は合っている（内部整合の確認）
Block 2: 既出 — 自然単位系(hbar=c=1)とプランク単位系。表の「4次元＝作用」の空席が hbar
Block 3: 決定的 — 質量の指数が2つあり衝突する（[T^3] vs [T^-1]）。一致するのは1点だけ
Block 4: M ∝ L^3 は「宇宙のあらゆる物質が同じ密度」を意味する。実測は 44 桁の幅
Block 5: 素粒子では質量と大きさは反比例（コンプトン）。3乗どころか符号が逆
Block 6: 尺度を粒子で決めると rho_M は粒子ごとに 13 桁違う
"""
import math
from fractions import Fraction as Fr

hbar=1.054571817e-34; c=299792458.0
me=9.1093837015e-31; mp=1.67262192369e-27
hbarc_MeVfm = 197.3269804

print("="*76)
print("Block 1  T の冪の帳尻（内部整合の確認）")
print("="*76)
# c=1, rho_M 無次元 とした場合の T 指数
n = {"時間":1, "長さ":1}
n["体積"]      = 3*n["長さ"]
n["質量"]      = n["体積"]                      # M = rho L^3
n["速度"]      = n["長さ"] - n["時間"]
n["加速度"]    = n["長さ"] - 2*n["時間"]
n["力"]        = n["質量"] + n["加速度"]
n["エネルギー"] = n["力"] + n["長さ"]
n["運動量"]    = n["質量"] + n["速度"]
n["作用"]      = n["エネルギー"] + n["時間"]
n["角運動量"]  = n["運動量"] + n["長さ"]
n["電荷"]      = Fr(1,2)*n["質量"] + Fr(3,2)*n["長さ"] - n["時間"]   # ガウス系
print(f"  {'量':<12s} {'T の冪':>8s}   提案の主張")
claim = {"時間":1,"長さ":1,"質量":3,"力":2,"エネルギー":3,"作用":4}
for k,v in n.items():
    tag = f"[T^{claim[k]}] と一致" if k in claim and v==claim[k] else ""
    print(f"  {k:<12s} {str(v):>8s}   {tag}")
for k,v in claim.items(): assert n[k]==v, (k,n[k],v)
assert n["電荷"] == n["力"] == 2
assert n["角運動量"] == n["作用"] == 4
print("\n  => 帳尻は完全に合っている。電荷と力がともに [T^2]、角運動量と作用がともに [T^4]。")
print("     alpha = e^2/(hbar c) の次元 = T^4/T^4 = T^0 も無次元で通る。ここに誤りはない。")

print()
print("="*76)
print("Block 2  既出 — これは自然単位系そのもの。表の空席が hbar")
print("="*76)
rows = [("時間",1,-1,0),("長さ",1,-1,0),("質量",3,1,0),("力",2,2,0),
        ("エネルギー",3,1,0),("作用",4,0,0)]
print(f"  {'量':<12s} {'提案 (c=1, rho=1)':>18s} {'自然単位 (hbar=c=1)':>20s} {'プランク (hbar=c=G=1)':>22s}")
for q,a,b,d in rows:
    print(f"  {q:<12s} {'T^'+str(a):>18s} {'E^'+str(b):>20s} {'純粋な数':>22s}")
print("\n  自然単位系では **作用 = E^0 = 無次元**。hbar を 1 と置いたから。")
print("  提案では **作用 = T^4 ≠ 無次元**。hbar を置いていないから。")
print("  => 提案の表の『4次元＝作用（J·s）』という空席に入る定数がちょうど hbar。")
print("     T^4 の枠に定数が座れば T が固定される＝9/13 前note の結論と同一。")
print("     提案の表は、自分の穴を自分で図示している。")
print("\n  文献: Duff, Okun, Veneziano, 'Trialogue on the number of fundamental")
print("        constants', JHEP 0203 (2002) 023 [physics/0110060]")
print("        — 基本定数の数が 0 か 2 か 3 かを3人が論争した論文。")
print("        『単位は人間の約束にすぎない』は Duff の立場そのもので、既に主流の議論。")

print()
print("="*76)
print("Block 3  決定的 — 質量の指数が2つあり、衝突する")
print("="*76)
print("  (i) rho_M から:  M = rho L^3          -> [M] = [T^3]")
print("  (ii) hbar から:  M = hbar/(c^2 T)     -> [M] = [T^-1]   (提案自身が E=hbar*omega で使用)")
print("  両立するのは T^3 = T^-1、すなわち T^4 = 一定 の**ただ1点**のみ。")
rho_readings = [(0.296,"0.296 kg/m^3"),(296.0,"0.296 g/cm^3"),(2.96e5,"0.296 g/mm^3")]
print(f"\n  {'rho の読み':<16s} {'T* [s]':>13s} {'L* [m]':>13s} {'M* [kg]':>13s} {'M*/m_e':>12s}")
for r,tag in rho_readings:
    L = (hbar/(c*r))**0.25
    T = L/c
    M1 = r*L**3          # rho L^3
    M2 = hbar/(c**2*T)   # hbar/(c^2 T)
    assert math.isclose(M1,M2,rel_tol=1e-9), (M1,M2)
    print(f"  {tag:<16s} {T:13.4e} {L:13.4e} {M1:13.4e} {M1/me:12.4f}")
print("\n  => 2つの質量定義が一致するのは各読みにつき1点だけ。**その1点でしか理論は正しくない**。")
print("     しかもその質量は電子でも陽子でもなく、rho の単位の読み方で変わる。")

print()
print("="*76)
print("Block 4  M ∝ L^3 は『万物が同じ密度』を意味する")
print("="*76)
dens = [("銀河間物質",1e-27),("空気(海面)",1.225),("水",1000.0),("地球(平均)",5514.0),
        ("太陽(平均)",1408.0),("金",19300.0),("白色矮星",1e9),("中性子星/核物質",2.3e17)]
print(f"  {'対象':<16s} {'密度 [kg/m^3]':>16s}")
for a,b in dens: print(f"  {a:<16s} {b:16.3e}")
span = dens[-1][1]/dens[0][1]
print(f"\n  幅 = {span:.2e} = {math.log10(span):.0f} 桁")
assert math.log10(span) > 40
print("  => 普遍的な質量／体積比 rho_M = 37/125 は、宇宙の全物質が同一密度であることを要求する。")
print("     実測は 44 桁の幅。これは調整で埋まる差ではない。")
print("     逃げ道（L を物体の実サイズでないと言う）を採ると rho_M は密度でなくなり、")
print("     M = rho L^3 は何も主張しない式になる。どちらでも落ちる。")

print()
print("="*76)
print("Block 5  素粒子では質量と大きさは反比例する（3乗ではなく符号が逆）")
print("="*76)
parts = [("電子",0.51099895),("ミューオン",105.6583755),("陽子",938.27208816),("W ボソン",80377.0)]
print(f"  {'粒子':<10s} {'m c^2 [MeV]':>14s} {'lambdabar_C [m]':>16s}")
lam = {}
for nm,E in parts:
    l = hbarc_MeVfm/E*1e-15
    lam[nm]=l
    print(f"  {nm:<10s} {E:14.5f} {l:16.4e}")
r_m = 938.27208816/0.51099895
r_l = lam["電子"]/lam["陽子"]
print(f"\n  陽子/電子 の質量比   = {r_m:.2f}")
print(f"  電子/陽子 の大きさ比 = {r_l:.2f}   ← 質量比とぴたり一致（反比例）")
assert math.isclose(r_m, r_l, rel_tol=1e-4)
print(f"  提案 M ∝ L^3 の予言: 大きさ比 = {r_m**(1/3):.2f} 倍、しかも**重い方が大きい**")
print(f"  => 向きが逆で、倍率も {r_m*r_m**(1/3):.0f} 倍ずれる。")
print("     自然単位系で [M]=E^1, [L]=E^-1 と符号が逆なのはこの事実の反映。")
print("     提案は [M]=[L^3] と同符号にしたので、素粒子のスケール則と真っ向から衝突する。")

print()
print("="*76)
print("Block 6  尺度を粒子で決めると rho_M は粒子ごとに桁違い")
print("="*76)
print("  L = (hbar/(c rho))^(1/4) を逆に解く:  rho = hbar/(c L^4)")
print(f"  {'粒子':<10s} {'L = lambdabar_C [m]':>20s} {'要求される rho [kg/m^3]':>26s}")
rhos=[]
for nm,_ in parts:
    L=lam[nm]; r = hbar/(c*L**4); rhos.append(r)
    print(f"  {nm:<10s} {L:20.4e} {r:26.4e}")
sp = rhos[-1]/rhos[0]
print(f"\n  幅 = {sp:.3e} = {math.log10(sp):.1f} 桁")
assert math.log10(sp) > 15
print("  => rho_M は普遍定数になれない。粒子ごとに要求値が違う（電子と W で "
      f"{math.log10(sp):.0f} 桁）。")
print("     『37/125 が普遍的比重』という前提はここで完全に閉じる。")

print()
print("="*76)
print("全ブロック assert 通過")
print("="*76)
