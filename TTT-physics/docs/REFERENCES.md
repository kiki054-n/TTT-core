# TTT-Physics 文献リスト

**目的:** `Unified Geometric Table — TTT-Physics Grand Synthesis v1.0` の A・C・D・E・F・G 節、および `PROOF_STATUS.md` / `ttt_definition_ledger.md` が依拠する外部文献の出典を確定する。

**最終更新:** 2026-09-06

---

## 0. なぜこれが要るか

監査 G6 の指摘。Grand Synthesis の8節のうち、**A・C・D・E・F・G の6節は既存文献の正しい要約**であって TTT 由来ではない。TTT 由来は B 節と H 節だけ。

出典を付けない実害は二つある。剽窃と読まれうることが一つ。もう一つが重い ── **出典がないと、どこまでが借り物でどこからが TTT かが読者にも著者にも分からなくなる。** TTT 自身の寄与が測れなくなれば、`PROOF_STATUS.md` の全部が意味を失う。

したがってこのリストは礼儀の問題ではなく、**測定の前提**である。

---

## 1. 検証状況の凡例

| 印 | 意味 |
|---|---|
| **✓** | 2026-09-06 に一次情報（arXiv 要旨頁、出版社頁、または当該論文を引く文献の参考文献欄）を照合済み |
| **△** | 識別子（arXiv 番号・DOI）は確かだが、巻・頁・年を本セッションでは照合できていない。**投稿前に各自で確認すること** |
| **※** | 査読を経ていない。引用する場合はその旨を明記する |

**規則.** △ の項目を ✓ に格上げするときは、出版社の当該頁を直接見ること。他の論文の参考文献欄からの孫引きは ✓ にしない ── 参考文献欄の誤りはよく伝播する。

---

## 2. A 節 — Planck–Electroweak Hierarchy (RS1 Geometry)

この節の内容（AdS₅ のワープ因子 $e^{-k\pi R}$ が Planck スケールを電弱スケールへ指数的に縮小する）は Randall–Sundrum モデルそのもの。

**✓ [A1]** L. Randall and R. Sundrum, *A Large Mass Hierarchy from a Small Extra Dimension*, Phys. Rev. Lett. **83**, 3370–3373 (1999). arXiv:hep-ph/9905221. DOI: 10.1103/PhysRevLett.83.3370

**△ [A2]** L. Randall and R. Sundrum, *An Alternative to Compactification*, Phys. Rev. Lett. **83**, 4690 (1999). arXiv:hep-th/9906064.
— RS2。A 節が使うのは RS1 のみなので必須ではないが、対にして挙げるのが慣例。

**付すべき一文（案）:**

> A 節の枠組みは Randall–Sundrum モデル [A1] であり、TTT による導出ではない。$k\pi R \approx 39.14$ および $v/M_{\rm Planck} \sim 10^{-17}$ は同モデルの標準的な数値である。

**併せて直すこと（監査 G7）:** $k\pi R \approx 39.14$ なら $e^{-k\pi R} = 1.0\times10^{-17}$ で、表の $2\times10^{-17}$ とは2倍ずれる。どちらかを直す。

---

## 3. C 節 — Composite Higgs Geometry (SO(5)/SO(4))

pNGB としてのヒッグス、$SO(5)/SO(4)$ 対称構造、$v = f\sin\theta$、$\kappa_V = \sqrt{1-\xi}$ — すべて最小複合ヒッグス模型の標準的内容。

**✓ [C1]** D. B. Kaplan and H. Georgi, *SU(2) × U(1) Breaking by Vacuum Misalignment*, Phys. Lett. B **136**, 183 (1984).
— 真空整列の破れによる pNGB ヒッグスという着想の原典。

**✓ [C2]** K. Agashe, R. Contino and A. Pomarol, *The Minimal Composite Higgs Model*, Nucl. Phys. B **719**, 165 (2005). arXiv:hep-ph/0412089.
— MCHM そのもの。C 節の $SO(5)/SO(4)$ はこの論文の構成。

**△ [C3]** K. Agashe and R. Contino, *The Minimal Composite Higgs Model and Electroweak Precision Tests*, Nucl. Phys. B **742**, 59–85 (2006). arXiv:hep-ph/0510164.

**△ [C4]** R. Contino, *The Higgs as a Composite Nambu-Goldstone Boson*, TASI 2009 講義録。arXiv:1005.4269.
— 教育的な導入。$\kappa_V = \sqrt{1-\xi}$ の導出が読みやすい形で載っている。

**△ [C5]** G. Panico and A. Wulzer, *The Composite Nambu–Goldstone Higgs*, Lect. Notes Phys. **913**, Springer (2016). arXiv:1506.01961.
— 現在の標準的な教科書。MCHM5/14/20 の表現論はここに整理されている。

**付すべき一文（案）:**

> C 節は最小複合ヒッグス模型 [C1, C2] の要約である。$SO(5)/SO(4)$ という選択、$h = f\theta$、$v = f\sin\theta$、$\kappa_V = \sqrt{1-\xi}$（$\xi = v^2/f^2$）はいずれも同模型の既知の結果であり、TTT から導かれたものではない。

**表記の誤りとして直すこと:** 表の「結合補正 $\kappa_V = 1-\xi$」は、標準的には $\kappa_V = \sqrt{1-\xi}$。$\xi \ll 1$ での展開なら $\kappa_V \simeq 1 - \xi/2$ であって $1-\xi$ にはならない。

---

## 4. D 節 — Higgs Potential (Coleman–Weinberg)

**✓ [D1]** S. Coleman and E. Weinberg, *Radiative Corrections as the Origin of Spontaneous Symmetry Breaking*, Phys. Rev. D **7**, 1888–1910 (1973). DOI: 10.1103/PhysRevD.7.1888

**△ [D2]** R. Contino, L. Da Rold and A. Pomarol — [F1] と同一（下記）。トップループによる真空傾きの生成を複合ヒッグス文脈で扱う。

**付すべき一文（案）:**

> D 節の1ループ有効ポテンシャルは Coleman–Weinberg 機構 [D1] を pNGB ヒッグスに適用したものであり、複合ヒッグス文脈での標準的な扱い [C5] に従う。TTT はこの計算に寄与していない。

---

## 5. E 節 — Weinberg Sum Rules (UV Finite Condition)

**✓ [E1]** S. Weinberg, *Precise Relations between the Spectra of Vector and Axial-Vector Mesons*, Phys. Rev. Lett. **18**, 507–509 (1967). DOI: 10.1103/PhysRevLett.18.507
— 和則の原典。もともとは QCD のベクトル／軸性ベクトル中間子の話で、複合ヒッグスへの適用は後年。

**✓ [E2]** D. Marzocca, M. Serone and J. Shu, *General Composite Higgs Models*, JHEP **08** (2012) 013. arXiv:1205.0770.

**✓ [E3]** A. Pomarol and F. Riva, *The Composite Higgs and Light Resonance Connection*, JHEP **08** (2012) 135. arXiv:1205.6434.
— 「125 GeV のヒッグスは TeV 以下のフェルミオン共鳴を一般に要求する」という E・F 節の主眼はこの論文の結論。

**△ [E4]** G. Panico, M. Redi, A. Tesi and A. Wulzer, *On the Tuning and the Mass of the Composite Higgs*, JHEP **03** (2013) 051. arXiv:1210.7114.
— 著者名・題名は照合済み。JHEP の巻・論文番号は未照合。

**付すべき一文（案）:**

> E 節の和則は Weinberg [E1] のものであり、複合ヒッグス質量への適用は [E2, E3, E4] による。$\beta \sim \frac{N_c}{2\pi^2} y_t^2 M_T^2 f^2 C$ の形もこれらの文献の結果であって、TTT からの導出ではない。

---

## 6. F 節 — Higgs–Top Partner Relation (MCHM)

**✓ [F1]** R. Contino, L. Da Rold and A. Pomarol, *Light Custodians in Natural Composite Higgs Models*, Phys. Rev. D **75**, 055014 (2007). arXiv:hep-ph/0612048.
— MCHM5 の「カストディアン」（電荷 5/3, 2/3, −1/3 の異種カラーフェルミオン、500–1500 GeV）を導入した論文。G 節の $X_{5/3}$ はここから来ている。

**△ [F2]** G. Panico and A. Wulzer — [C5] と同一。MCHM5 / MCHM14 / MCHM20 の表現ごとの $\sin^n$ ポテンシャルと $M_T/f$ の整理はここ。

**△ [F3]** M. Redi and A. Tesi, *Implications of a Light Higgs in Composite Models*, JHEP **10** (2012) 166. arXiv:1205.0232.

**付すべき一文（案）:**

> F 節の MCHM5 / MCHM14 / MCHM20 という表現の分類、対応する $\sin^n\theta$ ポテンシャル、および $M_T/f$ の値は複合ヒッグス文献 [F1, F2] の既知の結果である。統合関係式 $m_h \approx \frac{\sqrt{6}}{\pi} m_t \frac{M_T}{f}\sqrt{\frac{1-\xi}{2C}}$ もこの系列に属する。

**注意:** 統合関係式は文書中で $m_h \approx 6\pi m_t (M_T/f)\sqrt{(1-\xi)/2C}$ のように読める記法で書かれているが、係数が $6\pi$ なら $m_h$ は $m_t$ の桁を大きく超える。**元文献の係数を確認して書き直すこと。** これは出典の問題ではなく式の問題。

---

## 7. G 節 — LHC Direct Searches (ATLAS/CMS)

**この節は最も早く古びる。** 実験の下限は解析が出るたびに動くので、数値を書くなら**必ず日付と出典を添える**こと。日付のない下限値は、数年で誤りになる。

**✓ [G1]** ATLAS Collaboration, *Vector-like quark summary plots*, ATL-PHYS-PUB-2025-030 (2025).
— ATLAS の VLQ 探索の到達点をまとめた公開ノート。G 節の表を引くならここを基準にするのが最も安全。

**✓ [G2]** ATLAS Collaboration, *Combination of searches for singly produced vector-like top quarks in pp collisions at $\sqrt{s}=13$ TeV with the ATLAS detector*, arXiv:2408.08789.
— 単独生成。SU(2) 一重項・電弱結合 0.5 のベンチマークで **2.1 TeV 以下を排除**。文書の「単独生成 1.8〜2.0 TeV」より強い。

**✓ [G3]** *Vector-Like Quarks at the LHC: A Unified Perspective from ATLAS and CMS Exclusion Limits*, arXiv:2412.01761.
— ATLAS・CMS の制限を横断的に整理したレビュー。対生成で T は一重項で 1.49 TeV、B は二重項で 1.52 TeV、X は 1.46 TeV、Y は 1.7 TeV まで排除。

**△ [G4]** ATLAS Collaboration, *Search for single production of vector-like quarks decaying into $W(\ell\nu)b$ in pp collisions at $\sqrt{s}=13$ TeV*, arXiv:2506.15515.

**付すべき一文（案）:**

> G 節の下限値は ATLAS/CMS の直接探索による [G1–G3]。**2026年9月時点の値**であり、以後の解析で更新される。単独生成については、結合の仮定によって [G2] のように 2.1 TeV まで排除されている場合がある。

**併せて直すこと:** 表の「単独生成 1.8〜2.0 TeV」は [G2] の 2.1 TeV より緩い。更新するか、どのベンチマークの値かを明記すること。

---

## 8. B 節・H 節 — TTT 由来の部分

**この2節だけが TTT の仕事である。** ただし B 節の内部にも借り物がある。

**✓ [B1]** Y. Koide, *Fermion–Boson Two-Body Model of Quarks and Leptons and Cabibbo Mixing*, Lett. Nuovo Cimento **34**, 201–205 (1982). DOI: 10.1007/BF02817096
— 小出模型の最初期の論文。

**△ [B2]** Y. Koide, Phys. Lett. B **120**, 161 (1983).
**△ [B3]** Y. Koide, Phys. Rev. D **28**, 252 (1983).
— 荷電レプトン質量関係式
> $$m_e+m_\mu+m_\tau=\frac{2}{3}\left(\sqrt{m_e}+\sqrt{m_\mu}+\sqrt{m_\tau}\right)^{2}$$
> の出所。**巻・頁は未照合。投稿前に確認すること。**

**△※ [B4]** C. A. Brannen, *The Lepton Masses*, 自己刊行ノート（brannenworks.com）。
— 表の「タウ ← Koide 角 $2\pi/9$」が使っている表式の出所。**査読を経ていない。** 引用する場合はその旨を明記し、かつ **本来は3世代を $n=0,1,2$ で同時に与える表式であって $\mu\to\tau$ の倍率ではない**（監査 G3）ことに注意。

**B 節に付すべき一文（案）:**

> B 節の質量階層は TTT の構成である。ただしタウの行は小出の関係式 [B1–B3] に依拠しており、**関係式そのものは 1981 年以来知られたもので TTT の成果ではない**。TTT の寄与は、その関係式に幾何学的な理由を与えられた場合に初めて生じる。現時点でその導出はない。

**H 節に付すべき一文（案）:**

> H 節の2行（複合スケール $f$、Top Partner $M_T$）は、C–F 節の複合ヒッグス文献 [C2, E2, E3, F1] の関係式に TTT の $v$ を代入したものである。

---

## 9. 実験値・データの出典

数値を引くときはここを使う。**PDG の年を必ず書く**こと。値も誤差も年ごとに動く。

**△ [X1]** Particle Data Group, *Review of Particle Physics*（該当年版）。
— $m_H = 125.20 \pm 0.11$ GeV、$m_\tau = 1776.86 \pm 0.12$ MeV、$m_s = 93.4^{+8.6}_{-3.4}$ MeV などの出所。**どの年版か明記すること。**

**△ [X2]** CODATA 推奨値（該当年版）。
— $m_p/m_e = 1836.15267343(11)$ など。

**△ [X3]** ALEPH, DELPHI, L3, OPAL, SLD ほか, *Precision Electroweak Measurements on the Z Resonance*, Phys. Rept. **427**, 257 (2006). arXiv:hep-ex/0509008.
— 軽ニュートリノ世代数 $N_\nu = 2.9840 \pm 0.0082$。**P6 の反証条件はこの測定に当てる。**

---

## 10. 他の TTT 文書が参照している文献

`PROOF_STATUS.md` および `ttt_definition_ledger.md` から。すべて △（本セッションでは未照合）なので、引用の際に確認する。

### 幾何・対称性

**△ [Y1]** D. Shechtman, I. Blech, D. Gratias, J. W. Cahn, *Metallic Phase with Long-Range Orientational Order and No Translational Symmetry*, Phys. Rev. Lett. **53**, 1951 (1984).
— 準結晶。P6 の但し書き（結晶学的制限が禁じるのは並進周期格子への埋め込みであって5回対称そのものではない）の根拠。

**△ [Y2]** 結晶学的制限定理 — 原典を一つに帰属させにくい古典的定理。教科書（例: Hahn 編 *International Tables for Crystallography*）を引くのが安全。

### 境界・ホログラフィー

**△ [Y3]** C. W. Misner, K. S. Thorne, J. A. Wheeler, *Gravitation*, W. H. Freeman (1973).
— $\partial\partial = 0$（境界の境界はゼロ）。**O2 の導出の典拠。**

**△ [Y4]** G. 't Hooft, *Dimensional Reduction in Quantum Gravity*, arXiv:gr-qc/9310026 (1993).
**△ [Y5]** L. Susskind, *The World as a Hologram*, J. Math. Phys. **36**, 6377 (1995). arXiv:hep-th/9409089.
— ホログラフィック原理。「境界が内側を決める」の正式名。

**注意（台帳 §9 の保留）:** ブラックホールエントロピー $S=A/4\ell_P^2$ の係数 1/4 と、TTT の境界エネルギー 0.25 は**同じ数・違う理由**。傍証に使わないこと。

### 創発と媒質

**△ [Y6]** M. A. Levin and X.-G. Wen, *String-net condensation: A physical mechanism for topological phases*, Phys. Rev. B **71**, 045110 (2005). arXiv:cond-mat/0404617.
**△ [Y7]** X.-G. Wen ほか, *Colloquium: Photons and electrons as emergent phenomena*, Rev. Mod. Phys. **77**, 871 (2005).
— **台帳 §10 は [Y7] の書誌で [Y6] の内容を指している疑いがある。どちらを引くか確認すること。**

**△ [Y8]** B. Hensen ほか, *Loophole-free Bell inequality violation using electron spins separated by 1.3 kilometres*, Nature **526**, 682 (2015).
**△ [Y9]** M. Giustina ほか, Phys. Rev. Lett. **115**, 250401 (2015).
**△ [Y10]** L. K. Shalm ほか, Phys. Rev. Lett. **115**, 250402 (2015).
— 抜け穴なし Bell 検証。「局所実在的な媒質では量子論に到達できない」の根拠。

**△ [Y11]** Y. Couder and E. Fort, *Single-Particle Diffraction and Interference at a Macroscopic Scale*, Phys. Rev. Lett. **97**, 154101 (2006).
**△ [Y12]** T. Bohr ほか（Andersen et al.）, Phys. Rev. E **92**, 013006 (2015).
— 歩く液滴。量子化軌道は再現するが二重スリット干渉は再現しない。

### 宇宙論・その他

**△ [Y13]** E. P. Tryon, *Is the Universe a Vacuum Fluctuation?*, Nature **246**, 396 (1973).
— ゼロエネルギー宇宙。双極0公理と同型。

**△ [Y14]** V. Pavlidou and T. N. Tomaras, *Where the world stands still: turnaround as a strong test of ΛCDM cosmology*, JCAP (2014).
— ターンアラウンド半径 $R_{ta} = (3GM/\Lambda c^2)^{1/3}$。

**△ [Y15]** C. S. Wu ほか, *Experimental Test of Parity Conservation in Beta Decay*, Phys. Rev. **105**, 1413 (1957).
— パリティ非保存。**R6 の「本当の左右がある場所」。**

**△ [Y16]** M. Millot ほか, *Nanosecond X-ray diffraction of shock-compressed superionic water ice*, Nature **569**, 251 (2019).
— 超イオン氷。R5 の近傍で本物なのはこれ。

**△ [Y17]** Lord Kelvin, *Baltimore Lectures*（1893年の講義、1904年刊）。
— キラリティ（χείρ ＝手）の語源。

**△ [Y18]** T. L. V. Ulbricht and F. Vester, 1959。
— ホモキラリティとパリティ非保存を結ぶ仮説。**エネルギー差は相対 $10^{-17}$ 程度で未確認**であることを併記すること。

---

## 11. 作業手順

1. **G6 の6節に §2–§7 の「付すべき一文」を入れる。** これが最優先。配布前に済ませる。
2. **△ を潰す。** 特に [B2] [B3]（小出の原論文）と [Y7]（Levin–Wen の書誌）。この2箇所は間違えると内容の主張が変わる。
3. **B 節と H 節に「ここからが TTT」と明示する。** 節の頭に一行あれば足りる。
4. **G 節に日付を入れる。** 「2026年9月時点」。
5. **A 節の $2\times10^{-17}$、C 節の $\kappa_V = 1-\xi$、F 節の $6\pi$ 係数を直す。** いずれも出典と照らすと合わない。

---

## 12. 書式について

Zenodo 提出を前提にするなら、リポジトリ直下に BibTeX（`references.bib`）を置いて各文書から `\cite` するのが確実。Markdown のままなら、脚注番号ではなく本リストのキー（[A1] [C2] …）を本文に埋めるほうが、文書が増えたときに壊れにくい。

**やってはいけないこと:** 出典を「参考文献」として末尾にまとめて並べるだけにすること。それでは**どの主張が誰のものか**が復元できず、G6 の指摘は解消しない。節ごとに帰属を書くこと。
