# Navel–Tetra Lattice-Occupancy Model / へそとテトラの格子占有モデル

Kawakami Naoyuki（川上真潔）· ORCID [0009-0009-2972-6511](https://orcid.org/0009-0009-2972-6511) · 2026-10-29 · v1.0

**Zenodo DOI: [10.5281/zenodo.23756226](https://doi.org/10.5281/zenodo.23756226)**（全版共通 / all versions: [10.5281/zenodo.23756225](https://doi.org/10.5281/zenodo.23756225)）

> **判定 / Status: [C] 仮説・未検定** — 数値の一致は検算スクリプトで確認済み（47項目通過）だが、帰無対照（同じ自由度でランダムに組んだ式が同程度に一致する確率）は未実施。当てはめた選択は本文 §9。ヒッグス質量 125.1947 GeV は反証可能な予測。 / Numerical agreements verified (47 assertions); null-control test not yet done. Fitted choices listed in §9.

Continues *The Theory of Bipolar Zero* ([10.5281/zenodo.19704117](https://doi.org/10.5281/zenodo.19704117)).
「双極ゼロの理論」の続き。

## Contents / 内容

| File | Description |
|---|---|
| `navel_tetra_model.pdf` | Paper, bilingual English/Japanese / 本文（日英併記） |
| `paper.md` | Source of the paper / 本文のソース |
| `verify_navel_tetra.py` | Verification script, 47 assertions / 検算スクリプト（47項目） |
| `.zenodo.json`, `CITATION.cff` | Metadata / メタデータ |

## Key results / 主な結果

| Quantity | Model | Measured | Deviation |
|---|---|---|---|
| Nucleon mean / electron | 1837.4315 | 1837.4182 | +0.00073% |
| Proton / electron | 1836.1659 | 1836.1527 | +0.00072% |
| Neutron / electron | 1838.6971 | 1838.6837 | +0.00073% |
| He-4 nucleus / electron | 7294.3531 | 7294.2995 | +0.00073% |
| Q(β) in m_p/2000 units | 5/3 | 1.66760 | −0.06% |
| Higgs mass (prediction) | 125.1947 GeV | 125.20 ± 0.11 GeV | −0.05σ |

The fitted choices are listed in §9 of the paper. The Higgs value is a falsifiable prediction.
当てはめた選択は本文 §9 に明記。ヒッグス質量は反証可能な予測。

## Run / 実行

```
python3 verify_navel_tetra.py
```

Python 3 standard library only. / 標準ライブラリのみ。

## Citation / 引用

Kawakami, N. (2026). *Navel–Tetra Lattice-Occupancy Model: Nucleon, Electron and Higgs Mass Ratios from a Geometric Lattice, with an Outlook on Dark Matter and Black Holes* (v1.0). Zenodo. https://doi.org/10.5281/zenodo.23756226

## License / ライセンス

Text: CC BY-NC-SA 4.0. Code: MIT.
