# TTT-core

TTT-core（Tri-Tetra Theory 統合ハブ・根のリポジトリ）

TTT理論は、数学的公理系（TTT-mathematics）から物理定数（TTT-physics）を導くことを目指す理論です。社会構造（TTT-society）と意識モデル（TTT-consciousness）は、物理基盤確立後の推論的展開であり、現時点では独立した哲学的応用として位置づけられています。

このリポジトリ自身は理論の「入口」であり、以下の4領域への案内役を担います。

## 構成

```
TTT-core/              ← 統合ハブ（哲学・公理・全体像、このリポジトリ）
├── TTT-mathematics/    ← 純粋数学（証明の巣）
├── TTT-physics/        ← 物理理論（検証の場）
├── TTT-society/        ← 社会構造（応用の域）
└── TTT-consciousness/  ← 意識・観測者（推論の域）
```

（4領域は独立リポジトリではなく、このTTT-core内のサブディレクトリとして管理しています）

## 各領域の現状

| 領域 | 役割 | 現状 |
| --- | --- | --- |
| [TTT-mathematics](./TTT-mathematics/) | 物理単位を一切使わない、公理からの純粋数学的定理導出 | 7本のドキュメントで公理・定理を展開中 |
| [TTT-physics](./TTT-physics/) | 唯一、実験と対峙するリポジトリ。理論の反証可能性を担う | [INDEX.md](./TTT-physics/INDEX.md) に主要導出・CODATA比較・反証条件をまとめ済み |
| [TTT-society](./TTT-society/) | TTT-mathematicsの幾何学的構造からの推論的応用（実験的検証可能性なし） | 未着手（方針のみ） |
| [TTT-consciousness](./TTT-consciousness/) | 量子力学の測定問題への幾何学的解釈（哲学的・現象学的推論） | 未着手（方針のみ） |

TTT-societyとTTT-consciousnessの主張は、TTT-physicsのような実験的検証可能性を持ちません。これにより、物理領域の「科学性」が両者の推論的な主張によって汚染されないよう明確に区別しています。

## 使い方 - 間違いを育てる

TTT理論は辞書です。使い方の手順は `reading-the-wind` にあります。

> **OOπの表面を押せば、見えない裏面の変形が予想される。乖離の中に、次の変数が眠っている。**

詳細な運用手順、三列比較テンプレート、検証事例は以下を参照してください。

**→ [USAGE.md - TTT理論の使い方: 間違いを育てるフレームワーク](./USAGE.md)**

**→ [reading-the-wind: 見えないものを読む理論](https://github.com/kiki054-n/reading-the-wind)** - 気象・司法・砂川事件・日独比較の検証ログ

### Quick Start: 4ステップ

1.  **表面を記録:** 今見えている事実 (rR)
2.  **裏面を予想:** 6変数から支配変数を1つだけ選んで断言する (例: zZ≒0)
3.  **三列比較:** TTT予報 / データ予報 / 現実 を並べる
4.  **乖離を分類:** 量的・位置的・時間的・質的 → 第7項 (hH,eE,nN...)を発見

外れた記録はIssueで共有してください。



## 公理系（概要）

トリテトラ理論の基本公理: ΣV=0, JIK=-1, 0,0 → 1,-1

```
0,0（双極的無）→ 公理
└── TTT-mathematics（数学的必然）
    ├── 正多面体5種の証明
    ├── 黄金比の一意性
    └── 6次元解空間の構造
        └── TTT-physics（物理的帰結）← 検証の場
        │   ├── 1/α = 137.035...
        │   ├── m_p/m_e = 1836...
        │   └── m_H = 125...
        ├── TTT-society（社会的推論）
        │   └── 四権構造の数学的根拠
        └── TTT-consciousness（意識的推論）
            └── 観測者の幾何学的位置
```

厳密な公理の記述、5領域間の関係図、命題ごとにどのリポジトリで証明されるかの全体マップ、用語統一の辞書（glossary）は今後このREADMEに追記していく予定です。

## ライセンス

[LICENSE](./LICENSE)（CC BY-NC-SA 4.0）を参照してください。

## TTT理論の関連リポジトリ

TTT-coreの外側で公開している、TTT理論に関連する独立リポジトリ・成果物です。

- [cnt34](https://github.com/kiki054-n/cnt34) — 「Code Name Type ３４ 三四式」。TTTを未完結のオープンなキャンバスとして提示し、数学・物理、プログラミング、アート・哲学からの参加を募るプロジェクト（コード/シミュレーションはMIT、理論文章はCC BY-NC-SA 4.0）
- [dual-point-cosmology](https://github.com/kiki054-n/dual-point-cosmology) — 「直線の双極と円環宇宙論」。双極場から三角双錘（OOπO）構造を経て質量・粒子形成に至る宇宙生成モデル
- [tttwsp](https://github.com/kiki054-n/tttwsp) — TTT水分解プロジェクト。Quantum ESPRESSOによるDFT計算でS/Pドープ半導体表面の水吸着エネルギーを検証
- TTT-Fusion（Zenodo DOI: [10.5281/zenodo.20551789](https://doi.org/10.5281/zenodo.20551789)） — 正四面体波動干渉を核融合エネルギーへ応用するサブ理論
