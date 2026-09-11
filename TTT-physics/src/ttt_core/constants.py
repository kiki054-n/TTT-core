"""Physical constants (CODATA 2018, SI) and a few reference data used for comparison.

Values that come from experiment are kept here, in one place, so that every
script can be audited for *which measured numbers were fed in*.
"""

# --- CODATA 2018 -----------------------------------------------------------
C = 299_792_458.0                 # speed of light [m/s]
HBAR = 1.054_571_817e-34          # reduced Planck constant [J s]
H = 6.626_070_15e-34              # Planck constant [J s]
E_CHARGE = 1.602_176_634e-19      # elementary charge [C]  (= J per eV)
M_E = 9.109_383_7015e-31          # electron mass [kg]
ALPHA = 7.297_352_5693e-3         # fine-structure constant
BOHR_RADIUS = 5.291_772_109_03e-11  # a0 [m]
K_B = 1.380_649e-23               # Boltzmann constant [J/K]
R_GAS = 8.314_462_618             # gas constant [J/(mol K)]
N_A = 6.022_140_76e23             # Avogadro constant [1/mol]

EV = E_CHARGE
M_E_C2_EV = M_E * C**2 / EV       # 510 998.95 eV

# --- Particle masses [MeV/c^2], PDG ----------------------------------------
PARTICLE_MASS_MEV = {
    "e": 0.510_998_950,
    "mu": 105.658_3755,
    "pi+": 139.570_39,
    "pi0": 134.976_8,
    "K+": 493.677,
    "p": 938.272_088_16,
    "n": 939.565_420_52,
    "tau": 1776.86,
}

# --- Group-IV diamond-structure crystals (room temperature) ----------------
# atomic mass [u], lattice constant a [Angstrom], single-bond covalent radius [Angstrom]
# (covalent radii: Cordero et al., Dalton Trans. 2008)
GROUP_IV = {
    "C":  {"M": 12.011, "a": 3.567, "r_cov": 0.76},
    "Si": {"M": 28.085, "a": 5.431, "r_cov": 1.11},
    "Ge": {"M": 72.630, "a": 5.658, "r_cov": 1.20},
    "Sn": {"M": 118.71, "a": 6.489, "r_cov": 1.39},   # alpha-Sn
}

# --- Graphite / diamond standard thermodynamic data (298.15 K, 1 bar) -------
GRAPHITE_DIAMOND = {
    "dH_f_diamond": 1895.0,     # J/mol, enthalpy of formation of diamond from graphite
    "S_graphite": 5.740,        # J/(mol K)
    "S_diamond": 2.377,         # J/(mol K)
    "rho_graphite": 2.266e6,    # g/m^3
    "rho_diamond": 3.515e6,     # g/m^3
    "M_carbon": 12.011,         # g/mol
}
