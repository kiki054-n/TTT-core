Theme 2: 17粒子の統一的質量階層と Python 実装（docs/02_standard_model_17_particles.md）

標準模型の全 17 基本粒子の質量比（$m_i / m_e$）を統一的に代数化し、実験値（PDG/CODATA）と比較検証する計算プログラム。

レプトン系: $\alpha$ 展開および小出の公式（Koide Relation: $\theta_k = 2\pi/9$）による位相角解。

クォーク系: 色荷（$N_c=3$）の空間曲率（$6\pi^3, 6\pi^5, \alpha^{-2}$）および $\alpha_s$ 摂動展開。

ボソン系: 電弱真空期待値スケール $v/m_e \approx 4.8 \times 10^5$ と弱混合角 $\theta_W$ による拘束。

実装コード
計算スクリプトは src/ttt_17_mass_ratios.py に収録（Python 3 標準ライブラリのみで動作）。
