# Mathematical & Physical Foundations of TTT-Core Theory

本ドキュメントでは、`TTT-Core-Physics` モデルにおける主要な定量的導出の数学的背景を記録します。

---

## 1. (OπO)₄ における 109.47° の幾何学的必然性

空間内で 4 つの同等な単位ベクトル $\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3, \mathbf{v}_4$ の和がゼロとなる条件：

$$ \sum_{i=1}^4 \mathbf{v}_i = \mathbf{0} $$

両辺の二乗ノルムを取ることで相互角 $\theta$ は一意に定まります。

$$ \left| \sum_{i=1}^4 \mathbf{v}_i \right|^2 = \sum_{i=1}^4 |\mathbf{v}_i|^2 + 2 \sum_{i<j} \mathbf{v}_i \cdot \mathbf{v}_j = 0 $$

同等なノルム $|\mathbf{v}_i| = 1$ および対称性から $\mathbf{v}_i \cdot \mathbf{v}_j = \cos\theta$ とおくと、

$$ 4 + 2 \cdot \binom{4}{2} \cos\theta = 4 + 12 \cos\theta = 0 \implies \cos\theta = -\frac{1}{3} $$

$$ \theta = \arccos\left(-\frac{1}{3}\right) \approx 109.4712^\circ $$

---

## 2. 125/37 殻構造から C60 フラーレンへの位相幾何学マッピング

### ポアンカレ・ホップおよびガウス・ボンネの定理
2次元閉曲面 $S^2$ において、ガウス曲率 $K$ の全分はオイラー標数 $\chi(S^2) = 2$ に拘束されます。

$$ \int_{S^2} K \, dA = 2\pi \chi(S^2) = 4\pi $$

六角形格子（平坦曲面 $K=0$）に正五角形（120° $\rightarrow$ 108° の位相欠陥）を挿入した際の欠損角は $\delta = \pi/15 \text{ rad}$。必要な五角形の数 $N_5$ は：

$$ N_5 \times \frac{\pi}{3} = 4\pi \implies N_5 = 12 $$

125/37 モデルの最外殻 12 粒子（正二十面体頂点）は、この位相欠陥に正確に対応します。

---

## 3. フラクタル次元 $D_f \approx 2.40$ と質量スケーリング

IV 族元素における原子質量 $M$ と格子定数 $a$ のスケーリング関係：

$$ a \propto N_{(O\pi O)}^{1/D_f}, \quad N_{(O\pi O)} \propto M^\eta \quad (\eta \approx 0.564) $$

$$ \implies a(M) \propto M^{\frac{\eta}{D_f}} $$

実験データ（C, Si, Ge, $\alpha$-Sn）への最尤フィッティングにより、指数の比 $\frac{\eta}{D_f} \approx 0.235$ が得られ、ここから実効フラクタル次元 $D_f = \frac{0.564}{0.235} \approx 2.40$ が算出されます。
