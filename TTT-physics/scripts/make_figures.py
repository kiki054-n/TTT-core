"""Regenerate every figure in figures/ from the ttt_core package.

    python scripts/make_figures.py
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ttt_core import comparisons as K, geometry as G, ring_model as R  # noqa: E402
from ttt_core.constants import GROUP_IV  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 110, "axes.grid": True, "grid.alpha": 0.3})


def save(fig, name):
    fig.tight_layout()
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print("saved", os.path.normpath(p))


def fig_g_vs_n():
    n = np.linspace(0.5, 4, 200)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(n, R.g_factor(n), lw=2, label=r"analytic $g=(n+1)/n$")
    ns = [1, 2, 3]
    ax.plot(ns, [R.tetra_minimum(n=k)["g"] for k in ns], "o", ms=8,
            label=r"numeric, 4 rings on tetrahedral axes")
    ax.axhline(2.0023, color="C3", ls="--", label="electron (measured) 2.0023")
    ax.set_xlabel(r"confinement exponent $n$  in  $V=k\,r^n$")
    ax.set_ylabel("g-factor")
    ax.set_title(r"Massless ring $Lc/r$ + confinement $k r^n$: only $n=1$ gives $g=2$")
    ax.legend()
    save(fig, "g_factor_vs_confinement.png")


def fig_old_potential():
    s = np.logspace(-0.5, 3, 200)
    e = [R.old_potential((G.TETRA * x).ravel()) for x in s]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.loglog(s, e, lw=2)
    ax.set_xlabel("scale of the tetrahedron  s")
    ax.set_ylabel("potential")
    ax.set_title(r"Earlier potential (sum-zero + angle + $L^2/2r^2$): no minimum, $\propto 1/s^2$")
    save(fig, "old_potential_no_minimum.png")


def fig_fcc_split():
    sp = G.split_about_axis(G.fcc12())
    fig, ax = plt.subplots(figsize=(7, 4.5))
    labels = ["count whole vectors\n(6 perpendicular : 6 inclined)",
              "split by components\n(isotropy: 8 : 4)"]
    ring = [sp["n_perpendicular"], 12 - sp["axial_share_by_components"]]
    axis = [sp["n_inclined"], sp["axial_share_by_components"]]
    ax.bar(labels, ring, label="ring (O)")
    ax.bar(labels, axis, bottom=ring, label=r"axis ($\pi$)")
    for i, r in enumerate(ring):
        ax.text(i, 12.3, f"g = {12 / r:.2f}", ha="center", fontsize=12)
    ax.set_ylim(0, 14)
    ax.set_ylabel("lattice units (of 12)")
    ax.set_title(r"12 lattice vectors seen from one O$\pi$O axis (111)")
    ax.legend(loc="lower right")
    save(fig, "twelve_vectors_split.png")


def fig_particle_units():
    pu = K.particle_units()
    names = [k for k in pu if k != "e"]
    fr = [pu[k]["frac"] for k in names]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(names, fr, color="C1")
    ax.axhspan(-0.5, 0.5, color="0.9", zorder=-1)
    ax.axhline(0, color="k", lw=1)
    ax.set_ylim(-0.5, 0.5)
    ax.set_ylabel(r"distance to nearest integer  (units of $m_e/12$ = 42.58 keV)")
    ax.set_title("Measured masses are not integer multiples of m_e/12")
    save(fig, "mass_units_residuals.png")


def fig_group_iv():
    names = list(GROUP_IV)
    M = np.array([GROUP_IV[k]["M"] for k in names])
    a = np.array([GROUP_IV[k]["a"] for k in names])
    rc = np.array([GROUP_IV[k]["r_cov"] for k in names])
    gs = K.group_iv_scaling()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.5))
    a1.loglog(M, a, "o-", ms=8)
    mm = np.linspace(10, 130, 50)
    s, b = np.polyfit(np.log(M), np.log(a), 1)
    a1.loglog(mm, np.exp(b) * mm**s, "--", label=f"power-law fit, slope {gs['slope']:.3f}, $R^2$={gs['r2']:.2f}")
    for x, y, t in zip(M, a, names):
        a1.annotate(t, (x, y), textcoords="offset points", xytext=(5, -12))
    a1.set_xlabel("atomic mass [u]")
    a1.set_ylabel("lattice constant a [Å]")
    a1.set_title("vs mass: kinked (local slopes 0.49 / 0.04 / 0.28)")
    a1.legend(fontsize=8)
    x = np.linspace(0.6, 1.5, 10)
    a2.plot(x, 8 / np.sqrt(3) * x, "--", label=r"$a = (8/\sqrt{3})\,r_{\rm cov}$ (no fit)")
    a2.plot(rc, a, "o", ms=8)
    for xx, y, t in zip(rc, a, names):
        a2.annotate(t, (xx, y), textcoords="offset points", xytext=(5, -12))
    a2.set_xlabel("covalent radius [Å]")
    a2.set_ylabel("lattice constant a [Å]")
    a2.set_title("vs covalent radius: straight, within 1-6 %")
    a2.legend()
    save(fig, "group_iv_lattice.png")


def fig_clapeyron():
    c = K.clapeyron_graphite_diamond()
    T = np.linspace(0, 4000, 100)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(T, K.clapeyron_line(T, c), lw=2,
            label=f"Clapeyron from tables: {c['intercept_GPa']:.3f} + {c['slope_GPa_per_K']:.6f} T")
    ax.text(300, 6.5, "diamond", fontsize=12)
    ax.text(2600, 2.0, "graphite", fontsize=12)
    ax.set_xlabel("T [K]")
    ax.set_ylabel("P [GPa]")
    ax.set_title("Graphite-diamond baseline (no TTT input).\n"
                 f"TTT must supply dH = {c['dH_eV_per_atom']:.3f} eV/atom and dS = {c['dS_kB_per_atom']:.2f} kB/atom")
    ax.legend(loc="upper left", fontsize=8)
    save(fig, "graphite_diamond_baseline.png")


if __name__ == "__main__":
    fig_g_vs_n()
    fig_old_potential()
    fig_fcc_split()
    fig_particle_units()
    fig_group_iv()
    fig_clapeyron()
