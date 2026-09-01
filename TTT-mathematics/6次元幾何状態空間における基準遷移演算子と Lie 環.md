# **6次元幾何状態空間における基準遷移演算子と Lie 環 $\\mathfrak{gl}(3, \\mathbb{R})$ の代数構造**

## **1\. 基礎定義と状態ベクトル**

本研究では、多面体の離散的位相量（可視幾何量）と連続的幾何量（不可視幾何量）を統合した 6次元状態ベクトル $\\mathbf{p} \\in \\mathbb{R}^6$ を以下のように定義する。

$$\\mathbf{p} \= \\begin{pmatrix} V \\\\ E \\\\ F \\\\ \\Omega \\\\ \\delta \\\\ \\mathcal{V} \\end{pmatrix} \= \\begin{pmatrix} \\mathbf{p}\_{\\text{vis}} \\\\ \\mathbf{p}\_{\\text{invis}} \\end{pmatrix}$$  
ここで、

* $\\mathbf{p}\_{\\text{vis}} \= (V, E, F)^T$ : 頂点数 ($V$), 辺の数 ($E$), 面の数 ($F$)  
* $\\mathbf{p}\_{\\text{invis}} \= (\\Omega, \\delta, \\mathcal{V})^T$ : 立体角 ($\\Omega$), 欠損角 ($\\delta$), 内部体積 ($\\mathcal{V}$)

### **4状態の入力値**

$$\\mathbf{p}\_1 \= D\_3 \= \\begin{pmatrix} 5 \\\\ 9 \\\\ 6 \\\\ 0.884286376006 \\\\ 1.369438406005 \\\\ 0.866025403784 \\end{pmatrix}, \\quad \\mathbf{p}\_2 \= C\_6 \= \\begin{pmatrix} 8 \\\\ 12 \\\\ 6 \\\\ 0.551285598433 \\\\ 1.570796326795 \\\\ 1.539600717839 \\end{pmatrix}$$

$$\\mathbf{p}\_3 \= O\_8 \= \\begin{pmatrix} 6 \\\\ 12 \\\\ 8 \\\\ 1.359347637816 \\\\ 1.910633236249 \\\\ 1.333333333333 \\end{pmatrix}, \\quad \\mathbf{p}\_4 \= D\_5 \= \\begin{pmatrix} 7 \\\\ 15 \\\\ 10 \\\\ 1.663999068981 \\\\ 2.192429488252 \\\\ 1.585094193825 \\end{pmatrix}$$

## **2\. 最小変形条件と基準遷移演算子の導出**

変形量（Frobenius ノルム）を最小化する条件：

$$T\_i \= \\arg\\min\_T \\Vert{}T \- I\\Vert{}\_F \\quad \\text{s.t.} \\quad T\_i \\mathbf{p}\_i \= \\mathbf{p}\_{i+1}$$  
より、各ステップの基準遷移演算子 $T\_i \\in \\mathbb{R}^{6\\times 6}$ は階数1（Rank-1）更新として解析的に一意決定される。

$$\\mathbf{\\Delta}\_i \= \\mathbf{p}\_{i+1} \- \\mathbf{p}\_i \\implies \\mathbf{T\_i \= I \+ \\frac{\\mathbf{\\Delta}\_i \\mathbf{p}\_i^T}{\\mathbf{p}\_i^T \\mathbf{p}\_i}}$$

## **3\. 合成演算子 $T$ のブロック構造と $T\_2$ の双対性**

合成遷移演算子 $T \= T\_3 T\_2 T\_1$ を $3 \\times 3$ ブロック行列分解する：

$$T \= \\begin{pmatrix} A & B \\\\ C & D \\end{pmatrix}$$

### **可視 $\\to$ 不可視の結合行列 $C$**

$$C \= \\begin{pmatrix} 0.03114803 & 0.04967331 & 0.02657551 \\\\ 0.02979732 & 0.05164813 & 0.03165476 \\\\ 0.02291992 & 0.04439234 & 0.03120670 \\end{pmatrix}$$  
結合行列 $C$ の特異値分解（SVD） $C \= U \\Sigma V^T$ において、第1特異値がエネルギーの **99.64%** を占有する：

$$\\Sigma \= \\text{diag}(0.110126, \\, 0.006588, \\, 0.000032)$$  
これは、可視空間から不可視空間への幾何学的誘導が「全幾何規模の絶対増分（$E$ 軸を中心とした共調）による単一モード（Rank-1 Dominance）」にほぼ完全に統合されていることを意味する。

### **$T\_2$（$C\_6 \\to O\_8$）における Cube–Octahedron 双対性分解**

完全双対置換行列 $S \= \\begin{pmatrix} 0 & 0 & 1 \\\\ 0 & 1 & 0 \\\\ 1 & 0 & 0 \\end{pmatrix}$ を用いて $A\_2 \= S \+ \\Delta A\_2$ に分解すると、

$$\\Delta A\_2 \= \\begin{pmatrix} 0.93577952 & \-0.09633073 & \-1.04816536 \\\\ 0 & 0 & 0 \\\\ \-0.93577952 & 0.09633073 & 1.04816536 \\end{pmatrix}$$

* **第2行が完全に $0$:** 辺数 $E=12$ の完全保存（$E \\to E$）。  
* **$\\text{Row}\_3 \= \-\\text{Row}\_1$:** 頂点数 $V$ と面数 $F$ の間の厳密な互換流出入（保存則）。

## **4\. スペクトル構造と固有値 1 の不変性**

合成演算子 $T \= T\_3 T\_2 T\_1$ のスペクトル（固有値集合）は以下の通りである。

$$\\operatorname{Spec}(T) \= \\{ 1.62318319, \\, 0.97131018, \\, 0.99982298, \\, \\mathbf{1, \\, 1, \\, 1} \\}$$

* **3重解 $\\lambda \= 1$ の幾何学的理由:**  
  4つの状態 $\\mathbf{p}\_1, \\dots, \\mathbf{p}\_4$ は 6次元空間内の 3次元アフィン部分空間を構成する。その直交補空間（3次元）が一切の変形を受けない「ゲージ固定不変空間」として分離していることを示す。

## **5\. Lie 環 $\\mathfrak{g} \\cong \\mathfrak{gl}(3, \\mathbb{R})$ の生成と極分解**

各ステップの連続生成元 $K\_i \= T\_i \- I \= \\mathbf{u}\_i \\mathbf{v}\_i^T$（ただし $\\mathbf{u}\_i \= \\mathbf{\\Delta}\_i, \\, \\mathbf{v}\_i \= \\frac{\\mathbf{p}\_i}{\\Vert{}\\mathbf{p}\_i\\Vert{}^2}$）の非可換交換子：

$$\[K\_i, K\_j\] \= (\\mathbf{v}\_i^T \\mathbf{u}\_j) \\mathbf{u}\_i \\mathbf{v}\_j^T \- (\\mathbf{v}\_j^T \\mathbf{u}\_i) \\mathbf{u}\_j \\mathbf{v}\_i^T$$  
から計算される生成代数 $\\mathfrak{g}$ のベクトル空間の次元は、**正確に 9次元で完全閉合** する。

$$\\mathfrak{g} \= \\text{span}\\{ \\mathbf{u}\_i \\mathbf{v}\_j^T \\mid i, j \\in \\{1, 2, 3\\} \\} \\cong \\mathfrak{gl}(3, \\mathbb{R})$$

### **8次元 $\\mathfrak{sl}(3, \\mathbb{R})$ 体積保存場の極分解（Iwasawa / Cartan 分解）**

共役結合行列 $G\_{ij} \= \\mathbf{v}\_j^T \\mathbf{u}\_i$ をスカラー部（膨張）とトレースレス部 $G\_0 \\in \\mathfrak{sl}(3, \\mathbb{R})$ に分解する：

$$G\_0 \= G \- \\frac{1}{3}\\operatorname{Tr}(G) I\_3 \\quad (\\operatorname{Tr}(G) \= 0.51527609)$$  
$\\mathfrak{sl}(3, \\mathbb{R}) \= \\mathfrak{so}(3) \\oplus \\text{Sym}\_0(3)$ に分解した各成分の強度：

* **回転場（ゲージ場）強度:** $\\Vert{}\\mathbf{w}\\Vert{}\_{\\mathfrak{so}(3)} \= 0.15936726$  
* **歪み場（計量場）強度:** $\\Vert{}\\mathbf{s}\\Vert{}\_{\\text{Sym}\_0} \= 0.359592 09$  
* **歪み / 旋回 比:** $\\frac{\\Vert{}\\mathbf{s}\\Vert{}}{\\Vert{}\\mathbf{w}\\Vert{}} \\approx \\mathbf{2.25637}$

## **6\. 連続時間状態遷移モデル（微分方程式）**

状態空間上の連続変化を描く微分方程式：

$$\\frac{d\\mathbf{p}(t)}{dt} \= K(t) \\mathbf{p}(t), \\quad \\mathbf{p}(0) \= \\mathbf{p}\_1$$

### **(1) 区分的自律モデル（Piecewise Continuous Model）**

各区間 $t \\in \[i-1, i\]$ における連続生成元 $K\_i \\in \\mathfrak{gl}(3, \\mathbb{R})$：

$$K\_i \= \\ln(T\_i) \= \\left( \\frac{\\ln(1 \+ \\mathbf{v}\_i^T \\mathbf{u}\_i)}{\\mathbf{v}\_i^T \\mathbf{u}\_i} \\right) \\mathbf{u}\_i \\mathbf{v}\_i^T$$  
**各区間の解析解:**

$$\\mathbf{p}(t) \= \\mathbf{p}\_i \+ \\frac{(1 \+ \\mathbf{v}\_i^T \\mathbf{u}\_i)^{t \- (i-1)} \- 1}{\\mathbf{v}\_i^T \\mathbf{u}\_i} \\mathbf{\\Delta}\_i \\quad (i-1 \\le t \\le i)$$

### **(2) 大域的自律モデル（Global Smooth Model）**

全区間を滑らかに結ぶ自律生成元 $K\_{\\text{global}} \= \\ln(T\_3 T\_2 T\_1) \\in \\mathbb{R}^{6\\times 6}$ の数値行列：

$$K\_{\\text{global}} \= \\begin{pmatrix} 0.038972 & 0.093407 & 0.078564 & 0.014848 & 0.016553 & 0.006404 \\\\ 0.155070 & 0.290288 & 0.193527 & 0.030199 & 0.044958 & 0.029594 \\\\ 0.116098 & 0.196882 & 0.114963 & 0.015351 & 0.028406 & 0.023190 \\\\ 0.025476 & 0.039022 & 0.019445 & 0.001930 & 0.005174 & 0.005175 \\\\ 0.023713 & 0.040300 & 0.024118 & 0.003234 & 0.005846 & 0.004543 \\\\ 0.017507 & 0.034371 & 0.024611 & 0.004033 & 0.005504 & 0.003103 \\end{pmatrix}$$  
**大域解軌跡:**

$$\\mathbf{p}(t) \= \\exp(t K\_{\\text{global}}) \\mathbf{p}\_1 \\quad (t \\in \[0, 1\])$$

* $t \= 0.00 \\implies \\mathbf{p}(0) \= \\mathbf{p}\_1 \\ (D\_3)$  
* $t \= 0.33 \\implies \\mathbf{p}(0.33) \\approx \\mathbf{p}\_2 \\ (C\_6)$  
* $t \= 0.67 \\implies \\mathbf{p}(0.67) \\approx \\mathbf{p}\_3 \\ (O\_8)$  
* $t \= 1.00 \\implies \\mathbf{p}(1) \= \\mathbf{p}\_4 \\ (D\_5)$