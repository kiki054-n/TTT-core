"""
TTT 検証スクリプト v3: 八面体・四面体充填（面心立方格子）で 5×5×5 を数える

面心立方格子（FCC）の立方セル 1 個（辺 1）には、
  格子点 4、八面体の隙間 4、四面体の隙間 8
があり、空間はテトラ 8 個（各体積 1/24）＋オクタ 4 個（各体積 1/6）で隙間なく埋まる。

これを 5×5×5 = 125 セルに広げたときの数と体積を、
  (a) 周期境界（境界を隣と共有する＝境界を持たない数え方）
  (b) 有限ブロック（境界上の点も全部数える＝外郭を持つ数え方）
の 2 通りで、座標を列挙して数える。

実行: python3 verify_octet_125.py
"""
from fractions import Fraction as F
from itertools import product

N = 5  # 5×5×5


def sites_in_cell():
    """単位セル内（0 ≤ x < 1）の各サイトの分率座標（2倍、4倍した整数で扱う）"""
    # 4倍座標で表す（0..3）
    atoms = [(0, 0, 0), (0, 2, 2), (2, 0, 2), (2, 2, 0)]
    octa = [(2, 2, 2), (2, 0, 0), (0, 2, 0), (0, 0, 2)]
    tetra = [(x, y, z) for x, y, z in product((1, 3), repeat=3)]
    return atoms, octa, tetra


def periodic_counts(n):
    a, o, t = sites_in_cell()
    pts = {"格子点": set(), "八面体の隙間": set(), "四面体の隙間": set()}
    for i, j, k in product(range(n), repeat=3):
        for key, lst in zip(pts, (a, o, t)):
            for x, y, z in lst:
                pts[key].add(((4 * i + x) % (4 * n), (4 * j + y) % (4 * n), (4 * k + z) % (4 * n)))
    return {k: len(v) for k, v in pts.items()}


def finite_counts(n):
    """0 ≤ 座標 ≤ n の閉じたブロック内のサイトを全部数える"""
    L = 4 * n
    a, o, t = sites_in_cell()
    pts = {"格子点": set(), "八面体の隙間": set(), "四面体の隙間": set()}
    for i, j, k in product(range(n + 1), repeat=3):
        for key, lst in zip(pts, (a, o, t)):
            for x, y, z in lst:
                p = (4 * i + x, 4 * j + y, 4 * k + z)
                if all(0 <= c <= L for c in p):
                    pts[key].add(p)
    return {k: len(v) for k, v in pts.items()}


def interior_counts(n):
    """境界に触れない（0 < 座標 < n）サイトだけ数える"""
    L = 4 * n
    a, o, t = sites_in_cell()
    pts = {"格子点": set(), "八面体の隙間": set(), "四面体の隙間": set()}
    for i, j, k in product(range(n + 1), repeat=3):
        for key, lst in zip(pts, (a, o, t)):
            for x, y, z in lst:
                p = (4 * i + x, 4 * j + y, 4 * k + z)
                if all(0 < c < L for c in p):
                    pts[key].add(p)
    return {k: len(v) for k, v in pts.items()}


def show(title, d):
    tot = sum(d.values())
    holes = d["八面体の隙間"] + d["四面体の隙間"]
    print(f"\n[{title}]")
    for k, v in d.items():
        print(f"  {k:<10}{v:>6}")
    print(f"  {'隙間の合計':<10}{holes:>6}")
    print(f"  {'総計':<10}{tot:>6}")
    return d, holes, tot


print("=" * 64)
print(f"面心立方格子 {N}×{N}×{N} = {N**3} セル")
print("=" * 64)

# 体積の検算
vt, vo = F(1, 24), F(1, 6)
print(f"\nセル1個: テトラ 8×{vt} + オクタ 4×{vo} = {8*vt + 4*vo}（=1 なら隙間なし）")
print(f"体積の割合: テトラ {8*vt}  オクタ {4*vo}")
print(f"125セル: テトラ {8*N**3} 個（体積 {8*N**3*vt}）, オクタ {4*N**3} 個（体積 {4*N**3*vo}）")
print(f"         立体の総数 {12*N**3}")

p = show("(a) 周期境界：境界を共有する数え方", periodic_counts(N))
f = show("(b) 有限ブロック：境界上も全部数える", finite_counts(N))
i = show("(c) 内部だけ：境界に触れないもの", interior_counts(N))

print("\n" + "=" * 64)
print("TTT の数との照合")
print("=" * 64)
pa, ph, pt = p
checks = [
    ("格子点 = 500（外郭 O）", pa["格子点"] == 500),
    ("隙間の合計 = 1500（内部 OπO）", ph == 1500),
    ("総計 = 2000（要素数）", pt == 2000),
    ("1セルあたり 16（= 2000/125）", pt // N**3 == 16),
    ("立体の総数 = 1500（テトラ1000＋オクタ500）", 12 * N**3 == 1500),
]
for name, ok in checks:
    print(f"  {'PASS' if ok else 'FAIL'}  (a) {name}")

print("\n  501 / 125.25 の探索（各数え方で 501 が現れるか）")
for label, (d, h, t) in (("(a)", p), ("(b)", f), ("(c)", i)):
    vals = dict(d)
    vals["隙間の合計"] = h
    vals["総計"] = t
    found = [k for k, v in vals.items() if v in (501, 125)]
    near = {k: v for k, v in vals.items() if abs(v - 501) <= 20}
    print(f"   {label} 501 または 125 に一致: {found or 'なし'}   501±20: {near or 'なし'}")
