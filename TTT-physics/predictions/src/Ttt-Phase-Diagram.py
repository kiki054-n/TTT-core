
import numpy as np
# TTT phase diagram: G = E + PV - TS
# E_sp3 - E_sp2 = 0.02 eV/atom, V_sp3=3.417cm3/mol, V_sp2=5.31cm3/mol
# S_sp3=2.38 J/mol/K, S_sp2=5.74 J/mol/K
# P_eq = (-dE + T*dS)/dV
eV=1.602e-19
NA=6.022e23
dE=0.02*eV
V3=3.417e-6/NA
V2=5.31e-6/NA
dV=V3-V2
S3=2.38/NA
S2=5.74/NA
dS=S3-S2
def P_eq(T):
    return (-dE + T*dS)/dV/1e9 # GPa
for T in [0,1000,2000,3000]:
    print(T, P_eq(T))
