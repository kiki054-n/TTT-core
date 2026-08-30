# Tri-Tetra Theory (TTT理論) 統合ドキュメントインデックス (INDEX.md)

本リポジトリ／ドキュメントセットは、真空を正四面体（Tetrahedron）の最密充填構造およびプラトン立体（正多面体）の双対幾何学として捉える **Tri-Tetra Theory (TTT理論)** に基づき、標準模型における自由パラメータ（ヒッグス質量、微細構造定数、弱混合角、中性子・プロトン質量差等）の厳密導出、高エネルギー予言、および反証条件をまとめた全6つの論文・技術ノートの総合インデックスである。

---

## 1. ドキュメント構成一覧 (File Map)

| ファイル名 | 主要主題・概要 | 主要導出結果・結論 |
| :--- | :--- | :--- |
| **1. [higgs_mass_derivation.md](./higgs_mass_derivation.md)** | TTT理論の基本公理およびヒッグス質量 $m_h = 125.25\text{ GeV}$ の全9節にわたる厳密導出 | $m_h = 5^3 + \frac{V_{12}+V_{20}}{2^7} = 125.25\text{ GeV}$<br>*(LHC観測値 $125.25 \pm 0.17\text{ GeV}$ と完全一致)* |
| **2. [neutron_proton_splitting_derivation.md](./neutron_proton_splitting_derivation.md)** | 中性子とプロトンの質量差 $\Delta m_{np} \approx 1.29333\text{ MeV}$ の幾何学的導出 | $\Delta m_{np} = \frac{5^3}{100} + \frac{V_{\text{eff}}}{2^7} - \frac{V_6}{2^{14}} + \cdots = 1.29333236\text{ MeV}$<br>*(CODATA 2022 と8桁一致)* |
| **3. [running_alpha_prediction.md](./running_alpha_prediction.md)** | 微細構造定数の逆数 $1/\alpha(E)$ の高エネルギー走りの完全関数形決定 | $\alpha^{-1}(0) = 137.0359990835$ から $E_k$ 閾値での Kink 構造（ステップ補正 $\Delta b_k$）の定式化 |
| **4. [experimental_predictions.md](./experimental_predictions.md)** | LHC, HL-LHC, FCC-hh, 精密測定実験に対する事前予言の網羅的一覧 | TeVスケール高次ヒッグス励起状態（$2197, 2744, 3375\text{ GeV}$）の断面積・BR・シグネチャーの特定 |
| **5. [codata_comparison.md](./codata_comparison.md)** | TTT理論の各予言値と CODATA 2022 / PDG / LHC 最新観測値との高精度比較表 | 全物理定数の絶対誤差・相対誤差（ppb/ppm）・$\sigma$ 偏差評価および Python 検証コード |
| **6. [falsifiability_criteria.md](./falsifiability_criteria.md)** | ポッパー型反証可能性に基づく即時棄却クライテリア・反証トリガーの明記 | 自由パラメータを持たない厳密解モデルとしての明確な実験的反証プロトコル |

---

## 2. TTT理論の代数的・幾何学的核心概念 (Core Principles)

### 2.1 プラトン立体の頂点数集合 $V_n$
3次元空間を幾何学的に充填・被覆する5つの正多面体の頂点数：
$$V_4 = 4 \quad (\text{正四面体}), \quad V_6 = 6 \quad (\text{正八面体}), \quad V_8 = 8 \quad (\text{正六面体}), \quad V_{12} = 12 \quad (\text{正十二面体}), \quad V_{20} = 20 \quad (\text{正二十面体})$$

### 2.2 離散代数基底と透過演算子
* **真空体積基底**: $B_{\text{vol}} = 5^3 = 125$ （3次元空間における5進的充填量子）
* **透過格子基底**: $B_{\text{trans}} = 2^7 = 128 = V_4 \times (V_{12} + V_{20})$ （透過演算子 $\hat{O}_k = \frac{1}{2^{7k}} = \frac{1}{128^k}$）
* **有効幾何因子**: $V_{\text{eff}} = V_4 + \frac{V_{12}}{V_{20}} = 4 + \frac{12}{20} = 4.6 = \frac{23}{5}$

---

## 3. 主要物理定数の理論導出統一サマリー
