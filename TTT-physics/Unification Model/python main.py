---

### 3. 一括実行スクリプト `main.py`

これまでの数値シミュレーション（ポテンシャル最小化、弾性定数算出、IV族スケーリング、CNTカイラリティ分布）を一括で計算し、検証結果を出力するプロトタイプコードです。

```python
"""
TTT-Core-Physics Unified Simulation Suite
"""
import numpy as np
from scipy.optimize import minimize, curve_fit

# --- 1. (OπO)4 最小安定構造の最適化 ---
def run_opo4_optimization():
    print("\n=== [1] (OπO)4 Tetrahedral Geometry Minimization ===")
    target_rad = np.radians(109.4712)
    
    def ttt_potential(params, alpha=10.0, beta=5.0, gamma=1.0, L=0.5):
        v = params.reshape((4, 3))
        E_vec = alpha * np.sum(np.sum(v, axis=0)**2)
        E_ang = 0.0
        for i in range(4):
            for j in range(i + 1, 4):
                cos_t = np.clip(np.dot(v[i], v[j]) / (np.linalg.norm(v[i]) * np.linalg.norm(v[j])), -1.0, 1.0)
                E_ang += beta * (1.0 - np.cos(np.arccos(cos_t) - target_rad))**2
        E_rot = sum(gamma * (L**2) / (2.0 * np.linalg.norm(vi)**2) for vi in v)
        return E_vec + E_ang + E_rot

    init_v = np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]], dtype=float) + np.random.normal(0,0.05,(4,3))
    res = minimize(ttt_potential, init_v.flatten(), method='L-BFGS-B')
    opt_v = res.x.reshape((4, 3))
    
    angles = []
    for i in range(4):
        for j in range(i+1, 4):
            cos_t = np.clip(np.dot(opt_v[i], opt_v[j]) / (np.linalg.norm(opt_v[i]) * np.linalg.norm(opt_v[j])), -1.0, 1.0)
            angles.append(np.degrees(np.arccos(cos_t)))
            
    print(f"Convergence Success: {res.success}")
    print(f"Mean Inter-vector Angle: {np.mean(angles):.4f}° (Target: 109.4712°)")
    print(f"Effective Mass (m_eff = E_base / c^2): {res.fun:.6f}")

# --- 2. 同族IV族元素の格子定数・Df スケーリング検証 ---
def run_iv_group_scaling():
    print("\n=== [2] IV-Group Lattice Scaling Verification (D_f ~ 2.4) ===")
    masses = np.array([12.011, 28.085, 72.630, 118.710]) # C, Si, Ge, alpha-Sn
    a_exp = np.array([3.567, 5.431, 5.658, 6.489])
    
    def scaling_law(M, exponent):
        return a_exp[0] * (M / masses[0])**exponent

    popt, _ = curve_fit(scaling_law, masses, a_exp, p0=[0.235])
    exponent = popt[0]
    derived_Df = 0.564 / exponent
    
    print(f"Fitted Exponent (eta / D_f): {exponent:.4f}")
    print(f"Derived Fractal Dimension D_f: {derived_Df:.4f}")
    for m, a_act in zip(masses, a_exp):
        a_pred = scaling_law(m, exponent)
        print(f"Mass: {m:7.3f} | Actual a: {a_act:.3f} Å | Pred a: {a_pred:.3f} Å | Error: {(a_pred-a_act)/a_act*100:+.2f}%")

# --- 3. CNT カイラリティ安定性 (k=2 共鳴点) ---
def run_cnt_chirality_analysis():
    print("\n=== [3] CNT Chirality Resonance & Diameter Selection ===")
    a_cc = 0.1421
    d0_ttt = 0.710
    
    def get_cnt_energy(d, theta_deg):
        E_bend = 0.085 / (d**2)
        E_ttt = - 0.120 * np.exp(- ((d - 2.0 * d0_ttt)**2) / (2.0 * (0.180**2)))
        E_chiral = 0.015 * (np.cos(3.0 * np.radians(theta_deg))**2)
        return E_bend + E_ttt + E_chiral

    results = []
    for n in range(5, 20):
        for m in range(0, n + 1):
            d = (a_cc * np.sqrt(3) / np.pi) * np.sqrt(n**2 + n*m + m**2)
            cos_t = np.clip((2*n + m) / (2.0 * np.sqrt(n**2 + n*m + m**2)), -1.0, 1.0)
            theta = np.degrees(np.arccos(cos_t))
            E = get_cnt_energy(d, theta)
            results.append((n, m, d, theta, E))
            
    sorted_res = sorted(results, key=lambda x: x[4])
    print("Top 3 Most Stable CNT Chirality (TTT Model):")
    for rank, (n, m, d, theta, E) in enumerate(sorted_res[:3], 1):
        cnt_type = "Armchair" if n == m else ("Zigzag" if m == 0 else "Chiral")
        print(f"Rank {rank}: ({n:2d},{m:2d}) [{cnt_type:8s}] | Diameter: {d:.3f} nm | Energy: {E:.4f} eV/atom")

if __name__ == "__main__":
    print("=" * 60)
    print(" TTT-Core-Physics: Integrated Verification Execution")
    print("=" * 60)
    run_opo4_optimization()
    run_iv_group_scaling()
    run_cnt_chirality_analysis()
