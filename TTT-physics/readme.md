# TTT-physics（物理理論・検証の場）

**役割：** 唯一、実験と対峙するリポジトリ。ここが理論の「生死」を決める戦場です。本リポジトリの主張はすべて実験的に反証可能であることを原則とします。

## まずはこちら

**[`INDEX.md`](./INDEX.md)** — 公理系・ファイルマップ・全導出結果とCODATA/PDG観測値との比較表をまとめた総合インデックス。このリポジトリを読む最初の1本です。

## 導出ドキュメント

* [`fine_structure_derivation.md`](./fine_structure_derivation.md) → Alpha-V4：微細構造定数 $1/\alpha$ の級数を公理から導出
* [`proton_electron_ratio_derivation.md`](./proton_electron_ratio_derivation.md) → 陽子・電子質量比 1836 の一意性証明
* [`higgs_mass_derivation.md`](./higgs_mass_derivation.md) → ヒッグス質量 125.25 GeV の導出
* [`neutron_proton_splitting_derivation.md`](./neutron_proton_splitting_derivation.md) → 中性子・プロトン質量差 1.293 MeV の導出
* [`running_alpha_prediction.md`](./running_alpha_prediction.md) → 微細構造定数の高エネルギー走りの関数形
* [`experimental_predictions.md`](./experimental_predictions.md) → **最重要**。LHC・将来実験での予言一覧
* [`codata_comparison.md`](./codata_comparison.md) → 予言値と観測値の比較表（誤差評価つき、Python検証コード付き）
* [`falsifiability_criteria.md`](./falsifiability_criteria.md) → 反証条件・棄却プロトコルの明示
* [`verify_alpha_v4.py`](./verify_alpha_v4.py) → Alpha-V4の数値的一致を独立に再検証するスクリプト（公理からの導出の証明ではなく、既知の実測値への事後的な数値一致の再現であることを明記）
* [`TTT-physics.md`](./TTT-physics.md) → 探索ノート（素粒子17種のCoxeter群対応、スピン・重力・暗黒物質への推測段階のアイデア。まだ個別ファイルに昇格していない内容）
* [`GTM_v2.1_統合版.html`](./GTM_v2.1_統合版.html) → 125, 126, 128幾何学とAlpha V1〜V4のインタラクティブなシミュレーション

外部の物理学者が計算を再現できるよう、数式のLaTeXソースと簡易検証コード（Python等）を各ドキュメントに同梱しています。
