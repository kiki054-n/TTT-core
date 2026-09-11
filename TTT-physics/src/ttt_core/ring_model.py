"""Massless circulating constituent + confinement  ->  radius  ->  rest mass  ->  g-factor.

Model (TTT reading: O = ring circulating at c, pi = axis):
    E_rot(r)  = L c / r          massless constituent, angular momentum L (= hbar/2)
    E_conf(r) = k r^n            confinement ("the energy that keeps the space")

Stationary point:  L c / r = n k r^n   =>   E_rot = n * E_conf
    r*   = (L c / (n k))^(1/(n+1))
    m c^2 = E_rot + E_conf = E_rot (n+1)/n

If the charge rides only on the circulating part (current = e c / 2 pi r, area pi r^2)
    mu = e c r / 2 ,   L = E_rot r / c   =>   g = 2 m mu / (e L) = m c^2 / E_rot
    g = (n+1)/n                      -> only the LINEAR confinement (n = 1) gives g = 2.

NOTE: the non-relativistic centrifugal term L^2 / (2 m r^2) must NOT be used here:
it contains the mass m that the model is supposed to produce (circular), and
together with scale-free angle penalties it has no minimum at all
(see tests/test_ring_model.py::test_old_potential_has_no_minimum).
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize, minimize_scalar

from .constants import C, HBAR, M_E

L_SPIN = HBAR / 2.0


# --------------------------------------------------------------------------- #
# Analytic single-ring model                                                  #
# --------------------------------------------------------------------------- #
def equilibrium(k: float, n: float = 1.0, L: float = L_SPIN, c: float = C) -> dict:
    """Closed-form stationary point of E(r) = L c / r + k r^n."""
    r = (L * c / (n * k)) ** (1.0 / (n + 1.0))
    e_rot = L * c / r
    e_conf = k * r**n
    total = e_rot + e_conf
    share = e_rot / total
    return {
        "r": r,
        "E_rot": e_rot,
        "E_conf": e_conf,
        "E_total": total,
        "mass": total / c**2,
        "rot_share": share,
        "g": 1.0 / share,
    }


def g_factor(n: float) -> float:
    """g = (n+1)/n for confinement V = k r^n (charge on the circulating part)."""
    return (n + 1.0) / n


def tension_for_mass(m: float, L: float = L_SPIN, c: float = C) -> float:
    """Linear tension k [N] that makes the n=1 equilibrium carry rest mass m.

    n = 1:  m c^2 = 2 L c / r  and  k = L c / r^2   =>   k = m^2 c^3 / (4 L)
    with L = hbar/2:  k = m^2 c^3 / (2 hbar)        (electron: 0.1060 N)
    """
    return m**2 * c**3 / (4.0 * L)


def radius_for_mass(m: float, L: float = L_SPIN, c: float = C) -> float:
    """n = 1 equilibrium radius: r = 2 L / (m c)  (= hbar/(m c) for L = hbar/2)."""
    return 2.0 * L / (m * c)


def numeric_minimum(k: float, n: float = 1.0, L: float = L_SPIN, c: float = C) -> float:
    """Numerical check of the analytic radius. Works in the dimensionless
    variable s = r / r_guess, so the optimizer tolerance is not larger than r
    (the original script used xatol=1e-5 m on r ~ 1e-13 m and got r0/rc = 9.89).
    """
    r_guess = (L * c / (n * k)) ** (1.0 / (n + 1.0))

    def e(s):
        r = s * r_guess
        return (L * c / r + k * r**n) / (L * c / r_guess)

    res = minimize_scalar(e, bounds=(1e-3, 1e3), method="bounded", options={"xatol": 1e-12})
    return res.x * r_guess


def calibration_identity(m: float = M_E) -> float:
    """What the 'm_eff / m_e = 1.000' scripts actually compute.

    r_c is built FROM m, then m is recovered from r_c.  Returns m_eff/m, which is
    1 for every input m -- an identity, not a prediction.
    """
    r_c = HBAR / (m * C)
    m_eff = (HBAR * C / r_c) / C**2
    return m_eff / m


# --------------------------------------------------------------------------- #
# Four rings on the tetrahedral axes                                          #
# --------------------------------------------------------------------------- #
TETRA_TARGET = np.arccos(-1.0 / 3.0)


def _direction_penalty(v: np.ndarray) -> float:
    s = v.sum(axis=0)
    p = 10.0 * float(s @ s)
    for i in range(4):
        for j in range(i + 1, 4):
            cth = v[i] @ v[j] / (np.linalg.norm(v[i]) * np.linalg.norm(v[j]))
            p += 5.0 * (1.0 - np.cos(np.arccos(np.clip(cth, -1, 1)) - TETRA_TARGET)) ** 2
    return p


def tetra_energy(params: np.ndarray, k: float, n: float, L: float = 0.5) -> float:
    """Natural units (hbar = c = 1).  params = 4 vectors (12 numbers)."""
    v = params.reshape(4, 3)
    r = np.linalg.norm(v, axis=1)
    if np.any(r < 1e-9):
        return 1e9
    return _direction_penalty(v) + np.sum(L / r) + np.sum(k * r**n)


def tetra_minimum(k: float = 0.5, n: float = 1.0, L: float = 0.5, seed: int = 42) -> dict:
    rng = np.random.default_rng(seed)
    base = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / np.sqrt(3)
    x0 = (base + rng.normal(0, 0.1, (4, 3))).ravel()
    res = minimize(tetra_energy, x0, args=(k, n, L), method="L-BFGS-B")
    v = res.x.reshape(4, 3)
    r = np.linalg.norm(v, axis=1)
    e_rot = float(np.sum(L / r))
    e_conf = float(np.sum(k * r**n))
    share = e_rot / (e_rot + e_conf)
    return {"vectors": v, "r": r, "E_rot": e_rot, "E_conf": e_conf,
            "rot_share": share, "g": 1.0 / share, "E": float(res.fun)}


def old_potential(params: np.ndarray, L: float = 0.5) -> float:
    """The earlier potential (sum-zero + angle + L^2/2r^2).  Kept for the record:
    it decreases as 1/s^2 when the tetrahedron is scaled by s -> no minimum."""
    v = params.reshape(4, 3)
    r = np.linalg.norm(v, axis=1)
    return _direction_penalty(v) + np.sum(L**2 / (2 * r**2))
