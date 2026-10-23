"""
TTT 検証スクリプト: 創生の運動（Z の単振動と右手・左手の逆回り）

確認すること（すべて assert）
  1. 球面上で z = sin ωt のとき、XY の半径の2乗は (1 + cos 2ωt)/2（XY は 2ω で振動）
  2. 右手（左回り）の軌跡は XYZ = -1 の正四面体の4頂点、左手（右回り）は XYZ = +1 の4頂点を通る
  3. 両手の和は X 軸、差は Y 軸上の直線になる
  4. |E|^2 = 1 + (1/2) sin^2 2ωt（内側の境界 1、外側の境界 sqrt(3/2)）
  5. 正四面体の頂点で Z の速度が 0、速さは最小 1。軸上の点で速さは最大 sqrt(3)
  6. 1/4 周期の時間の進みは (x, y, z) -> (-y, x, -z)（4回回映）で、動かない点は原点だけ
  7. 1周期の時間平均は原点

実行: python3 verify_genesis_motion.py
"""
import numpy as np

t = np.linspace(0, 2 * np.pi, 4001)


def right(th):
    return np.array([np.cos(th), np.sin(th), -np.sin(2 * th) / np.sqrt(2)])


def left(th):
    return np.array([np.cos(th), -np.sin(th), -np.sin(2 * th) / np.sqrt(2)])


# 1
z = np.sin(t)
r2 = 1 - z**2
assert np.allclose(r2, (1 + np.cos(2 * t)) / 2)
print("PASS 1: z = sin ωt → XY 半径² = (1 + cos 2ωt)/2")

# 2
verts = np.pi / 4 + np.arange(4) * np.pi / 2
R = {tuple(np.sign(right(a)).astype(int)) for a in verts}
L = {tuple(np.sign(left(a)).astype(int)) for a in verts}
assert R == {(1, 1, -1), (-1, 1, 1), (-1, -1, -1), (1, -1, 1)}
assert L == {(1, -1, -1), (-1, -1, 1), (-1, 1, -1), (1, 1, 1)}
for a in verts:
    v = right(a)
    assert np.allclose(np.abs(v), np.abs(v[0]))  # (±1,±1,±1) の方向そのもの
assert all(np.prod(p) == -1 for p in R) and all(np.prod(p) == 1 for p in L)
print("PASS 2: 右手 → XYZ=-1 の4頂点、左手 → XYZ=+1 の4頂点")

# 3
S = right(t)[:2] + left(t)[:2]
D = right(t)[:2] - left(t)[:2]
assert np.allclose(S[1], 0) and np.allclose(S[0], 2 * np.cos(t))
assert np.allclose(D[0], 0) and np.allclose(D[1], 2 * np.sin(t))
print("PASS 3: 和 = (2cos ωt, 0)（X 軸）、差 = (0, 2sin ωt)（Y 軸）")

# 4
E2 = np.sum(right(t) ** 2, axis=0)
assert np.allclose(E2, 1 + 0.5 * np.sin(2 * t) ** 2)
assert np.isclose(E2.min(), 1) and np.isclose(E2.max(), 1.5)
print("PASS 4: |E|² = 1 + ½ sin² 2ωt（1 〜 3/2）")

# 5
vel = np.array([-np.sin(t), np.cos(t), -np.sqrt(2) * np.cos(2 * t)])
speed2 = np.sum(vel**2, axis=0)
assert np.allclose(speed2, 1 + 2 * np.cos(2 * t) ** 2)
for a in verts:
    assert np.isclose(-np.sqrt(2) * np.cos(2 * a), 0, atol=1e-12)
print("PASS 5: 四面体の頂点で Z の速度 0・速さ 1、軸上で速さ √3")

# 6
for th in np.linspace(0, 2 * np.pi, 97):
    x, y, zz = right(th)
    assert np.allclose(right(th + np.pi / 2), [-y, x, -zz])
M = np.array([[0, -1, 0], [1, 0, 0], [0, 0, -1]])
w, vecs = np.linalg.eig(M)
assert not np.any(np.isclose(w, 1))  # 固有値1がない → 動かない点は原点だけ
print("PASS 6: 1/4 周期 = (x,y,z)→(-y,x,-z)、固有値1なし → 不動点は原点のみ")

# 7
tt = np.linspace(0, 2 * np.pi, 100000, endpoint=False)
assert np.allclose(right(tt).mean(axis=1), 0, atol=1e-12)
assert np.allclose(left(tt).mean(axis=1), 0, atol=1e-12)
print("PASS 7: 1周期の時間平均 = 原点")
