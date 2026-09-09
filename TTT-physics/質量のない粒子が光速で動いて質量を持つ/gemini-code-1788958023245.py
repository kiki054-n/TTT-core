import numpy as np
from scipy.optimize import minimize

# --- 物理定数・単位系（自然単位系に近いスケールで正規化） ---
# c = 1, hbar = 1 とした単位系
HBAR = 1.0
C = 1.0
TARGET_ANGLE_DEG = 109.4712
TARGET_ANGLE_RAD = np.radians(TARGET_ANGLE_DEG)

def calc_vector_sum_penalty(v_vectors):
    """
    第1項: ベクトル総和ゼロの要請 (TriTetraの力の相殺)
    """
    total_v = np.sum(v_vectors, axis=0)
    return np.sum(total_v**2)

def calc_tetrahedral_angle_penalty(v_vectors):
    """
    第2項: 四面体角 (109.47°) からのズレへのペナルティ
    """
    penalty = 0.0
    N = len(v_vectors)
    for i in range(N):
        for j in range(i + 1, N):
            v1, v2 = v_vectors[i], v_vectors[j]
            norm1, norm2 = np.linalg.norm(v1), np.linalg.norm(v2)
            if norm1 == 0 or norm2 == 0:
                continue
            cos_theta = np.dot(v1, v2) / (norm1 * norm2)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)
            theta = np.arccos(cos_theta)
            penalty += (1.0 - np.cos(theta - TARGET_ANGLE_RAD))**2
    return penalty

def calc_centrifugal_potential(r, L=0.5):
    """
    第3項: 光速回転場による角運動量 L (hbar/2 = 0.5) の遠心力ポテンシャル
    U_rot = L^2 / (2 * m * r^2) 相当
    """
    if r <= 1e-6:
        return 1e9
    return (L**2) / (2.0 * (r**2))

def ttt_potential_energy(params, alpha=10.0, beta=5.0, gamma=1.0, L=0.5):
    """
    TTTポテンシャル関数の計算
    params: 4つの3次元ベクトル (12次元配列)
    """
    v_vectors = params.reshape((4, 3))
    
    # 1. ベクトル総和ペナルティ
    E_vec = alpha * calc_vector_sum_penalty(v_vectors)
    
    # 2. 角度ペナルティ
    E_ang = beta * calc_tetrahedral_angle_penalty(v_vectors)
    
    # 3. 各粒子の回転拘束ポテンシャル (半径 r の収縮を防ぎ質量の安定化を図る)
    E_rot = 0.0
    for v in v_vectors:
        r = np.linalg.norm(v)
        E_rot += gamma * calc_centrifugal_potential(r, L=L)
        
    return E_vec + E_ang + E_rot

# --- 初期状態の設定 (少し乱した正四面体配置) ---
np.random.seed(42)
initial_v = np.array([
    [1.0, 1.0, 1.0],
    [1.0, -1.0, -1.0],
    [-1.0, 1.0, -1.0],
    [-1.0, -1.0, 1.0]
]) + np.random.normal(0, 0.1, (4, 3))

# --- ポテンシャル最小化（構造最適化） ---
result = minimize(
    ttt_potential_energy, 
    initial_v.flatten(), 
    args=(10.0, 5.0, 1.0, 0.5),
    method='L-BFGS-B'
)

optimized_v = result.x.reshape((4, 3))

# --- 結果の評価 ---
print("=== Optimization Result ===")
print(f"Convergence Success: {result.success}")
print(f"Total Potential Energy: {result.fun:.6f}\n")

print("--- Optimized Vectors (OπO)_4 ---")
for i, v in enumerate(optimized_v):
    r = np.linalg.norm(v)
    print(f"v_{i+1}: {v.round(4)} | |v| = {r:.4f}")

# 内角の計算
angles = []
for i in range(4):
    for j in range(i + 1, 4):
        cos_t = np.dot(optimized_v[i], optimized_v[j]) / (np.linalg.norm(optimized_v[i]) * np.linalg.norm(optimized_v[j]))
        angles.append(np.degrees(np.arccos(np.clip(cos_t, -1.0, 1.0))))

print(f"\nMean Inter-vector Angle: {np.mean(angles):.4f}° (Target: {TARGET_ANGLE_DEG}°)")
print(f"Vector Sum Norm |Σv|: {np.linalg.norm(np.sum(optimized_v, axis=0)):.6f}")

# --- 質量の創発 (Effective Mass Calculation) ---
# E = m * c^2 (c=1) より、回転ポテンシャルの基底エネルギーから実効質量を算出
effective_mass = result.fun / (C**2)
print(f"\nEmergent Effective Mass (m = E_base / c^2): {effective_mass:.6f}")