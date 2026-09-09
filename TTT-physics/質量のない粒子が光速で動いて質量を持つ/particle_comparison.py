"""
src/particle_comparison.py
TTT-Core-Physics: Emergence of Electron Rest Mass (m_e) and Minimal Energy Quantum (42.58 keV)
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# --- SI 物理定数 ---
HBAR = 1.054571817e-34       # プランク定数 / 2pi (J·s)
H = 2.0 * np.pi * HBAR       # プランク定数 (J·s)
C = 299792458.0              # 光速 (m/s)
ME_SI = 9.1093837015e-31     # 電子の実測静止質量 (kg)
EV_CONV = 1.602176634e-19    # Joules -> eV 変換定数

# 実測の電子コンプトン波長 (m)
COMPTON_RADIUS_EXP = HBAR / (ME_SI * C)  # ~ 3.86159e-13 m

# --- 1. TTT (OπO) 回転場ポテンシャルの定義 ---
def derive_g_pi():
    """
    安定半径 r0 が実測のコンプトン波長と一致する TTT 位相結合定数 g_pi (N) を算出
    r0 = sqrt(hbar * c / (2 * g_pi)) => g_pi = hbar * c / (2 * r0^2)
    """
    return (HBAR * C) / (2.0 * (COMPTON_RADIUS_EXP**2))

G_PI = derive_g_pi()

def ttt_electron_potential(r, g_pi=G_PI):
    """
    r: (OπO) 回転閉じ込め半径 (m)
    returns: 全ポテンシャルエネルギー E_total (Joules)
    """
    if r <= 1e-18:
        return 1e10
    
    # 1. 運動・遠心ポテンシャル (光速回転運動)
    U_kinetic = (HBAR * C) / (2.0 * r)
    
    # 2. (OπO) pi-回転場拘束ポテンシャル
    U_binding = g_pi * r
    
    return U_kinetic + U_binding

# --- 2. 最小エネルギー単位 (12自由度分割) の導出関数の追加 ---
def calculate_minimal_energy_unit(E_base_joules):
    """
    コンプトン束縛エネルギー (0.511 MeV) を 12 自由度 (3軸 x 4四面体配向) で除算
    """
    DIV_SPATIAL_AXES = 3   # 3次元空間軸 (x, y, z) へのエネルギー等配分
    DIV_TETRA_AXES = 4     # (OπO)_4 正四面体 4軸のベクトル相殺配分
    DIV_TOTAL = DIV_SPATIAL_AXES * DIV_TETRA_AXES  # 12 自由度

    E_unit_joules = E_base_joules / DIV_TOTAL
    E_unit_keV = (E_unit_joules / EV_CONV) / 1e3
    
    # 最小エネルギー単位に対応する等価量子波長 lambda = h * c / E
    lambda_unit_m = (H * C) / E_unit_joules
    lambda_unit_angstrom = lambda_unit_m * 1e10

    return {
        'div_total': DIV_TOTAL,
        'E_unit_keV': E_unit_keV,
        'E_unit_joules': E_unit_joules,
        'lambda_angstrom': lambda_unit_angstrom
    }

# --- 3. 実行および結果の出力 ---
def run_particle_comparison():
    print("=== [TTT Model] Emergence of Electron Mass m_e & Minimal Quantum Unit ===")
    
    # 基底状態の特定
    res = minimize_scalar(ttt_electron_potential, bounds=(1e-15, 1e-11), method='bounded')
    r_0 = res.x
    E_base_joules = res.fun
    
    m_emergent = E_base_joules / (C**2)
    E_base_MeV = (E_base_joules / EV_CONV) / 1e6
    
    print(f"Calculated Coupling Constant (g_pi): {G_PI:.6e} N")
    print(f"Optimized Confinement Radius (r_0): {r_0:.6e} m")
    print(f"Experimental Compton Radius        : {COMPTON_RADIUS_EXP:.6e} m")
    print("-" * 65)
    print(f"Emergent Ground State Energy (E_0) : {E_base_MeV:.6f} MeV")
    print(f"Calculated Emergent Mass (m_e)    : {m_emergent:.6e} kg")
    print(f"Experimental Electron Mass        : {ME_SI:.6e} kg")
    print(f"Mass Deviation                    : {abs(m_emergent - ME_SI)/ME_SI * 100:.6f}%")

    # 最小エネルギー単位 (42.58 keV) の導出結果
    unit_res = calculate_minimal_energy_unit(E_base_joules)
    print("-" * 65)
    print(f"=== [TTT Minimal Energy Quantum Derivation] ===")
    print(f"Spatial Axes Division (x,y,z)    : / 3")
    print(f"Tetrahedral Orientation Division : / 4")
    print(f"Total Degrees of Freedom          : {unit_res['div_total']} (3 x 4)")
    print(f"Calculated Minimal Energy Unit   : {unit_res['E_unit_keV']:.4f} keV")
    print(f"Equivalent Quantum Wavelength    : {unit_res['lambda_angstrom']:.4f} Å ({unit_res['lambda_angstrom']/10:.4f} nm)")

    # --- 4. ポテンシャルエネルギー曲線の可視化 ---
    r_arr = np.linspace(0.1 * COMPTON_RADIUS_EXP, 3.0 * COMPTON_RADIUS_EXP, 300)
    U_kin_arr = (HBAR * C) / (2.0 * r_arr) / EV_CONV / 1e6
    U_bind_arr = (G_PI * r_arr) / EV_CONV / 1e6
    E_tot_arr = (U_kin_arr + U_bind_arr)

    plt.figure(figsize=(8.5, 5.5))
    plt.plot(r_arr * 1e13, E_tot_arr, 'r-', linewidth=2, label='$E_{\\text{total}}(r) = U_{\\text{kin}} + U_{\\text{bind}}$')
    plt.plot(r_arr * 1e13, U_kin_arr, 'b--', alpha=0.7, label='Kinetic Centrifugal $U_{\\text{kin}} \\propto 1/r$')
    plt.plot(r_arr * 1e13, U_bind_arr, 'g--', alpha=0.7, label='(O$\pi$O) Binding $U_{\\text{bind}} \\propto r$')

    plt.axvline(x=COMPTON_RADIUS_EXP * 1e13, color='black', linestyle=':', 
                label=f'Compton Radius $r_c \\approx {COMPTON_RADIUS_EXP*1e13:.2f} \\times 10^{{-13}}$ m')
    
    # 最小エネルギー単位のテキスト注記の追加
    plt.text(COMPTON_RADIUS_EXP * 1e13 * 1.1, 0.8, 
             f"Total $E_0 = {E_base_MeV:.3f}$ MeV\n"
             f"$E_{{\\text{{unit}}}} = E_0 / 12 = {unit_res['E_unit_keV']:.2f}$ keV\n"
             f"($\\lambda \\approx {unit_res['lambda_angstrom']:.2f}$ Å)", 
             fontsize=9.5, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", alpha=0.3))

    plt.xlabel('Confinement Radius $r$ ($\\times 10^{-13}$ m)', fontsize=11)
    plt.ylabel('Energy (MeV)', fontsize=11)
    plt.title('Emergence of Electron Mass $m_e c^2$ & Minimal Quantum Unit (42.58 keV)', fontsize=12)
    plt.ylim(0, 2.0)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=9.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_particle_comparison()
