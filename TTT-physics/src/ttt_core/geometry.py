"""Tetrahedral / FCC / Platonic / fullerene geometry used by TTT-Core.

Everything here is exact geometry (level A): true regardless of physics.
"""
from __future__ import annotations

import itertools
import math

import numpy as np

# --------------------------------------------------------------------------- #
# Tetrahedron                                                                 #
# --------------------------------------------------------------------------- #
TETRA = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / math.sqrt(3)
TETRA_ANGLE_DEG = math.degrees(math.acos(-1.0 / 3.0))  # 109.4712...

# Four unit vectors summing to zero that are NOT a tetrahedron (square in a plane).
# => "sum = 0" alone does not fix 109.47 deg; "all pair angles equal" is the extra axiom.
SQUARE_COUNTEREXAMPLE = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]], float)


def pair_angles_deg(v: np.ndarray) -> list[float]:
    out = []
    for i, j in itertools.combinations(range(len(v)), 2):
        c = v[i] @ v[j] / (np.linalg.norm(v[i]) * np.linalg.norm(v[j]))
        out.append(math.degrees(math.acos(max(-1.0, min(1.0, c)))))
    return out


# --------------------------------------------------------------------------- #
# The 12 lattice vectors (directed edges of T+ / T-  =  FCC nearest neighbours) #
# --------------------------------------------------------------------------- #
def fcc12() -> np.ndarray:
    vecs = set()
    for p in itertools.permutations([1, 1, 0]):
        for s in itertools.product([1, -1], repeat=3):
            v = tuple(a * b for a, b in zip(p, s))
            vecs.add(v)
    return np.array(sorted(vecs), float)


def split_about_axis(vectors: np.ndarray, axis=(1, 1, 1)) -> dict:
    """Count vectors perpendicular vs inclined to an axis, and the axial energy
    share if energy were split by squared projection (isotropy -> N/3)."""
    n = np.asarray(axis, float)
    n /= np.linalg.norm(n)
    cos = vectors @ n / np.linalg.norm(vectors, axis=1)
    perp = int(np.sum(np.abs(cos) < 1e-12))
    return {
        "n_total": len(vectors),
        "n_perpendicular": perp,
        "n_inclined": len(vectors) - perp,
        "axial_share_by_components": float(np.sum(cos**2)),  # = N/3 for cubic sets
    }


# --------------------------------------------------------------------------- #
# Platonic solids                                                             #
# --------------------------------------------------------------------------- #
PLATONIC = {  # (V, E, F)
    "tetrahedron": (4, 6, 4),
    "cube": (8, 12, 6),
    "octahedron": (6, 12, 8),
    "dodecahedron": (20, 30, 12),
    "icosahedron": (12, 30, 20),
}

# Orbit sizes of the full icosahedral group I_h acting on points (no 4, no 37).
ICOSAHEDRAL_ORBITS = (1, 12, 20, 30, 60, 120)
# Mackay icosahedral cluster magic numbers and shell sizes.
MACKAY_MAGIC = (1, 13, 55, 147, 309)
MACKAY_SHELLS = (12, 42, 92, 162)


def centered_hexagonal(k: int) -> int:
    """1, 7, 19, 37, 61, 91 ...  (37 is PLANAR hexagonal, k = 4)."""
    return 3 * k * (k - 1) + 1


# --------------------------------------------------------------------------- #
# Fullerenes (Euler / Gauss-Bonnet)                                           #
# --------------------------------------------------------------------------- #
def fullerene_faces(n_atoms: int) -> dict:
    """Any closed cage of 3-valent atoms with only pentagons and hexagons:
    pentagons = 12 always (Euler),  hexagons = N/2 - 10."""
    return {"pentagons": 12, "hexagons": n_atoms // 2 - 10,
            "edges": 3 * n_atoms // 2, "euler": n_atoms - 3 * n_atoms // 2 + (12 + n_atoms // 2 - 10)}


def c60_angle_deficits() -> dict:
    """Vertex of C60: two hexagons + one pentagon -> 120+120+108 = 348 deg."""
    vertex = 2 * math.pi - math.radians(120 + 120 + 108)       # pi/15
    per_pentagon = 5 * vertex                                   # pi/3 (isolated pentagons)
    return {"per_vertex": vertex, "per_pentagon": per_pentagon,
            "total": 60 * vertex}                               # 4 pi  (Gauss-Bonnet)
