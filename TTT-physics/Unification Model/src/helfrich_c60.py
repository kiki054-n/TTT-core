"""
src/helfrich_c60.py
Helfrich bending energy and topological disclination dynamics for C60 self-assembly.
"""
import numpy as np

def calculate_helfrich_energy(radius, kappa=1.5, H0=1.0/0.355):
    """
    37拘束殻の Helfrich 曲げエネルギー (eV)
    F = integral [ (kappa/2) * (H - H0)^2 ] dA
    ここで H = 1/R (平均曲率), Area = 4 * pi * R^2
    """
    if radius <= 0.1:
        return 1e9
    H = 1.0 / radius
    area = 4.0 * np.pi * (radius**2)
    f_density = (kappa / 2.0) * ((H - H0)**2)
    return f_density * area

def calculate_defect_repulsion_energy(vertices_3d, mu_disclination=0.5):
    """
    球面上の 12 個の五角形位相欠陥間の対反発ポテンシャル (eV)
    U_defects = sum_{i < j} ln(1 / sin(theta_ij / 2))
    """
    N = len(vertices_3d)
    E_defects = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            v1 = vertices_3d[i] / np.linalg.norm(vertices_3d[i])
            v2 = vertices_3d[j] / np.linalg.norm(vertices_3d[j])
            cos_theta = np.clip(np.dot(v1, v2), -1.0, 1.0)
            theta = np.arccos(cos_theta)
            sin_half_theta = np.sin(theta / 2.0)
            if sin_half_theta > 1e-5:
                E_defects += mu_disclination * np.log(1.0 / sin_half_theta)
            else:
                E_defects += 1e5
    return E_defects

def run_c60_topological_analysis():
    print("=== C60 Topological Self-Assembly (Helfrich & Disclination Model) ===")
    
    # 正二十面体の 12 頂点 (12 個の五角形位相欠陥の位置)
    phi = (1.0 + np.sqrt(5.0)) / 2.0  # 黄金比
    ico_vertices = np.array([
        [-1,  phi,  0], [ 1,  phi,  0], [-1, -phi,  0], [ 1, -phi,  0],
        [ 0, -1,  phi], [ 0,  1,  phi], [ 0, -1, -phi], [ 0,  1, -phi],
        [ phi,  0, -1], [ phi,  0,  1], [-phi,  0, -1], [-phi,  0,  1]
    ], dtype=float)
    
    # C60 の平均半径 R ≈ 0.355 nm
    r_c60 = 0.355
    E_bend = calculate_helfrich_energy(r_c60)
    E_defects = calculate_defect_repulsion_energy(ico_vertices * r_c60)
    
    print(f"Optimal Radius: {r_c60:.3f} nm (Diameter: {2*r_c60:.3f} nm)")
    print(f"Bending Free Energy (Helfrich): {E_bend:.4f} eV")
    print(f"Icosahedral Disclination Repulsion: {E_defects:.4f} eV")
    print(f"Total Topological Energy: {E_bend + E_defects:.4f} eV")

if __name__ == "__main__":
    run_c60_topological_analysis()
