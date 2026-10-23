"""
TTT 検証スクリプト v2: 「どんな測り方なら 1/500 が出るか」の逆探索

目標 r* = 1/500 = 0.002
  (501/500 − 1 = 125.25/125 − 1 = 1/500。角度にすると 1周の 0.72°)

方針（後付けの数合わせを防ぐため、探索の前に条件を固定する）
  1. 正四面体から出る角度を事前に固定する（下の ANGLES）
  2. 個数 n も TTT に出てくる数に事前に固定する（下の N_TTT）
  3. 測り方: n 個並べたときの閉じからのずれ r = |n·x − 最も近い整数|
     （x は「1周（または全立体角）に対する割合」）
  4. r が 1/500 の ±1% 以内なら「一致」
  5. 帰無検定: 角度を一様乱数に置き換えて同じ探索を 20000 回行い、
     偶然に同じ数以上の一致が出る確率 p を求める

実行: python3 verify_tetra_twist_v2.py
"""
import random
from mpmath import mp, mpf, acos, asin, atan, sqrt, pi, nstr

mp.dps = 40
TARGET = mpf(1) / 500
TOL = mpf("0.01")  # 相対 ±1%

# ---- 1. 正四面体由来の角度（割合で表す） -------------------------------
ANGLES = {
    "二面角 arccos(1/3) / 2π": acos(mpf(1) / 3) / (2 * pi),
    "中心角 arccos(-1/3) / 2π（109.47°）": acos(mpf(-1) / 3) / (2 * pi),
    "頂点立体角 arccos(23/27) / 4π": acos(mpf(23) / 27) / (4 * pi),
    "BCらせんのねじれ arccos(-2/3) / 2π": acos(mpf(-2) / 3) / (2 * pi),
    "辺と面の角 arccos(1/√3) / 2π（54.74°）": acos(1 / sqrt(3)) / (2 * pi),
    "面と中心軸の角 arcsin(1/3) / 2π（19.47°）": asin(mpf(1) / 3) / (2 * pi),
}

# ---- 2. TTT に出てくる個数 ----------------------------------------------
N_TTT = [2, 3, 4, 5, 6, 8, 10, 12, 17, 18, 20, 24, 30, 36, 37, 54, 60,
         74, 91, 125, 126, 137, 162, 486, 500, 501, 1500, 1875, 2000]


def residual(n, x):
    v = n * x
    return abs(v - mp.nint(v))


def hits(angle_values, ns):
    out = []
    for name, x in angle_values.items():
        for n in ns:
            r = residual(n, x)
            rel = abs(r - TARGET) / TARGET
            out.append((rel, name, n, r))
    return out


print("=" * 72)
print("目標 r* = 1/500 = 0.002（1周の 0.72°）、許容 ±1%")
print(f"角度 {len(ANGLES)} 種 × 個数 {len(N_TTT)} 種 = {len(ANGLES)*len(N_TTT)} 通り")
print("=" * 72)

res = hits(ANGLES, N_TTT)
res.sort(key=lambda t: t[0])
matched = [t for t in res if t[0] <= TOL]

print("\n[結果] 1/500 に近い順 上位10")
print(f"{'角度':<42}{'n':>6}{'ずれ r':>14}{'1/500との相対差':>16}")
for rel, name, n, r in res[:10]:
    flag = "  ← 一致" if rel <= TOL else ""
    print(f"{name:<42}{n:>6}{nstr(r, 8):>14}{nstr(rel*100, 4)+'%':>16}{flag}")
print(f"\n一致（±1%以内）: {len(matched)} 件")

# ---- 5. 帰無検定 ----------------------------------------------------------
random.seed(20261023)
TRIALS = 20000
k_obs = len(matched)
count_ge = 0
total_hits = 0
for _ in range(TRIALS):
    fake = {f"r{i}": mpf(random.random()) for i in range(len(ANGLES))}
    h = sum(1 for t in hits(fake, N_TTT) if t[0] <= TOL)
    total_hits += h
    if h >= max(k_obs, 1):
        count_ge += 1
print("\n[帰無検定] 角度を一様乱数に置き換えた場合")
print(f"  偶然に出る一致数の平均: {total_hits/TRIALS:.3f} 件")
print(f"  {max(k_obs,1)} 件以上出る確率 p = {count_ge/TRIALS:.4f}")

# ---- 補助: 125 の半周ずれ ---------------------------------------------------
print("\n[補助] 前回目立った n=125（二面角）の半周からのずれ")
x = ANGLES["二面角 arccos(1/3) / 2π"]
v = 125 * x
half = abs(v - (mp.floor(v) + mpf(1) / 2))
print(f"  125·θ/2π = {nstr(v, 12)} 周、半周 24.5 からのずれ = {nstr(half, 8)} 周"
      f"（1/500 の {nstr(half/TARGET, 5)} 倍）")

print("\n" + "=" * 72)
if k_obs == 0:
    print("判定: 事前に固定した測り方では 1/500 は出ない")
elif count_ge / TRIALS < 0.05:
    print("判定: 一致あり、かつ偶然では出にくい（p < 0.05）→ 候補として残す")
else:
    print("判定: 一致はあるが、偶然でも同程度に出る（p ≥ 0.05）→ 根拠にならない")
