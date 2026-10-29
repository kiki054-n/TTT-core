---
title: "Navel–Tetra Lattice-Occupancy Model: Nucleon, Electron and Higgs Mass Ratios from a Geometric Lattice, with an Outlook on Dark Matter and Black Holes"
subtitle: "へそとテトラの格子占有モデル — 幾何学的格子から導く核子・電子・ヒッグスの質量比と、ダークマター・ブラックホールへの展望"
author:
  - "Kawakami Naoyuki（川上真潔）· ORCID 0009-0009-2972-6511"
  - "Team Shiojiri, Shiojiri, Nagano, Japan"
date: "2026-10-29 · Version 1.0"
---

**Relation to earlier records / 先行記録との関係.** This note continues *The Theory of Bipolar Zero* (Kawakami 2026, DOI 10.5281/zenodo.19704117). All numbers below are recomputed and fixed by assertions in the accompanying script `verify_navel_tetra.py` (47 checks, all passing).
本稿は「双極ゼロの理論」（DOI 10.5281/zenodo.19704117）の続きです。本文の数値はすべて付属スクリプト `verify_navel_tetra.py`（47項目、全項目合格）で再計算・固定しています。

**Status / 位置づけ.** This is a phenomenological lattice-occupancy model. It reproduces several measured mass ratios with small integer rules, but it is **not** derived from quantum field theory, and the choices that enter it are listed explicitly in §9. Readers should judge it by the falsifiable prediction in §7 and the open tests in §12.
本稿は、格子の占有数に基づく現象論的モデルです。いくつかの実測の質量比を少数の整数の規則で再現しますが、場の量子論から導出したものではありません。モデルに入っている選択は §9 にすべて明記します。評価は、§7 の反証可能な予測と §12 の検証課題によって行ってください。

---

## Abstract

A cubic lattice of $n^3$ cells is filled by a population that triples each generation, $2\cdot3^n$. The population first exceeds the lattice at $5^3=125$ (162 vs 125), leaving an overflow of $37=4^3-3^3$. Treating 125 cells as the space of one nucleon with 2000 units, a compression factor $\lambda=501/500$ obtained from the central quarter-cell of the $5^3$ block, and an ordering rule for which parts of the 162 are compressed, gives

$$\frac{m_N}{m_e}=125\cdot16-\left[125\lambda^2+34\lambda+3\right]=1837.4315,$$

within $+0.0007\%$ of the measured nucleon mean. Splitting the nucleon by the free-neutron decay relation $m_n-m_p=m_e+\tfrac53u$ (with $\tfrac53$ obtained from the twist released when an icosahedron relaxes to a pentagonal bipyramid) gives the proton and neutron to the same $+0.0007\%$. Helium-4 follows with a binding of $60u$ plus a connection term $\tfrac14 m_e$, again $+0.0007\%$. A separate counting gives $m_H/m_e=245\,000$, i.e. a Higgs mass of **125.1947 GeV**, compared with the PDG 2025 average $125.20\pm0.11$ GeV. The model frames mass as the energy of lattice occupancy and spatial energy per cell as constant; we outline how these two statements lead to concrete questions about dark matter and black holes.

## 要旨

$n^3$ 個のマスからなる立方格子に、世代ごとに3倍になる誕生数 $2\cdot3^n$ が入ります。誕生数が初めて格子を超えるのは $5^3=125$ で（162 対 125）、超過は $37=4^3-3^3$ です。125 マスを核子1個の空間（2000単位）とし、$5^3$ の中心の 1/4 マスから得られる圧縮係数 $\lambda=501/500$ と、162 のどの部分が何段圧縮されるかという順序の規則を使うと、核子と電子の質量比が実測の核子平均と $+0.0007\%$ で一致します。中性子のβ崩壊の関係 $m_n-m_p=m_e+\tfrac53u$（$\tfrac53$ は正二十面体が五角双錐へとねじれを解くときに放出される量）で陽子と中性子に分けても、同じ $+0.0007\%$ です。ヘリウム4は、結合 $60u$ とつながりの項 $\tfrac14 m_e$ を加えて、やはり $+0.0007\%$ で一致します。別の数え方から $m_H/m_e=245\,000$、つまりヒッグス質量 **125.1947 GeV** が出ます（PDG 2025 の平均は $125.20\pm0.11$ GeV）。本モデルは、質量を格子占有のエネルギーとして、またマスあたりの空間エネルギーを一定として扱います。この二つの立場から、ダークマターとブラックホールについての具体的な問いを立てます。

---

## 1. Physical standpoint / 物理的立場

The model rests on statements that are standard physics, restated in its own terms:

1. **Mass is confined energy.** About 99% of the proton mass is field energy of confined quarks and gluons; the Higgs mechanism supplies only the current-quark masses. In this model, mass is the energy required for particles and the lattice to coexist (occupancy energy).
2. **Energy added to a body increases its mass.** $E=\gamma mc^2$ diverges as $v\to c$.
3. **Gravity is not a force between masses.** In general relativity bodies follow geodesics of spacetime whose curvature is sourced by energy–momentum. In this model, the source of spatial shape is the occupancy of the lattice.
4. **Energy per unit space is constant; total energy grows with expansion.** This is the behaviour of a cosmological constant. Global energy conservation does not hold in an expanding spacetime; local conservation does.
5. **Quantum mechanics treats time as an external fixed parameter**, not an observable — the "problem of time" between quantum theory and general relativity.

本モデルは、次の標準的な物理の事実を、モデルの言葉で言い直したものに立っています。

1. **質量は閉じ込められたエネルギーである。** 陽子の質量の約99%はクォークとグルーオンを閉じ込める場のエネルギーで、ヒッグス機構が与えるのはクォーク自身の質量だけです。本モデルでは、質量を「粒子と格子が共存するためのエネルギー（占有エネルギー）」として扱います。
2. **エネルギーを加えると質量が増える。** $E=\gamma mc^2$ は $v\to c$ で発散します。
3. **重力は質量どうしの引力ではない。** 一般相対論では、物体はエネルギー・運動量が曲げた時空の測地線に沿って慣性で進みます。本モデルでは、空間の形を決める源は格子の占有です。
4. **空間あたりのエネルギーは一定で、総量は膨張とともに増える。** これは宇宙定数の振る舞いです。膨張する時空では全体のエネルギー保存は成り立たず、局所的な保存が成り立ちます。
5. **量子力学は時間を外から与えられる固定した目盛りとして扱う。** 量子論と一般相対論の間の「時間の問題」です。

## 2. Lattice and counting rules / 格子と数え方

The genesis population starts at 2 (the bipolar pair) and triples each generation; the available space is a cube of side $n+1$.

誕生数は双極の2から始まり、世代ごとに3倍になります。入れる空間は一辺 $n+1$ の立方体です。

| Generation 世代 $n$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Births 誕生数 $2\cdot3^n$ | 2 | 6 | 18 | 54 | **162** |
| Cells マス $(n+1)^3$ | 1 | 8 | 27 | 64 | **125** |
| Spare 余裕 | −1 | 2 | 9 | 10 | **−37** |
| Wall 壁 | breaks 破る | holds | holds | holds | **breaks 破る** |

After genesis, the first break is at $5^3$; the overflow $37=4^3-3^3$ and the total $162=125+37$ are fixed by the rule, not chosen. The $5^3$ block decomposes as shell $98=5^3-3^3$ plus core $27$, and the cube identity $3^3+4^3+5^3=6^3$ gives the layer $91=6^3-5^3=3^3+4^3=7\cdot13$, the midpoint $108=6^3/2$, and the steps $91\to108\to125$ of $17$ each ($91+2\cdot17=125$). The overflow splits as $37=34+3$: 34 enters with the next layer, 3 fits within the spare 10 of the $4^3$ stage.

創成の後、最初に壁が破れるのは $5^3$ で、超過 $37=4^3-3^3$ と総数 $162=125+37$ は規則から自動的に決まります。$5^3$ のブロックは外郭 $98=5^3-3^3$ と内部 27 に分かれ、立方数の恒等式 $3^3+4^3+5^3=6^3$ から、広がる層 $91=6^3-5^3=3^3+4^3=7\cdot13$、中点 $108=6^3/2$、17 ずつの段 $91\to108\to125$ が出ます。超過は $37=34+3$ に分かれ、34 は次の層とともに入り、3 は $4^3$ の段の余裕 10 の中に収まります。

## 3. Compression factor / 圧縮係数

The $5^3$ block has a central cell. A centre of value 1 would violate the bipolar-zero axiom and a centre of value 0 would deny existence; the centre is therefore assigned $\tfrac14$, so the energy that can exist in 125 cells is $125.25$. Multiplying by the tetra 4: $125.25\times4=501=500+1$. The compression factor per pressure stage is

$$\lambda=\frac{501}{500}.$$

$5^3$ のブロックには中心のマスがあります。中心が 1 だと双極ゼロの公理が通らず、0 だと存在が否定されるので、中心は $\tfrac14$ とします。125 マスに存在できるエネルギーは 125.25 で、テトラの 4 を掛けると $501=500+1$ です。圧力1段あたりの圧縮係数は $\lambda=501/500$ です。

## 4. Nucleon–electron mass ratio / 核子と電子の質量比

The 162 births are compressed according to when they entered:

| Part 部分 | Count 数 | Pressure 受ける圧力 | Stages 段 | Compressed 圧縮後 |
|---|---|---|---|---|
| Original space 最初からある空間 | 125 | space + tetra binding of the 37 / 空間 ＋ 37 のテトラ拘束 | 2 | 125.5005 |
| Next overflow 次からのはみだし | 34 | entering $6^3$ (same magnitude) / $6^3$ に入る圧力 | 1 | 34.0680 |
| Within $4^3$ spare / $4^3$ の余裕内 | 3 | none / なし | 0 | 3 |
| Total 合計 | 162 | | | 162.5685 |

With the nucleon unit $125\cdot16=2000$ (in electron-scale units):

$$\frac{m_N}{m_e}=2000-\left[125\lambda^2+34\lambda+3\right]=1837.4315\qquad(\text{measured mean }1837.4182,\ +0.00073\%).$$

For the record, compressing all 162 twice gives $-0.0036\%$, and leaving only the 3 uncompressed gives $-0.0030\%$; the improvement comes from the one-stage rule for the 34.

記録として、162 すべてを二段圧縮すると $-0.0036\%$、3 だけを圧縮しない場合は $-0.0030\%$ です。改善をもたらしているのは「34 は一段」という規則です。

## 5. Proton–neutron split and the 5/3 / 陽子・中性子の分離と 5/3

**Navel as twist.** The connection (umbilical cord) between a neutron and a proton is a twist. While connected there is no navel; when the twist is cut it gathers into a bipyramidal navel. In physical terms this is free-neutron β-decay, $n\to p+e^-+\bar\nu_e$, so

$$m_n=m_p+m_e+Q_\beta .$$

**Why 5/3.** The twisted state is the icosahedron, which is the "gyroelongated pentagonal bipyramid": two pentagonal pyramids (10 faces) joined by a twisted antiprism band (10 faces). Untwisting removes the band and leaves a pentagonal bipyramid. Measured in units of the triangular bipyramid (the shape of the navel and of the 1:3 particle condition), the released band is $5/3$ in every count:

| | Icosahedron 正二十面体 | Pentagonal bipyramid 五角双錐 | Released 放出 | Triangular-bipyramid unit 三角双錐の単位 | Ratio 比 |
|---|---|---|---|---|---|
| Vertices 頂点 | 12 | 7 | 5 | 3 (triangle) | 5/3 |
| Faces 面 | 20 | 10 | 10 | 6 | 5/3 |
| Edges 辺 | 30 | 15 | 15 | 9 | 5/3 |

With $u=m_N/2000=0.918716\,m_e$, the model gives $m_n-m_p=m_e+\tfrac53u=2.53119\,m_e$ (measured 2.53099). Independently, the measured $Q_\beta=0.78233$ MeV equals $1.6676$ in units of $m_p/2000$, i.e. $\tfrac53$ to $0.06\%$. The proton and neutron then follow at $+0.0007\%$ (Table §8).

**へそ＝ねじれ。** 中性子と陽子のつながり（へその緒）はねじれです。つながっている間はへそではなく、ねじれが切れると双錐の形のへそにまとまります。物理ではこれは中性子のβ崩壊で、$m_n=m_p+m_e+Q_\beta$ です。

**5/3 の理由。** ねじれた状態は正二十面体（別名「ねじれ五角双錐」）で、上下の五角錐（10面）とねじれた帯（10面）でできています。ねじれが解けると帯が抜け、五角双錐が残ります。抜けた帯を、へその形であり 1:3 の粒子条件の形でもある三角双錐の単位で測ると、頂点・面・辺のどれでも 5/3 になります。実測の $Q_\beta=0.78233$ MeV は、$m_p/2000$ の単位で 1.6676 で、5/3 と 0.06% で一致します。

## 6. Helium-4 / ヘリウム4

**Spatial energy as the vessel.** The value $8000=4\times2000$ is the spatial energy of four nucleon cells. It is the same before, at and after "birth" (binding); what changes is the distribution between particles and connections inside it.

**Binding $60u$.** Sharing one outer tetra among four nucleons frees 3 tetras; replacing each tetra vertex by a triangular bipyramid (5 vertices) multiplies by 5; $3\times5=15$ tetras $=60$ units. The same 60 appears as the face–edge count of the dual pair icosahedron/dodecahedron ($20\times3=12\times5=60$). Measured: $0.7534\%$ of $2m_p+2m_n$, i.e. $60.27$ on the 8000 scale.

**Connection term $\tfrac14 m_e$.** In electron units the measured binding exceeds $60u$ by $0.2502\,m_e$. This equals $2/8$: the two electrons of the first shell over the eight places of the second. In the model, of the four symbols of $OO\pi O$ one $O$ enters the 125-cell and carries the connecting force with energy $\tfrac14$ of the unit it enters. Then

$$\frac{M_\alpha}{m_e}=2m_p+2m_n-\left(60u+\tfrac14\right)=7294.353\qquad(\text{measured }7294.300,\ +0.00073\%).$$

The residual that remains is the same $+0.0007\%$ as for single nucleons; helium adds no new deviation.

**器としての空間エネルギー。** 8000 は核子4個分の空間エネルギーで、誕生（結合）の前・時・後で変わりません。変わるのは、その中の粒子とつながりの配分です。

**結合 $60u$。** 4 核子が外郭を1つ共有すると3テトラが抜け、テトラの各頂点を三角双錐（5頂点）に置き換えると ×5 になり、$3\times5=15$ テトラ ＝ 60 単位です。同じ 60 は、双対の正二十面体・正十二面体の $20\times3=12\times5$ としても現れます。

**つながりの項 $\tfrac14 m_e$。** 電子の単位で測ると、実測の結合は $60u$ より $0.2502\,m_e$ 大きく、これは第1殻の電子2個と第2殻の8席の比 2/8 に等しい値です。モデルでは、$OO\pi O$ の4つの記号のうち1つの $O$ が 125 のマスに入り、入った先の単位の 1/4 のエネルギーでつながる力を担います。残る差は単独の核子と同じ $+0.0007\%$ で、ヘリウムによる新しいずれは生じません。

## 7. Higgs–electron ratio: a falsifiable prediction / ヒッグスと電子の比：反証可能な予測

$$\frac{m_H}{m_e}=\frac{(125\cdot8-20)\,(125\cdot16)}{8}=\frac{980\times2000}{8}=245\,000 .$$

Here $125\cdot8=1000$ is the eight $O$ of two $OO\pi O$, each expanded to 125; $20$ is the twist (icosahedral faces) removed; $125\cdot16=2000$ is the nucleon unit. Because this is a ratio of masses, it does not depend on GeV or any human unit. With $m_ec^2=0.51099895069$ MeV:

$$m_H=245\,000\,m_e=\mathbf{125.1947\ GeV}.$$

| Measurement 測定 | Value 値 (GeV) | Pull vs 125.1947 |
|---|---|---|
| PDG 2025 average 世界平均 | 125.20 ± 0.11 | −0.05σ |
| ATLAS 2023 | 125.11 ± 0.11 | +0.77σ |
| CMS 2020 | 125.38 ± 0.14 | −1.32σ |

The earlier centre-quarter reading (125.25, equal to the PDG 2022/23 average) differs by 55 MeV. HL-LHC (projected ±20–30 MeV) can separate the two at about 2σ; a future $e^+e^-$ Higgs factory (projected ± a few MeV) will decide. **If the measured value settles away from 125.1947 GeV beyond its uncertainty, this part of the model is falsified.**

$125\cdot8=1000$ は $OO\pi O$ 2つの 8 つの $O$ がそれぞれ 125 に展開された数、20 は抜けるねじれ（正二十面体の面）、$125\cdot16=2000$ は核子の単位です。質量どうしの比なので、GeV などの人間の単位に依存しません。予測は **125.1947 GeV** です。中心 1/4 の読み（125.25、PDG 2022/23 の平均と同じ値）とは 55 MeV 違い、HL-LHC でおよそ 2σ、将来のヒッグス工場ではっきり区別されます。**測定値が誤差を超えて 125.1947 GeV から外れれば、この部分は反証されます。**

## 8. Results / 結果の一覧

Inputs: CODATA 2022 mass ratios; PDG 2025 Higgs mass. 入力値：CODATA 2022、PDG 2025。

| Quantity 量 | Model モデル | Measured 実測 | Deviation 差 |
|---|---|---|---|
| Nucleon mean / electron 核子平均 | 1837.4315 | 1837.4182 | +0.00073% |
| Proton / electron 陽子 | 1836.1659 | 1836.1527 | +0.00072% |
| Neutron / electron 中性子 | 1838.6971 | 1838.6837 | +0.00073% |
| He-4 nucleus / electron ヘリウム4原子核 | 7294.3531 | 7294.2995 | +0.00073% |
| $Q_\beta$ in $m_p/2000$ units | 5/3 = 1.66667 | 1.66760 | −0.06% |
| He-4 binding fraction 結合の割合 | 60/8000 = 0.750% | 0.7534% | (closed by $\tfrac14 m_e$) |
| Higgs / electron ヒッグス | 245 000 (125.1947 GeV) | 245 010 (125.20 ± 0.11 GeV) | −0.05σ |

## 9. Honest accounting / 選択の明記

The agreements above depend on the following choices. They are motivated in the text, but they were fixed while looking at the data, so they count as fitted structure until derived independently.

1. The nucleon unit $2000=125\cdot16$.
2. The centre value $\tfrac14$ and hence $\lambda=501/500$.
3. The staging rule (125 twice, 34 once, 3 not at all).
4. The use of $\tfrac53$ in nucleon units for the $n$–$p$ split.
5. The helium connection term $\tfrac14 m_e$ (2/8); a rule for other nuclei has **not** yet been fixed.
6. In the Higgs formula, the numbers 8, 20 and 16.

**Look-elsewhere caution.** Small integers built from 2, 3, 4, 5 can reproduce many targets at the $10^{-3}$–$10^{-4}$ level. Earlier checks by the author found that unconstrained searches of this kind hit TTT-style numbers at rates of order 10–25%. The present results are stronger in two respects — one compression factor is reused across nucleons and helium, and the Higgs ratio is a prediction with no adjustable unit — but they are not yet a derivation.

**Common residual.** All four mass ratios deviate by the same $+0.0007\%$. A single shared correction is therefore missing; it is not attributable to helium binding.

**Not claimed.** The model does not derive the fine-structure constant, the weak coupling, or $\hbar$; the chemistry in §10 is qualitative.

上の一致は、次の選択に依存しています。本文で動機は述べましたが、データを見ながら固めたものなので、独立に導かれるまでは「当てはめた構造」として扱います。①核子の単位 2000 ②中心 1/4 と $\lambda=501/500$ ③段数の規則 ④陽子・中性子の分離での 5/3 ⑤ヘリウムのつながりの項 1/4（他の原子核での規則は未確定）⑥ヒッグスの式の 8、20、16。2〜5 の小さな整数の組み合わせは、多くの目標値を $10^{-3}$〜$10^{-4}$ の精度で再現できます。4つの質量比がすべて同じ $+0.0007\%$ ずれていることは、共通の補正が一つ欠けていることを示します。本モデルは微細構造定数・弱い結合定数・$\hbar$ を導いていません。

## 10. Appendix: chemistry and solids (qualitative) / 付録：化学と固体（定性的）

**Where the connection is cut.** Cutting $OO\pi O$ at different positions corresponds to the three levels of binding: electron to nucleus (atom), neutron to proton (nucleus, pion exchange), nucleus to nucleus via shared electrons (molecule).

**σ and π.** Axial overlap (σ, "line") and lateral overlap (π, "surface") correspond to $OO$ and $O\pi$. From average carbon bond enthalpies (C–C 347/346, C=C 614/602, C≡C 839/835 kJ/mol), the mean π over σ is $0.709/0.707\approx1/\sqrt2$; individual π bonds are not equal (≈267 and ≈225).

**Per-electron atomization.** Dividing atomization enthalpies by total electron count gives $\mathrm{CH_4}:\mathrm{C_2H_4}:\mathrm{C_2H_2}=166.35:140.81:117.33$ kJ/mol, ratios to acetylene 1.418 and 1.200.

**Octahedral bipole.** The four sp³ directions (tetrahedron $T_1$) and the opposite set $T_2$ together are the eight face normals of an octahedron — the two sublattices of diamond and the octet of eight electrons.

**Diamond, graphite, silicon.** Diamond ($4\sigma$) and graphite ($3\sigma+\pi$) differ in cohesive energy by only 1.9 kJ/mol. Silicon has the diamond structure but no stable π-bonded allotrope. Band gaps along C → Si → Ge → α-Sn (5.48, 1.17, 0.74, 0 eV at 0 K) show the bond fixation weakening with shell number and vanishing at the fifth shell.

これらは定性的な対応で、数値の一致は検証として扱いません。へその緒の切れる位置が原子・原子核・分子の三つの結合に対応し、σ（線）と π（面）が $OO$ と $O\pi$ に対応します。炭素の σ と π の平均の比は約 $1/\sqrt2$、電子1個あたりの原子化エネルギーの比はメタン 1.418、エチレン 1.200（アセチレン基準）です。sp³ の4方向とその逆向きは正八面体の8面で、ダイヤモンドの2つの副格子とオクテットの8に当たります。C→Si→Ge→α-Sn のバンドギャップは殻が上がるほど小さくなり、第5殻で0になります。

## 11. Outlook: dark matter and black holes / 展望：ダークマターとブラックホール

The model makes two structural statements: (A) the spatial energy per cell is constant; (B) mass is occupancy energy of particles bound into the lattice. These lead to the following research questions. They are stated as questions with quantitative targets, not as results.

本モデルの構造上の主張は二つです。(A) マスあたりの空間エネルギーは一定である。(B) 質量は格子に拘束された粒子の占有エネルギーである。ここから次の研究課題が立ちます。結果ではなく、数値の目標を伴う問いとして書きます。

**11.1 Dark energy.** Statement A is the defining property of a cosmological constant (constant energy density, total growing with volume). Target: the model must give the observed dark-energy density, $\Omega_\Lambda\approx0.69$, from the per-cell energy without inserting it.
**ダークエネルギー。** (A) は宇宙定数の性質そのものです。目標：マスあたりのエネルギーから、観測される $\Omega_\Lambda\approx0.69$ を外から入れずに出すこと。

**11.2 Dark matter.** Occupancy units that carry energy but no outer shell — no navel to an electron, hence no electromagnetic coupling — would gravitate (energy sources curvature) without emitting or absorbing light. The model already contains such objects: the uncut connection ("0-navel") state and bare $O\pi O$ cells. Targets: (i) the ratio of dark to baryonic matter, $\Omega_c h^2/\Omega_b h^2=0.120/0.0224\approx5.36$ (Planck 2018), from the counting of shelled vs. unshelled occupancy; (ii) collisionless behaviour on galactic scales; (iii) no conflict with direct-detection limits.
**ダークマター。** エネルギーを持つが外郭を持たない（電子へのへそがなく、電磁的に結合しない）占有単位は、光を出さず吸わずに重力だけを及ぼします。モデルには、切れていないつながり（0 のへそ）の状態や、外郭のない $O\pi O$ のマスとして、すでにそのような対象があります。目標：(i) 外郭のある占有と外郭のない占有の数え方から、暗黒物質と通常物質の比 $\approx5.36$（Planck 2018）を出す (ii) 銀河スケールで衝突しない振る舞い (iii) 直接探索の制限と矛盾しないこと。

**11.3 Black holes.** Statement B implies a maximum occupancy: in the author's earlier counting the 125-cell box holds between 125 (all space) and 500 (all mass) units, and compression beyond the lattice wall breaks it. Nuclear matter already has constant per-nucleon volume, and neutron stars are bound near that density up to the TOV limit (about 2.2–2.3 solar masses). Questions: (i) does lattice saturation give a maximum mass for a nucleon-occupied star, and where relative to the TOV limit? (ii) does a fully saturated region behave as a horizon? (iii) The Bekenstein–Hawking entropy is $S=A/(4\ell_P^2)$, one quarter per Planck area; the model also assigns $\tfrac14$ per connecting $O$. Whether this is the same quarter or a coincidence must be decided by deriving the area law from occupancy counting, not by noting the shared number.
**ブラックホール。** (B) からは占有の上限が出ます。これまでの勘定では 125 マスの箱は 125（すべて空間）から 500（すべて質量）までを収め、格子の壁を超える圧縮で箱が壊れます。原子核物質は核子あたりの体積が一定で、中性子星はその密度付近で TOV 限界（太陽質量の約 2.2〜2.3 倍）まで支えられます。問い：(i) 格子の飽和が、核子でできた星の最大質量を与えるか、それは TOV 限界に対してどこか (ii) 完全に飽和した領域は地平面として振る舞うか (iii) ベッケンシュタイン・ホーキングのエントロピーは $S=A/(4\ell_P^2)$ でプランク面積あたり 1/4 です。モデルもつながる $O$ に 1/4 を割り当てています。同じ 1/4 か偶然かは、数字が同じことではなく、占有の数え方から面積則を導けるかで決める必要があります。

## 12. Next tests / 次の検証

1. **Higgs mass** — 125.1947 GeV against HL-LHC and future Higgs-factory measurements (§7). ヒッグス質量の精密測定との照合。
2. **Other nuclei** — fix, before computing, the connection term for deuteron, He-3, C-12, O-16 from shell filling, then compare with CODATA/AME masses. 計算の前に重水素などのつながりの項を殻の埋まり方から決め、その後で実測と比べる。
3. **Common residual** — identify the single correction behind the shared $+0.0007\%$. 共通に残る $+0.0007\%$ の出どころ。
4. **Derivations** — derive the staging rule and the equal-pressure assumption from the order of births; derive the 7 left over from the spare 10. 段数の規則・等しい圧力の仮定・余裕10のうち残る7の導出。
5. **Cosmology** — the targets in §11. §11 の目標値。

## References / 参考文献

- Kawakami, N. (2026). *The Theory of Bipolar Zero*. Zenodo. doi:10.5281/zenodo.19704117
- Mohr, P. J., Newell, D. B., Taylor, B. N. & Tiesinga, E. CODATA Recommended Values of the Fundamental Physical Constants: 2022.
- Navas, S. et al. (Particle Data Group), Phys. Rev. D 110, 030001 (2024) and 2025 update — Higgs mass $125.20\pm0.11$ GeV.
- ATLAS Collaboration, Phys. Rev. Lett. 131, 251802 (2023) — $m_H=125.11\pm0.11$ GeV.
- CMS Collaboration, Phys. Lett. B 805, 135425 (2020) — $m_H=125.38\pm0.14$ GeV.
- Planck Collaboration, Astron. Astrophys. 641, A6 (2020) — cosmological parameters.
- Yukawa, H. (1935). Proc. Phys.-Math. Soc. Japan 17, 48.
- Aubert, J. J. et al. (EMC), Phys. Lett. B 123, 275 (1983).
- Bekenstein, J. D. (1973), Phys. Rev. D 7, 2333; Hawking, S. W. (1975), Commun. Math. Phys. 43, 199.
- Karton, A. & Martin, J. M. L. (2007) — heat of formation of Si(g), 452.7 ± 0.8 kJ/mol.

---

**License.** Text: CC BY-NC-SA 4.0. Code (`verify_navel_tetra.py`): MIT.
**ライセンス。** 本文：CC BY-NC-SA 4.0。コード：MIT。
