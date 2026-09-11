"""Comparisons of TTT-style counting rules with measured data.

Each function returns plain numbers so that tests and figures can reuse them.
"""
from __future__ import annotations

import math

import numpy as np

from .constants import (ALPHA, BOHR_RADIUS, C, GRAPHITE_DIAMOND, GROUP_IV, HBAR, M_E,
                        M_E_C2_EV, EV, PARTICLE_MASS_MEV)
from .geometry import PLATONIC

# --------------------------------------------------------------------------- #
# Length / energy ladder of the electron (why 137 keeps reappearing)          #
# --------------------------------------------------------------------------- #
def alpha_ladder() -> dict:
    """classical radius : reduced Compton : Bohr  =  alpha : 1 : 1/alpha."""
    lam_c = HBAR / (M_E * C)
    r_e = ALPHA * lam_c
    a0 = BOHR_RADIUS
    e_orbit = HBAR * C / a0 / EV                     # = alpha m c^2 = 3728.9 eV
    ke = e_orbit**2 / (2 * M_E_C2_EV)                # = 13.606 eV (hydrogen binding)
    return {"r_e": r_e, "lambda_C": lam_c, "a0": a0,
            "a0_over_lambdaC": a0 / lam_c, "lambdaC_over_re": lam_c / r_e,
            "hbar_c_over_a0_eV": e_orbit, "kinetic_eV": ke}


def coulomb_vs_needed_force() -> float:
    """Force needed to bend energy m c^2 onto radius hbar/(m c), divided by the
    Coulomb force e^2/(4 pi eps0 r^2) at that radius.  Exactly 1/alpha."""
    r = HBAR / (M_E * C)
    f_needed = M_E * C**2 / r
    f_coulomb = ALPHA * HBAR * C / r**2
    return f_needed / f_coulomb


# --------------------------------------------------------------------------- #
# "12 lattice units = m_e"  counting rule                                      #
# --------------------------------------------------------------------------- #
UNIT_KEV = M_E_C2_EV / 12 / 1e3   # 42.583 keV


def platonic_masses() -> dict:
    """Mass if every directed edge carries m_e/12 (additive rule)."""
    return {name: {"directed_edges": 2 * E, "m_over_me": 2 * E / 12,
                   "MeV": 2 * E / 12 * PARTICLE_MASS_MEV["e"]}
            for name, (V, E, F) in PLATONIC.items()}


def particle_units() -> dict:
    """Measured masses in units of m_e/12.  An additive integer rule predicts
    integers; observed fractional parts are spread 0.17-0.41 (no signal)."""
    out = {}
    for name, m in PARTICLE_MASS_MEV.items():
        u = m / PARTICLE_MASS_MEV["e"] * 12
        out[name] = {"units": u, "frac": u - round(u)}
    return out


def koide_ratio() -> dict:
    me, mm, mt = (PARTICLE_MASS_MEV[k] for k in ("e", "mu", "tau"))
    q = (me + mm + mt) / (math.sqrt(me) + math.sqrt(mm) + math.sqrt(mt)) ** 2
    v = np.sqrt([me, mm, mt])
    angle = math.degrees(math.acos(v.sum() / (np.linalg.norm(v) * math.sqrt(3))))
    return {"Q": q, "angle_to_body_diagonal_deg": angle}   # 2/3 <-> 45 deg


# --------------------------------------------------------------------------- #
# Group IV lattice constants                                                  #
# --------------------------------------------------------------------------- #
def group_iv_scaling() -> dict:
    names = list(GROUP_IV)
    M = np.array([GROUP_IV[k]["M"] for k in names])
    a = np.array([GROUP_IV[k]["a"] for k in names])
    rc = np.array([GROUP_IV[k]["r_cov"] for k in names])
    x, y = np.log(M), np.log(a)
    slope, icpt = np.polyfit(x, y, 1)
    pred = slope * x + icpt
    r2 = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
    local = np.diff(y) / np.diff(x)
    # diamond structure: bond d = sqrt(3)/4 a  and  d ~ 2 r_cov  ->  a = 8/sqrt(3) r_cov
    cov_ratio = a / (8 / math.sqrt(3) * rc)
    return {"names": names, "slope": float(slope), "r2": float(r2),
            "local_slopes": local.tolist(),
            "Df_if_eta_0564": 0.564 / slope,   # circular: eta is an input
            "a_over_covalent": cov_ratio.tolist()}


# --------------------------------------------------------------------------- #
# Graphite / diamond Clapeyron baseline (pure thermodynamic tables)           #
# --------------------------------------------------------------------------- #
def clapeyron_graphite_diamond() -> dict:
    d = GRAPHITE_DIAMOND
    v_g = d["M_carbon"] / d["rho_graphite"]
    v_d = d["M_carbon"] / d["rho_diamond"]
    dV = v_g - v_d                       # m^3/mol
    dS = d["S_graphite"] - d["S_diamond"]
    return {"dV_cm3_mol": dV * 1e6, "dS_J_molK": dS,
            "intercept_GPa": d["dH_f_diamond"] / dV / 1e9,
            "slope_GPa_per_K": dS / dV / 1e9,
            "dH_eV_per_atom": d["dH_f_diamond"] / 96485.33212,
            "dS_kB_per_atom": dS / 8.314462618}


def clapeyron_line(T, res=None):
    res = res or clapeyron_graphite_diamond()
    return res["intercept_GPa"] + res["slope_GPa_per_K"] * np.asarray(T, float)
