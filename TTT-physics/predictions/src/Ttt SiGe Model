
import numpy as np
r_c=3.862e-13
Df=2.4
geom_factor=7.2
def bond_from_N(N):
    return r_c * (N**(1/Df)) * geom_factor *1e10  # Angstrom
def N_from_bond(d_ang):
    return (d_ang*1e-10/(r_c*geom_factor))**Df

# 実験値から逆算
for elem,d in [("C",1.544),("Si",2.352),("Ge",2.45),("alpha-Sn",2.81)]:
    print(elem, N_from_bond(d))

# フィット: N = 4581.56 * mass^0.564
# これがTTTの第2階層スケーリング則候補
