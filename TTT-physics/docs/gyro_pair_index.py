"""
TTT 検算 2: 柔らかい±ジャイロ対の「遅くなる効果」を屈折率として読めるか
連続体極限: K = I v0^2 k^2。和 S=psi_a+psi_b, 差 D=psi_a-psi_b で分離すると
  (-I w^2 + K) S - L w D = 0
  (-I w^2 + K + 2 kin) D - L w S = 0
→ 厳密な分散関係: (K - I w^2)(K - I w^2 + 2 kin) = L^2 w^2
"""
import numpy as np
I, v0, L, kin = 1.0, 1.0, 1.0, 10.0
w0 = np.sqrt(2*kin/I)      # 対の内部振動(差モード)の固有振動数
wp = L/I                   # ジャイロ振動数

def k_of_w(w, Lp=L, Lm=-L):
    # 一般形 (L+ , L-): 2x2 を直接解いて k^2 を求める
    # [[K+kin - I w^2 - Lp w, -kin], [-kin, K+kin - I w^2 - Lm w]] の行列式=0 を K について解く
    A = kin - I*w**2 - Lp*w
    B = kin - I*w**2 - Lm*w
    # (K+A)(K+B) - kin^2 = 0
    disc = (A-B)**2 + 4*kin**2
    Ks = [(-(A+B) + np.sqrt(disc))/2, (-(A+B) - np.sqrt(disc))/2]
    return [Kx/(I*v0**2) for Kx in Ks]   # k^2 候補

def n2_exact(w):
    k2 = max(k_of_w(w))           # 伝播する枝(光的な枝)
    return k2*v0**2/w**2

def n2_lorentz(w):
    return 1 + wp**2/(w0**2 - w**2)

print("=== 1: 低周波の屈折率 ===")
print(f" 前回の結果 v/v0 = 1/sqrt(1+L^2/(2 I kin)) → n^2(0) = {1+L**2/(2*I*kin):.6f}")
print(f" 数値 n^2(w=1e-4) = {n2_exact(1e-4):.6f}")

print("\n=== 2: 周波数依存性 と ローレンツ振動子模型の比較 ===")
print(f" w0 = sqrt(2kin/I) = {w0:.4f},  wp = L/I = {wp:.4f}")
print("   w      n^2(厳密)     n^2(ローレンツ)   相対差")
for w in [0.01, 0.5, 1.0, 2.0, 3.0, 4.0, 4.4]:
    e, l = n2_exact(w), n2_lorentz(w)
    print(f" {w:5.2f}  {e:12.6f}  {l:12.6f}   {(e-l)/l:+.2e}")
print(" (ローレンツ形は K << 2kin の近似。厳密式との差はその補正)")

print("\n=== 3: 共鳴の上に禁止帯(光が進めない帯域)があるか ===")
w_gap_top = np.sqrt(w0**2 + wp**2)
print(f" ローレンツ予想: w0={w0:.4f} < w < sqrt(w0^2+wp^2)={w_gap_top:.4f} で n^2<0")
for w in [w0*0.999, w0*1.001, (w0+w_gap_top)/2, w_gap_top*0.999, w_gap_top*1.001]:
    k2 = max(k_of_w(w))
    print(f"   w={w:.5f}  最大 k^2={k2:+.4e}  {'伝播' if k2>0 else '進めない(エバネッセント)'}")

print("\n=== 4: L+ ≠ L- (対の回転が不釣り合い) → 左右円偏光の屈折率差 ===")
# 複素表示 psi=thx+i thy で w>0 と w<0 が逆回りの円偏光
for dL in [0.0, 0.01, 0.1]:
    Lp, Lm = L+dL, -L
    w = 0.5
    kR = max(k_of_w(+w, Lp, Lm)); kL = max(k_of_w(-w, Lp, Lm))
    nR, nL = np.sqrt(kR)*v0/w, np.sqrt(kL)*v0/w
    print(f"  dL={dL:4.2f}  n_R={nR:.7f}  n_L={nL:.7f}  n_R-n_L={nR-nL:+.3e}")
print("  → 合計角運動量が残ると円偏光で屈折率が分かれる (ファラデー効果/旋光性と同じ型)")
