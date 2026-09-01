# Polyhedral Transition — Strict Numerical Definition

## 多面体から多面体への遷移と6次元状態

### Status

**Mathematical definition / numerical specification**

本稿では、

\[
D_3\rightarrow C_6\rightarrow O_8\rightarrow D_5
\]

という4つの幾何状態を、同一の外接球半径

\[
\boxed{R=1}
\]

に正規化し、6次元状態ベクトルとして厳密に定義する。

目的は、微細構造定数 \(\alpha\) を先に仮定することではない。

まず、

\[
\boxed{
\text{geometry}
\rightarrow
\text{state}
\rightarrow
\text{transition}
\rightarrow
\text{operator}
}
\]

という数学的構造を確定する。

---

# 1. 6次元状態ベクトル

6つの成分を次の順序で固定する。

\[
\boxed{
\mathbf p(P)=
\begin{pmatrix}
V\\
E\\
F\\
\Omega\\
\delta\\
\mathcal V
\end{pmatrix}
}
\]

ここで、

- \(V\)：頂点数
- \(E\)：辺数
- \(F\)：面数
- \(\Omega\)：**赤道頂点における立体角**
- \(\delta\)：**頂点—赤道辺に沿った内二面角**
- \(\mathcal V\)：体積

とする。

## 重要な規約

\(D_3,D_5\) は頂点推移的ではない。

したがって \(\Omega\) は曖昧に「頂点立体角」とせず、

\[
\boxed{
\Omega=\Omega_{\mathrm{eq}}
}
\]

すなわち**赤道頂点の立体角**と定義する。

また二面角は、

\[
\boxed{
\delta=\delta_{\mathrm{apex-eq}}
}
\]

すなわち**双錐の頂点（apex）と赤道頂点を結ぶ辺に接する2面の内二面角**と定義する。

\(C_6,O_8\) は頂点・辺が対称なので、この選択による曖昧性はない。

---

# 2. 共通スケール

全ての立体について外接球半径を

\[
\boxed{R=1}
\]

とする。

したがって、

- 長さ：\(R\)
- 面積：\(R^2\)
- 体積：\(R^3\)

を基準とする。

本稿で使用する体積はすべて \(R=1\) における値である。

---

# 3. \(D_3\)：三角双錐

赤道を \(xy\) 平面上に置く。

\[
q_k=
\left(
\cos\frac{2\pi k}{3},
\sin\frac{2\pi k}{3},
0
\right),
\qquad k=0,1,2
\]

上頂点・下頂点を

\[
a_+=(0,0,1),
\qquad
a_-=(0,0,-1)
\]

とする。

頂点数・辺数・面数は

\[
\boxed{
V=5,\qquad E=9,\qquad F=6
}
\]

である。

---

## 3.1 体積

赤道三角形の面積は

\[
A_3
=
\frac{3\sqrt3}{4}.
\]

上下2つの四面体に分割すると、

\[
\mathcal V_{D_3}
=
\frac{2}{3}A_3
=
\boxed{\frac{\sqrt3}{2}}
\]

したがって、

\[
\boxed{
\mathcal V_{D_3}=0.8660254037844386
}
\]

である。

---

## 3.2 赤道頂点の立体角

赤道頂点 \(q_0\) から隣接頂点への3次元ベクトルを用いて球面四辺形を2つの球面三角形へ分割する。

球面三角形の立体角を

\[
\Omega(a,b,c)
=
2\arctan
\frac{
|\mathbf a\cdot(\mathbf b\times\mathbf c)|
}{
|\mathbf a||\mathbf b||\mathbf c|
+\mathbf a\cdot\mathbf b\,|\mathbf c|
+\mathbf b\cdot\mathbf c\,|\mathbf a|
+\mathbf c\cdot\mathbf a\,|\mathbf b|
}
\]

と定義する。

その結果、

\[
\boxed{
\Omega_{D_3}
=
4\arctan
\frac{\sqrt3}{2\sqrt3+3\sqrt2}
}
\]

であり、

\[
\boxed{
\Omega_{D_3}
=
0.884286376005907
}
\]

となる。

---

## 3.3 二面角

頂点—赤道辺に沿う内二面角を

\[
\delta_{D_3}
\]

とする。

厳密には、

\[
\boxed{
\cos\delta_{D_3}=\frac15
}
\]

したがって、

\[
\boxed{
\delta_{D_3}
=
\arccos\frac15
=
1.369438406004566
}
\]

である。

---

# 4. \(C_6\)：正六面体

外接球半径を1とする立方体の頂点を

\[
\left(
\pm\frac1{\sqrt3},
\pm\frac1{\sqrt3},
\pm\frac1{\sqrt3}
\right)
\]

とする。

したがって、

\[
\boxed{
V=8,\qquad E=12,\qquad F=6
}
\]

である。

---

## 4.1 体積

辺長は

\[
a=\frac2{\sqrt3}.
\]

したがって、

\[
\mathcal V_{C_6}
=
a^3
=
\boxed{\frac{8}{3\sqrt3}}
\]

数値的には、

\[
\boxed{
\mathcal V_{C_6}
=
1.539600717839002
}
\]

---

## 4.2 頂点立体角

正六面体の頂点立体角は、

\[
\boxed{
\Omega_{C_6}
=
\arccos\frac{23}{27}
}
\]

である。

数値は、

\[
\boxed{
\Omega_{C_6}
=
0.551285598432531
}
\]

---

## 4.3 二面角

正六面体では、

\[
\boxed{
\delta_{C_6}=\frac{\pi}{2}
}
\]

したがって、

\[
\boxed{
\delta_{C_6}
=
1.570796326794897
}
\]

---

# 5. \(O_8\)：正八面体

頂点を

\[
(\pm1,0,0),
\quad
(0,\pm1,0),
\quad
(0,0,\pm1)
\]

とする。

したがって外接球半径は1。

\[
\boxed{
V=6,\qquad E=12,\qquad F=8
}
\]

---

## 5.1 体積

正八面体は8個の合同な四面体に分割できる。

したがって、

\[
\boxed{
\mathcal V_{O_8}=\frac43
}
\]

すなわち、

\[
\boxed{
\mathcal V_{O_8}=1.333333333333333
}
\]

---

## 5.2 頂点立体角

頂点 \((1,0,0)\) における立体角は、

\[
\boxed{
\Omega_{O_8}
=
4\arctan\frac{\sqrt2}{4}
}
\]

したがって、

\[
\boxed{
\Omega_{O_8}
=
1.359347637816487
}
\]

---

## 5.3 二面角

正八面体の内二面角は、

\[
\boxed{
\cos\delta_{O_8}=-\frac13
}
\]

したがって、

\[
\boxed{
\delta_{O_8}
=
\arccos\left(-\frac13\right)
=
1.910633236249019
}
\]

---

# 6. \(D_5\)：五角双錐

赤道を

\[
q_k=
\left(
\cos\frac{2\pi k}{5},
\sin\frac{2\pi k}{5},
0
\right),
\qquad k=0,\ldots,4
\]

とする。

上下頂点は、

\[
a_\pm=(0,0,\pm1)
\]

である。

したがって、

\[
\boxed{
V=7,\qquad E=15,\qquad F=10
}
\]

---

## 6.1 体積

正五角形の面積は、

\[
A_5
=
\frac52\sin\frac{2\pi}{5}.
\]

双錐の高さは2なので、

\[
\mathcal V_{D_5}
=
\frac23 A_5
\]

したがって、

\[
\boxed{
\mathcal V_{D_5}
=
\frac53\sin\frac{2\pi}{5}
}
\]

数値は、

\[
\boxed{
\mathcal V_{D_5}
=
1.585094193825255
}
\]

---

## 6.2 赤道頂点の立体角

本研究では \(D_3\) と同じ規約を使用し、

\[
\Omega_{D_5}
=
\Omega_{\mathrm{eq}}
\]

とする。

厳密な球面三角形分割によって、

\[
\boxed{
\Omega_{D_5}
=
1.66399906898128
}
\]

となる。

---

## 6.3 二面角

頂点—赤道辺に沿う内二面角を

\[
\delta_{D_5}
\]

と定義する。

数値的には、

\[
\boxed{
\delta_{D_5}
=
2.19242948825248
}
\]

rad。

厳密値については、五角形頂点座標から面法線を構成し、

\[
\boxed{
\cos\delta_{D_5}
=
-\frac{
\mathbf n_1\cdot\mathbf n_2
}{
|\mathbf n_1||\mathbf n_2|
}
}
\]

として定義する。

この定義を採用すれば、近似値の丸めに依存しない。

---

# 7. 4状態の厳密な6次元状態ベクトル

以上から、

\[
\boxed{
\mathbf p_{D_3}
=
\begin{pmatrix}
5\\
9\\
6\\
0.884286376005907\\
1.369438406004566\\
0.866025403784439
\end{pmatrix}
}
\]

\[
\boxed{
\mathbf p_{C_6}
=
\begin{pmatrix}
8\\
12\\
6\\
0.551285598432531\\
1.570796326794897\\
1.539600717839002
\end{pmatrix}
}
\]

\[
\boxed{
\mathbf p_{O_8}
=
\begin{pmatrix}
6\\
12\\
8\\
1.359347637816487\\
1.910633236249019\\
1.333333333333333
\end{pmatrix}
}
\]

\[
\boxed{
\mathbf p_{D_5}
=
\begin{pmatrix}
7\\
15\\
10\\
1.663999068981280\\
2.192429488252480\\
1.585094193825255
\end{pmatrix}
}
\]

とする。

---

# 8. 重要：正規化しない

前版では「平均値で規格化する」という案を示した。

しかし、現段階ではこれは採用しない。

理由は、

\[
\boxed{
\text{規格化方法そのものが遷移スペクトルを変える}
}
\]

からである。

特に将来、

\[
\alpha^{-1}
\]

のような無次元固有値を調べる場合、恣意的な基準値による規格化は避ける必要がある。

したがって第一段階では、

\[
\boxed{
\mathbf p_i=
(V,E,F,\Omega,\delta,\mathcal V)^T
}
\]

を**生の幾何量のまま**状態ベクトルとする。

---

# 9. 3つの遷移ベクトル

\[
\Delta\mathbf p_i
=
\mathbf p_{i+1}-\mathbf p_i
\]

と定義する。

## \(T_1\)：\(D_3\rightarrow C_6\)

\[
\boxed{
\Delta\mathbf p_1=
\begin{pmatrix}
3\\
3\\
0\\
-0.333000777573376\\
0.201357920790331\\
0.673575314054563
\end{pmatrix}
}
\]

---

## \(T_2\)：\(C_6\rightarrow O_8\)

\[
\boxed{
\Delta\mathbf p_2=
\begin{pmatrix}
-2\\
0\\
2\\
0.808062039383956\\
0.339836909454122\\
-0.206267384505669
\end{pmatrix}
}
\]

---

## \(T_3\)：\(O_8\rightarrow D_5\)

\[
\boxed{
\Delta\mathbf p_3=
\begin{pmatrix}
1\\
3\\
2\\
0.304651431164793\\
0.281796252003461\\
0.251760860491922
\end{pmatrix}
}
\]

したがって、差分行列は

\[
\boxed{
\Delta P=
\begin{pmatrix}
3&3&0&-0.333000778&0.201357921&0.673575314\\
-2&0&2&0.808062039&0.339836909&-0.206267385\\
1&3&2&0.304651431&0.281796252&0.251760860
\end{pmatrix}
}
\]

となる。

---

# 10. 「遷移差行列」と「遷移演算子」を分離する

ここは厳密性のために前版から変更する。

\[
\boxed{\Delta P\neq T}
\]

である。

\(\Delta P\) は3つの観測された差分を並べただけであり、

\[
\boxed{
\mathbf p_{i+1}=T_i\mathbf p_i
}
\]

を満たす6×6線形演算子 \(T_i\) とは別物である。

したがって、

### 観測

\[
\Delta\mathbf p_i
\]

### 演算子

\[
T_i
\]

を明確に区別する。

---

# 11. 遷移演算子の数学的定義

遷移演算子は、

\[
\boxed{
T_i\in GL(6,\mathbb R)
}
\]

または必要に応じて

\[
T_i\in M_6(\mathbb R)
\]

とする。

基本条件は、

\[
\boxed{
T_i\mathbf p_i=\mathbf p_{i+1}
}
\]

である。

ただし、この条件だけでは \(T_i\) は一意に決まらない。

これは6×6行列の自由度が36個あるのに対し、1つの状態から次の状態への条件は6個しかないためである。

---

# 12. 最小ノルム遷移演算子

追加条件なしで恣意性を最小化する一つの方法として、

\[
\boxed{
T_i
=
\arg\min_T \|T-I\|_F
}
\]

subject to

\[
T\mathbf p_i=\mathbf p_{i+1}
\]

を採用できる。

ここで \(\|\cdot\|_F\) はFrobeniusノルム。

この問題の解は、

\[
\boxed{
T_i
=
I+
\frac{
(\mathbf p_{i+1}-\mathbf p_i)\mathbf p_i^T
}{
\mathbf p_i^T\mathbf p_i
}
}
\]

となる。

実際、

\[
T_i\mathbf p_i
=
\mathbf p_i+
\frac{
(\mathbf p_{i+1}-\mathbf p_i)
\mathbf p_i^T\mathbf p_i
}{
\mathbf p_i^T\mathbf p_i
}
=
\mathbf p_{i+1}.
\]

これは現時点での**基準遷移演算子**として明確に定義できる。

---

# 13. ただし、この \(T_i\) はTTT固有ではない

重要な注意点。

最小ノルム解は数学的には一意に定義できるが、

\[
\boxed{
\text{TTTから必然的に導かれた}
}
\]

とはまだ言えない。

したがって、

\[
T_i^{\mathrm{min}}
\]

と表記し、

\[
\boxed{
T_i^{\mathrm{TTT}}
}
\]

とは区別する。

TTT固有の \(T_i\) を得るには、TTTの公理・保存則・双対性などを追加拘束として導入する必要がある。

---

# 14. Cube–Octahedron遷移

中央遷移では、

\[
C_6=(8,12,6)
\]

\[
O_8=(6,12,8)
\]

なので、

\[
\boxed{
(V,E,F)\rightarrow(F,E,V)
}
\]

が成立する。

構造3成分だけについて、

\[
\boxed{
S=
\begin{pmatrix}
0&0&1\\
0&1&0\\
1&0&0
\end{pmatrix}
}
\]

とすると、

\[
S
\begin{pmatrix}
8\\12\\6
\end{pmatrix}
=
\begin{pmatrix}
6\\12\\8
\end{pmatrix}.
\]

さらに、

\[
\boxed{
S^2=I
}
\]

である。

したがって、

\[
\boxed{
C_6\leftrightarrow O_8
}
\]

は明確な対合（involution）として定義できる。

---

# 15. 6次元遷移演算子への拡張

6次元を

\[
\mathbf p=
\begin{pmatrix}
\mathbf s\\
\mathbf q
\end{pmatrix}
\]

と分割する。

\[
\mathbf s\in\mathbb R^3,
\qquad
\mathbf q\in\mathbb R^3.
\]

TTT式

\[
P=xX+yY+zZ+Uu+vV+wW
\]

との対応を、

\[
\mathbf s=(x,y,z)^T
\]

\[
\mathbf q=(u,v,w)^T
\]

とする。

遷移演算子は、

\[
\boxed{
T_i=
\begin{pmatrix}
A_i&B_i\\
C_i&D_i
\end{pmatrix}
}
\]

とする。

---

# 16. 「見えない状態」の逆問題

観測可能な成分を \(\mathbf s\)、潜在成分を \(\mathbf q\) とする。

\[
\mathbf s'
=
A\mathbf s+B\mathbf q
\]

であり、\(B\) が可逆なら、

\[
\boxed{
\mathbf q
=
B^{-1}
(\mathbf s'-A\mathbf s)
}
\]

となる。

これを本研究における、

\[
\boxed{
\text{Hidden-State Reconstruction}
}
\]

の基本式とする。

すなわち、

\[
\boxed{
\text{多面体の変化}
\rightarrow
\text{潜在6次元状態の推定}
}
\]

である。

---

# 17. 現段階で確定しているもの

### 確定

\[
R=1
\]

\[
\mathbf p=
(V,E,F,\Omega_{\mathrm{eq}},
\delta_{\mathrm{apex-eq}},\mathcal V)^T
\]

\[
D_3,\ C_6,\ O_8,\ D_5
\]

の座標系。

各状態の \(V,E,F,\Omega,\delta,\mathcal V\)。

3つの差分ベクトル。

Cube–Octahedron双対変換。

---

# 18. 現段階で未確定のもの

以下はまだ仮説であり、数値を勝手に固定してはいけない。

\[
\boxed{
T_1^{\mathrm{TTT}},
T_2^{\mathrm{TTT}},
T_3^{\mathrm{TTT}}
}
\]

特に、

\[
T_{\mathrm{total}}
=
T_3T_2T_1
\]

の固有値を物理定数と同一視することは、現段階では未証明である。

---

# 19. 次の数学的課題

次に解くべき問題は、

\[
\boxed{
\text{TTT公理}
+
\text{幾何学的拘束}
\Rightarrow
T_1,T_2,T_3
}
\]

である。

具体的には、

1. \(\Sigma V=0\) の平衡条件
2. \(C_6\leftrightarrow O_8\) の双対条件
3. 保存量
4. 最小変形条件
5. 必要なら正規直交条件
6. 6次元3+3分解

を同時に課し、\(T_i\) の自由度を削減する。

その結果として一意または有限個の候補が得られれば、

\[
\boxed{
T_{\mathrm{total}}
=
T_3T_2T_1
}
\]

を計算し、

\[
\boxed{
\det(T_{\mathrm{total}}-\lambda I)=0
}
\]

を解く。

ここで得られる固有値が、次の研究対象となる。

---

# 20. 微細構造定数について

微細構造定数は現段階では**入力値ではなく検証対象**とする。

したがって、

\[
\alpha^{-1}\approx137.035999177
\]

を使って遷移行列を調整することはしない。

正しい順序は、

\[
\boxed{
D_3,C_6,O_8,D_5
}
\]

\[
\downarrow
\]

\[
\boxed{
\mathbf p_1,\mathbf p_2,\mathbf p_3,\mathbf p_4
}
\]

\[
\downarrow
\]

\[
\boxed{
T_1,T_2,T_3
}
\]

\[
\downarrow
\]

\[
\boxed{
T_{\mathrm{total}}
}
\]

\[
\downarrow
\]

\[
\boxed{
\lambda_1,\lambda_2,\ldots
}
\]

\[
\downarrow
\]

\[
\boxed{
\text{物理定数との比較}
}
\]

である。

---

# 21. 研究上の中心命題

本研究の中心命題を、現時点では次のように置く。

\[
\boxed{
\textbf{
Observable Polyhedral Transition
}
\quad\Longrightarrow\quad
\textbf{
Hidden 6D State
}
}
\]

すなわち、

> **多面体そのものではなく、多面体間の変化に含まれる情報から、観測されない6次元状態を再構成できるか。**

これを数学的に検証する。

そして、その6次元状態遷移に自然な無次元不変量が存在するなら、その値を物理定数との比較対象とする。

この順序を守ることで、数値合わせではなく、**幾何学 → 遷移 → 不変量 → 物理**という反証可能な研究体系にする。