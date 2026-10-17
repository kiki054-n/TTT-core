"""
多面体の内圧・軸張力と陽子／電子の双極モデル（2026-10-17）の数値検算。

すべての値をこのスクリプトで再計算し、assert で確認する。
単位: 一辺 a = 1、内圧 P = 1（張力は P a^2 単位）。
"""
import itertools
import math

import numpy as np

SQ2, SQ3, SQ5 = math.sqrt(2), math.sqrt(3), math.sqrt(5)
PHI = (1 + SQ5) / 2


def close(x, y, tol=1e-9):
    return abs(x - y) <= tol * max(1.0, abs(y))


# ---------------------------------------------------------------- 第1部
# Block 1: 立方体と外接球
ratio_sphere_cube = (4 / 3) * math.pi * (SQ3 / 2) ** 3
assert close(ratio_sphere_cube, SQ3 * math.pi / 2)
assert close(round(ratio_sphere_cube, 4), 2.7207)
assert close(round(25 * ratio_sphere_cube, 2), 68.02)
assert close(round(125 * ratio_sphere_cube, 2), 340.09)


# Block 2: 正多面体を「頂点に面の力を等分配」で解く
def hull_faces(verts):
    """凸多面体の面（頂点インデックスの組）を返す。"""
    faces = set()
    n = len(verts)
    for i, j, k in itertools.combinations(range(n), 3):
        normal = np.cross(verts[j] - verts[i], verts[k] - verts[i])
        if np.linalg.norm(normal) < 1e-9:
            continue
        normal /= np.linalg.norm(normal)
        d = normal @ verts[i]
        side = verts @ normal - d
        if np.all(side <= 1e-7) or np.all(side >= -1e-7):
            on = tuple(sorted(np.where(np.abs(side) < 1e-7)[0]))
            faces.add(on)
    return list(faces)


def face_area_vector(verts, idx):
    pts = verts[list(idx)]
    c = pts.mean(axis=0)
    # 面内で角度順に並べる
    n0 = np.cross(pts[1] - pts[0], pts[2] - pts[0])
    n0 /= np.linalg.norm(n0)
    if n0 @ c < 0:
        n0 = -n0
    u = pts[0] - c
    u /= np.linalg.norm(u)
    w = np.cross(n0, u)
    ang = np.arctan2((pts - c) @ w, (pts - c) @ u)
    pts = pts[np.argsort(ang)]
    area = 0.0
    for p, q in zip(pts, np.roll(pts, -1, axis=0)):
        area += np.cross(p - c, q - c) @ n0 / 2
    return area * n0


def vertex_loads(verts):
    loads = np.zeros_like(verts)
    for f in hull_faces(verts):
        av = face_area_vector(verts, f)
        for v in f:
            loads[v] += av / len(f)
    return loads


def volume(verts):
    return sum(face_area_vector(verts, f) @ verts[list(f)].mean(axis=0)
               for f in hull_faces(verts)) / 3


def edge_length(verts):
    d = [np.linalg.norm(p - q) for p, q in itertools.combinations(verts, 2)]
    return min(d)


def normalize(verts):
    verts = np.array(verts, dtype=float)
    verts -= verts.mean(axis=0)
    return verts / edge_length(verts)


cube = normalize(list(itertools.product([-1, 1], repeat=3)))
octa = normalize([s * e for e in np.eye(3) for s in (1, -1)])
ico = normalize([p for a, b in itertools.product([-1, 1], repeat=2)
                 for p in ([0, a, b * PHI], [a, b * PHI, 0], [b * PHI, 0, a])])
dod = normalize(list(itertools.product([-1, 1], repeat=3)) +
                [p for a, b in itertools.product([-1, 1], repeat=2)
                 for p in ([0, a / PHI, b * PHI], [a / PHI, b * PHI, 0],
                           [b * PHI, 0, a / PHI])])

expected_axis_tension = {
    "cube": SQ3 / 4,
    "octa": 1 / 3,
    "ico": 5 * (3 + SQ5) / (12 * math.sqrt(10 + 2 * SQ5)),
    "dod": SQ3 * (5 + 2 * SQ5) / 20,
}
for name, v in [("cube", cube), ("octa", octa), ("ico", ico), ("dod", dod)]:
    L = vertex_loads(v)
    # 頂点の合力は中心→頂点方向（軸方向）と一致し、辺の力は0
    for p, f in zip(v, L):
        assert np.linalg.norm(np.cross(p, f)) < 1e-9
    T = np.linalg.norm(L[0])
    assert close(T, expected_axis_tension[name], 1e-7), (name, T)
    n_axes = len(v) // 2
    R = np.linalg.norm(v[0])
    assert close(n_axes * T * 2 * R, 3 * volume(v), 1e-7)  # ΣTL = 3PV

# 正四面体: 辺6本、節点法
tet = normalize([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
L = vertex_loads(tet)
F = np.linalg.norm(L[0])
assert close(F, SQ3 / 12)
cos_t = math.sqrt(2 / 3)
T_tet = F / (3 * cos_t)
assert close(T_tet, 1 / (12 * SQ2))
assert close(6 * T_tet * 1, 3 * volume(tet))


# Block 3: 双錘（全辺 1）
def bipyramid(n):
    rho = 1 / (2 * math.sin(math.pi / n))
    h = math.sqrt(1 - rho ** 2)
    eq = [[rho * math.cos(2 * math.pi * k / n), rho * math.sin(2 * math.pi * k / n), 0]
          for k in range(n)]
    return np.array(eq + [[0, 0, h], [0, 0, -h]]), rho, h


for n, T_ax_exp, T_eq_exp in [(3, SQ3 / 12, SQ2 / 9),
                              (5, math.sqrt(25 + 10 * SQ5) / 12, (5 + SQ5) / 30)]:
    v, rho, h = bipyramid(n)
    L = vertex_loads(v)
    apex = L[n]
    assert close(apex[0], 0, 1e-9) and close(apex[1], 0, 1e-9)
    T_ax = apex[2]
    assert close(T_ax, T_ax_exp)
    F_eq = np.linalg.norm(L[0])
    assert close(L[0][2], 0, 1e-9)
    half_int = (math.pi - 2 * math.pi / n) / 2  # 辺と放射方向のなす角
    T_eq = F_eq / (2 * math.cos(half_int))
    assert close(T_eq, T_eq_exp)
    V = volume(v)
    axis_share = T_ax * 2 * h
    assert close(axis_share + n * T_eq * 1, 3 * V)
    assert close(axis_share / (3 * V), 1 / 3)  # 軸 1/3・赤道 2/3


# ---------------------------------------------------------------- 第3部
def sum_inv_2d(pts):
    return [sum(1 / (2 * np.linalg.norm(p - q)) for q in pts if q is not p) for p in pts]


def unit(v):
    return v / np.linalg.norm(v, axis=1, keepdims=True)


tet_u = unit(tet)
oct_u = unit(octa)
bip_u = np.array([[math.cos(2 * math.pi * k / 3), math.sin(2 * math.pi * k / 3), 0]
                  for k in range(3)] + [[0, 0, 1], [0, 0, -1]])

for pts, N, ratio_exp, energy_exp in [(tet_u, 4, 0.2296, -0.7704), (oct_u, 6, 0.2774, -0.7226)]:
    s = sum_inv_2d(list(pts))
    assert max(s) - min(s) < 1e-12  # 全点同等
    assert round(s[0] / N, 4) == ratio_exp
    E_rep = sum(1 / np.linalg.norm(p - q) for p, q in itertools.combinations(pts, 2)) / N ** 2
    assert round(E_rep - 1, 4) == energy_exp

s = sum_inv_2d(list(bip_u))
assert round(s[3] / 5, 4) == 0.2621 and round(s[0] / 5, 4) == 0.2569
E_rep = sum(1 / np.linalg.norm(p - q) for p, q in itertools.combinations(bip_u, 2)) / 25
assert round(E_rep - 1, 4) == -0.7410

# 水素1sの自己クーロンエネルギー
HARTREE_EV = 27.211386
assert round(5 / 8 * HARTREE_EV, 1) == 17.0

# ---------------------------------------------------------------- 第4部
HBARC = 197.3269804          # MeV fm
MP = 938.27208816            # MeV
ME = 0.51099895              # MeV
ALPHA_INV = 137.035999177
A0 = 52917.721               # fm
RP_2022, DRP_2022 = 0.84075, 0.00064
RP_2018 = 0.8414

lam_p = HBARC / MP
lam_e = HBARC / ME
assert round(lam_p, 6) == 0.210309
assert round(A0 / lam_e, 3) == round(ALPHA_INV, 3)
r22 = RP_2022 / lam_p
assert round(r22, 4) == 3.9977
assert round(abs(4 - r22) / (DRP_2022 / lam_p), 2) == 0.76
assert round(RP_2018 / lam_p, 4) == 4.0008
assert round(HBARC / RP_2022, 1) == 234.7
assert round(2 * ALPHA_INV, 2) == 274.07
assert round(ALPHA_INV / 4, 2) == 34.26

print("all checks passed")
