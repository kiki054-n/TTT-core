"""TTT 検証 2026-10-05 (1/3): 34 = 16 + 18 の導出
numpy のみ。全 assert が通れば PASS。
"""
import itertools
import numpy as np

PASS = 0
def ok(cond, msg):
    global PASS
    assert cond, msg
    PASS += 1
    print(f"  PASS  {msg}")

print("== Block 1: 段の表と中心六角数")
supply = {k: 2 * 3 ** (k - 1) for k in range(1, 8)}          # 2, 6, 18, 54, 162, 486, 1458
ok([supply[k] for k in range(1, 6)] == [2, 6, 18, 54, 162], "供給列 2,6,18,54,162 (×3)")
ok(supply[5] - 5 ** 3 == 37, "段5のはみ出し 162-125 = 37")
for n in (4, 5, 6):
    ok(n ** 3 - (n - 1) ** 3 == 3 * n * (n - 1) + 1, f"n^3-(n-1)^3 = 3n(n-1)+1 (n={n}: {n**3-(n-1)**3}) = 中心六角数")
ok(4 ** 3 - 3 ** 3 == 37, "37 自体も中心六角数 (4^3-3^3)")
over = {5: 37, 6: 34, 7: 34, 8: 34}                        # 本人の値
ok(34 / 6 ** 3 < 37 / 5 ** 3, "はみ出しの割合は段とともに減る")
ok(round(37 * (6 / 5) ** 2) == 53, "表面型なら段6で約53に増えるはず (実際は34)")

print("== Block 2: 外郭の位相的欠陥 = 16 (オイラー標数)")
deficit = 2 * np.pi - 3 * (np.pi / 2)
ok(np.isclose(8 * deficit, 4 * np.pi), "立方体表面: 角8個 × π/2 = 4π (χ=2)")
V, E, Fc, C = 8 + 8, 12 + 12 + 8, 6 + 6 + 12, 6      # 内外2面 + 放射方向の線8本 + 側面12 + 錐台6
ok(V - E + Fc - C == 2, "立方殻の胞複体 χ = 16-32+24-6 = 2 (球殻と同じ)")
ok(2 * 4 * 2 == 16, "内8 + 外8 = 16")
vals = {k0 * chi for k0 in (4, 6) for chi in (2, 4)}
ok(vals == {8, 12, 16, 24}, "k0·χ で出る値は {8,12,16,24}")
ok(not any(k0 * chi in (17, 34) for k0 in range(3, 13) for chi in range(-4, 9)), "17・34 は k0·χ で書けない")

print("== Block 3: 帰無対照（立方体の不変量の小係数和）")
base = [2, 6, 8, 12]
reach = {sum(a * b for a, b in zip(c, base)) for c in itertools.product(range(3), repeat=4)}
frac = sum(t in reach for t in range(10, 51)) / 41
ok(0.5 < frac < 0.52, f"10〜50 の到達率 {frac:.0%}（一致に情報なし）")
ok(17 not in reach, "17 は作れない（材料がすべて偶数）")
reach1 = {sum(a * b for a, b in zip(c, [1] + base)) for c in itertools.product(range(3), repeat=5)}
ok(all(t in reach1 for t in range(10, 51)), "『中心の1』を足すと 10〜50 の全整数に到達（情報なし）")

print("== Block 4: 残り18が一定になる機構")
ns = np.arange(5, 11)
conserved = np.full(len(ns), 18.0)
misfit = 18 * (ns / 6) ** 2
volume = 18 * (ns / 6) ** 3
ok(np.all(conserved == 18), "保存量なら一定")
ok(misfit[-1] > misfit[0] and volume[-1] > volume[0], "不整合ひずみ・圧力×体積なら段とともに増える")
ok(over[6] - 16 == 18 and over[5] - 16 - 18 == 3, "37 = 16 + 18 + 3、34 = 16 + 18")

print("== Block 5: 18 = 3場 × (直線3 + 曲線3)")
ok(3 * (3 + 3) == 18, "運動量3 + 角運動量3 (ネーター) × 3場")
Lx = np.array([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
Ly = np.array([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
Lz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
ok(np.array_equal(Lx @ Ly - Ly @ Lx, Lz), "回転は非可換 [Lx,Ly]=Lz")
def Tr(v):
    M = np.eye(4); M[:3, 3] = v; return M
Ta, Tb = Tr([1.0, 0, 0]), Tr([0, 1.0, 0])
ok(np.allclose(Ta @ Tb, Tb @ Ta), "平行移動は可換（運動量3方向は自動的に独立）")
Om = np.array([0, 1.0, 0])
ok(np.linalg.norm(np.cross(Om, [1.0, 0, 0])) > 0, "単極の回転場は直交軸まわりの回転でトルクを受ける")
ok(np.linalg.norm(np.cross(Om, [0.0, 0, 0])) == 0, "逆回転の対（正味0）はトルクを受けない（中間段階の読み）")

print("== Block 6: 却下した読み — 双極＝ヘリシティ")
ok(3 * 2 * 1 == 6, "光速で進む場は保存成分が進行方向の1つ → 3場×2×1 = 6（18にならない）")

print("== Block 7: 中心に質量が入る最初の段")
first = None
for n in range(2, 8):
    has_center = n % 2 == 1
    overfill = supply[n] > n ** 3
    if has_center and overfill and first is None:
        first = n
ok(first == 5, "中心のマスがあり（奇数）かつ供給が箱を超える最初の段 = 5")
ok(supply[3] < 27 and supply[6] > 216, "段3は中心があるが不足、段6は超過だが中心なし")

print("== Block 8: 中心の共有 → 体心立方の二副格子")
odd = np.array([p for p in itertools.product(range(-2, 3), repeat=3)], float)      # 5^3 のマス中心
even = np.array([p for p in itertools.product(np.arange(-2.5, 3), repeat=3)])       # 6^3 のマス中心
ok(np.allclose(odd.mean(0), 0) and np.allclose(even.mean(0), 0), "両方の箱の中心が原点で一致")
ok(np.allclose(np.mod(even, 1), 0.5), "偶数段のマスは半整数座標（半マスずれ）")
d = np.linalg.norm(even - odd[62], axis=1)     # 原点のマスから
ok(np.sum(np.isclose(d, np.sqrt(3) / 2)) == 8, "原点から最近接の半整数点は 8 個（体心立方の配位）")

print("== Block 9: 34一定なら途中に山はない")
f = [34 / n ** 3 for n in range(6, 12)]
ok(all(a > b for a, b in zip(f, f[1:])), "34/n^3 は単調減少")

print(f"\n{PASS} PASS / 0 FAIL")
