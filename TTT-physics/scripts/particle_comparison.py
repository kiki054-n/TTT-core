"""
scripts/particle_comparison.py
TTT-Core-Physics: electron as a massless ring + linear (O pi O) confinement.

What this script shows (and what it does not):
  * SHOWS   - E(r) = hbar c / (2r) + g_pi r has a genuine minimum, and at the
              minimum the rotational and confinement energies are EQUAL (1:1),
              which is exactly the condition for the magnetic g-factor g = 2.
  * DOES NOT derive m_e - g_pi is CALIBRATED from the measured Compton radius,
              so recovering m_e is an identity.  The one open number is the
              tension  g_pi = m_e^2 c^3 / (2 hbar) = 0.1060 N.
  * The "12-unit quantum" m_e c^2 / 12 = 42.58 keV is a division.  It is
              compatible with g = 2 only if the 12 lattice vectors are split
              6 (ring) : 6 (axis) as whole units (see docs/FOUNDATIONS.md s4).

Fixes against the first version:
  - minimize_scalar(bounded) default xatol = 1e-5 m is larger than r ~ 1e-13 m
    (it returned r0/rc = 9.89, m/m_e = 5.0).  We minimise in s = r / r_c.
  - plt.show() replaced by savefig so it runs headless / in CI.
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ttt_core.constants import C, EV, H, HBAR, M_E  # noqa: E402

R_C = HBAR / (M_E * C)                     # measured (reduced) Compton radius  <- INPUT
G_PI = HBAR * C / (2.0 * R_C**2)           # calibrated tension                 <- from INPUT


def energy(r, g_pi=G_PI):
    u_rot = HBAR * C / (2.0 * r)           # massless ring, L = hbar/2
    u_bind = g_pi * r                      # linear confinement
    return u_rot + u_bind, u_rot, u_bind


def main(outdir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")):
    res = minimize_scalar(lambda s: energy(s * R_C)[0] / (M_E * C**2),
                          bounds=(0.01, 100), method="bounded", options={"xatol": 1e-12})
    r0 = res.x * R_C
    e0, e_rot, e_bind = energy(r0)
    unit = e0 / 12

    print("=== [TTT] massless ring + linear confinement ===")
    print(f"tension g_pi (calibrated)    : {G_PI:.6e} N   <- the number to derive")
    print(f"r0 / r_C                     : {r0 / R_C:.9f}")
    print(f"E0                           : {e0 / EV / 1e6:.6f} MeV")
    print(f"m_emergent / m_e             : {e0 / C**2 / M_E:.9f}   (identity: g_pi came from m_e)")
    print(f"E_rot : E_bind               : {e_rot / e_bind:.6f}   -> g = E0/E_rot = {e0 / e_rot:.6f}")
    print(f"E0 / 12                      : {unit / EV / 1e3:.4f} keV,  lambda = hc/E = "
          f"{H * C / unit * 1e10:.4f} A (= 12 x Compton wavelength)")

    os.makedirs(outdir, exist_ok=True)
    s = np.linspace(0.15, 3.0, 400)
    tot, rot, bind = energy(s * R_C)
    mev = EV * 1e6
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(s, tot / mev, lw=2.2, label=r"$E_{\rm total}$")
    ax.plot(s, rot / mev, "--", label=r"ring (O): $\hbar c/2r$")
    ax.plot(s, bind / mev, "--", label=r"axis ($\pi$) confinement: $g_\pi r$")
    ax.axvline(1.0, color="k", ls=":", lw=1)
    ax.annotate(f"minimum at r = r_C\nE_rot = E_conf  ->  g = 2\nE0 = {e0 / mev:.4f} MeV",
                xy=(1.0, e0 / mev), xytext=(1.5, 1.5), arrowprops=dict(arrowstyle="->"))
    ax.set_xlabel(r"$r / r_C$   ($r_C=\hbar/m_ec$)")
    ax.set_ylabel("energy [MeV]")
    ax.set_ylim(0, 3.5)
    ax.set_title(r"Massless ring + linear $\pi$ confinement (tension calibrated to $m_e$)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = os.path.join(outdir, "electron_ring_energy.png")
    fig.savefig(path, dpi=150)
    print("saved", path)


if __name__ == "__main__":
    main()
