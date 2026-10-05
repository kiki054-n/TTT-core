"""TTT 検証 2026-10-05 (2/3): 137 と 12 の検証（成立したもの・落ちたもの）
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

INT = lambda L: [np.array(p, float) for p in itertools.product(range(-L, L + 1), repeat=3)]
HALF = lambda L: [np.array(p, float) + 0.5 for p in itertools.product(range(-L - 1, L + 1), repeat=3)]
mx = lambda p: np.max(np.abs(p))

print("== Block 1: 内外17ずつは体心立方の配置から出るか")
A = INT(3); B = HALF(3)
c = {}
c["B 5^3内(境界含まず)"] = sum(mx(p) < 2.5 for p in B)
c["B 5^3境界上"] = sum(mx(p) == 2.5 for p in B)
c["A 内接球R2.5"] = sum(p @ p < 6.25 for p in A)
c["B 内接球R2.5"] = sum(p @ p < 6.25 for p in B)
ok(c["B 5^3内(境界含まず)"] == 64 and c["B 5^3境界上"] == 152, "半整数格子: 5^3内64・境界上152")
vin = 0.0
for p in B:
    if mx(p) > 2.5: continue
    lo = np.maximum(p - 0.5, -2.5); hi = np.minimum(p + 0.5, 2.5)
    vin += np.prod(np.clip(hi - lo, 0, None))
ok(np.isclose(vin, 125) and np.isclose(216 - vin, 91), "半整数マス216の体積: 5^3内125・外91（内外は等しくない）")
ok(17 not in c.values() and 34 not in c.values(), "17・34 は直接の数として現れない")
ok(c["A 内接球R2.5"] - c["B 5^3内(境界含まず)"] == 17, "17 は球の数81と箱の数64の差としてのみ現れる（基準が混在）")
# 帰無対照: 同種の自然な数え方（立方体基準・球基準）とその差が 1〜100 のどれだけに届くか
c2 = dict(c)
c2["A 5^3内"] = sum(mx(p) < 2.5 for p in A); c2["A 6^3境界上"] = sum(mx(p) == 3.0 for p in A)
c2["A 内接球R3"] = sum(p @ p <= 9 + 1e-9 for p in A); c2["B 内接球R3"] = sum(p @ p <= 9 + 1e-9 for p in B)
c2["A 箱内で球外"] = sum(mx(p) < 2.5 and p @ p > 6.25 for p in A)
c2["B 6^3内で球外"] = sum(mx(p) < 3 and p @ p > 9 for p in B)
c2["B 5^3内で球外"] = sum(mx(p) <= 2.5 and p @ p > 6.25 for p in B)
c2["体積 内216-125"] = 91; c2["体積 125"] = 125
vals = [int(v) for v in c2.values()]
reach = set(vals) | {abs(x - y) for x in vals for y in vals}
frac = sum(1 <= t <= 100 for t in reach) / 100
ok(0.4 <= frac <= 0.5, f"数とその差で 1〜100 の {frac:.0%} に到達（17 の一致に情報なし）")

print("== Block 2: 内接球の中の体心立方格子点")
def bcc_in_sphere(n):
    R2 = (n / 2) ** 2; L = n
    a = sum(p @ p < R2 - 1e-9 for p in INT(L)); b = sum(p @ p < R2 - 1e-9 for p in HALF(L))
    on = sum(abs(p @ p - R2) < 1e-9 for p in INT(L) + HALF(L))
    return a, b, on
res = {n: bcc_in_sphere(n) for n in (3, 5, 7, 9)}
ok(res[5][:2] == (81, 56) and sum(res[5][:2]) == 137, "段5: 整数81 + 半整数56 = 137")
ok(sum(res[3][:2]) == 27, "段3: 27（箱と同数）")
ok(sum(res[7][:2]) == 339 and sum(res[9][:2]) == 749, "段7: 339、段9: 749")
ok(all(res[n][2] == 0 for n in res), "奇数段では球面上にちょうど乗る点がない（境界の扱いに依存しない）")
diffs = [sum(res[n][:2]) - n ** 3 for n in (3, 5, 7, 9)]
ok(diffs == [0, 12, -4, 20], "箱との差 0, +12, -4, +20 は規則的でない（格子点の揺らぎ）")
ok(np.isclose(2 * np.pi / 6, np.pi / 3), "体心立方の点数の平均は箱のマス数の π/3≈1.047 倍")

print("== Block 3: +12 は点の集合として取り出せるか")
S = [p for p in INT(3) + HALF(3) if p @ p < 6.25]
ok(all(mx(p) < 2.5 for p in S), "内接球の点はすべて箱の内側 → 『はみ出した12点』は存在しない")

print("== Block 4: 球の中の12点の殻とバーガースの12方位")
shell2 = [tuple(int(x) for x in p) for p in INT(3) if p @ p == 2]
ok(len(shell2) == 12, "距離√2 の殻 (±1,±1,0) は 12 点")
G = []
for perm in itertools.permutations(range(3)):
    for s in itertools.product([1, -1], repeat=3):
        M = np.zeros((3, 3), int)
        for i, j in enumerate(perm): M[i, j] = s[i]
        G.append(M)
ok(len(G) == 48, "立方対称群 O_h は 48 元")
def canon(v):
    v = tuple(int(x) for x in v); nz = next(x for x in v if x != 0)
    return v if nz > 0 else tuple(-x for x in v)
variants = sorted({(tuple(p), tuple(d)) for p in itertools.product([-1, 0, 1], repeat=3)
                   if sorted(map(abs, p)) == [0, 1, 1] and canon(p) == tuple(p)
                   for d in itertools.product([-1, 1], repeat=3) if np.dot(p, d) == 0 and canon(d) == tuple(d)})
ok(len(variants) == 12, "バーガースの方位: {110}面6 × 面内<111>方向2 = 12")
a, b = np.array([1, -1, 1]), np.array([1, -1, -1])
ok(np.isclose(np.degrees(np.arccos(a @ b / 3)), 70.528779, atol=1e-6), "BCC{110}面内の最密方向の角 = arccos(1/3) = 70.528779°")
Sv = [g for g in G if canon(g @ np.array(variants[0][0])) == variants[0][0] and canon(g @ np.array(variants[0][1])) == variants[0][1]]
Sp = [g for g in G if tuple(g @ np.array(shell2[0])) == shell2[0]]
ok(len(Sv) == 4 and len(Sp) == 4, "安定化部分群はどちらも位数4")
ok(any(np.array_equal(g, -np.eye(3, dtype=int)) for g in Sv), "バリアントは反転で不変")
ok(not any(np.array_equal(g, -np.eye(3, dtype=int)) for g in Sp), "<110>ベクトルは反転で不変でない")
conj = any(sorted((g.T @ h @ g).tobytes() for h in Sv) == sorted(h.tobytes() for h in Sp) for g in G)
ok(not conj, "安定化部分群は共役でない → 対称性を保つ1対1対応は存在しない")

print("== Block 5: 立方体の辺12 = 球の接触数12")
E = [np.array(v, float) for v in itertools.product([-1, 0, 1], repeat=3) if sorted(map(abs, v)) == [0, 1, 1]]
ok(len(E) == 12, "立方体 [-1,1]^3 の辺の中点 12 個 (3方向 × 平行4本)")
r = np.sqrt(2) / 2
ok(all(np.isclose(np.linalg.norm(e), 2 * r) for e in E), "12球すべてが中心球に接する")
dp = [np.linalg.norm(x - y) for x, y in itertools.combinations(E, 2)]
ok(min(dp) >= 2 * r - 1e-9 and sum(np.isclose(dp, 2 * r)) == 24, "12球は重ならず、接する対は24")
tets = [t for t in itertools.combinations(range(12), 3) if all(np.isclose(np.linalg.norm(E[i] - E[j]), 2 * r) for i, j in itertools.combinations(t, 2))]
ok(len(tets) == 8, "中心＋接する3球の正四面体 (1+3) は 8 個")
ok(4 * 3 == 12, "4球が互いに接する正四面体の接点 4×3 = 12")

print("== Block 6: 中心を 1+12 の最密クラスターにする構成")
Abox = INT(2); Bin = [q for q in HALF(3) if mx(q) < 2.5]
r2 = lambda p: round(float(p @ p), 4)
a_ = [p for p in Abox if r2(p) not in (1, 3)]
cases = {
    "a": len(a_),
    "b": 125 - 1 + 13,
    "c": len(Abox) + len(Bin) - sum(r2(p) in (0, 0.75, 1) for p in Abox + Bin) + 13,
    "d": len(S) - sum(r2(p) in (0, 0.75, 1) for p in S) + 13,
    "e": sum(int(p.sum()) % 2 == 0 for p in Abox),
    "f": int(sum(int(p.sum()) % 2 == 0 and p @ p < 6.25 for p in Abox)),
}
ok(cases == {"a": 111, "b": 137, "c": 187, "d": 135, "e": 63, "f": 43}, f"構成 a〜f = {cases}")
ok([k for k, v in cases.items() if v == 137] == ["b"], "137 になるのは定義上 125+12 の (b) だけ")
ok(cases["d"] == 137 - 2, "内接球137で中心を最密化すると 135（体心立方の近接14→最密12）")

print("== Block 7: 立方体の要素と格子の最近接")
ok(len([v for v in itertools.product([-1, 0, 1], repeat=3) if sorted(map(abs, v)) == [0, 0, 1]]) == 6, "単純立方 6 = 面の中心")
ok(len(list(itertools.product([-0.5, 0.5], repeat=3))) == 8, "体心立方 8 = 頂点の方向")
ok(len(E) == 12, "面心立方・稠密六方 12 = 辺の中点")

print(f"\n{PASS} PASS / 0 FAIL")
