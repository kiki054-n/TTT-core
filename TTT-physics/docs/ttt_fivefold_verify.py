#!/usr/bin/env python3
"""
ttt_fivefold_verify.py — 「7.356 度の行き先」補注 v2 の検算
2026-09-12 / 全 assert 通過で検証完了

v2 の追加: LJ7 / LJ13 の大域最小、LJ7 五角双錐の実測パラメータと軸伸長、
          正二十面体の 36 度スタガー、全辺等長の五角双錐の非存在、
          Tersoff g の 108 / 63.8 / 82.4 度

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
SIN36 = math.sin(math.radians(36))


# ======================================================================
# §1 幾何 — 7.356103 度と恒等式
# ======================================================================
def check_geometry():
    print("[1] 5 個の正四面体は 1 辺のまわりで閉じない")
    dih = math.degrees(math.acos(1 / 3))
    bond = math.degrees(math.acos(-1 / 3))
    print(f"    二面角 = arccos(1/3)  = {dih:.6f} deg")
    print(f"    結合角 = arccos(-1/3) = {bond:.6f} deg")
    assert abs(dih - 70.528779) < 1e-6
    assert abs(bond - 109.471221) < 1e-6
    assert abs(dih + bond - 180.0) < 1e-12

    for k in (3, 4, 5, 6):
        print(f"     k={k}: 合計 {k * dih:11.6f} deg  隙間 {360 - k * dih:+11.6f} deg")
    gap = 360 - 5 * dih
    assert abs(gap - 7.356103) < 1e-6
    assert 360 - 4 * dih > 0 and 360 - 6 * dih < 0, "5 個だけが「わずかに閉じない」"

    per = gap / 5
    print(f"    1 領域あたり = {per:.6f} deg")
    print(f"      72 - 二面角  = {72 - dih:.6f}")
    print(f"      結合角 - 108 = {bond - 108:.6f}")
    assert abs(per - (72 - dih)) < 1e-12
    assert abs(per - (bond - 108)) < 1e-12
    print("    -> 恒等式: 四面体結合角が正五角形の内角を超える分 = 5 回対称の食い違い")

    sa = 3 * math.acos(1 / 3) - math.pi
    deficit = 4 * math.pi - 20 * sa
    print(f"    正四面体の立体角 = {sa:.6f} sr, 20 個 = {20 * sa:.6f} sr")
    print(f"    4pi = {4 * math.pi:.6f} sr -> 不足 {deficit:.6f} sr ({100 * deficit / (4 * math.pi):.2f}%)")
    assert abs(sa - 0.551286) < 1e-6 and abs(deficit - 1.540659) < 1e-6
    contraction = math.sin(2 * math.pi / 5)
    print(f"    Mackay 二十面体の動径収縮 sin(2pi/5) = {contraction:.6f} -> {100 * (1 - contraction):.2f}% 短縮")
    assert abs(contraction - 0.951057) < 1e-6
    print(OK)
    return gap


def check_no_equilateral_bipyramid():
    """5 回対称を課すと全辺等長の五角双錐は存在しない（7.356 度の座標版）。"""
    print("\n[2] 全辺等長の五角双錐は存在しない")
    # 赤道半径 r=1, 極-極 h。赤道最近接 = 2 sin36, 極-赤道 = sqrt(1 + h^2/4)
    eqeq = 2 * SIN36
    h = eqeq                      # 極-極 を赤道最近接に等しく置く
    poleeq = math.sqrt(1 + h**2 / 4)
    mismatch = eqeq / poleeq - 1
    print(f"    赤道最近接 = 2 sin36 = {eqeq:.6f} r")
    print(f"    h = 赤道最近接 とすると 極-赤道 = {poleeq:.6f} r")
    print(f"    食い違い = {100 * mismatch:.3f} %")
    assert abs(eqeq - 1.175571) < 1e-6
    assert abs(poleeq - 1.159953) < 1e-6
    assert abs(100 * mismatch - 1.346) < 0.01
    print("    -> 5 個の正四面体が閉じないことの長さ表示")
    print(OK)
    return 100 * mismatch


# ======================================================================
# §2 双錐族
# ======================================================================
def bipyramid(n):
    V = [[math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n), 0] for k in range(n)]
    V += [[0, 0, 1], [0, 0, -1]]
    V = np.array(V, float)
    return V / np.linalg.norm(V, axis=1, keepdims=True)


def check_bipyramids():
    print("\n[3] 双錐族 B_n : B_4 = 正八面体だけが特別")
    for n in range(3, 7):
        V = bipyramid(n)
        m = len(V)
        assert m == n + 2
        dots = sorted({round(V[i] @ V[j], 4) for i, j in itertools.combinations(range(m), 2)})
        M = sum(np.outer(v, v) for v in V)
        iso = np.allclose(M, (m / 3) * np.eye(3), atol=1e-9)
        print(f"    B_{n}: 頂点{m:2d} 辺{3 * n:2d} 面{2 * n:2d}  |sum v|={np.linalg.norm(V.sum(0)):.4f}"
              f"  内積={dots}  等方タイトフレーム={iso}")
        assert np.linalg.norm(V.sum(0)) < 1e-12
        assert iso == (n == 4), "等方タイトフレームは B_4 のみ"
        assert len(dots) >= 2, "全対等内積は不可能"
    assert np.allclose(sum(np.outer(v, v) for v in bipyramid(4)), 2 * np.eye(3))
    print("    -> 全対等内積が可能なのは正四面体（4 本・1 クラス）のみ = 特異点")
    print(OK)


# ======================================================================
# §2 トムソン問題
# ======================================================================
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


def thomson_min(N, restarts=40):
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
    print("\n[4] トムソン問題 : 双錐は N=5,6,7 で大域最小、正十二面体は N=20 で落ちる")
    for n, label in ((3, "三方両錐"), (4, "正八面体"), (5, "五角双錐")):
        V = bipyramid(n)
        N = len(V)
        u = thomson(V.ravel())[0]
        gm = thomson_min(N)
        print(f"    N={N}  {label:6s} U={u:.6f}   大域最小 U={gm:.6f}   差 {u - gm:+.2e}")
        assert abs(u - gm) < 1e-6
    D = dodecahedron()
    u20 = thomson(D.ravel())[0]
    gm20 = thomson_min(20, restarts=60)
    print(f"    N=20 正十二面体 U={u20:.6f}   大域最小 U={gm20:.6f}   差 {u20 - gm20:+.6f}")
    assert abs(gm20 - 150.881568) < 1e-3
    assert u20 - gm20 > 0.5
    print(OK)


# ======================================================================
# §3 LJ クラスター — N=7 は軸を伸ばして吸収する
# ======================================================================
def lj(x):
    P = x.reshape(-1, 3)
    diff = P[:, None, :] - P[None, :, :]
    d2 = np.sum(diff**2, axis=-1)
    np.fill_diagonal(d2, np.inf)
    inv6 = d2**-3
    inv12 = inv6**2
    E = 0.5 * np.sum(4 * (inv12 - inv6))
    coef = 4 * (-12 * inv12 + 6 * inv6) / d2
    G = 2 * np.sum(coef[:, :, None] * diff, axis=1)
    return E, G.ravel()


def icosahedron(centered=False):
    phi = (1 + math.sqrt(5)) / 2
    V = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            V += [[0, s1, s2 * phi], [s1, s2 * phi, 0], [s1 * phi, 0, s2]]
    V = np.array(V, float)
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    if centered:
        V = np.vstack([[[0.0, 0.0, 0.0]], V])
    return V


def check_lj():
    print("\n[5] LJ クラスターの大域最小（文書の -2.007 / -3.394 は誤り）")
    # 理想構造から局所緩和すると決定的に大域最小へ落ちる
    seeds = {
        7: bipyramid(5) * 0.96,
        13: icosahedron(centered=True) * 1.0,
    }
    lit = {7: -16.505384, 13: -44.326801}
    doc = {7: -2.007, 13: -3.394}
    res = {}
    for N in (7, 13):
        r = minimize(lj, seeds[N].ravel(), jac=True, method="L-BFGS-B", options={"maxiter": 8000})
        res[N] = r
        print(f"    LJ{N:<2d} E={r.fun:11.6f}  E/N={r.fun / N:9.6f}   "
              f"(文献 E={lit[N]:.6f} -> E/N={lit[N] / N:.6f} / 文書 {doc[N]})")
        assert abs(r.fun - lit[N]) < 1e-5, f"LJ{N} が文献値と一致"
        assert abs(r.fun / N - doc[N]) > 0.01, f"文書の E/N は誤り"
    # LJ7 が大域最小であることを乱数多重開始で確認
    best = np.inf
    for _ in range(200):
        rr = minimize(lj, np.random.normal(scale=1.05, size=21), jac=True,
                      method="L-BFGS-B", options={"maxiter": 4000})
        best = min(best, rr.fun)
    print(f"    LJ7 乱数 200 回の最良 = {best:.6f} -> 五角双錐が大域最小")
    assert abs(best - lit[7]) < 1e-5
    print(OK)
    return res[7].x.reshape(7, 3)


def check_lj7_geometry(P, mismatch_pct):
    print("\n[6] LJ7 五角双錐の実測パラメータ（文書の値は LJ 最小ではない）")
    P = P - P.mean(0)
    d = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=-1)
    nn = np.sort(d, axis=1)[:, 1]
    cn = [int(np.sum(d[i] < 1.30 * nn[i])) - 1 for i in range(7)]
    poles = [i for i in range(7) if cn[i] == max(cn)]
    eqs = [i for i in range(7) if i not in poles]
    assert len(poles) == 2 and len(eqs) == 5, "極 2 / 赤道 5"

    pp = d[poles[0], poles[1]]
    eqeq = np.mean(sorted(d[i, j] for i, j in itertools.combinations(eqs, 2))[:5])
    eqpo = np.mean([d[i, p] for i in eqs for p in poles])
    c = P[poles].mean(0)
    req = np.mean([np.linalg.norm(P[i] - c) for i in eqs])

    doc = {"極-極": 1.6000, "赤道最近接": 1.0748, "赤道-極": 1.2149, "r_eq": 0.9143, "r_ax": 0.8000}
    act = {"極-極": pp, "赤道最近接": eqeq, "赤道-極": eqpo, "r_eq": req, "r_ax": pp / 2}
    for k in doc:
        print(f"    {k:10s} 実際 {act[k]:.4f}   文書 {doc[k]:.4f}")
    assert abs(pp - 1.1477) < 1e-3 and abs(pp / 2 - 0.5739) < 1e-3
    assert abs(eqeq - 1.1241) < 1e-3 and abs(eqpo - 1.1152) < 1e-3
    assert abs(req - 0.9562) < 1e-3
    assert abs(pp - doc["極-極"]) > 0.4, "文書は軸を約 39% 長く取っている"

    # 5 回対称は赤道最近接 = 2 sin36 * r_eq を強制する
    assert abs(eqeq / req - 2 * SIN36) < 2e-3, "5 回対称の強制"
    ratio = pp / eqeq
    hr = pp / req
    print(f"    極-極 / 赤道最近接 = {ratio:.4f}  -> ほぼ全辺等長 = 5 個のほぼ正四面体")
    print(f"    h/r_eq = {hr:.4f}  vs 理想（全辺等長）{2 * SIN36:.4f}"
          f"  -> 軸が {100 * (hr / (2 * SIN36) - 1):.1f}% 伸びている")
    assert abs(ratio - 1.0210) < 1e-3
    axial = 100 * (hr / (2 * SIN36) - 1)
    assert 1.5 < axial < 3.0, "軸伸長は数 % のオーダー"
    assert axial > mismatch_pct, "実測の伸びは理論下限の食い違いと同桁"
    print(f"    -> N=7 は 7.356 deg を「5 回軸を約 {axial:.1f}% 伸ばす」ことで吸収している")
    print(OK)


# ======================================================================
# §3 正二十面体は「重層五角双錐」ではない
# ======================================================================
def align_to_z(V, axis):
    z = np.array([0.0, 0.0, 1.0])
    v = np.cross(axis, z)
    s = np.linalg.norm(v)
    if s < 1e-12:
        return V
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R = np.eye(3) + K + K @ K * ((1 - axis @ z) / s**2)
    return V @ R.T


def check_icosahedron_stagger():
    print("\n[7] 正二十面体は「重層五角双錐」ではない")
    I = icosahedron()
    top = I[np.argmax(I[:, 2])]
    J = align_to_z(I, top / np.linalg.norm(top))
    J = J[np.argsort(-J[:, 2])]
    zs = np.round(J[:, 2], 6)
    print(f"    z 座標の層: {sorted(set(zs), reverse=True)}")
    up, lo = J[1:6], J[6:11]
    assert np.allclose(up[:, 2], up[0, 2]) and np.allclose(lo[:, 2], lo[0, 2])

    azi = lambda Q: np.sort([math.degrees(math.atan2(p[1], p[0])) % 72 for p in Q])
    a_up, a_lo = azi(up), azi(lo)
    print(f"    上五角形 方位(mod 72) = {np.round(a_up, 3)}  (ばらつき {a_up.std():.1e})")
    print(f"    下五角形 方位(mod 72) = {np.round(a_lo, 3)}  (ばらつき {a_lo.std():.1e})")
    stagger = abs(a_up[0] - a_lo[0])
    print(f"    ずれ = {stagger:.3f} deg -> 五角逆プリズム。単純な「赤道面の二重化」ではない")
    assert a_up.std() < 1e-9 and a_lo.std() < 1e-9
    assert abs(stagger - 36.0) < 1e-6, "36 度スタガー"

    # 頂点 0 からの距離クラス（文書の数値はここは正しい）
    dist = np.array([np.linalg.norm(v - top) for v in I])
    cls = sorted(set(np.round(dist, 4)))
    print(f"    頂点 0 からの距離: {cls}  (文書 0 / 1.0515 / 1.7013 / 2.0000 と一致)")
    assert cls == [0.0, 1.0515, 1.7013, 2.0]
    upi = I[np.abs(dist - cls[1]) < 1e-3]
    rp = [np.linalg.norm(v - upi.mean(0)) for v in upi]
    print(f"    上五角形の中心からの距離 = {np.mean(rp):.4f} (標準偏差 {np.std(rp):.1e})  文書 0.8944 と一致")
    assert abs(np.mean(rp) - 0.8944) < 1e-4 and np.std(rp) < 1e-12

    bot = I[np.argmin(I[:, 2])]
    dbot = np.mean([np.linalg.norm(v - bot) for v in upi])
    print(f"    下極 - 上五角形 = {dbot:.4f}  vs 辺長 {cls[1]:.4f}  ({dbot / cls[1]:.2f} 倍) -> 非結合")
    assert dbot / cls[1] > 1.3, "両極が同じ五角形に結合しない"
    print("    => {上極 + 上五角形 + 下極} は五角双錐ではない")
    print("       正しい分解: 五角逆プリズム(10) + 冠(2)、または頂点まわりの五角錘(6)")
    print(OK)


# ======================================================================
# §4 ディスクリネーション歪みエネルギー
# ======================================================================
def disclination_energy_density(mu, nu, omega_rad):
    return mu * omega_rad**2 / (16 * math.pi**2 * (1 - nu))


def check_elastic(gap_deg):
    print("\n[8] ディスクリネーション歪みエネルギー（ダイヤモンド vs Au）")
    w = math.radians(gap_deg)
    assert abs(w - 0.128388) < 1e-6
    n_dia = 8 / (3.567e-10) ** 3
    n_au = 4 / (4.078e-10) ** 3
    per_atom = {}
    for name, mu, nu, n in (("ダイヤモンド", 535e9, 0.070, n_dia), ("Au", 27e9, 0.42, n_au)):
        ev = disclination_energy_density(mu, nu, w)
        pa = ev / n / EV * 1000
        per_atom[name] = pa
        print(f"    {name:10s} mu={mu / 1e9:6.1f} GPa nu={nu:.3f}  "
              f"W/V={ev / 1e6:7.2f} MJ/m3  {pa:.3f} meV/原子")
    assert abs(per_atom["ダイヤモンド"] - 2.126) < 0.01
    assert abs(per_atom["Au"] - 0.514) < 0.01
    ratio = per_atom["ダイヤモンド"] / per_atom["Au"]
    print(f"    -> ダイヤは Au の {ratio:.2f} 倍（原子あたり）")
    assert abs(ratio - 4.13) < 0.05
    print("    対照: 黒鉛->ダイヤ ~20 meV/原子, 六方ダイヤ 20-30 meV/原子")
    assert per_atom["ダイヤモンド"] < 20 / 5

    print("\n    弾性定数 (GPa) と異方性")
    for nm, c11, c12, c44 in (("ダイヤモンド", 1079, 124, 578), ("Au", 192.9, 163.8, 41.5)):
        A = 2 * c44 / (c11 - c12)
        nu100 = c12 / (c11 + c12)
        print(f"      {nm:10s} A={A:.4f}  nu_[100]={nu100:.4f}")
        if nm == "ダイヤモンド":
            assert abs(A - 1.2105) < 1e-3 and abs(nu100 - 0.1031) < 1e-3
        else:
            assert abs(A - 2.8522) < 1e-3 and abs(nu100 - 0.4592) < 1e-3

    print("\n    5 gamma/(pi R) = W/V となる半径")
    ev_dia = disclination_energy_density(535e9, 0.070, w)
    for g in (0.03, 0.05, 0.09):
        R = 5 * g / (math.pi * ev_dia)
        print(f"      gamma_tb={g:.2f} J/m2 -> R = {R * 1e9:.3f} nm")
        assert 0.5e-9 < R < 3e-9
    print(OK)


# ======================================================================
# §3 Au 実測の分解
# ======================================================================
def check_au_decomposition(gap_deg):
    print("\n[9] Au 実測の分解（Sci. Adv. 2025）と本恒等式の一致")
    per = gap_deg / 5
    parts = (("引張", 0.66, 45.0), ("せん断", 0.33, 22.5), ("回転・曲げ", 0.48, 32.5))
    tot = sum(p[1] for p in parts)
    for lab, dd, pc in parts:
        print(f"    {lab:10s} {dd:.2f} deg  ({pc:.1f}%)")
    print(f"    合計 {tot:.2f} deg  /  本恒等式の 1 領域あたり {per:.6f} deg")
    assert abs(tot - 1.47) < 0.005 and abs(tot - per) < 0.005
    assert abs(sum(p[2] for p in parts) - 100.0) < 0.01
    print("    -> 実験が使っている 1.47 deg は 72 - arccos(1/3) そのもの")
    print(OK)


# ======================================================================
# 付録 Tersoff g(theta)
# ======================================================================
def check_tersoff():
    print("\n[10] Tersoff g(theta) — 文書の 4 値はすべて誤り")
    c, d, h = 3.8049e4, 4.3484, -0.57058
    g = lambda t, hh=h: 1 + c**2 / d**2 - c**2 / (d**2 + (math.cos(math.radians(t)) - hh) ** 2)
    th_min = math.degrees(math.acos(h))
    print(f"    最小は theta = {th_min:.2f} deg (g = {g(th_min):.4f})")
    assert abs(th_min - 124.79) < 0.02 and abs(g(th_min) - 1.0) < 1e-3
    claims = {109.4712: "1.0 (最小)", 108.0: "~1.0", 63.8: "~1e4", 82.4: "~1e3"}
    vals = {}
    for t, cl in claims.items():
        vals[t] = g(t)
        print(f"    g({t:9.4f}) 文書 {cl:11s} 実際 {g(t):.4e}   h=-1/3 版 {g(t, -1 / 3):.4e}")
    print(f"    g(120) = {g(120):.4e}")
    assert vals[109.4712] > 1e5, "109.47 は最小ではない"
    assert vals[108.0] > vals[109.4712], "g(108) > g(109.47) なので「108 はほぼ最適」は偽"
    assert vals[63.8] > 1e6 and vals[82.4] > 1e6, "63.8 / 82.4 の桁も誤り"
    assert g(120) < vals[109.4712], "Tersoff は四面体角を黒鉛角より強く罰する"
    print(f"    -> g(109.47)/g(120) = {vals[109.4712] / g(120):.1f}")
    print(OK)


if __name__ == "__main__":
    print("=" * 74)
    print("ttt_fivefold_verify.py v2 — 2026-09-12")
    print("=" * 74)
    gap = check_geometry()
    mm = check_no_equilateral_bipyramid()
    check_bipyramids()
    check_thomson()
    P7 = check_lj()
    check_lj7_geometry(P7, mm)
    check_icosahedron_stagger()
    check_elastic(gap)
    check_au_decomposition(gap)
    check_tersoff()
    print("\n" + "=" * 74)
    print("全 assert 通過")
    print("=" * 74)
