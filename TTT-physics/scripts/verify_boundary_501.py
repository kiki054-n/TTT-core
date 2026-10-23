"""
TTT 検証スクリプト v4: 面心立方格子 5×5×5 の境界の分解と「501 の 1」

調べること
  1. 有限ブロックの点を 角・辺・面・内部 に分け、種類ごとに数える
  2. 境界の点を「セルの内側にある割合」（面1/2・辺1/4・角1/8）で重みづけすると
     周期境界の 500 / 500 / 1000 に戻るか
  3. ブロックの中心はどの種類の点か（N=3..7 で比較）
  4. ブロックの対称操作（立方体の 48 個の対称）で動かない点はいくつあるか
     → 500 に足される「1」の自然な候補になるか

実行: python3 verify_boundary_501.py
"""
from fractions import Fraction as Fr
from itertools import product, permutations


def kind(p):
    """4倍座標 p の種類（格子点 / 八面体 / 四面体 / なし）"""
    m = tuple(c % 4 for c in p)
    if all(c % 2 == 1 for c in m):
        return "四面体"
    if all(c % 2 == 0 for c in m):
        n2 = sum(1 for c in m if c == 2)
        return "格子点" if n2 % 2 == 0 else "八面体"
    return None


def block_sites(N):
    L = 4 * N
    return [p for p in product(range(L + 1), repeat=3) if kind(p)]


def place(p, L):
    b = sum(1 for c in p if c in (0, L))
    return {0: "内部", 1: "面", 2: "辺", 3: "角"}[b]


WEIGHT = {"内部": Fr(1), "面": Fr(1, 2), "辺": Fr(1, 4), "角": Fr(1, 8)}


def analyze(N, verbose=True):
    L = 4 * N
    sites = block_sites(N)
    table = {}
    for p in sites:
        k, w = kind(p), place(p, L)
        table.setdefault(k, {}).setdefault(w, 0)
        table[k][w] += 1
    weighted = {k: sum(WEIGHT[w] * n for w, n in d.items()) for k, d in table.items()}
    center = (2 * N, 2 * N, 2 * N)
    ckind = kind(center)

    # 立方体の対称 48 個（座標の置換 × 反転、中心 L/2 まわり）
    def ops():
        for perm in permutations(range(3)):
            for signs in product((1, -1), repeat=3):
                yield perm, signs

    def apply(p, op):
        perm, signs = op
        q = [p[perm[i]] for i in range(3)]
        return tuple(L - q[i] if signs[i] < 0 else q[i] for i in range(3))

    fixed = [p for p in sites if all(apply(p, op) == p for op in ops())]
    # 軌道の大きさの分布
    seen, orbit_sizes = set(), {}
    for p in sites:
        if p in seen:
            continue
        orb = {apply(p, op) for op in ops()}
        seen |= orb
        orbit_sizes[len(orb)] = orbit_sizes.get(len(orb), 0) + 1

    if verbose:
        print("=" * 66)
        print(f"N = {N}（{N}×{N}×{N} = {N**3} セル）")
        print("=" * 66)
        cols = ["角", "辺", "面", "内部"]
        print(f"{'種類':<8}" + "".join(f"{c:>8}" for c in cols) + f"{'合計':>8}{'重みづけ':>10}")
        for k in ("格子点", "八面体", "四面体"):
            d = table.get(k, {})
            row = f"{k:<8}" + "".join(f"{d.get(c, 0):>8}" for c in cols)
            row += f"{sum(d.values()):>8}{str(weighted[k]):>10}"
            print(row)
        print(f"\n中心 ({N/2}, {N/2}, {N/2}) の種類: {ckind}")
        print(f"48個の対称すべてで動かない点: {len(fixed)} 個 → {[kind(p) for p in fixed]}")
        print(f"軌道の大きさの分布 {{大きさ: 個数}}: {dict(sorted(orbit_sizes.items()))}")
    return table, weighted, ckind, fixed


t5, w5, c5, f5 = analyze(5)

print("\n" + "=" * 66)
print("判定（N = 5）")
print("=" * 66)
ok_w = (w5["格子点"], w5["八面体"], w5["四面体"]) == (500, 500, 1000)
print(f"  {'PASS' if ok_w else 'FAIL'}  重みづけ（面1/2・辺1/4・角1/8）で 500 / 500 / 1000 に戻る")
print(f"  {'PASS' if len(f5) == 1 else 'FAIL'}  すべての対称で動かない点はちょうど 1 個")
print(f"  INFO  その 1 個（中心）は「{c5}」")
print(f"  INFO  格子点 500 ＋ 中心 1 = 501、501 / 4 = {Fr(501, 4)} = {501/4}")

print("\n" + "=" * 66)
print("N による中心の種類の違い")
print("=" * 66)
print(f"{'N':>3}{'セル':>7}{'中心の種類':>10}{'動かない点':>10}{'格子点(周期)':>14}{'＋1':>7}{'÷4':>10}")
for N in range(2, 9):
    _, w, ck, fx = analyze(N, verbose=False)
    a = int(w["格子点"])
    print(f"{N:>3}{N**3:>7}{ck:>10}{len(fx):>10}{a:>14}{a+1:>7}{(a+1)/4:>10}")
