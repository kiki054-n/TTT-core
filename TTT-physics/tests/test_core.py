"""Machine checks for every statement in docs/FOUNDATIONS.md.

Run:  pytest -q        (or: python tests/run_tests.py  without pytest)
Each test name says what is being asserted; "identity" / "refuted" tests pin
down results that are NOT evidence for the model, so they cannot silently return
as claims.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ttt_core import comparisons as K, geometry as G, ring_model as R  # noqa: E402
from ttt_core.constants import M_E  # noqa: E402


# ---------------- geometry (level A) ---------------------------------------
def test_tetrahedral_angle():
    angles = G.pair_angles_deg(G.TETRA)
    assert all(abs(a - 109.4712206) < 1e-6 for a in angles)
    assert np.allclose(G.TETRA.sum(axis=0), 0)


def test_sum_zero_does_not_fix_the_angle():
    v = G.SQUARE_COUNTEREXAMPLE
    assert np.allclose(v.sum(axis=0), 0)
    assert sorted(round(a) for a in G.pair_angles_deg(v)) == [90, 90, 90, 90, 180, 180]


def test_twelve_vectors_split_6_6_by_count_but_8_4_by_components():
    sp = G.split_about_axis(G.fcc12())
    assert sp["n_total"] == 12
    assert (sp["n_perpendicular"], sp["n_inclined"]) == (6, 6)
    assert abs(sp["axial_share_by_components"] - 4.0) < 1e-12


def test_fullerene_euler_rules():
    for n in (60, 70, 76, 78, 84):
        f = G.fullerene_faces(n)
        assert f["pentagons"] == 12 and f["euler"] == 2
    assert G.fullerene_faces(60)["hexagons"] == 20
    assert G.fullerene_faces(70)["hexagons"] == 25


def test_c60_angle_deficits():
    d = G.c60_angle_deficits()
    assert abs(d["per_vertex"] - math.pi / 15) < 1e-12
    assert abs(d["per_pentagon"] - math.pi / 3) < 1e-12
    assert abs(d["total"] - 4 * math.pi) < 1e-12


def test_37_is_not_an_icosahedral_shell():
    assert 37 not in G.ICOSAHEDRAL_ORBITS and 4 not in G.ICOSAHEDRAL_ORBITS
    assert 37 not in G.MACKAY_MAGIC and 37 not in G.MACKAY_SHELLS
    assert G.centered_hexagonal(4) == 37          # 37 is planar hexagonal


# ---------------- ring model (derived) -------------------------------------
def test_g_equals_2_only_for_linear_confinement():
    for n in (0.5, 1, 2, 3):
        eq = R.equilibrium(k=1.0, n=n, L=0.5, c=1.0)
        assert abs(eq["g"] - (n + 1) / n) < 1e-12
    assert R.g_factor(1) == 2.0


def test_tetra_rings_numeric_matches_analytic():
    for n in (1, 2, 3):
        assert abs(R.tetra_minimum(n=n)["g"] - R.g_factor(n)) < 1e-3


def test_electron_tension_and_radius():
    k = R.tension_for_mass(M_E)
    assert abs(k - 0.10600685) < 1e-6                     # N
    eq = R.equilibrium(k)
    assert abs(eq["mass"] / M_E - 1) < 1e-12
    assert abs(eq["rot_share"] - 0.5) < 1e-12
    assert abs(R.numeric_minimum(k) / R.radius_for_mass(M_E) - 1) < 1e-6


def test_mass_recovery_is_an_identity():
    """m_eff/m = 1 for ANY input mass -> not evidence."""
    for m in (M_E, 0.5 * M_E, 206.77 * M_E, 1.0):
        assert abs(R.calibration_identity(m) - 1) < 1e-12


def test_old_potential_has_no_minimum():
    e = [R.old_potential((G.TETRA * s).ravel()) for s in (1, 10, 100)]
    assert e[0] > e[1] > e[2] and abs(e[1] / e[2] - 100) < 1e-6


# ---------------- comparisons with data ------------------------------------
def test_alpha_ladder():
    a = K.alpha_ladder()
    assert abs(a["a0_over_lambdaC"] - 137.036) < 1e-3
    assert abs(a["lambdaC_over_re"] - 137.036) < 1e-3
    assert abs(a["hbar_c_over_a0_eV"] - 3728.94) < 0.01
    assert abs(a["kinetic_eV"] - 13.6057) < 1e-3
    assert abs(K.coulomb_vs_needed_force() - 137.036) < 1e-3


def test_unit_42_58_keV_and_platonic_counts():
    assert abs(K.UNIT_KEV - 42.5832) < 1e-3
    pm = K.platonic_masses()
    assert pm["tetrahedron"]["m_over_me"] == 1
    assert pm["cube"]["m_over_me"] == pm["octahedron"]["m_over_me"] == 2
    assert pm["dodecahedron"]["m_over_me"] == pm["icosahedron"]["m_over_me"] == 5


def test_additive_integer_rule_refuted():
    pu = K.particle_units()
    fr = [abs(v["frac"]) for k, v in pu.items() if k != "e"]
    assert min(fr) > 0.15            # no particle lands on an integer


def test_koide_45_degrees():
    k = K.koide_ratio()
    assert abs(k["Q"] - 2 / 3) < 1e-5
    assert abs(k["angle_to_body_diagonal_deg"] - 45) < 1e-3


def test_group_iv_power_law_not_supported():
    g = K.group_iv_scaling()
    assert abs(g["slope"] - 0.235) < 1e-3 and abs(g["r2"] - 0.858) < 1e-3
    assert max(g["local_slopes"]) / min(g["local_slopes"]) > 10      # kinked
    assert abs(g["Df_if_eta_0564"] - 2.40) < 0.01                    # circular by construction
    assert all(1.0 < r < 1.07 for r in g["a_over_covalent"])         # bond length explains a


def test_clapeyron_baseline_reproduces_the_ttt_line():
    c = K.clapeyron_graphite_diamond()
    assert abs(c["intercept_GPa"] - 1.006) < 1e-3
    assert abs(c["slope_GPa_per_K"] - 0.001786) < 1e-6
    assert abs(K.clapeyron_line(4000, c) - 8.15) < 0.01
