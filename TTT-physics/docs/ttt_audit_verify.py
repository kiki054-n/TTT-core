#!/usr/bin/env python3
"""
ttt_audit_verify.py — 「TTT理論の再評価」HTML文書の照合スクリプト
2026-09-11 / 全 assert 通過で検証完了

依存: numpy, scipy
実行: python3 ttt_audit_verify.py
"""
import itertools
import math

import numpy as np
from scipy.optimize import minimize

np.random.seed(2)
OK = "  [OK]"


# ----------------------------------------------------------------------
# 1. Tersoff の角度項 g(theta)
# ----------------------------------------------------------------------
def tersoff_g(theta_deg, c, d, h):
    """g(th) = 1 + c^2/d^2 - c^2/[d^2 + (cos th - h)^2]. 最小は cos th = h で g = 1."""
    x = math.cos(math.radians(theta_deg)) - h
    return 1.0 + c**2 / d**2 - c**2 / (d**2 + x**2)


def check_tersoff():
    print("[1] Tersoff g(theta) — 文書の数値は h を -1/3 に差し替えたもの")
    # 公表パラメータ (Tersoff 1988, carbon)
    cC, dC, hC = 3.8049e4, 4.3484, -0.57058
    cS, dS, hS = 1.0039e5, 16.217, -0.59825

    th_min_C = math.degrees(math.acos(hC))
    th_min_S = math.degrees(math.acos(hS))
    print(f"    C : g の最小は theta = {th_min_C:.2f} deg (g = {tersoff_g(th_min_C, cC, dC, hC):.4f})")
    print(f"    Si: g の最小は theta = {th_min_S:.2f} deg")
    assert abs(th_min_C - 124.79) < 0.02, "炭素の最小角"
    assert abs(th_min_S - 126.74) < 0.02, "シリコンの最小角"
    assert abs(tersoff_g(th_min_C, cC, dC, hC) - 1.0) < 1e-3

    g109 = tersoff_g(109.4712, cC, dC, hC)
    g120 = tersoff_g(120.0, cC, dC, hC)
    g090 = tersoff_g(90.0, cC, dC, hC)
    print(f"    実際: g(90)={g090:.4e}  g(109.47)={g109:.4e}  g(120)={g120:.4e}")
    print(f"    -> g(109.47)/g(120) = {g109 / g120:.1f} : 四面体角の方が強く罰される")
    assert g109 > g120, "公表パラメータでは四面体角が黒鉛角より高い"
    assert abs(g109 / g120 - 11.3) < 0.3

    # h を四面体角に差し替えると文書の数値が再現される
    h_tet = -1.0 / 3.0
    g109b = tersoff_g(109.4712, cC, dC, h_tet)
    g120b = tersoff_g(120.0, cC, dC, h_tet)
    g090b = tersoff_g(90.0, cC, dC, h_tet)
    print(f"    h=-1/3 に差し替え: g(109.47)={g109b:.4f}  g(120)={g120b:.3e}  g(90)={g090b:.3e}")
    print("    -> 文書の主張 g(109.47)=1 / g(120)~1e5 / g(90)~4e5 と一致")
    assert abs(g109b - 1.0) < 1e-3, "差し替えると 109.47 が最小になる"
    assert 0.9e5 < g120b < 1.5e5, "文書の ~1e5"
    assert 3.5e5 < g090b < 5.5e5, "文書の ~4e5"
    print(OK)


# ----------------------------------------------------------------------
# 2. sum v = 0 は 109.47 度を一意に定めない
# ----------------------------------------------------------------------
def check_sum_zero_not_unique():
    print("\n[2] sum v = 0 だけでは角は一意でない（正方平面が反例）")
    sq = np.array([[1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0]], float)
    assert np.linalg.norm(sq.sum(0)) < 1e-12, "正方平面も sum v = 0"
    dots = sorted(round(sq[i] @ sq[j], 6) for i, j in itertools.combinations(range(4), 2))
    print(f"    正方平面: |sum v| = 0, 内積 = {dots}  (90 deg / 180 deg)")
    assert dots == [-1.0, -1.0, 0.0, 0.0, 0.0, 0.0]

    # 全対等内積を課すと一意（Gram 行列の階数）
    G = np.full((4, 4), -1.0 / 3.0)
    np.fill_diagonal(G, 1.0)
    ev = np.linalg.eigvalsh(G)
    rank = int(np.sum(ev > 1e-9))
    print(f"    全対 -1/3 の Gram 固有値 = {np.round(ev, 6)} -> 階数 {rank}, O(3) を除き一意")
    assert rank == 3
    print(OK)


# ----------------------------------------------------------------------
# 3. トムソン問題 N=20 : 正十二面体は最小解でない
# ----------------------------------------------------------------------
def thomson_energy_grad(x):
    P = x.reshape(-1, 3)
    n = np.linalg.norm(P, axis=1, keepdims=True)
    Q = P / n
    diff = Q[:, None, :] - Q[None, :, :]
    dm = np.linalg.norm(diff, axis=-1)
    np.fill_diagonal(dm, np.inf)
    U = 0.5 * np.sum(1.0 / dm)
    gq = -np.sum(diff / dm[:, :, None] ** 3, axis=1)
    gp = (gq - np.sum(gq * Q, axis=1, keepdims=True) * Q) / n
    return U, gp.ravel()


def dodecahedron():
    phi = (1 + math.sqrt(5)) / 2
    V = [[s1, s2, s3] for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [[0, s1 / phi, s2 * phi], [s1 / phi, s2 * phi, 0], [s1 * phi, 0, s2 / phi]]
    V = np.array(V, float)
    return V / np.linalg.norm(V, axis=1, keepdims=True)


def check_thomson(restarts=60):
    print("\n[3] トムソン問題 N=20 : 正十二面体は大域最小ではない")
    D = dodecahedron()
    assert D.shape == (20, 3)
    U_dod = thomson_energy_grad(D.ravel())[0]

    best = np.inf
    for _ in range(restarts):
        r = minimize(thomson_energy_grad, np.random.normal(size=60),
                     jac=True, method="L-BFGS-B", options={"maxiter": 3000})
        best = min(best, r.fun)
    print(f"    正十二面体 U = {U_dod:.6f}")
    print(f"    大域最小   U = {best:.6f}  (文献値 150.881568)")
    print(f"    差 = +{U_dod - best:.6f}")
    assert abs(best - 150.881568) < 1e-3, "文献値と一致"
    assert U_dod - best > 0.5, "正十二面体は有意に高い"

    T = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
    T /= np.linalg.norm(T, axis=1, keepdims=True)
    U_tet = thomson_energy_grad(T.ravel())[0]
    print(f"    (N=4 正四面体 U = {U_tet:.6f} — これは最小解)")
    assert abs(U_tet - 3.674235) < 1e-5
    print(OK)


# ----------------------------------------------------------------------
# 4. Goldberg-Coxeter : 20 はレシュ数でない
# ----------------------------------------------------------------------
def check_goldberg_coxeter():
    print("\n[4] Goldberg-Coxeter N = 20(m^2+mn+n^2) : 殻数 20 は写像できない")
    L = {m * m + m * n + n * n for m in range(30) for n in range(30)}
    small = sorted(t for t in L if 0 < t <= 30)
    print(f"    レシュ数 (<=30): {small}")
    for t in (1, 4, 20, 12):
        inL = t in L
        print(f"      T={t:2d}  レシュ数か: {str(inL):5s}  N=20T -> {20 * t if inL else 'n/a'}")
    assert 1 in L and 4 in L and 12 in L
    assert 20 not in L, "20 は m^2+mn+n^2 の形に書けない"
    assert 20 * 3 == 60 and 3 in L, "C60 は T=3"
    assert 20 * 12 == 240, "C240 は T=12"
    print(OK)


# ----------------------------------------------------------------------
# 5. 5 本の単位ベクトルで全対 -1/4 は 3 次元に存在しない
# ----------------------------------------------------------------------
def E5(x, k1=1.0, k2=1.0, c=-0.25):
    V = x.reshape(5, 3)
    V = V / np.linalg.norm(V, axis=1, keepdims=True)
    t1 = np.linalg.norm(V.sum(0)) ** 2
    t2 = sum((V[i] @ V[j] - c) ** 2 for i, j in itertools.combinations(range(5), 2))
    return k1 * t1 + k2 * t2


def check_five_fold(restarts=200):
    print("\n[5] 5 本で全対 -1/4 は 4 次元の対象（3D に存在しない）")
    for n, c in ((4, -1 / 3), (5, -1 / 4), (6, -1 / 5)):
        G = np.full((n, n), c)
        np.fill_diagonal(G, 1.0)
        ev = np.linalg.eigvalsh(G)
        rank = int(np.sum(ev > 1e-9))
        print(f"    n={n} c={c:+.4f} ({math.degrees(math.acos(c)):.3f} deg) 階数 {rank}")
        assert rank == n - 1 if n == 4 else True
    G5 = np.full((5, 5), -0.25)
    np.fill_diagonal(G5, 1.0)
    assert int(np.sum(np.linalg.eigvalsh(G5) > 1e-9)) == 4, "5 本 -1/4 は階数 4 = 4 次元"

    # 全対 -1/4 なら和は厳密にゼロ（提示の 0.287 と不整合）
    assert abs(5 + 2 * 10 * (-0.25)) < 1e-12

    best = None
    for _ in range(restarts):
        r = minimize(E5, np.random.normal(size=15), method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    V = best.x.reshape(5, 3)
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    print(f"    3D での大域最小 E5 = {best.fun:.4f}  |sum v| = {np.linalg.norm(V.sum(0)):.4f}")
    assert abs(best.fun - 1.125) < 1e-3, "三方両錐の 1.125"

    tbp = np.array([[1, 0, 0], [-0.5, math.sqrt(3) / 2, 0], [-0.5, -math.sqrt(3) / 2, 0],
                    [0, 0, 1], [0, 0, -1]], float)
    assert abs(E5(tbp.ravel()) - 1.125) < 1e-12, "三方両錐 = 1.125"
    print("    三方両錐 1.1250 / 正五角形 3.1250 / 四角錐 2.6250 — 提示の 2.44 はどれでもない")
    print(OK)


# ----------------------------------------------------------------------
# 6. 配向結合: 二乗は厳密に定数、三次は分裂する
# ----------------------------------------------------------------------
def tetra():
    T = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
    return T / np.linalg.norm(T, axis=1, keepdims=True)


def rand_rot():
    q = np.random.normal(size=4)
    q /= np.linalg.norm(q)
    w, x, y, z = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def check_orientation(trials=20000):
    print("\n[6] E_int = -J sum (vA.vB)^2 は相対回転に厳密に依存しない")
    T = tetra()
    M = sum(np.outer(v, v) for v in T)
    assert np.allclose(M, (4 / 3) * np.eye(3)), "正四面体は等方タイトフレーム (4/3)I"
    s2 = []
    s3 = []
    for _ in range(trials):
        B = T @ rand_rot().T
        s2.append(sum((T[i] @ B[j]) ** 2 for i in range(4) for j in range(4)))
        s3.append(sum((T[i] @ B[j]) ** 3 for i in range(4) for j in range(4)))
    print(f"    二乗: min={min(s2):.10f}  max={max(s2):.10f}  (16/3 = {16/3:.10f})")
    assert max(s2) - min(s2) < 1e-9, "回転に依存しない"
    assert abs(np.mean(s2) - 16 / 3) < 1e-9
    ecl = sum((T[i] @ T[j]) ** 2 for i in range(4) for j in range(4))
    stg = sum((T[i] @ (-T[j])) ** 2 for i in range(4) for j in range(4))
    assert abs(ecl - stg) < 1e-12, "eclipsed と staggered が同値"
    print("    -> eclipsed と staggered が同値。staggered は導けない")

    M3 = np.zeros((3, 3, 3))
    for v in T:
        M3 += np.einsum("i,j,k->ijk", v, v, v)
    print(f"    三次: 八極モーメントのノルム = {np.linalg.norm(M3):.6f} (非ゼロ)")
    ecl3 = sum((T[i] @ T[j]) ** 3 for i in range(4) for j in range(4))
    stg3 = sum((T[i] @ (-T[j])) ** 3 for i in range(4) for j in range(4))
    print(f"    三次: eclipsed = {ecl3:+.6f}  staggered = {stg3:+.6f}  分裂 = {ecl3 - stg3:.6f} (64/9)")
    assert abs(ecl3 - 32 / 9) < 1e-12 and abs(stg3 + 32 / 9) < 1e-12
    assert abs((ecl3 - stg3) - 64 / 9) < 1e-12
    assert max(s3) <= 32 / 9 + 1e-9, "三次の極値は eclipsed / staggered"
    print(OK)


# ----------------------------------------------------------------------
# 7. 体積と格子定数
# ----------------------------------------------------------------------
def check_volumes():
    print("\n[7] C60 -> ダイヤモンドは圧縮（文書の 2.99 A^3 は約 4 倍違い）")
    a_dia = 3.567
    v_dia = a_dia**3 / 8
    a_c60 = 14.17
    v_c60 = a_c60**3 / 240  # fcc, 4 分子 x 60 原子
    print(f"    ダイヤ {v_dia:.4f} A^3/atom, fcc C60 {v_c60:.4f} A^3/atom -> 比 {v_dia / v_c60:.4f}")
    assert abs(v_dia - 5.6731) < 1e-3
    assert abs(v_c60 - 11.8549) < 1e-3
    assert v_dia < v_c60, "ダイヤの方が小さい = 圧縮"
    assert abs(v_c60 / 2.99 - 3.96) < 0.05, "文書の 2.99 は約 3.96 倍違い"
    v_gra = 8.78
    print(f"    黒鉛 {v_gra} -> 比 {v_dia / v_gra:.4f} : 分子性/層状 -> 網目はどれも約半分")
    print(OK)


def check_lattice_options():
    print("\n[8] 125 -> 3.567 A の A / B / C")
    a_dia, a0, alpha = 3.567, 0.529177, 1 / 137.035999
    print(f"    A: 3.567/5 = {a_dia / 5:.4f} (主張の「スケール因子」の言い換え)")
    assert abs(a_dia / 5 - 0.7134) < 1e-3
    print(f"    B: a0/alpha = {a0 / alpha:.3f} A, 必要な f(phi) = {a_dia / (5 * a0 / alpha):.5f}")
    assert abs(a_dia / (5 * a0 / alpha) - 0.00984) < 1e-4
    d_cc = a_dia * math.sqrt(3) / 4
    cval = 5 * d_cc / math.sqrt(3) * math.sqrt(2)
    print(f"    C: 5*d/sqrt3*sqrt2 = {cval:.4f} A ({cval / a_dia:.2f} 倍) ; d 代入で a=(5sqrt2/4)a の自己矛盾")
    assert abs(cval - 6.3056) < 1e-3
    assert abs(cval / a_dia - 5 * math.sqrt(2) / 4) < 1e-9
    print(OK)


# ----------------------------------------------------------------------
# 9. 転位線の周期（線エネルギー <-> サイトエネルギー）
# ----------------------------------------------------------------------
def check_dislocation_period():
    print("\n[9] 転位芯: 線エネルギーとサイトエネルギーの換算")
    a = 3.567
    b = a / math.sqrt(6)
    p_sp = a / math.sqrt(2)
    print(f"    90deg partial |b| = a/sqrt6 = {b:.4f} A")
    print(f"    <110> 線方向の繰り返し: SP = {p_sp:.4f} A, DP = {2 * p_sp:.4f} A")
    assert abs(b - 1.4562) < 1e-3 and abs(p_sp - 2.5222) < 1e-3
    for E in (1.5, 2.5):
        print(f"      {E} eV/A -> 1 周期あたり {E * p_sp:.2f} eV (DP で {2 * E * p_sp:.2f} eV)")
    print(OK)


if __name__ == "__main__":
    print("=" * 72)
    print("ttt_audit_verify.py — 2026-09-11")
    print("=" * 72)
    check_tersoff()
    check_sum_zero_not_unique()
    check_thomson()
    check_goldberg_coxeter()
    check_five_fold()
    check_orientation()
    check_volumes()
    check_lattice_options()
    check_dislocation_period()
    print("\n" + "=" * 72)
    print("全 assert 通過")
    print("=" * 72)
