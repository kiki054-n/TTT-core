# 五回双晶ノート v5 — Cheng 全文 + Lin プレプリント入手後の全面改訂

2026-09-13 / v4 を置き換える。**v4 には誤りが一つ、過剰主張が一つあり、
さらに二つの予言（P1・P4）が新しい一次データで死んだ。**

入手した一次文献：

> **[C]** Zhihua Cheng, Chuqiao Shi, Kaijie Zhao, Michael Engel, Matthew R. Jones, Yimo Han,
> *Precision mapping of equilibrium disclination strain in pentagonally twinned nanostructures*,
> **Sci. Adv. 11, eaea9781 (2025)** — Rice + FAU Erlangen。CC BY-NC。
> 生データ Zenodo 10.5281/zenodo.17156384。**全文取得済み**

> **[L]** Oliver Lin, Zhiheng Lyu, Hsu-Chih Ni, Xiaokang Wang, Yetong Jia, Chu-Yun Hwang,
> Lehan Yao, Sohini Mandal, Jian-Min Zuo, Qian Chen,
> *Each Grain Different in Its Own Way: Size-Dependent Pseudosymmetry in Fivefold Twinned
> Nanoparticles Mapped by 4D-STEM*, **Adv. Mater. 38(27), e21658 (2026 May; epub Apr 16)**
> DOI 10.1002/adma.202521658 — UIUC。DOE BES DE-SC0024064。
> **プレプリント全文取得済み**：arXiv 2507.14781
> *Size-Dependent Lattice Pseudosymmetry for Frustrated Decahedral Nanoparticles*（2025-07）

---

## 0. 先に訂正二件

### 訂正① — 「Cheng は Yu et al. に言及なし」は誤り（v4 §1）

[C] の **ref 24** は

> H. Wu, **R. Yu**, **J. Zhu**, W. Chen, Y. Li, T. Wang,
> *Size-dependent strain in fivefold twins of gold*, Acta Cryst. B **77**, 93 (2021)

Wu・Yu・Zhu は 2017 年ダイヤモンド論文（Yu, Wu, Wang, Zhu）の著者三名と同一で、
[C] は序論でこれを対立軸の一方として引く：

> "more recent investigations propose tensile strain as the dominant
> accommodation mechanism, with only minor contributions from lattice bending (24)"

しかも **[L] も同じグループを引く**（[L] ref 33、d < 5 nm の粒子で BCT 対称性を
原子座標から割り当てた仕事として）。つまり **BCT という読み自体が Yu/Wu/Zhu 由来**。

金側の Yu との接続は、二本とも既に張っている。未占有のまま残るのは
**ダイヤモンド／シリコン／Pugh 比の側だけ**（[C] にも [L] にも一語もない。確認済み）。

### 訂正② — q = 0.232 の数値棄却は撤回（v4 §3）

v4 は「実験 ν=0.415 vs MD ν=0.36」を弾性レバーに使った。[C] の Methods が禁じている：

> "The simulations used an LJ potential for Au-Au interactions, which reproduced
> surface tension reasonably well but still existed an **~15 % deviation in Young's
> modulus and Poisson's ratio**."

> "strain fields in simulations were extracted from a narrow region of ~3 atomic
> layers near the surface, whereas the experimental strain values were averaged
> across a much larger depth"

$$\frac{\sigma^{\rm sim}}{\sigma^{\rm exp}} = \frac{\gamma^{\rm sim}/h^{\rm sim}}{\gamma^{\rm exp}/h^{\rm exp}} \approx 1.58 \;\Rightarrow\; \frac{h^{\rm sim}}{h^{\rm exp}} = 0.67$$

> "we further average the tensile values in simulation over around 10 atomic layers
> and the discrepancy for 0 truncation drops from around 11 to 6 %"

ν_sim = 0.36 は**第二の材料ではなくポテンシャルの誤差**で、差は弾性ではなく
測定深さに帰属される。**v4 §3 の数値的棄却と q = 0.232 は撤回。**

ただし **P2′ は依然死んでいる**。死因が構造的論証に変わり、そちらの方が強い（§1）。

---

## 1. 構造的論証は [C] 自身の式で確認された

Methods の応力式（逐語）：

$$\sigma = \frac{E}{1+\nu}\,(e_{xx} - e_{yy})$$

$E/(1+\nu) = 2G$ は恒等式なので

$$\boxed{\;\sigma = 2G\,(e_{xx} - e_{yy})\;}$$

**支配方程式に体積弾性率 B が現れない。** 角度欠損を閉じる量は偏差的な法線差
$e_{xx}-e_{yy}$ であり、代価は $2G$。数値も再現する：

| | $e_{xx}$ | $e_{yy}$ | $G$ (GPa) | $\sigma$ (GPa) |
|---|---|---|---|---|
| 実験（edge） | +0.58 % | −0.61 % | 31.10 | 0.740 |
| MD（edge） | +0.67 % | −0.75 % | 40.44 | 1.149 |

比 1.552（論文の ~1.58 と一致）。さらに実験側では
$e_{xx}-e_{yy} = 0.01190$ rad = **0.682°**、報告された引張シェア **0.66°** と 3 % 一致。
**引張チャンネルの角度貢献は $\delta_t = e_{xx}-e_{yy}$ そのもの**と読める。

> **P2″（維持・強化）** $x_t/x_s$ に $B$ は主要項として入らない。両チャンネルは
> 同じ偏差テンソルの成分で、等方体では縮退して同じ $G$ を払う。分配比はほぼ普遍で、
> ダイヤモンドでも 2–3 を出ない。**v3 の「ダイヤモンド 15.4」は誤り。**

---

## 2. [L] が与えた幾何恒等式 — 法線チャンネルの飽和限界は BCT

[L] Eq. 1：

$$k = \frac{d_{220}}{d_{002}} = \frac{1}{\sqrt2}\,\frac{1+\varepsilon_{220}}{1+\varepsilon_{002}} = \tan\theta$$

ここで $2\theta$ が (111) 双晶方向間の面間角。**これは [C] の引張比と同じ観測量**
（実空間/逆空間、220/002 の順が逆）だが、**[L] は幾何的意味を与えている**：

| | $k$ | $2\theta$ |
|---|---|---|
| 理想 FCC | 0.7071 | 70.528° |
| 五回双晶 BCT | 0.7265 | **71.997°** |

$72° \times 5 = 360°$。すなわち

> **BCT とは、法線ひずみチャンネルだけで欠損を完全に閉じ切った状態である。**

これは恒等式であってフィットではない。**法線チャンネルには飽和限界があり、
その限界が BCT** — [C] にも v4 にもなかった視点で、TTT 側にも効く（§6）。

そして [L] の実測：

| 粒径 | $k$ 分布 | 不均一性 |
|---|---|---|
| d < 35 nm | 粒子全体が均質な BCT（FCC 領域 ~10 %） | **粒間**が大・粒内が小 |
| d ≈ 35 nm | 双晶境界と稜に FCC が現れる（主に一つの粒） | 遷移 |
| d > 35 nm | 五つの境界と稜に FCC、粒内は BCT のまま | 粒間が小・**粒内**が大 |

> "the normalized population of fcc-like phase **never exceeds 40 %**"

---

## 3. P4 と P4′ は両方死んだ

[L] 逐語：

> "The NPs exhibit **size-independent** spatial patterns of γ and R to close the
> 7.35° geometric gap"

> "The alternating patterns in γ and R maps across five grains sustain for all the
> NPs, **confirming the size-independence of the gap closing mechanism**."

d > 35 nm では $(R+\gamma)$ の和が 7.35° にプラトー、d < 35 nm では 7.35° 周りを
約 1° ゆらぐ。

- **P4**（回転シェアが R と共に増大、勾配機構）→ **反証**
- **P4′**（回転シェアは切頭深さ TD が支配、サイズ依存は TD が媒介）→ **これも反証**。
  [L] の粒子はクロスオーバーを跨いで実際に形が変わる（丸い modified-Wulff →
  面の立った五角双錐）のに、γ/R のギャップ閉鎖は変わらない。**形状ルートも閉じた。**

v4 §3 で私は「Cheng と Lin を一つの機構で和解させた」と書いたが、
その和解は [L] のプレプリント本文によって**成立しない**。撤回する。

サイズ依存なのは**法線ひずみの分布**と BCT/FCC 比（§2 の表）であって、
チャンネル間の**分配**ではない。

### 3.1 ただし [L] 内部に未解決の緊張がある（重要）

$\gamma + R$ の和が既に 7.35° なら、法線ひずみには閉じるべき残りがない。
にもかかわらず $k > 0.7071$ が至るところで成り立つ＝法線チャンネルは寄与している。

つまり **[C] の分配（引張 45 % / せん断 22.5 % / 回転 32.5 %）と
[L] の会計（γ + R = 7.35°）は同じ分割ではない。**
どちらかの角度換算に二重計上か規格化差がある。

**図を見るまで、両者を合わせた分配数値を引用してはいけない。**
これは今この瞬間の最重要の未解決点であり、v4 のように急いで埋めてはならない。

---

## 4. 二本の論文が正面から食い違っている一点（未占有）

偏心ディスクリネーション（Gryaznov et al., Cryst. Res. Technol. 34, 1091 (1999)）について：

| | 結論 |
|---|---|
| **[C]** | MD で検証し、観測されたひずみ変動を再現するには **35 % 以上の偏心**が必要で「実験観測と整合しない」→ **棄却** |
| **[L]** | 「中心シフトを入れて他を同一に保つと、k が大きく歪んだ粒が再現できる」→ **必須** |

同じ材料・同じ手法（4D-STEM）・同じ仮説について正反対の結論で、
しかも**互いを引用していない**（[L] プレプリント 2025-07、[C] 公刊 2025-10、
[L] 誌上版 2026-04）。

**このトラックで唯一、どちらのグループにも占有されていない争点である。**
第三者が入れる余地があるのはここ。

---

## 5. P1 も死んだ — [L] が界面エネルギーをくれたので初めて数値テストできた

[L] が引用する値（mJ/m²）：

| | Au | Ag |
|---|---|---|
| 積層欠陥 γ_ISF | 32 | 16 |
| 双晶境界 γ_tb | **15** | 8 |
| 粒界 | 364 | 790 |

P1 の $R^\ast = 80\pi(1-\nu)\gamma_{\rm tb}/(\mu\omega^2)$ に入れると（$\omega$ = 0.128388 rad）：

$$R^\ast(\mathrm{Au}) = 4.30\ \mathrm{nm}, \qquad R^\ast(\mathrm{Ag}) = 2.54\ \mathrm{nm}$$

**問題：** 五回双晶 Au 粒子は 20–55 nm で弾性歪みのまま無欠陥であり（[L] と [C] の両方）、
1200 °C まで加熱して初めて部分転位で緩和する。**一桁合わない。**

**診断：** P1 の釣り合いは三項のうち二項しかない。十面体が存在する理由そのものが
**表面エネルギーの低さ**（Marks / Ino）であり、その項を落とした $R^\ast$ は
安定性の閾値として意味を持たない。[L] も言葉でそう言っている — Au の構造安定性は
競合金属に比べた双晶境界コストの低さから来る、という**三者比較**である。

> **P1 は表面項を入れて再定式化するか、撤回する。** 現状の形では死んでいる。

---

## 6. TTT 側に効く一次事実

1. **五角双錐（V_PB = 7）は 35 nm 以上の平衡形態**（[L]）。TTT が固定語彙に
   五角双錐を置くことに、実在の平衡形としての裏付けがつく。
   ただし [L] は幾何的フラストレーションからこれを得ている。**裏付けであって導出ではない。**
2. **7.35° の正確な起源**が一次文献で確認：70.53° × 5 = 352.65° < 360°。
   本トラックの $360° - 5\arccos(1/3) = 7.356103°$、境界あたり 1.4712206° は
   [C] の正規化定数 1.47° と一致。
3. **飽和限界としての 72°**（§2）。$\arccos(1/3) = 70.5288°$ を $72°$ まで歪めれば
   欠損はゼロになる。TTT が扱う 7.356° は「$72° - \arccos(1/3)$ の五倍」でもある。
   $72°$ は五回対称が要求する角度であり、$70.5288°$ は正四面体が与える角度。
   **欠損は「五回対称の要求」と「正四面体の実在」の差**という形に書き直せる。
   これは TTT の公理の言葉に近い。
4. **緩和経路**（[C]）：1200 °C で部分転位配列（中心側 Frank $b=\frac13\langle111\rangle$、
   外側 Shockley $b=\frac16\langle112\rangle$）が回転双極子を作り 5.5° の大部分を吸収。
   平均引張 0.97 % → 0.23 %、転移は **1.8 ms 未満**。
   → **7.356° は転位という逃げ道を持つ。** 幾何的必然として扱うなら、
   この逃げ道を公理の側で明示する必要がある。
5. **形状（切頭深さ TD）が強い制御変数**（[C] Fig. 3G–I）：TD 増加で
   (i) 稜の引張減少、(ii) 頂点のせん断増加、(iii) 回転減少（切頭部では反転）。
   一方サイズは平均には効かず、ゆらぎに効く。
   **ただし §3 の通り、これで [L] のサイズ依存を説明することはできない。**

---

## 7. 予言リスト（v5 時点）

| | 内容 | 状態 |
|---|---|---|
| ~~P1~~ | $R^\ast = 80\pi(1-\nu)\gamma_{\rm tb}/(\mu\omega^2)$ | **死**（§5、Au で 4.3 nm、一桁外れ）。表面項を入れて再定式化 or 撤回 |
| ~~P2~~ | E/G 制御 | v2 撤回 |
| ~~P2′~~ | $x_t/x_s = C(G/B)$, q=1 → ダイヤ 15.4 | 死。死因は §1 の構造的論証。v4 の数値棄却は訂正② |
| **P2″** | $x_t/x_s$ はほぼ普遍（≈2）。$B$ は主要項に入らない | **強化**（§1、[C] 自身の $\sigma=2G(e_{xx}-e_{yy})$） |
| **P3** | 集中度は $W_{\rm dev}/W_{\rm vol}=[1/(2G/B)]\langle s{:}s\rangle/\langle p^2\rangle$ | 維持。**唯一の未占有地**（両論文とも diamond/Si/Pugh に触れない） |
| ~~P4~~ | 回転シェアは R と共に増大 | **死**（§3、[L] 逐語） |
| ~~P4′~~ | 回転シェアは TD が支配 | **死**（§3、形状は変わるのに γ/R は不変） |
| ~~P5~~ | 残差は Zener 異方性 | **保留・ほぼ既占有**（Johnson et al., Nat. Mater. 7, 120 (2008) が題名そのまま） |
| **P6** | 法線チャンネルの飽和限界は BCT（$2\theta = 72°$、$k = 0.7265$） | **新規だが恒等式**（§2）。予言ではなく構造。[L] が既に持っている |
| **Q1** | [C] の分配と [L] の会計は同じ分割か | **未解決・最重要**（§3.1） |
| **Q2** | 偏心ディスクリネーションは必須か不要か | **未解決・未占有**（§4） |

**生き残っているのは P2″ と P3 の二つだけ**である。そして P3 が立つ場所は
「ダイヤモンド／Pugh」の一点に狭まった。

---

## 8. 次にやること

| 優先 | 文献 | 何が決まるか | 取得 |
|---|---|---|---|
| 1 | **[L] の図 2e・3・4b–d**（arXiv 2507.14781 の図） | **Q1**。プレプリントは取得済みなので図の数値読み取りが次の作業 | 済（本文）／図は要精読 |
| 2 | **Johnson et al., Nat. Mater. 7, 120 (2008)** | P5 が既占有か。異方性の話を続けてよいか | 有料 |
| 3 | **Wu, Yu, Zhu et al., Acta Cryst. B 77, 93 (2021)** | Yu グループの金での主張。P3 の橋の相手側 | 要入手 |
| 4 | **Gryaznov et al., Cryst. Res. Technol. 34, 1091 (1999)** | **Q2** の元の主張 | 要入手 |
| 5 | [C] の SI（figs. S1–S25, table S1） | S18/table S1 のゆらぎのサイズ依存、S19–S20 の TD 依存数値 | Sci. Adv. は OA |
| 6 | Zenodo 10.5281/zenodo.17156384 | [C] の生データ。TD 系列の分配が直接取れる可能性 | 公開 |
| 7 | Patala, Marks, Olvera de la Cruz, JPCC 117, 1485 (2013) | エネルギー分配（P1 再定式化の表面項） | 要入手 |
| 8 | Yu et al. 2017 本文 | P3 の定量化 | ryu@tsinghua.edu.cn |

補足：同グループの **Shi, Cheng, Leonardi, Yang, Engel, Jones, Han,
*Preserving surface strain in nanocatalysts via morphology control*,
Sci. Adv. 10, eadp3788 (2024)**（[C] ref 30）は完全 OA。形態によるひずみ制御そのもの。

---

## 9. 方法論の記録

P2 は四回、P1 と P4 はそれぞれ一回、一次データで死んだ。今回の教訓：

1. **要旨と断片では足りない。** [C] の支配方程式は Methods の最後にしかなく、
   「サイズではなく形状」という主要結果は要旨に一行もない。
   [L] の $k = \tan\theta$ という恒等式も、サイズ独立性の明言も、要旨にはない。
2. **参考文献リストは自分の思いつきの着地点を最速で確認できる場所。**
   v4 で「新規」と書いた異方性の話は、[C] の ref 22（2008 年 Nature Materials）が
   題名そのままやっていた。
3. **プレプリントを探す。** [L] は Wiley で 403 だったが arXiv 2507.14781 が
   全文公開されていた。DOE 資金（DE-SC0024064）→ OSTI → arXiv の経路で見つかった。
   **有料誌で止まったら、資金源から遡る。**
4. **二点あれば指数が決まる、は誤り。** 正しい問いは「その二点は同じ量を
   測っているか」だった（訂正②）。
5. **急いで和解させない。** v4 §3 の Cheng–Lin 和解は、[L] 本文で一行に否定された。
   §3.1 の Q1 を、今回は空白のまま置く。
