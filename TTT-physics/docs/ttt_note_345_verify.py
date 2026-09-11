"""TTT-CORE 補注 2026-09-11 の検算（標準ライブラリのみ）。全 assert が通れば完走。"""
import itertools as it, math

# --- §1 3-4-5 と 37 ---
assert 3*4 + 5**2 == 3**2 + 3*4 + 4**2 == 4**3 - 3**3 == 37
assert [round(25 - 24*math.cos(math.radians(t))) for t in (0, 60, 90, 120, 180)] == [1, 13, 25, 37, 49]
assert all(a*b + c*c == a*a + a*b + b*b for a, b, c in [(3,4,5), (5,12,13), (8,15,17)])  # (3,4) は特別でない
assert [3*n*n + 3*n + 1 for n in range(6)] == [1, 7, 19, 37, 61, 91]                       # 中心六角数

# 正四面体 T+ の有向辺 12 本 = FCC 最近接 12
Tp = [v for v in it.product([1,-1], repeat=3) if v[0]*v[1]*v[2] == 1]
Tm = [tuple(-x for x in v) for v in Tp]
sub = lambda a, b: tuple(x-y for x, y in zip(a, b))
E  = {sub(Tp[i], Tp[j]) for i, j in it.permutations(range(4), 2)}
Em = {sub(Tm[i], Tm[j]) for i, j in it.permutations(range(4), 2)}
fcc = {v for v in it.product([2,-2,0], repeat=3) if sorted(map(abs, v)) == [0,2,2]}
assert len(E) == 12 and E == Em == fcc
# 6 辺 15 対 = 直交 3 + 60° 12
und = [sub(Tp[i], Tp[j]) for i, j in it.combinations(range(4), 2)]
dot = lambda a, b: sum(x*y for x, y in zip(a, b))
angles = [round(math.degrees(math.acos(abs(dot(u, w)) / 8))) for u, w in it.combinations(und, 2)]
assert sorted(angles) == [60]*12 + [90]*3
# 各座標軸に直交する線分は 4 本ずつ
assert [sum(1 for e in E if e[i] == 0) for i in range(3)] == [4, 4, 4]
# 正方格子で 25、三角格子で 37
u, v, w = (1,1,0), (1,-1,0), (1,0,-1)
lin = lambda a, x, b, y: tuple(a*p + b*q for p, q in zip(x, y))
assert dot(lin(3,u,4,v), lin(3,u,4,v)) // 2 == 25
assert dot(lin(3,v,4,w), lin(3,v,4,w)) // 2 == 37
# 核本来のピタゴラス 1+2=3
assert 1 + 2 == 3

# --- §2 立方版 3-4-5 ---
assert 3**3 + 4**3 + 5**3 == 6**3 == 216
assert [a for a in range(1, 10**5) if a**3 + (a+1)**3 + (a+2)**3 == (a+3)**3] == [3]
assert 6**3 - 5**3 == 3**3 + 4**3 == 91
assert 91 + 37 == 128 == 2*4**3 and 91 - 37 == 54 == 2*3**3
assert 5**3 + 4**3 - 3**3 == 6**3 - 2*3**3 == 216 - 54 == 162
assert 162 - 125 == 37
R = [2*3**(k-1) for k in range(1, 6)]; B = [3**(k-1) for k in range(1, 6)]
assert R == [2,6,18,54,162] and B == [1,3,9,27,81]
assert 125 - 81 == 44 and 162 - 125 == 37 and 44 + 37 == 81
assert 2*3**4 + 3**3 == 5**3 + 4**3 == 189 == 7*27

# --- §3 17 の帳簿（D-1: 先に収縮） ---
assert 486 - 162 == 324 and 324 // 3 == 108 and 108 - 91 == 17
assert 324 - 91 == 233 == 216 + 17 == 2*108 + 17
assert 233 % 3 != 0            # 後で収縮すると非整数 → 先に収縮のみ生存
assert (108 + 162) % 3 == 0    # k=6 の 270 → あふれ 54 は 3 で割れる（9/7 検定）

# --- §4 S8 試み ---
def consecutive_power_solutions(d, N=2000):
    return [n for n in range(d+1, N) if sum((n-i)**d for i in range(1, d+1)) == n**d]
assert consecutive_power_solutions(2) == [5] and consecutive_power_solutions(3) == [6]
assert all(consecutive_power_solutions(d) == [] for d in (1, 4, 5, 6))
core = {3, 4, 6, 7, 8, 12}
assert 5 not in core                       # 核に 5 はない
assert {(x, y) for x in core for y in core if x - y == 5} == {(8, 3), (12, 7)}
small = [(a,b,c,d) for d in range(1,20) for a in range(1,d) for b in range(a,d) for c in range(b,d) if a**3+b**3+c**3==d**3]
assert small[0] == (3,4,5,6) and (1,6,8,9) in small   # 「連続」を外せば最小解にすぎない

print("ttt_note_345_verify: all assertions passed")
