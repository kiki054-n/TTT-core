# TTT-Core-Physics: Topological Tri-Tetrahedral Unification Model

`TTT-Core-Physics` は、素粒子スケール（質量ゼロの光速回転場）からミクロな四面体配向 $(O\pi O)_4$、125/37超粒子核、そして地上スケールの物性（ダイヤモンド、C60、同族IV族元素、カーボンナノチューブ）に至る**幾何学的自己相似（フラクタル）自己組織化理論**の計算・検証用Pythonライブラリです。

---

## 🌌 4段階のフラクタル・スケール階層

本モデルでは、ミクロ（地下）の幾何学的拘束が繰り込み群的にマクロ（地上）の物性を決定する4段階の階層構造を定式化しています。

| 階層 | スケール | 幾何構造 / 物理的解釈 |
|---|---|---|
| **地下 0階** | $c$ (光速) | 質量ゼロの位相要素 $O$ の運動 |
| **地下 1階** | $\sim 10^{-13}\text{ m}$ | $\pi$-回転拘束による電子状態（コンプトン波長 $m_e = E/c^2$） |
| **地下 2階** | $\sim 0.016\text{ nm}$ | $(O\pi O)_4$ 最小安定ベクトル相殺ユニット（109.47° 正四面体） |
| **地下 3階** | $\sim 0.04\text{ nm}$ | 125コア ($5^3$ 立方閉包) + 37拘束殻 (正二十面体/十二面体双対トポロジー) |
| **地 上** | $\sim 0.154 - 0.357\text{ nm}$ | 炭素・ダイヤモンド格子 ($a = 3.567\text{ Å}$)、C60 ($d = 0.71\text{ nm}$)、CNT ($d \approx 1.42\text{ nm}$) |

---

## 📐 主要な幾何法則とトポロジー方程式

### 1. (OπO)₄ TTT ポテンシャル
$$ U = \alpha \cdot \left(\sum \mathbf{v}_i\right)^2 + \beta \cdot \sum_{i<j} (1 - \cos(\theta_{ij} - 109.47^\circ))^2 + \gamma \cdot \sum \frac{L^2}{2r^2} $$

### 2. 同族IV族のスケーリング法則 ($D_f \approx 2.40$)
$$ a(M) = a_{\text{carbon}} \cdot \left(\frac{M}{M_{\text{carbon}}}\right)^{\frac{\eta}{D_f}} \quad (\eta \approx 0.564) $$

### 3. C60 位相閉包（ポアンカレ・ホップの定理）
$$ \int_{S^2} K \, dA = 4\pi \implies N_{\text{pentagons}} = 12 $$
（125コアの直交歪みを 37 拘束殻が包摂する際、12個の五角形位相欠陥が自律発生）

---

## 🚀 クイックスタート

### 依存ライブラリのインストール
```bash
pip install -r requirements.txt
