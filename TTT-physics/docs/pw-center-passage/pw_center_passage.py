"""
ペイジ＝ウッターズ模型による「中心の通過」と「基底状態」の検証
  系 S : 調和振動子（ħ = m = ω = 1, E_n = n + 1/2）を N 準位で打ち切り
  時計 C: 固有エネルギー ε_n = -E_n を持つ N 準位の理想時計
  全体  : |Ψ> = Σ c_n |E_n>_S ⊗ |-E_n>_C   →  (H_C + H_S)|Ψ> = 0

時計の目盛り状態 |t> = Σ_k e^{-i ε_k t} |ε_k> で条件付けると
  |ψ(t)> = <t|_C |Ψ> = Σ c_n e^{-i E_n t} |E_n>
が得られ、中から見た時間発展になる。

確認すること
  1. 拘束 (H_C + H_S)|Ψ> = 0 が成り立つ（外から見て静止）
  2. コヒーレント状態：系と時計が相関し、中心を「通過」する
  3. 基底状態：系と時計の相関がゼロ、中心の確率は時間によらず一定（最大）
"""
import numpy as np
from numpy.polynomial.hermite import hermval
from math import factorial, pi
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = 40                      # 打ち切り準位数
E = np.arange(N) + 0.5      # 系のエネルギー
eps = -E                    # 時計のエネルギー（双極の対）
x = np.linspace(-5, 5, 801)
dx = x[1] - x[0]
t = np.linspace(0, 2 * pi, 241)   # 1周期
CENTER = 0.3                # 「中心付近」とみなす幅 |x| < CENTER

# 振動子の固有関数 φ_n(x)
phi = np.zeros((N, x.size))
for n in range(N):
    c = np.zeros(n + 1); c[n] = 1
    phi[n] = hermval(x, c) * np.exp(-x**2 / 2) / np.sqrt(2**n * factorial(n) * np.sqrt(pi))

def coherent(alpha):
    n = np.arange(N)
    c = np.exp(-abs(alpha)**2 / 2) * alpha**n / np.sqrt([float(factorial(k)) for k in n])
    return c / np.linalg.norm(c)

def ground():
    c = np.zeros(N, complex); c[0] = 1
    return c

def global_state(c):
    """|Ψ> を S⊗C の N×N 行列として作る（行=系の準位, 列=時計の準位）"""
    return np.diag(c).astype(complex)

def constraint_residual(Psi):
    """|| (H_S ⊗ 1 + 1 ⊗ H_C) Ψ ||"""
    HS = np.diag(E); HC = np.diag(eps)
    return np.linalg.norm(HS @ Psi + Psi @ HC.T)

def entanglement_entropy(Psi):
    s = np.linalg.svd(Psi, compute_uv=False)
    p = s**2; p = p[p > 1e-15]
    return float(-(p * np.log(p)).sum())

def conditional(Psi, tt):
    """<t|_C Ψ : 時計の目盛り t で条件付けた系の状態（エネルギー基底）"""
    clock_t = np.exp(-1j * eps * tt)          # |t> の成分
    return Psi @ np.conj(clock_t)             # 時計側で内積

def analyse(name, c):
    Psi = global_state(c)
    res = constraint_residual(Psi)
    S = entanglement_entropy(Psi)
    dens = np.zeros((t.size, x.size)); xm = np.zeros(t.size); pc = np.zeros(t.size)
    for i, tt in enumerate(t):
        psi_x = conditional(Psi, tt) @ phi
        d = abs(psi_x)**2; d /= d.sum() * dx
        dens[i] = d
        xm[i] = (x * d).sum() * dx
        pc[i] = d[abs(x) < CENTER].sum() * dx
    print(f"--- {name} ---")
    print(f"  拘束の残差 ||(H_C+H_S)Ψ||   = {res:.2e}")
    print(f"  系と時計のもつれエントロピー = {S:.4f}")
    print(f"  <x>(t) の振れ幅              = {xm.max() - xm.min():.4f}")
    print(f"  中心付近の確率 最小/最大/時間平均 = "
          f"{pc.min():.4f} / {pc.max():.4f} / {pc.mean():.4f}")
    return dens, xm, pc

alpha = 2.0
d_coh, xm_coh, pc_coh = analyse(f"コヒーレント状態 α={alpha}", coherent(alpha))
d_gr,  xm_gr,  pc_gr  = analyse("基底状態", ground())

# 時間平均した位置分布（中心で最小になるか）
avg_coh = d_coh.mean(axis=0)
i0 = np.argmin(abs(x)); imax = np.argmax(avg_coh)
print(f"\nコヒーレント状態の時間平均密度: x=0 で {avg_coh[i0]:.4f}, "
      f"最大は x={x[imax]:+.2f} で {avg_coh[imax]:.4f}")
print(f"基底状態の時間平均密度:         x=0 で {d_gr.mean(axis=0)[i0]:.4f}（最大）")

# ---- 図 ----
import logging; logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
plt.rcParams["font.family"] = ["Noto Sans CJK JP", "Noto Serif CJK JP", "IPAexGothic", "DejaVu Sans"]
fig, ax = plt.subplots(2, 2, figsize=(11, 8))
ext = [x[0], x[-1], t[-1], t[0]]
ax[0, 0].imshow(d_coh, aspect="auto", extent=ext, cmap="magma")
ax[0, 0].set_title(f"コヒーレント状態：時計の目盛り t ごとの系の位置分布")
ax[0, 0].set_xlabel("x"); ax[0, 0].set_ylabel("時計の目盛り t")
ax[0, 1].imshow(d_gr, aspect="auto", extent=ext, cmap="magma")
ax[0, 1].set_title("基底状態：t によらず同じ（時計と無相関）")
ax[0, 1].set_xlabel("x"); ax[0, 1].set_ylabel("時計の目盛り t")
ax[1, 0].plot(t, pc_coh, label="コヒーレント状態")
ax[1, 0].plot(t, pc_gr, label="基底状態")
ax[1, 0].set_title(f"中心付近 |x|<{CENTER} にいる確率")
ax[1, 0].set_xlabel("時計の目盛り t"); ax[1, 0].legend()
ax[1, 1].plot(x, avg_coh, label="コヒーレント状態（時間平均）")
ax[1, 1].plot(x, d_gr.mean(axis=0), label="基底状態")
ax[1, 1].set_title("時間平均した位置分布")
ax[1, 1].set_xlabel("x"); ax[1, 1].legend()
fig.tight_layout()
fig.savefig("pw_center_passage.png", dpi=130)
print("\n図を pw_center_passage.png に保存")
