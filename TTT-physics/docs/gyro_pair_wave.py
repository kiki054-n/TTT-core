"""
TTT 検算: ±の対の回転剛性から横波の速さを出す
モデル: 1次元格子 (間隔 a)。各サイトにジャイロ(スピン角運動量 L, 横慣性モーメント I)。
傾き(横2成分)を複素数 psi = th_x + i th_y で表す。
隣接サイト間に回転剛性 kappa (MacCullagh型: 相対的な向きの差にだけ抵抗)。
単体ジャイロの線形方程式: I psi'' - i s L psi' = kappa * (psi_{j+1} - 2 psi_j + psi_{j-1}),  s = ±1
Bloch 解 psi ~ exp(i(kx - w t)) で  -I w^2 - s L w + K(k) = 0,  K(k) = 2 kappa (1 - cos ka)
"""
import numpy as np

I, kappa, a = 1.0, 1.0, 1.0
v0 = a*np.sqrt(kappa/I)          # 回転剛性だけで決まる速さ (1個あたりの慣性)

def K(k): return 2*kappa*(1-np.cos(k*a))

def quad_eig(M, G, Kmat):
    # (-w^2 M - w G + Kmat) x = 0 を一般化固有値問題に線形化
    n = M.shape[0]
    Z, Id = np.zeros((n,n)), np.eye(n)
    A = np.block([[Z, Id], [Kmat, -G]])
    B = np.block([[Id, Z], [Z, M]])
    w = np.linalg.eigvals(np.linalg.solve(B, A))
    return np.sort(w.real[np.abs(w.imag) < 1e-9])

ks = np.array([1e-3, 3e-3, 1e-2, 3e-2, 0.1])

print("=== A: 片方向だけのジャイロ (s=+1, L=1) ===")
L = 1.0
for k in ks:
    w = quad_eig(np.array([[I]]), np.array([[L]]), np.array([[K(k)]]))
    wpos = w[w > 0].min()
    print(f"k={k:.0e}  最低正振動数 w={wpos:.3e}  w/k={wpos/k:.3e}  w/k^2={wpos/k**2:.4f}")
print("  → w ≈ kappa a^2 k^2 / L (二次分散)。位相速度が k とともに 0 へ: 光にはなれない")
w_gap = quad_eig(np.array([[I]]), np.array([[L]]), np.array([[K(1e-3)]]))
print(f"  もう一方の枝 (k→0): w={w_gap[np.argmax(np.abs(w_gap))]:.4f} = -L/I (ギャップあり)")

print("\n=== B: ±の対を剛に固定 (同じ向きで一体, 合計L=0) ===")
for k in ks:
    w = quad_eig(np.array([[2*I]]), np.array([[0.0]]), np.array([[2*K(k)]]))
    wpos = w[w > 0].min()
    exact = (2*v0/a)*np.sin(k*a/2)
    print(f"k={k:.0e}  w/k={wpos/k:.10f}  格子式 2v0 sin(ka/2)/a との差={wpos-exact:.1e}")
print(f"  → 位相速度 = v0 = a sqrt(kappa/I) = {v0}。ジャイロ項は厳密に相殺")
print("  (剛性・慣性とも2倍なので速さは単体の比 kappa/I と同じ)")

print("\n=== C: ±の対を内部ばね kappa_in で結合 (柔らかい対) ===")
for kin in [1.0, 10.0, 100.0]:
    M = np.diag([I, I])
    G = np.diag([L, -L])                     # +スピンと-スピン
    print(f" kappa_in={kin}")
    for k in [1e-3, 1e-2, 0.1]:
        Kmat = np.array([[K(k)+kin, -kin], [-kin, K(k)+kin]])
        w = quad_eig(M, G, Kmat)
        wpos = w[w > 0].min()
        lattice = (2*v0/a)*np.sin(k*a/2)
        rel = (wpos - lattice)/lattice
        print(f"   k={k:.0e}  w/k={wpos/k:.8f}  格子式からの相対ずれ={rel:+.3e}")
# 解析: 音響枝の補正 dv/v ≈ -(L^2/(4 I kappa_in)) * ... を数値で係数確認
print("  係数チェック: 小k での相対ずれ ×(kappa_in/L^2)")
for kin in [10.0, 100.0, 1000.0]:
    k = 1e-3
    Kmat = np.array([[K(k)+kin, -kin], [-kin, K(k)+kin]])
    w = quad_eig(np.diag([I,I]), np.diag([L,-L]), Kmat)
    wpos = w[w>0].min(); lattice = (2*v0/a)*np.sin(k*a/2)
    print(f"   kappa_in={kin:6.0f}  rel*kappa_in/L^2 = {(wpos-lattice)/lattice*kin/L**2:+.5f}")

print("\n=== D: 偏光の数 ===")
print("  傾きは th_x, th_y の2成分 → 横波2偏光 (光子の2偏光と一致)")
print("  縦方向 (スピン軸まわりの回転 th_z) は MacCullagh 型エネルギー (curl)^2 では復元力の扱いが別。")
print("  スピン軸まわりの回転は向きを変えないのでジャイロ剛性を生まない → 縦波を持たない条件は別途要請")

print("\n=== E: 格子分散と観測 (記憶値の制限を使った目安) ===")
hbarc = 1.97327e-16   # GeV·m
for EQG2 in [1e10, 1.3e11]:
    a_max = np.sqrt(24)*hbarc/EQG2
    print(f"  E_QG,2 > {EQG2:.1e} GeV なら 格子間隔 a < {a_max:.2e} m  (プランク長 1.6e-35 m の {a_max/1.616e-35:.1e} 倍)")
