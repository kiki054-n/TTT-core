
# TTT-style electron model: massless O particle circulating at c => massive electron
# Author: TTT-core simulation draft
import numpy as np
import matplotlib.pyplot as plt

c = 299792458.0
hbar = 1.054571817e-34
m_e = 9.10938356e-31

r_c = hbar/(m_e*c)  # Compton radius
omega = c/r_c       # Zitter frequency

# Time evolution: x(t)=r_c cos(omega t), y(t)=r_c sin(omega t)
dt = 1e-23
t_max = 5e-21
t = np.arange(0, t_max, dt)
x = r_c*np.cos(omega*t)
y = r_c*np.sin(omega*t)

# Check: |v| = c
v_mag = r_c*omega  # = c

# Effective mass from confined photon energy: E = hbar*c / r_c
E_conf = hbar*c/r_c
m_eff = E_conf / c**2
print(f"m_eff = {m_eff} kg, m_e = {m_e} kg, ratio = {m_eff/m_e}")

# TTT tetrahedral potential: sum_v = 0 and cosθ = -1/3
def ttt_potential(positions):
    sum_v = np.sum(positions, axis=0)
    term1 = np.dot(sum_v, sum_v)
    norms = np.linalg.norm(positions, axis=1, keepdims=True)+1e-30
    unit = positions/norms
    cos_target = -1/3
    term2 = 0
    for i in range(4):
        for j in range(i+1,4):
            term2 += (np.dot(unit[i], unit[j]) - cos_target)**2
    return term1 + 0.5*term2

# ideal tetrahedron -> potential 0 (minimum)
ideal = np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]], float)
ideal /= np.linalg.norm(ideal[0])
print("V_ideal:", ttt_potential(ideal))
