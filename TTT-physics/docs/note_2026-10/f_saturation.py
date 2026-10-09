"""
TTT 検証スクリプト 2026-10-09 (2/2)：光速での飽和・回転する直線・6点・F＝E/R・結合エネルギー
  numpy のみ（図は matplotlib があれば rel_osc.png に出力）。すべての assert が通れば成立。
  単位：c ＝ 1
"""
import numpy as np

ok = 0
def check(cond, msg):
    global ok
    assert cond, msg
    ok += 1
    print("  ✓", msg)

# ---- Block 1：球の数列と格子 ----
print("Block 1：球 2·3^(n−1) と立方体 n³")
n = np.arange(1, 8)
sph, cub = 2 * 3.0 ** (n - 1), n ** 3.0
diff = sph - cub
check(list(diff[:5].astype(int)) == [1, -2, -9, -10, 37], "差は +1, −2, −9, −10, +37（段1〜5）")
check(int(n[np.argmax((diff > 0) & (n > 1))]) == 5, "段2以降で球が格子を初めて上回るのは段5（125）")
g = lambda x: np.log(2) + (x - 1) * np.log(3) - 3 * np.log(x)
lo, hi = 4.0, 5.0
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if g(mid) < 0 else (lo, mid)
check(4.4 < lo < 4.5, f"連続で解くと交わるのは一辺 ≈ {lo:.3f}（4 と 5 の間）")

# ---- Block 2：相対論的な単振動の飽和 ----
print("Block 2：相対論的な単振動 dp/dt = −z, v = p/√(1+p²)")
def oscillate(A, dt=2e-4):
    z, p, t = A, 0.0, 0.0
    T, Z, V = [0.0], [z], [0.0]
    while True:
        p -= z * dt
        z += p / np.sqrt(1 + p * p) * dt
        t += dt
        T.append(t); Z.append(z); V.append(p / np.sqrt(1 + p * p))
        if p > 0 and z >= A:
            return np.array(T), np.array(Z), np.array(V)

res = {}
for A in (0.3, 3.0, 30.0):
    T, Z, V = oscillate(A)
    res[A] = (T, Z, V)
    print(f"    振幅 {A:5}: 最大の速さ {np.abs(V).max():.4f}, 周期/(4A) {T[-1]/(4*A):.3f}")
check(np.abs(res[0.3][2]).max() < 0.3, "小さい振幅では最大の速さは光速よりずっと小さい")
check(np.abs(res[30.0][2]).max() > 0.9999, "振幅が大きいと最大の速さは光速に飽和する")
check(abs(res[30.0][0][-1] / (4 * 30.0) - 1) < 0.01, "周期は往復の距離 ÷ 光速（4A）に近づく")
T, Z, V = res[30.0]
ph = T / T[-1]
tri = 1 - 4 * np.minimum(ph, 1 - ph)
check(np.sqrt(np.mean((Z / 30.0 - tri) ** 2)) < 0.02, "波形は三角波になる（正弦波から三角波へ）")
T, Z, V = res[0.3]
ph = T / T[-1]
check(np.sqrt(np.mean((Z / 0.3 - np.cos(2 * np.pi * ph)) ** 2)) < 0.01, "小さい振幅では正弦波（ふつうの単振動）")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import logging
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    plt.rcParams["font.family"] = ["Noto Sans CJK JP", "IPAexGothic", "DejaVu Sans"]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for A in (0.3, 1.0, 3.0, 10.0, 30.0):
        T, Z, V = res[A] if A in res else oscillate(A)
        ax[0].plot(T / T[-1], Z / A, label=f"振幅 {A}")
        ax[1].plot(T / T[-1], V, label=f"振幅 {A}")
    ax[0].set_title("位置（振幅で規格化）：正弦波 → 三角波"); ax[0].set_xlabel("1周期"); ax[0].legend()
    ax[1].set_title("速さ（光速＝1）：±1 で飽和"); ax[1].set_xlabel("1周期")
    fig.tight_layout(); fig.savefig("rel_osc.png", dpi=120)
    print("    図を rel_osc.png に保存")
except ImportError:
    pass

# ---- Block 3：光速で回る直線のエネルギー ----
print("Block 3：0 から長さ R の直線を、先端が光速になるよう回す（張力 T）")
th = np.linspace(0, np.pi / 2, 200001)          # u = sin θ と置き換えて端の発散を避ける
E_TR = np.trapezoid(np.ones_like(th), th)                    # ∫0^1 du/√(1−u²)
J_TR2 = np.trapezoid(np.sin(th) ** 2, th)                    # ∫0^1 u² du/√(1−u²)
check(np.isclose(E_TR, np.pi / 2), "E ＝ (π/2)·T·R（静止時 T·R の π/2 倍）")
check(np.isclose(J_TR2, np.pi / 4), "J ＝ (π/4)·T·R²")
check(np.isclose(J_TR2 * np.pi / E_TR ** 2, 1.0), "J ＝ E²/(πT)：角運動量はエネルギーの2乗に比例")

# ---- Block 4：6点 (±1,0,0), (0,±1,0), (0,0,±1) の回転 ----
print("Block 4：6点（正八面体）を回す軸")
P = np.eye(3); M = -P
def radii(axis):
    a = axis / np.linalg.norm(axis)
    return np.array([np.linalg.norm(p - (p @ a) * a) for p in P])
check(np.allclose(radii(np.array([0, 0, 1.0])), [1, 1, 0]), "Z 軸まわりでは Z1 が止まり、3点は同時に光速にならない")
nd = np.ones(3) / np.sqrt(3)
check(np.allclose(radii(nd), np.sqrt(2 / 3)), "体対角線まわりでは3点の回転半径がそろう（√(2/3)）")
half = np.degrees(np.arccos(P[0] @ nd))
check(np.isclose(half, 54.735610317), "直線は軸から 54.74° 傾いた円錐を描く")
check(np.isclose(2 * half, np.degrees(np.arccos(-1 / 3))), "＋側と−側の開き 109.47° ＝ 正四面体の中心角")
check(np.allclose([p @ nd for p in P], 1 / np.sqrt(3)) and np.allclose([p @ nd for p in M], -1 / np.sqrt(3)),
      "＋の3点と−の3点は軸上 ±1/√3 の二つの輪に乗る")
e1 = P[0] - (P[0] @ nd) * nd; e1 /= np.linalg.norm(e1); e2 = np.cross(nd, e1)
ang = lambda p: round(np.degrees(np.arctan2(p @ e2, p @ e1)) % 360, 6)
check(sorted(ang(p) for p in P) == [0, 120, 240] and sorted(ang(p) for p in M) == [60, 180, 300],
      "＋は 0°・120°・240°、−は 60°・180°・300°（互い違いの三角形）")
c, s = np.cos(2 * np.pi / 3), np.sin(2 * np.pi / 3)
K = np.array([[0, -nd[2], nd[1]], [nd[2], 0, -nd[0]], [-nd[1], nd[0], 0]])
R120 = np.eye(3) + s * K + (1 - c) * K @ K
check(np.allclose(R120 @ P[0], P[1]) and np.allclose(R120 @ P[1], P[2]) and np.allclose(R120 @ P[2], P[0]),
      "1/3 回転で X1→Y1→Z1 と入れ替わる")
check(np.isclose(6 * E_TR, 3 * np.pi), "6本のエネルギーは 3π·T·R（比は π/2 のまま）")

# ---- Block 5：F と光速 ----
print("Block 5：F ＝ mA と E ＝ mc² を光速の円運動で組み合わせる")
for E, R in ((1.0, 1.0), (5.0, 2.0)):
    p, w = E, 1.0 / R                     # 光速：p ＝ E/c, ω ＝ c/R
    check(np.isclose(p * w, E / R), f"F ＝ pω ＝ E/R（E={E}, R={R}）：c は式から消える")
check(np.isclose(2 / np.pi * E_TR, 1.0), "直線では F ＝ T ＝ (2/π)·E/R")
m, v, dv = 1.0, 0.9, 1e-7
gam = lambda v: 1 / np.sqrt(1 - v * v)
dp_long = (gam(v + dv) * (v + dv) - gam(v) * v) / dv
check(np.isclose(dp_long, gam(v) ** 3 * m, rtol=1e-5), "直線運動（速さが変わる）では F ＝ γ³mA")
dth = 1e-7                                       # 速さ v のまま向きを dθ 回す
p0 = gam(v) * m * v * np.array([1.0, 0.0])
p1 = gam(v) * m * v * np.array([np.cos(dth), np.sin(dth)])
a_tran = v * dth                                 # 速度ベクトルの変化の大きさ
check(np.isclose(np.linalg.norm(p1 - p0) / a_tran, gam(v) * m, rtol=1e-5),
      "曲線運動（向きだけ変わる）では F ＝ γmA")

# ---- Block 6：まとまるとエネルギーが出る（結合エネルギー） ----
print("Block 6：結合エネルギーと鉄の山")
mp, mn = 938.272088, 939.565421                 # MeV
check(abs(2.224566 / (mp + mn) * 100 - 0.118) < 0.001, "重水素：2.22 MeV、質量の約 0.12% が光になる")
check(abs(26.73 / (4 * mp) * 100 - 0.712) < 0.002, "水素4つ → ヘリウム4：26.7 MeV、約 0.71%")
aV, aS, aC, aA = 15.75, 17.8, 0.711, 23.7
A = np.arange(4, 260)
Z = A / (2 + 0.0154 * A ** (2 / 3))
BA = (aV * A - aS * A ** (2 / 3) - aC * Z ** 2 / A ** (1 / 3) - aA * (A - 2 * Z) ** 2 / A) / A
Apk = int(A[np.argmax(BA)])
check(50 <= Apk <= 65, f"核子あたりの結合エネルギーは A ≈ {Apk}（鉄・ニッケル付近）で最大")
BA0 = (aV * A - aS * A ** (2 / 3)) / A
check(np.all(np.diff(BA0) > 0), "反発の項（A^(5/3) で増える）を除くと山は消え、単調に増える")

print(f"\n{ok} assert 全通過")
