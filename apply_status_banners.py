#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_status_banners.py -- TTT-core の各文書に「状態バナー」を挿入する

方針:
  - ファイルは移動しない（2026-09-06 に cnt34 を再編したとき内部リンクが60本壊れた）
  - 本文は一文字も変えない（PROOF_STATUS.md §27「後から黙って直さない」）
  - 冒頭に4行のバナーを足すだけ
  - 冪等（既にバナーがあるファイルはスキップ）

用法: python3 apply_status_banners.py [リポジトリのルート]
"""

import sys
import os

MARK = "<!-- TTT-STATUS v1 -->"
DATE = "2026-09-08"
REF = "`TTT-physics/docs/TTT_CORE.md` / `TTT-physics/docs/PROOF_STATUS.md` / `STATUS.md`"

# path -> (段, 判定の一行)
#   A = 核（水準A、機械検証済み） / 監査 = 判定の記録
#   F = 反証済み / C = 仮説・未検定 / U = 未判定
J = {
 # ---------------- 核 ----------------
 "TTT-physics/docs/TTT_CORE.md": ("A",
   "構成の鎖 S1-S7。置いた仮定は公理Zのみ、他は全て定理または強制。ttt_core_verify.py で機械検証できる。"),

 # ---------------- 監査の記録 ----------------
 "TTT-physics/docs/PROOF_STATUS.md": ("監査",
   "22項目の証明状況と判定水準の記録。理論そのものではなく、理論に対する判定の記録である。"),
 "TTT-physics/docs/ttt_definition_ledger.md": ("監査",
   "用語・数え方・境界規則の台帳。確定/棄却/未決の対応表を含む。"),
 "TTT-physics/docs/REFERENCES.md": ("監査",
   "出典と帰属文の一覧。✓は一次情報照合済み、△は未照合、※は査読なし。"),

 # ---------------- 反証済み（F） ----------------
 "TTT-physics/INDEX.md": ("F",
   "本文の中心的主張は判定済み。(1)「自由パラメータを持たない厳密解モデル」は成立しない"
   "（2026-09-06 の監査で17質量に対し最低9個の手置き数）。(2) ヒッグスの 0.00σ は旧値 125.25±0.17 "
   "に対するもので、PDG2025 の 125.20±0.11 では 0.45σ、かつ 125.25 は較正点であって予言ではない。"
   "(3) m_p/m_e = 3×4×153 は 1836 の因数分解（153 = 1836/12）であり、実測 1836.152673426(32) に対し約 477万σ。"
   "(4) 1/α の式は手置き数 4.6 と 1.15 を含む。"),
 "TTT-physics/higgs_mass_derivation.md": ("F",
   "125.25 GeV は較正点であって予言ではない（2026-09-07 に確定）。"
   "「0.00σ」は標的と予言が同一値であることの言い換えで、しかも参照値が旧版。PDG2025 では 0.45σ。"),
 "TTT-physics/proton_electron_ratio_derivation.md": ("F",
   "標的 m_p/m_e = 1836.152673426(32) は整数ではない。1836 との差は約 477万σ。"
   "3×4×153 は 1836 の因数分解であって導出ではない（153 = 1836/12）。"),
 "TTT-physics/codata_comparison.md": ("F",
   "「完全一致」「0.00σ」の行を含む。実験誤差より細かい一致は強い結果ではなく、検定されていない結果である"
   "（PROOF_STATUS §8 項目8）。参照値の版と日付を各行に付す必要がある。"),
 "TTT-mathematics/golden_ratio_proofs.md": ("F",
   "§1 の根の取り違え（x²+x−1=0 の正の解は 0.618… = 1/φ であって φ ではない）と "
   "§5 の最適化（唯一解は x = 1/2）を、2026-09-01 に指摘して以降 未修正のまま。"),
 "TTT-mathematics/fibonacci_and_6d_equation.md": ("C",
   "収束の証明が不完全。「極限 r = lim r_n が存在すると仮定すると」で存在を仮定している（M12、2026-09-06）。"
   "修正は容易で、r_{n+1} = 1 + 1/r_n が縮小写像であることを示せばよい。"
   "また「6次元方程式の自己相似条件 x = 1 + 1/x と同型」という接続は、公理6そのものが黄金比の方程式であるため"
   "内容を加えない（M10）。なお φ は正二十面体・正十二面体族の数であり、TTT_CORE の正四面体・立方体族"
   "（R/r = 3）からは出てこない。"),
 "TTT-mathematics/geometry_and_solution_space.md": ("F",
   "「Σv=0 を満たす有限点系は5種」は成立しない。任意の中心対称点系がこれを満たす（M11、2026-09-06）。"),
 "TTT-physics/geometry_and_solution_space_1.md": ("F",
   "TTT-mathematics/geometry_and_solution_space.md の重複。判定は同じ（M11）。どちらか一方を残すこと。"),
 "TTT-physics/Topological Field Theory & Geometric Mass Derivation Framework/docs/Unified Geometric Table .md": ("F",
   "G1: 「m_s, m_c, m_b, m_t を再現」は成立せず、17粒子中7つが 55〜99% 外れる（同梱の "
   "src/ttt_17_mass_ratios.py を無改変で実行して確認、2026-09-06）。"
   "G5: 「自由パラメータなし」は不成立、最低9個の手置き数。"
   "G6: 8節中6節（A・C・D・E・F・G）は既存文献の要約で TTT 由来ではない。出典明記が必要。"),

 # ---------------- 仮説・未検定（C） ----------------
 "TTT-physics/fine_structure_derivation.md": ("C",
   "1/α の展開式は手置き数（4.6, 1.15）を含み、帰無対照を通していない。"
   "2026-09-02 の対照では、この種の語彙で2桁値への到達率は 26.4%。"
   "また α は走る量であり、どのスケールの α を狙うのかの明示が必要。"),
 "TTT-physics/fine_structure_derivation_1.md": ("C",
   "fine_structure_derivation.md の重複（15620 B / 15832 B）。判定は同じ。どちらが正なのかを決めること。"),
 "TTT-physics/neutron_proton_splitting_derivation.md": ("C",
   "Δm_np の式は係数を複数手置きしている。帰無対照を通していない。"),
 "TTT-physics/running_alpha_prediction.md": ("C",
   "α の走りの取り扱いは方向として正しいが、β関数のステップ Δb₁ = 1.5 の根拠が未提示。"),
 "TTT-physics/experimental_predictions.md": ("C",
   "予言されている 2197 / 2744 / 3375 GeV はそれぞれ 13³ / 14³ / 15³ である。"
   "立方数の列を GeV と読む換算則（O1）が未定のため、現状では検定にかけられない。"),
 "TTT-physics/falsifiability_criteria.md": ("C",
   "反証条件の多くが理論の内側で閉じている（2026-09-06 の監査）。"
   "反証条件は理論の外側の事実でなければならない。PROOF_STATUS v2.1 §0 の書き換え済みの形を参照。"),
 "TTT-mathematics/Axiomatization of 6-Dimensional Equations (First Edition).md": ("C",
   "「黄金比の導出」は代数としては正しいが、公理6そのものが黄金比の方程式であり内容がない（M10、2026-09-06）。"),
 "TTT-mathematics/golden_ratio_from_6d_equation.md": ("C",
   "φ は正二十面体・正十二面体族の数であり、TTT_CORE の構成（正四面体・立方体族、R/r = 3）からは出てこない。"
   "入れ子のスケール比を 3 とするか φ とするかは二者択一。"),
 "TTT-mathematics/fractal_dimension_and_6d_equation.md": ("C",
   "log3/logφ 等の根拠が未提示（M13、2026-09-06）。"),
 "TTT-mathematics/6次元幾何状態空間における基準遷移演算子と Lie 環.md": ("C",
   "M1/M2 は再現できる（水準A）。ただし M3・M4（λ=1 の三重解と9次元閉合）は乱数4ベクトルでも再現される構成の産物、"
   "M5（rank-1 優位 99.64%）は乱数対照 77.9〜98.3% の中、"
   "M6（歪み/旋回比 2.256）は単位依存で不変量ではない。無次元化規約を先に定めれば修理可能。"),
 "TTT-physics/Topological Field Theory & Geometric Mass Derivation Framework/src/ttt_17_mass_ratios.py": ("C",
   "実装の誤り。v_ratio の式 (1/(α√2π))·6π³ の返り値は 5738 で、コメントの 481450 と 84 倍食い違う。"
   "このため W・Z・H が揃って −99.12% 外れる。修正版は ttt_mass_refit_test.py を参照。"),

 # ---------------- 未判定（U） ----------------
 "README.md": ("U",
   "リポジトリの入口。1836 と 137.03… を看板に掲げているが、どちらも判定済みである（STATUS.md 参照）。"
   "書き換えの優先度は最も高い。"),
 "TTT-physics/readme.md": ("U", "個別監査は未了。125.25 と 1836 への言及を含む。"),
 "TTT-physics/TTT-physics.md": ("U", "個別監査は未了。"),
 "TTT-physics/TTT‑physics v3 .md": ("U",
   "個別監査は未了。ファイル名に非ASCIIのハイフン（U+2011）と末尾空白が含まれており、リンクが張れない。"),
 "TTT-physics/POLYHEDRAL_TRANSITION_6D.md": ("U",
   "個別監査は未了。『Polyhedral Transition and Hidden 6D State.md』とほぼ同内容（13740 B / 13743 B）。"),
 "TTT-physics/Polyhedral Transition and Hidden 6D State.md": ("U",
   "個別監査は未了。POLYHEDRAL_TRANSITION_6D.md とほぼ同内容。どちらが正かを決めること。"),
 "TTT-physics/Polyhedral Transition — Strict Numerical Definition.md": ("U", "個別監査は未了。"),
 "TTT-physics/TTT_6D_Observation_Matrix_Analysis.md": ("U", "個別監査は未了。137.03… 系の主張を含む。"),
 "TTT-physics/TTT_Alpha_Fine_Structure_Constant_Convergence.md": ("U", "個別監査は未了。137.03… 系の主張を含む。"),
 "TTT-physics/TTT_Polyhedra_Transition_Analysis.md": ("U",
   "個別監査は未了。「完全一致」の語を含む（PROOF_STATUS §8 項目8 を参照）。"),
 "TTT-paper/fin/Geometric-Topological Derivation of the Fine-Structure Constant via TTT 6D Polyhedral Dynamics.md": ("U",
   "個別監査は未了。137.03… 系の主張を含む。投稿前に fine_structure_derivation.md の判定（C）を反映すること。"),
 "TTT-mathematics/godel_nash_and_judicial_structure.md": ("U",
   "個別監査は未了。『godel_nash_and_judicial_structure.md .md』（末尾に空白＋.md）と重複している。"),
 "TTT-mathematics/godel_nash_and_judicial_structure.md .md": ("U",
   "ファイル名が壊れている（末尾に「 .md」が余分）。godel_nash_and_judicial_structure.md と重複。削除候補。"),
 "TTT-physics/Topological Field Theory & Geometric Mass Derivation Framework/docs/02_standard_model_17_particles.md": ("U",
   "個別監査は未了。「素粒子17種類」は物理の事実ではなく数え方の約束である"
   "（型なら17、W± を別に数えれば18、色電荷と反粒子込みで61、場の自由度で118/124）。"),
}

BANNER = """{mark}
> **状態**: {tier}{tier_note}
> **判定**: {verdict}
> **参照**: {ref}
> 本文は当時のまま。PROOF_STATUS.md §27「後から黙って直さない」による。（{date}）

"""

TIER_NOTE = {
    "A":    " — 核。TTT_CORE.md v1.0 の構成の鎖に含まれる",
    "監査": " — 判定の記録。理論そのものではない",
    "F":    "（反証済み） — この文書の主張は判定を受けている",
    "C":    "（仮説・未検定） — 検定を通っていない",
    "U":    "（未判定） — TTT_CORE.md v1.0 の鎖には含まれない",
}


def apply(root):
    added = skipped = missing = 0
    for rel, (tier, verdict) in sorted(J.items()):
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            print(f"  [欠] {rel}")
            missing += 1
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if MARK in text:
            print(f"  [済] {rel}")
            skipped += 1
            continue
        banner = BANNER.format(mark=MARK, tier=tier, tier_note=TIER_NOTE[tier],
                               verdict=verdict, ref=REF, date=DATE)
        if rel.endswith(".py"):
            body = "".join("# " + ln if ln.strip() else "#\n"
                           for ln in banner.splitlines(keepends=True))
            lines = text.splitlines(keepends=True)
            n = 0
            while n < len(lines) and (lines[n].startswith("#!") or "coding" in lines[n]):
                n += 1
            text = "".join(lines[:n]) + body + "".join(lines[n:])
        else:
            lines = text.splitlines(keepends=True)
            n = 1 if lines and lines[0].startswith("# ") else 0
            text = "".join(lines[:n]) + ("\n" if n else "") + banner + "".join(lines[n:])
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  [{tier:>2}] {rel}")
        added += 1
    print(f"\n挿入 {added} / スキップ {skipped} / 欠 {missing}")


if __name__ == "__main__":
    apply(sys.argv[1] if len(sys.argv) > 1 else ".")
