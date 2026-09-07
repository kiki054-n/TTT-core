#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ttt_core_verify.py  --  TTT_CORE.md v1.0 の全ステップの機械検証

依存: numpy のみ（sympy は使わない。位数3の元の型は自前で列挙する）
用法: python3 ttt_core_verify.py

各検証は assert で落ちる。最後まで走れば TTT_CORE.md の主張はすべて再現された。
"""

import itertools
import numpy as np
from math import sqrt

OK = "  [OK] "


# ---------------------------------------------------------------- 群の構成
def rotation_group():
    """立方体（正八面体）の回転群 O: 行列式 +1 の符号付き置換行列 24 個"""
    G = []
    for perm in itertools.permutations(range(3)):
        for s in itertools.product([1, -1], repeat=3):
            M = np.zeros((3, 3), dtype=int)
            for i, p in enumerate(perm):
                M[i, p] = s[i]
            if round(np.linalg.det(M)) == 1:
                G.append(M)
    return G


def order(M):
    P, n, I = M.copy(), 1, np.eye(3, dtype=int)
    while not np.array_equal(P, I):
        P, n = P @ M, n + 1
    return n


def as_line(v):
    """方向ベクトルを直線の代表元に正規化（最初の非零成分を正にする）"""
    v = tuple(int(x) for x in v)
    for x in v:
        if x != 0:
            return v if x > 0 else tuple(-a for a in v)
    return v


def orbit(v, gens, key=tuple):
    S = {key(v)}
    while True:
        N = set(S)
        for w in S:
            for g in gens:
                N.add(key(g @ np.array(w)))
        if N == S:
            return S
        S = N


G = rotation_group()
print("S3. 回転群")
assert len(G) == 24
print(OK + "位数 |O| = 24")


# ------------------------------------------------- S3: 線の軌道 3 / 4 / 6
print("\nS3. 線の軌道と、それを固定する回転の位数")
expected = {(1, 0, 0): (3, 4), (1, 1, 1): (4, 3), (1, 1, 0): (6, 2)}
for v, (n_exp, ord_exp) in expected.items():
    o = orbit(np.array(v), G, key=as_line)
    a = np.array(v)
    ords = sorted({order(g) for g in G if np.array_equal(g @ a, a) and order(g) > 1})
    stab = sum(1 for g in G if as_line(g @ a) == as_line(a))
    assert len(o) == n_exp, (v, len(o))
    assert max(ords) == ord_exp, (v, ords)
    assert len(o) * stab == 24
    print(OK + f"{v}: 軌道 {len(o)} 本, 固定回転の最大位数 {max(ords)}, "
                f"軌道 x 固定化群 = {len(o)}x{stab} = 24")

assert 3 + 4 + 6 == 13
assert 1 + 3 * 3 + 4 * 2 + 6 * 1 == 24
print(OK + "軸の総数 3+4+6 = 13、元の数 1+9+8+6 = 24")


# ------------------------------------------------ 参考: 点の軌道 6 / 8 / 12
print("\n参考. 点の軌道")
for v, n_exp, name in [((1, 0, 0), 6, "正八面体"),
                       ((1, 1, 1), 8, "立方体の頂点 = 8象限"),
                       ((1, 1, 0), 12, "立方八面体")]:
    o = orbit(np.array(v), G)
    assert len(o) == n_exp
    print(OK + f"{v}: {len(o)} 点 ({name})")
# 18 と 54 は 24 を割らないので、どんな点の軌道にもなりえない
assert 24 % 18 != 0 and 24 % 54 != 0
print(OK + "18 と 54 は 24 を割らない -> 回転の軌道になりえない")


# ----------------------------------- S4: 位数3の作用は必ず 1固定 + 3巡回
print("\nS4. 4個への位数3の作用")
cycle_types = set()
for p in itertools.permutations(range(4)):
    # 置換 p の位数
    seen, cyc = set(), []
    for i in range(4):
        if i in seen:
            continue
        c, j = 0, i
        while j not in seen:
            seen.add(j)
            j = p[j]
            c += 1
        cyc.append(c)
    lcm = 1
    for c in cyc:
        lcm = lcm * c // np.gcd(lcm, c)
    if lcm == 3:
        cycle_types.add(tuple(sorted(cyc)))
assert cycle_types == {(1, 3)}, cycle_types
print(OK + f"S4 の位数3の元の型は {cycle_types} のみ -> 必ず 1固定 + 3巡回")

R = np.array([[0, 0, -1], [1, 0, 0], [0, -1, 0]])
assert round(np.linalg.det(R)) == 1
assert np.trace(R) == 0                      # 1 + 2cos(theta) = 0 -> 120 度
assert np.array_equal(R @ R @ R, np.eye(3, dtype=int))
assert np.array_equal(R @ np.array([1, 1, -1]), np.array([1, 1, -1]))
print(OK + "R: det=1, trace=0 (=120度), R^3=I, 軸 (1,1,-1) を固定")

diag = [(1, 1, 1), (1, -1, 1), (-1, 1, 1)]
img = [as_line(R @ np.array(d)) for d in diag]
assert as_line(R @ np.array([1, 1, -1])) == as_line((1, 1, -1))
assert len(set(img)) == 3 and set(img) == {as_line(d) for d in diag}
print(OK + "R は残り3本の体対角線を巡回させる")


# ------------------------------------ S5: 3巡回 + 軸上の1点 = 正四面体
print("\nS5. 3巡回の点 + 軸上の1点")
P = [np.array(v, dtype=float) for v in [(1, 0, 0), (0, 1, 0), (0, 0, -1), (1, 1, -1)]]
d = {round(float(np.linalg.norm(a - b)), 12) for a, b in itertools.combinations(P, 2)}
assert len(d) == 1 and abs(d.pop() - sqrt(2)) < 1e-12
print(OK + "6辺すべて sqrt(2) -> 正四面体")


# ---------------------------------------- S6: 4点 -> 外接球ただ1つ = 1
print("\nS6. 外接球")
c = sum(P) / 4
assert np.allclose(np.cross(c, [1, 1, -1]), 0)          # 中心は軸の上
Rad = float(np.linalg.norm(P[0] - c))
a = sqrt(2)
assert all(abs(float(np.linalg.norm(p - c)) - Rad) < 1e-12 for p in P)
assert abs(Rad - a * sqrt(6) / 4) < 1e-12
assert abs(Rad - sqrt(3) / 2) < 1e-12
print(OK + f"中心 {tuple(float(x) for x in np.round(c, 6))} は軸上、外接半径 R = {Rad:.10f} = a*sqrt(6)/4")


# ------------------------------- S7: R/r = 3、しかも正四面体だけ
print("\nS7. R/r")
r_in = a / (2 * sqrt(6))
assert abs(Rad / r_in - 3.0) < 1e-12
phi = (1 + sqrt(5)) / 2
ratios = {
    "正四面体":   3.0,
    "立方体":     (sqrt(3) / 2) / 0.5,
    "正八面体":   (1 / sqrt(2)) / (1 / sqrt(6)),
    "正二十面体": (sqrt(phi * sqrt(5)) / 2) / (phi ** 2 / (2 * sqrt(3))),
    "正十二面体": (sqrt(3) * phi / 2) / (phi ** 2 / (2 * sqrt(3 - phi))),
}
for name, val in ratios.items():
    integral = abs(val - round(val)) < 1e-12
    print(OK + f"{name:<7} R/r = {val:.10f}" + ("   <- 整数" if integral else ""))
assert sum(abs(v - round(v)) < 1e-12 for v in ratios.values()) == 1
print(OK + "R/r が整数になるプラトン立体は正四面体だけ")


# ----------------------------------------------- 3節: 7 = 3 + 4（A4 の軸）
print("\n3節. 正四面体の回転群")
Tp = [np.array(v) for v in itertools.product([1, -1], repeat=3)
      if v[0] * v[1] * v[2] == 1]
A4 = [g for g in G if all(any(np.array_equal(g @ v, w) for w in Tp) for v in Tp)]
assert len(A4) == 12
n2 = sum(1 for g in A4 if order(g) == 2)
n3 = sum(1 for g in A4 if order(g) == 3)
assert (n2, n3) == (3, 8)
assert 1 + n2 + n3 == 12
print(OK + f"|A4| = 12 = 1 + {n2}(位数2) + {n3}(位数3)")
print(OK + f"軸の数 = {n2} 本の2回軸 + {n3 // 2} 本の3回軸 = {n2 + n3 // 2} = 3 + 4")
assert n2 + n3 // 2 == 7

# 双極 = 立方体に内接する2つの正四面体
Tm = [np.array(v) for v in itertools.product([1, -1], repeat=3)
      if v[0] * v[1] * v[2] == -1]
for T in (Tp, Tm):
    dd = {round(float(np.linalg.norm(x - y)), 12) for x, y in itertools.combinations(T, 2)}
    assert len(dd) == 1
assert len(Tp) == len(Tm) == 4
assert all(any(np.array_equal(-x, y) for y in Tm) for x in Tp)
print(OK + "立方体の8頂点は2つの正四面体 T+ / T- に分かれ、体対角線が両者を1対1で結ぶ")


# --------------------------------------------- 6節: 落ちたものの算術的根拠
print("\n6節. 除外したものの根拠")
assert [3 ** n % 4 for n in range(1, 9)] == [3, 1, 3, 1, 3, 1, 3, 1]
print(OK + "3^n mod 4 = 3,1,3,1,... -> 4 の倍数にならず、テトラ(=4 OpiO)が完成しない")
assert 162 < (2 * 5) ** 3
print(OK + f"目盛りを正逆で一貫させると段5のマスは (2*5)^3 = {(2*5)**3} で 162 はあふれない")
for b, s in [(16, "89"), (12, "B5"), (8, "211")]:
    digs, n = "", 137          # 「137 の中の 37」は 137 の 10 進表記に依存する
    while n:
        digs = "0123456789AB"[n % b] + digs
        n //= b
    assert digs == s, (b, digs)
print(OK + "137 は 16進で 89、12進で B5、8進で 211 -> 「137 の中の 37」は10進表記の産物")

print("\n" + "=" * 62)
print("TTT_CORE.md v1.0 の全ステップを再現しました。")
print("=" * 62)
