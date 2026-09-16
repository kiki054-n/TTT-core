"""
TTT 検算 2b: 「空間(真空)の±対」＋「その場に結合した局所の対(物質)」
真空: 剛な±対 (慣性 Iv, 隣接剛性で K = Iv v0^2 k^2)。ジャイロ項は相殺
物質: 各点に局所OπO (慣性 Im, 正味スピン Lm)。隣とはつながらず、真空とだけ kc で結合
  真空: -Iv w^2 psi + K psi + kc (psi - chi) = 0
  物質: -Im w^2 chi - s Lm w chi + kc (chi - psi) = 0     (s=±1 は円偏光の向き)
予想: n^2 = 1 + (kc/Iv) / (w0^2 - w^2 - s (Lm/Im) w),  w0^2 = kc/Im
"""
import numpy as np
Iv, v0, Im, kc = 1.0, 1.0, 0.2, 2.0
w0, wp = np.sqrt(kc/Im), np.sqrt(kc/Iv)

def n2_numeric(w, Lm=0.0, s=1):
    # 2x2 行列式=0 を K について解く (K は1次なので一意)
    a = -Im*w**2 - s*Lm*w + kc
    # (-Iv w^2 + K + kc) a - kc^2 = 0
    K = kc**2/a + Iv*w**2 - kc
    return K/(Iv*w**2)      # = v0^2 k^2 / w^2

def n2_lorentz(w, Lm=0.0, s=1):
    return 1 + wp**2/(w0**2 - w**2 - s*(Lm/Im)*w)

print(f"w0={w0:.4f}  wp={wp:.4f}")
print("=== 1: Lm=0 ローレンツ振動子模型と一致するか ===")
for w in [0.1, 1.0, 2.0, 3.0, 3.1, 3.2, 3.5, 3.8, 5.0, 20.0]:
    e, l = n2_numeric(w), n2_lorentz(w)
    tag = "伝播" if e > 0 else "進めない"
    print(f"  w={w:5.2f}  n^2={e:+10.5f}  Lorentz={l:+10.5f}  差={e-l:+.1e}  {tag}")
print(f"  禁止帯の予想: {w0:.4f} < w < {np.sqrt(w0**2+wp**2):.4f}")
print("  w→∞ で n^2→1 (高周波では物質が追従できず真空と同じ)")

print("\n=== 2: 物質側に正味スピン Lm → 左右円偏光で n が分かれる ===")
for Lm in [0.0, 0.01, 0.05]:
    w = 1.0
    nR, nL = np.sqrt(n2_numeric(w, Lm, +1)), np.sqrt(n2_numeric(w, Lm, -1))
    wc = Lm/Im
    print(f"  Lm={Lm:.2f} (wc=Lm/Im={wc:.2f})  n_R={nR:.7f}  n_L={nL:.7f}  差={nR-nL:+.3e}")
print("  → 電子のサイクロトロン振動数 wc=eB/m を wc=Lm/Im に置き換えた古典ファラデー効果の式と同型")

print("\n=== 3: 真空だけ(物質なし)で n を測れるか ===")
print("  一様な±対(前回 C)では v = v0/sqrt(1+L^2/(2 I kin)) が全域で同じ → 比べる相手がなく c の定義に吸収される")
