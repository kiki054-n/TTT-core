#!/usr/bin/env python3
"""
ttt_fivefold_verify.py — 「7.356 度の行き先」補注の検算
2026-09-11 / 全 assert 通過で検証完了

依存: numpy, scipy
実行: python3 ttt_fivefold_verify.py
"""
import itertools
import math

import numpy as np
from scipy.optimize import minimize

np.random.seed(3)
OK = "  [OK]"
EV = 1.602176634e-19  # J per eV


# ----------------------------------------------------------------------
# §1 幾何 — 7.356103 度と恒等式
# ----------------------------------------------------------------------
def check_geometry():
    print("[1] 5 個の正四面体は 1 辺のまわりで閉じない")
    dih = math.degrees(math.acos(1 / 3))
    bond = math.degrees(math.acos(-1 / 3))
    print(f"    二面角 = arccos(1/3)  = {dih:.6f} deg")
    print(f"    結合角 = arccos(-1/3) = {bond:.6f} deg")
    assert abs(dih - 70.528779) < 1e-6
    assert abs(bond - 109.471221) < 1e-6
    assert abs(dih + bond - 180.0) < 1e-12, "二面角 + 結合角 = 180"

    for k in (3, 4, 5, 6):
        print(f"     k={k}: 合計 {k * dih:11.6f} deg  隙間 {360 - k * dih:+11.6f} deg")
    gap = 360 - 5 * dih
    assert abs(gap - 7.356103) < 1e-6, "5 個での隙間"
    assert 360 - 4 * dih > 0 and 360 - 6 * dih < 0, "5 個だけが「わずかに閉じない」"

    per = gap / 5
    print(f"    1 領域あたり = {per:.6f} deg")
    # 恒等式: per = 72 - dih = bond - 108
    print(f"      72 - 二面角  = {72 - dih:.6f}")
    print(f"      結合角 - 108 = {bond - 108:.6f}")
    assert abs(per - (72 - dih)) < 1e-12, "恒等式 per = 72 - dih"
    assert abs(per - (bond - 108)) < 1e-12, "恒等式 per = bond - 108"
    print("    -> 恒等式: 四面体結合角が正五角形の内角を超える分 = 5 回対称の食い違い")

    # 頂点まわり（二十面体版）
    sa = 3 * math.acos(1 / 3) - math.pi
    deficit = 4 * math.pi - 20 * sa
    print(f"    正四面体の立体角 = {sa:.6f} sr, 20 個 = {20 * sa:.6f} sr")
    print(f"    4pi = {4 * math.pi:.6f} sr -> 不足 {deficit:.6f} sr ({100 * deficit / (4 * math.pi):.2f}%)")
    assert abs(sa - 0.551286) < 1e-6
    assert abs(deficit - 1.540659) < 1e-6
    contraction = math.sin(2 * math.pi / 5)
    print(f"    Mackay 二十面体の動径収縮 sin(2pi/5) = {contraction:.6f} -> {100 * (1 - contraction):.2f}% 短縮")
    assert abs(contraction - 0.951057) < 1e-6
    print(OK)
    return gap


# ----------------------------------------------------------------------
# §2 双錐族
# ----------------------------------------------------------------------
def bipyramid(n):
    """n 角双錐の頂点を中心からの単位ベクトルとして返す（n+2 本）。"""
    V = [[math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n), 0] for k in range(n)]
    V += [[0, 0, 1], [0, 0, -1]]
    V = np.array(V, float)
    return V / np.linalg.norm(V, axis=1, keepdims=True)


def check_bipyramids():
    print("\n[2] 双錐族 B_n : B_4 = 正八面体だけが特別")
    for n in range(3, 7):
        V = bipyramid(n)
        m = len(V)
        assert m == n + 2
        dots = sorted({round(V[i] @ V[j], 4) for i, j in itertools.combinations(range(m), 2)})
        M = sum(np.outer(v, v) for v in V)
        iso = np.allclose(M, (m / 3) * np.eye(3), atol=1e-9)
        print(f"    B_{n}: 頂点{m:2d} 辺{3 * n:2d} 面{2 * n:2d}  |sum v|={np.linalg.norm(V.sum(0)):.4f}"
              f"  内積={dots}  等方タイトフレーム={iso}")
        assert np.linalg.norm(V.sum(0)) < 1e-12, "どの双錐も sum v = 0"
        assert iso == (n == 4), "等方タイトフレームは B_4 のみ"
        assert len(dots) >= 2, "全対等内積は不可能（軸-軸 と 軸-赤道 が別クラス）"
    M4 = sum(np.outer(v, v) for v in bipyramid(4))
    assert np.allclose(M4, 2 * np.eye(3)), "B_4 は sum v v^T = 2I"
    print("    -> 全対等内積が可能なのは正四面体（4 本・1 クラス）のみ = 特異点")
    print(OK)


# ----------------------------------------------------------------------
# §2 トムソン問題
# ----------------------------------------------------------------------
def thomson(x):
    P = x.reshape(-1, 3)
    nn = np.linalg.norm(P, axis=1, keepdims=True)
    Q = P / nn
    diff = Q[:, None, :] - Q[None, :, :]
    dm = np.linalg.norm(diff, axis=-1)
    np.fill_diagonal(dm, np.inf)
    U = 0.5 * np.sum(1.0 / dm)
    gq = -np.sum(diff / dm[:, :, None] ** 3, axis=1)
    gp = (gq - np.sum(gq * Q, axis=1, keepdims=True) * Q) / nn
    return U, gp.ravel()


def global_min(N, restarts=40):
    best = np.inf
    for _ in range(restarts):
        r = minimize(thomson, np.random.normal(size=3 * N), jac=True,
                     method="L-BFGS-B", options={"maxiter": 3000})
        best = min(best, r.fun)
    return best


def dodecahedron():
    phi = (1 + math.sqrt(5)) / 2
    V = [[s1, s2, s3] for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [[0, s1 / phi, s2 * phi], [s1 / phi, s2 * phi, 0], [s1 * phi, 0, s2 / phi]]
    V = np.array(V, float)
    return V / np.linalg.norm(V, axis=1, keepdims=True)


def check_thomson():
    print("\n[3] トムソン問題 : 双錐は N=5,6,7 で大域最小、正十二面体は N=20 で落ちる")
    for n, label in ((3, "三方両錐"), (4, "正八面体"), (5, "五角双錐")):
        V = bipyramid(n)
        N = len(V)
        u = thomson(V.ravel())[0]
        gm = global_min(N)
        print(f"    N={N}  {label:6s} U={u:.6f}   大域最小 U={gm:.6f}   差 {u - gm:+.2e}")
        assert abs(u - gm) < 1e-6, f"N={N} で双錐が大域最小"
    D = dodecahedron()
    u20 = thomson(D.ravel())[0]
    gm20 = global_min(20, restarts=60)
    print(f"    N=20 正十二面体 U={u20:.6f}   大域最小 U={gm20:.6f}   差 {u20 - gm20:+.6f}")
    assert abs(gm20 - 150.881568) < 1e-3, "文献値と一致"
    assert u20 - gm20 > 0.5, "正十二面体は大域最小ではない"
    print(OK)


# ----------------------------------------------------------------------
# §4 ディスクリネーション歪みエネルギー
# ----------------------------------------------------------------------
def disclination_energy_density(mu, nu, omega_rad):
    """W/V = mu omega^2 / (16 pi^2 (1-nu))  [J/m^3]  (W = mu w^2 R^2/(16 pi (1-nu)) per length)"""
    return mu * omega_rad**2 / (16 * math.pi**2 * (1 - nu))


def check_elastic(gap_deg):
    print("\n[4] ディスクリネーション歪みエネルギー（ダイヤモンド vs Au）")
    w = math.radians(gap_deg)
    assert abs(w - 0.128388) < 1e-6
    n_dia = 8 / (3.567e-10) ** 3
    n_au = 4 / (4.078e-10) ** 3
    rows = [("ダイヤモンド", 535e9, 0.070, n_dia), ("Au", 27e9, 0.42, n_au)]
    per_atom = {}
    for name, mu, nu, n in rows:
        ev = disclination_energy_density(mu, nu, w)
        pa = ev / n / EV * 1000
        per_atom[name] = pa
        print(f"    {name:10s} mu={mu / 1e9:6.1f} GPa nu={nu:.3f}  "
              f"W/V={ev / 1e6:7.2f} MJ/m3  {pa:.3f} meV/原子")
    assert abs(per_atom["ダイヤモンド"] - 2.126) < 0.01
    assert abs(per_atom["Au"] - 0.514) < 0.01
    ratio = per_atom["ダイヤモンド"] / per_atom["Au"]
    print(f"    -> ダイヤはAuの {ratio:.2f} 倍（原子あたり）")
    assert abs(ratio - 4.13) < 0.05
    print("    対照: 黒鉛->ダイヤ ~20 meV/原子, 六方ダイヤ 20-30 meV/原子")
    assert per_atom["ダイヤモンド"] < 20 / 5, "5回双晶は相転移の1割程度"

    # 異方性と Poisson 比
    print("\n    弾性定数 (GPa) と異方性")
    for nm, c11, c12, c44 in (("ダイヤモンド", 1079, 124, 578), ("Au", 192.9, 163.8, 41.5)):
        A = 2 * c44 / (c11 - c12)
        nu100 = c12 / (c11 + c12)
        print(f"      {nm:10s} A={A:.4f}  nu_[100]={nu100:.4f}")
        if nm == "ダイヤモンド":
            assert abs(A - 1.2105) < 1e-3 and abs(nu100 - 0.1031) < 1e-3
        else:
            assert abs(A - 2.8522) < 1e-3 and abs(nu100 - 0.4592) < 1e-3
    print("    -> Au の分解比がダイヤでそのまま成り立つ理由はない（予言の出る場所）")

    # 双晶境界項と等しくなる半径
    print("\n    5 gamma/(pi R) = W/V となる半径")
    ev_dia = disclination_energy_density(535e9, 0.070, w)
    for g in (0.03, 0.05, 0.09):
        R = 5 * g / (math.pi * ev_dia)
        print(f"      gamma_tb={g:.2f} J/m2 -> R = {R * 1e9:.3f} nm")
        assert 0.5e-9 < R < 3e-9
    print(OK)


# ----------------------------------------------------------------------
# §3 Au 実測の分解（外部データの整合確認）
# ----------------------------------------------------------------------
def check_au_decomposition(gap_deg):
    print("\n[5] Au 実測の分解（Sci. Adv. 2025）と本恒等式の一致")
    per = gap_deg / 5
    parts = (("引張", 0.66, 45.0), ("せん断", 0.33, 22.5), ("回転・曲げ", 0.48, 32.5))
    tot = sum(p[1] for p in parts)
    for lab, d, pc in parts:
        print(f"    {lab:10s} {d:.2f} deg  ({pc:.1f}%)")
    print(f"    合計 {tot:.2f} deg  /  本恒等式の 1 領域あたり {per:.6f} deg")
    assert abs(tot - 1.47) < 0.005, "実測の分解和"
    assert abs(tot - per) < 0.005, "実測値と幾何恒等式が一致"
    assert abs(sum(p[2] for p in parts) - 100.0) < 0.01
    print("    -> 実験が使っている 1.47 deg は 72 - arccos(1/3) そのもの")
    print(OK)


if __name__ == "__main__":
    print("=" * 72)
    print("ttt_fivefold_verify.py — 2026-09-11")
    print("=" * 72)
    gap = check_geometry()
    check_bipyramids()
    check_thomson()
    check_elastic(gap)
    check_au_decomposition(gap)
    print("\n" + "=" * 72)
    print("全 assert 通過")
    print("=" * 72)
