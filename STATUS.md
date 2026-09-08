# STATUS — TTT-core 文書の状態一覧

**版**: v1.0 (2026-09-08)
**目的**: このリポジトリのどの文書がどの段にあるかを、一枚で示す。

---

## この一枚がある理由

同じ主張が、判定を受けたあとに別の文書から再輸入される、ということが実際に繰り返し起きている（$501/147$ は三度、$486$ は撤回した翌日に復活した）。原因は「どこに何があるか」は分かるのに「**どれがどの段か**」が分からないことにある。本書はそれだけを扱う。

**方針**:

- **ファイルは移動しない。** 2026-09-06 に cnt34 をフラットから再編したとき、内部リンクが60本壊れた。同じことをここで繰り返す理由がない
- **本文は一文字も変えない。** `PROOF_STATUS.md` §27「後から黙って直さない」による。判定は各ファイル冒頭の**状態バナー**として足すだけ
- **削除もしない。** 判定の履歴はこのプロジェクトで最も信用できる部分である

---

## 段の読み方

| 段 | 意味 |
|---|---|
| **A（核）** | 機械検証を通る。`TTT_CORE.md` v1.0 の構成の鎖に含まれる |
| **監査** | 判定の記録。理論そのものではない |
| **F（反証済み）** | 主張が成立しないことが確認された。本文は当時のまま残す |
| **C（仮説・未検定）** | 検定を通っていない。帰無対照・換算則・出典のいずれかが欠けている |
| **U（未判定）** | 個別監査が未了。核の鎖には含まれない |

**A に入れる条件**：機械検証を通ること。`ttt_core_verify.py` のような、assert で落ちるスクリプトが伴わないものは A に入れない。

---

## A — 核（2件）

| ファイル | 内容 |
|---|---|
| `TTT-physics/docs/TTT_CORE.md` | 構成の鎖 S1–S7。仮定は公理Zのみ、他は全て定理または強制 |
| `TTT-physics/docs/ttt_core_verify.py` | 上の全ステップを assert で検証（numpy のみ） |

> **この核が出力する数**: 3, 4, 6, 7, 8, 12, スケール比 3
> **確定した予言**: 0件（`TTT_CORE.md` §5）

---

## 監査 — 判定の記録（6件）

| ファイル | 内容 |
|---|---|
| `TTT-physics/docs/PROOF_STATUS.md` | 22項目の証明状況（v2.1） |
| `TTT-physics/docs/ttt_definition_ledger.md` | 用語・数え方・境界規則の台帳 |
| `TTT-physics/docs/REFERENCES.md` | 出典と帰属文（✓照合済 / △未照合 / ※査読なし） |
| `.../src/ttt_lie_audit.py` | Lie 環監査の再現（乱数対照・単位変換テスト付き） |
| `.../src/ttt_mass_refit_test.py` | 質量比の修正後再判定と帰無対照 |
| `TTT-physics/verify_alpha_v4.py` | α 系の検証スクリプト（未確認） |

---

## F — 反証済み（9件）

| ファイル | 判定の要点 |
|---|---|
| `TTT-physics/INDEX.md` | **最優先。** 「自由パラメータを持たない厳密解モデル」は不成立（最低9個の手置き数）。ヒッグス 0.00σ は旧値に対するもので PDG2025 では 0.45σ、かつ 125.25 は較正点。$3\times4\times153$ は 1836 の因数分解（$153=1836/12$）で実測に対し約 477万σ。$1/\alpha$ の式は手置き数 4.6 と 1.15 を含む |
| `TTT-physics/higgs_mass_derivation.md` | 125.25 GeV は較正点であって予言ではない |
| `TTT-physics/proton_electron_ratio_derivation.md` | 標的 $m_p/m_e = 1836.152673426(32)$ は整数ではない。1836 との差は約 477万σ |
| `TTT-physics/codata_comparison.md` | 「完全一致」「0.00σ」。実験誤差より細かい一致は、強い結果ではなく検定されていない結果 |
| `TTT-mathematics/golden_ratio_proofs.md` | §1 の根の取り違え（$x^2+x-1=0$ の正の解は $1/\varphi$）。2026-09-01 指摘、未修正 |
| `TTT-mathematics/geometry_and_solution_space.md` | 「$\Sigma v=0$ を満たす有限点系は5種」は任意の中心対称点系が満たす |
| `TTT-physics/geometry_and_solution_space_1.md` | 上の重複 |
| `.../docs/Unified Geometric Table .md` | 17粒子中7つが 55〜99% 外れる。8節中6節は既存文献の要約 |

---

## C — 仮説・未検定（12件）

`fibonacci_and_6d_equation.md` ／ `fine_structure_derivation.md` ／ `fine_structure_derivation_1.md` ／ `neutron_proton_splitting_derivation.md` ／ `running_alpha_prediction.md` ／ `experimental_predictions.md` ／ `falsifiability_criteria.md` ／ `Axiomatization of 6-Dimensional Equations (First Edition).md` ／ `golden_ratio_from_6d_equation.md` ／ `fractal_dimension_and_6d_equation.md` ／ `6次元幾何状態空間における基準遷移演算子と Lie 環.md` ／ `.../src/ttt_17_mass_ratios.py`

各ファイルの冒頭バナーに個別の判定を記した。共通する欠けは三つ：**帰無対照を通していない／換算則（O1）が未定／出典が未照合**。

> 補足：`experimental_predictions.md` の 2197 / 2744 / 3375 GeV は、それぞれ $13^3$ / $14^3$ / $15^3$ である。立方数の列を GeV と読む換算則が要る。

---

## U — 未判定（14件）

`README.md`（**要更新**：1836 と 137.03… を看板にしている） ／ `TTT-physics/readme.md` ／ `TTT-physics.md` ／ `TTT‑physics v3 .md` ／ `POLYHEDRAL_TRANSITION_6D.md` ／ `Polyhedral Transition and Hidden 6D State.md` ／ `Polyhedral Transition — Strict Numerical Definition.md` ／ `TTT_6D_Observation_Matrix_Analysis.md` ／ `TTT_Alpha_Fine_Structure_Constant_Convergence.md` ／ `TTT_Polyhedra_Transition_Analysis.md` ／ `TTT-paper/fin/Geometric-Topological Derivation…md` ／ `godel_nash_and_judicial_structure.md`（＋壊れた重複） ／ `.../docs/02_standard_model_17_particles.md`

---

## 未分類（バナーなし・35件）

`TTT-society/` 4件、`TTT-consciousness/readme.md`、`TTT-paper/` のビルド一式、各 `Readme.md`、`USAGE.md`、`index.html`、PDF 5件、`table.csv`、`src/setup_ttt_repository.sh`、`.github/`。

これらは TTT の主張を直接には述べていないか、生成物である。ただし `TTT-society/` は AI-ladder 等の社会側の主張を含むため、次の巡回で判定対象に入れるべき。

---

## 重複とファイル名の問題

**完全に同一（md5 一致）— 3ファイルが1つの内容:**

- `TTT-physics/GTM_v2.1_統合版1.html`
- `TTT-physics/GTM_v2.1_総合版.html`
- `index１.html`

いずれも 984,116 バイトで中身が同一。1つ残して2つ削除してよい。なお `index１.html` の「１」は**全角数字**である。

**ほぼ同一（内容の照合が必要）:**

| A | B | サイズ |
|---|---|---|
| `POLYHEDRAL_TRANSITION_6D.md` | `Polyhedral Transition and Hidden 6D State.md` | 13,740 / 13,743 |
| `fine_structure_derivation.md` | `fine_structure_derivation_1.md` | 15,832 / 15,620 |
| `TTT-mathematics/geometry_and_solution_space.md` | `TTT-physics/geometry_and_solution_space_1.md` | 6,596 / 6,562 |
| `godel_nash_and_judicial_structure.md` | `godel_nash_and_judicial_structure.md .md` | 4,363 / 4,372 |

**`_1` 問題は続いている。** GitHub の web UI の "Add files via upload" で同名ファイルを上げると `_1` が生成される。2026-09-06 に cnt34 で確認したとおり、**`_1` の方が新しく内容も厚いことがある**ため、機械的にどちらかを消してはいけない。差分を見てから決めること。

**リンクが張れないファイル名:**

- `TTT-physics/TTT‑physics v3 .md` — ハイフンが非ASCII（U+2011 NON-BREAKING HYPHEN）、かつ拡張子の前に空白
- `TTT-mathematics/godel_nash_and_judicial_structure.md .md` — 拡張子が二重
- `.../docs/Unified Geometric Table .md` — 拡張子の前に空白

---

## 次の一手（優先順）

1. **`TTT-physics/INDEX.md` を書き換える。** ここが最も外から見える文書で、最も多くの判定済み主張を断定形で載せている。バナーだけでは足りない
2. **`README.md` を書き換える。** リポジトリの入口。1836 と 137.03… を看板から外し、`TTT_CORE.md` と本書へ導線を張る
3. **完全重複の HTML 2件を削除する。** 中身が同一なので判断が要らない
4. **`_1` 4組の差分を取って正本を決める。** 機械的に消さない
5. **壊れたファイル名 3件を修正する**（リンク不能のため）
6. `TTT-society/` を判定対象に入れる

### 未コミットの文書について（重要）

2026-09-08 に提示された「フィボナッチ数列と6次元方程式：**動的な成長プロセスの証明**」（$x=1, y=1, z=x+y, r=y+z, i=z+r, j=r+i$ を6成分に割り当てるもの）は、**本リポジトリには存在しない**。リポジトリ内の `fibonacci_and_6d_equation.md` は別内容（比の収束定理）である。

前者を追加する場合は、**F 判定を添えること**。理由：

- $z=x+y,\ r=y+z,\ i=z+r,\ j=r+i$ を課すと $P$ の6成分は $(x,y)$ だけで決まり、**張る部分空間の階数は 2 になる**。「次元拡張の証明」と題しながら次元を 6 から 2 へ落としている
- 6段で止めれば $j/i = 1.600$ で $\varphi$ に 1.11% 届かない（収束は $n\to\infty$ の性質）。「6次元で $P$ が完成する」と「$\varphi$ へ収束する」は同時に成り立たない
- $i, j$ が 2026-09-05 に確定した四元数の $i, j$ と記号衝突している

---

## 状態バナーの更新方法

```
python3 apply_status_banners.py .
```

冪等（既にバナーがあるファイルはスキップ）。判定を変えるときは、スクリプト内の判定表 `J` を編集し、対象ファイルの先頭にある `<!-- TTT-STATUS v1 -->` ブロックを削除してから再実行する。

**判定を変えたときは、本書の改訂履歴に一行残すこと。** 黙って段を上げないことが、この仕組みが働く唯一の条件である。

---

## 改訂履歴

**v1.0 (2026-09-08)** — 新規。73ファイルを棚卸しし、38ファイルに状態バナーを挿入。A 2件／監査 6件／F 9件／C 12件／U 14件／未分類 35件。完全重複3ファイル、ほぼ同一4組、壊れたファイル名3件を検出。
