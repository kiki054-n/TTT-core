"""
TTT 検証スクリプト 2026-10-09：F の発生
  円運動する B と I から、F ＝ I × B の単振動が体対角線 (1,1,1) 上に生じる条件を調べる。
  numpy のみ。すべての assert が通れば成立。
"""
import numpy as np

n = np.array([1.0, 1.0, 1.0]) / np.sqrt(3)          # 体対角線 (1,1,1)
e1 = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)        # n に垂直な面の基底
e2 = np.cross(n, e1)
w = 1.0
t = np.linspace(0, 2 * np.pi, 4001)[:-1]
I0, B0, phi = 1.0, 1.0, 0.7

def rot(sense, phase):
    a = sense * w * t + phase
    return np.outer(np.cos(a), e1) + np.outer(np.sin(a), e2)

def main_freq(sig):
    spec = np.abs(np.fft.rfft(sig - sig.mean()))
    return np.argmax(spec)        # 1周期 2π の窓なので、値 k は角振動数 k·ω

ok = 0
def check(cond, msg):
    global ok
    assert cond, msg
    ok += 1
    print("  ✓", msg)

# ---- Block 1：B と I が逆向きに回る（双極の回転） ----
print("Block 1：B と I が体対角線に垂直な面で逆向きに回る")
B = B0 * rot(+1, 0.0)
I = I0 * rot(-1, phi)
F = np.cross(I, B)
Fpar = F @ n
check(np.allclose(F - np.outer(Fpar, n), 0), "F は常に体対角線 (1,1,1) の上にある")
shm = I0 * B0 * np.sin(2 * w * t - phi)
check(np.allclose(Fpar, shm) or np.allclose(Fpar, -shm),
      "F は単振動 ±I0·B0·sin(2ωt − φ)（符号は右手系・左手系で決まる）")
check(main_freq(Fpar) == 2, "振動数は回転の 2 倍（2ω）")
check(abs(Fpar.mean()) < 1e-12, "F の時間平均はゼロ（＋F と −F で総和ゼロ）")
check(np.isclose(np.abs(Fpar).max(), I0 * B0), "振幅は |I|·|B|（＋F と −F が両端）")

# ---- Block 2：B と I が同じ向きに回る ----
print("Block 2：B と I が同じ向きに回る")
I_co = I0 * rot(+1, phi)
F_co = np.cross(I_co, B) @ n
check(np.allclose(F_co, F_co[0]), "F は一定で振動しない")
check(np.isclose(F_co[0], -I0 * B0 * np.sin(phi)) or np.isclose(F_co[0], I0 * B0 * np.sin(phi)),
      "大きさは位相差で決まる I0·B0·sin φ（φ＝0 なら F＝0）")
check(abs(F_co.mean()) > 0.1, "時間平均がゼロにならない（総和ゼロを保てない）")

# ---- Block 3：B と I が別の面で回る ----
print("Block 3：B と I が別々の面で回る")
m = np.array([1.0, 0.0, 0.0])
a = w * t
I_x = I0 * (np.outer(np.cos(-a), [0, 1, 0]) + np.outer(np.sin(-a), [0, 0, 1]))
F_x = np.cross(I_x, B)
dirs = F_x / np.linalg.norm(F_x, axis=1, keepdims=True).clip(1e-12)
spread = np.linalg.svd(dirs - dirs.mean(0), compute_uv=False)
check(spread[1] > 1e-3, "F の向きが一本の線に定まらない（単振動にならない）")

# ---- Block 4：Cl(3) の中での F・B・I と体対角線 ----
print("Block 4：Cl(3)（パウリ行列）で F＋B＋I と体対角線の関係")
sx = np.array([[0, 1], [1, 0]], complex)
sy = np.array([[0, -1j], [1j, 0]], complex)
sz = np.array([[1, 0], [0, -1]], complex)
E = np.eye(2)
X, Y, Z = sx, sy, sz
PS = X @ Y @ Z                                  # XYZ（擬スカラー）
Fb, Bb, Ib = Z @ Y, X @ Z, Y @ X                # 2026-10-05 ノートの定義
check(np.allclose(Fb @ Bb @ Ib, -E), "F・B・I ＝ −1（10-05 ノートと一致）")
S = Fb + Bb + Ib
check(np.allclose(S, -(X + Y + Z) @ PS), "F＋B＋I ＝ −(X＋Y＋Z)·XYZ：三つの回転面の和は体対角線の双対")
check(np.allclose(S @ S, -3 * E), "(F＋B＋I)² ＝ −3")
u = S / np.sqrt(3)
check(np.allclose(u @ u, -E), "u ＝ (F＋B＋I)/√3 は 2乗 −1 の新しい回転生成元（体対角線まわり）")
q = (E + S) / 2
check(np.allclose(q, np.cos(np.pi/3) * E + np.sin(np.pi/3) * u), "(1＋F＋B＋I)/2 ＝ e^{πu/3}")
img = [q @ V @ np.linalg.inv(q) for V in (X, Y, Z)]
cyc = (np.allclose(img[0], Y) and np.allclose(img[1], Z) and np.allclose(img[2], X)) or \
      (np.allclose(img[0], Z) and np.allclose(img[1], X) and np.allclose(img[2], Y))
check(cyc, "e^{πu/3} は X・Y・Z を巡回させる（体対角線まわり 120°）")
check(np.allclose(np.linalg.matrix_power(q, 3), -E), "e^{πu} ＝ (e^{πu/3})³ ＝ −1")
check(np.allclose(Fb @ Bb @ Ib @ np.linalg.matrix_power(q, 3), E), "F・B・I・e^{πu} ＝ ＋1（π を体対角線の位相として閉じる）")
check(np.allclose(np.linalg.matrix_power(q, 6), E), "6 回で元に戻る（3次元では 3 回、双極で 2 倍）")

print(f"\n{ok} assert 全通過")
