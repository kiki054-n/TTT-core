import numpy as np
import matplotlib.pyplot as plt

# ---- 省略せず全文をここに貼る（前回提示したコード） ----

import numpy as np

# ---- 1. 遷移演算子 T_total（あなたの計算結果を使用） ----
T_total = np.array([
    [2.558327, 0, 0, 0, 0, 0],
    [0, 1.666667, 0, 0, 0, 0],
    [0, 0, 1.666667, 0, 0, 0],
    [0, 0, 0, 4.778893, 0, 0],
    [0, 0, 0, 0, 1.959338, 0],
    [0, 0, 0, 0, 0, 2.558327]
])

# ---- 2. 固有値の絶対値 ----
eigs = np.abs(np.linalg.eigvals(T_total))

# ---- 3. 無限遷移の極限を数値的に評価 ----
def alpha_inverse(N):
    # T_total^N のトレース
    trace_N = np.sum(eigs**N)
    
    S_topo  = 12*np.pi**2 * 3
    S_local = 4*np.pi*(27/23)
    S_RG    = -(1/(2*np.pi))*np.log(trace_N)
    
    return S_topo + S_local + S_RG

# ---- 4. 収束の様子を表示 ----
for N in [10, 20, 50, 100, 200, 500, 1000]:
    print(N, alpha_inverse(N))
for N in [10, 20, 50, 100, 200, 500, 1000]:
    print(N, alpha_inverse(N))

import numpy as np
import matplotlib.pyplot as plt

eigs = np.array([2.558327, 1.666667, 1.666667, 4.778893, 1.959338, 2.558327])

def alpha_inverse(N):
    trace_N = np.sum(eigs**N)
    S_topo  = 12*np.pi**2 * 3
    S_local = 4*np.pi*(27/23)
    S_RG    = -(1/(2*np.pi))*np.log(trace_N)
    return S_topo + S_local + S_RG

Ns = np.array([10, 20, 50, 100, 200, 500, 1000])
alphas = np.array([alpha_inverse(N) for N in Ns])

plt.figure(figsize=(6,4))
plt.plot(Ns, alphas, 'o-', label=r'$\alpha^{-1}(N)$ (TTT model)')
plt.axhline(137.035999, color='r', linestyle='--',
            label=r'Experimental $\alpha^{-1}$')
plt.xlabel('Transition count N')
plt.ylabel(r'$\alpha^{-1}$')
plt.title('Convergence of fine-structure constant in TTT model')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

eigs = np.array([2.558327, 1.666667, 1.666667, 4.778893, 1.959338, 2.558327])

def alpha_inverse(N):
    trace_N = np.sum(eigs**N)
    S_topo  = 12*np.pi**2 * 3
    S_local = 4*np.pi*(27/23)
    S_RG    = -(1/(2*np.pi))*np.log(trace_N)
    return S_topo + S_local + S_RG

Ns = np.array([10, 20, 50, 100, 200, 500, 1000])
alphas = np.array([alpha_inverse(N) for N in Ns])

plt.figure(figsize=(6,4))
plt.plot(Ns, alphas, 'o-', label=r'$\alpha^{-1}(N)$ (TTT model)')
plt.axhline(137.035999, color='r', linestyle='--',
            label=r'Experimental $\alpha^{-1}$')
plt.xlabel('Transition count N')
plt.ylabel(r'$\alpha^{-1}$')
plt.title('Convergence of fine-structure constant in TTT model')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('alpha_convergence.png', dpi=300)
plt.show()



import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. 観測行列 M の定義
# ---------------------------------------------------------
M_struct = np.array([
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 1.0],
    [1.0, -1.0, 1.0]
])

M_metric = np.diag([
    1.0/np.pi,
    1.0/np.pi,
    1.0/np.sqrt(2.0)
])

M = np.block([
    [M_struct, np.zeros((3,3))],
    [np.zeros((3,3)), M_metric]
])

M_inv = np.linalg.inv(M)

# ---------------------------------------------------------
# 2. 4つの多面体の観測ベクトル O = [V, E, F, Omega, delta, Vol]
# ---------------------------------------------------------
O_D3   = np.array([5,  9,  6,  0.5512855984, 1.2309594, 0.23570226])
O_Cube = np.array([8, 12,  6,  0.5512855984, 1.5707963, 1.53960072])
O_Octa = np.array([6, 12,  8,  1.3593476378, 1.9106332, 1.88561808])
O_D5   = np.array([7, 15, 10,  2.6345472111, 2.4118649, 0.60300566])

# ---------------------------------------------------------
# 3. 6次元状態ベクトル P_i = M^{-1} O_i
# ---------------------------------------------------------
P_D3   = M_inv @ O_D3
P_Cube = M_inv @ O_Cube
P_Octa = M_inv @ O_Octa
P_D5   = M_inv @ O_D5

# ---------------------------------------------------------
# 4. 遷移演算子 T_i（対角行列として定義）
#    P_{i+1} = T_i * P_i
# ---------------------------------------------------------
T1 = np.diag(P_Cube / P_D3)
T2 = np.diag(P_Octa / P_Cube)
T3 = np.diag(P_D5 / P_Octa)

T_total = T3 @ T2 @ T1

# 固有値とトレースの確認
eigs = np.linalg.eigvals(T_total)
trace_T = np.trace(T_total)

print("Eigenvalues of T_total:", np.round(eigs, 6))
print("Trace(T_total):", trace_T)

# ---------------------------------------------------------
# 5. 微細構造定数 α^{-1}(N) の定義
# ---------------------------------------------------------
W = 3  # winding number

def alpha_inverse(N):
    """
    TTTモデルにおける微細構造定数の逆数 α^{-1}(N) を計算
    """
    # T_total^N のトレースを固有値から計算
    trace_N = np.sum(np.abs(eigs)**N)

    S_topo  = 12.0 * np.pi**2 * W
    S_local = 4.0 * np.pi * (27.0/23.0)
    S_RG    = -(1.0/(2.0*np.pi)) * np.log(trace_N)

    return S_topo + S_local + S_RG

# ---------------------------------------------------------
# 6. 収束挙動の数値評価
# ---------------------------------------------------------
Ns = np.array([10, 20, 50, 100, 200, 500, 1000])
alphas = np.array([alpha_inverse(N) for N in Ns])

print("\nConvergence of alpha^{-1}(N):")
for N, a in zip(Ns, alphas):
    print(f"N = {N:4d}, alpha^{-1}(N) = {a:.6f}")

# ---------------------------------------------------------
# 7. 収束グラフの描画
# ---------------------------------------------------------
plt.figure(figsize=(6,4))
plt.plot(Ns, alphas, 'o-', label=r'$\alpha^{-1}(N)$ (TTT model)')
plt.axhline(137.035999, color='r', linestyle='--',
            label=r'Experimental $\alpha^{-1}$')
plt.xlabel('Transition count $N$')
plt.ylabel(r'$\alpha^{-1}$')
plt.title('Convergence of fine-structure constant in TTT model')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('alpha_convergence.png', dpi=300)
plt.show()

