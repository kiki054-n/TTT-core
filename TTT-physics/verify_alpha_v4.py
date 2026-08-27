"""
verify_alpha_v4.py

TTT-physics: fine_structure_derivation.md セクション7「別系統の傍証」に
記載した Alpha-V4（正多面体頂点数による微細構造定数の数値的一致）を
独立に再現・検証するスクリプト。

出典: GTM_v2.1/Alpha-V4-Final.html
      (統合版: GTM_v2.1/GTM_v2.1_統合版.html)

注意: このスクリプトは「公理からの導出」を検証するものではなく、既知の
実測値へ事後的に一致する係数の組み合わせを数値的に再現しているだけである。
詳細は fine_structure_derivation.md セクション7.6「位置づけと限界」を参照。

参照値の出典:
  - CODATA 2018: 1/alpha = 137.035999084(21)
    (GTM_v2.1のオリジナル探索が基準にした値)
  - CODATA 2022: 1/alpha = 137.035999177(21)
    (現在の最新推奨値。NIST/CODATA, Wikipedia "Fine-structure constant")
  - PDG 2025: Higgs boson mass = 125.20 +/- 0.11 GeV
    (rpp2025-sum-gauge-higgs-bosons.pdf, world average)
"""

from fractions import Fraction

# ---- 正多面体の頂点数 ----------------------------------------------------
V4, V6, V8, V12, V20 = 4, 6, 8, 12, 20

# ---- 有効頂点数 Veff = V4 + V12/V20 --------------------------------------
V_EFF = Fraction(V4) + Fraction(V12, V20)          # 23/5 = 4.6
assert V_EFF == Fraction(23, 5)

# ---- 透過の基底 2^(V6+1) --------------------------------------------------
BASE = 2 ** (V6 + 1)                                # 128
assert BASE == 128

# ---- 参照値 ---------------------------------------------------------------
ALPHA_INV_CODATA_2018 = 137.035999084
ALPHA_INV_CODATA_2018_UNCERTAINTY = 0.000000021  # 末尾2桁 "21"

ALPHA_INV_CODATA_2022 = 137.035999177
ALPHA_INV_CODATA_2022_UNCERTAINTY = 0.000000021  # 末尾2桁 "21"

HIGGS_MASS_PDG_2025_GEV = 125.20
HIGGS_MASS_PDG_2025_UNCERTAINTY_GEV = 0.11


def alpha_inv_series():
    """段階的な級数 v1 -> v4 を Fraction で厳密計算し、Fraction値の辞書で返す。"""
    v1 = Fraction(125) + V12
    v2 = v1 + V_EFF / BASE
    v3 = v2 + Fraction(1, BASE**2)
    v4 = v3 + (V_EFF / V4) / BASE**3
    return {"v1": v1, "v2": v2, "v3": v3, "v4": v4}


def higgs_mass_gev():
    return Fraction(5**3) + Fraction(V12 + V20, BASE)  # 125 + 32/128 = 125.25


def report():
    terms = alpha_inv_series()
    print("=== 1/alpha 段階的近似 (v1 -> v4) — 2018年CODATA基準 ===")
    for name, value in terms.items():
        fv = float(value)
        err = abs(fv - ALPHA_INV_CODATA_2018)
        print(f"{name}: {fv:.15f}   誤差 = {err:.3e}")

    v4 = float(terms["v4"])
    print()
    print("=== v4 の CODATA 2018 vs 2022 での評価 ===")
    for label, ref, unc in [
        ("CODATA 2018", ALPHA_INV_CODATA_2018, ALPHA_INV_CODATA_2018_UNCERTAINTY),
        ("CODATA 2022", ALPHA_INV_CODATA_2022, ALPHA_INV_CODATA_2022_UNCERTAINTY),
    ]:
        err = abs(v4 - ref)
        sigma = err / unc
        within = err <= unc
        print(f"{label}: 1/alpha = {ref} +/- {unc}")
        print(f"  v4との誤差 = {err:.3e}  ({sigma:.2f}σ)  不確かさ以内: {within}")

    print()
    print("=== ヒッグス質量 (同一の V4,V12,V20 のみを使用) ===")
    m_h = float(higgs_mass_gev())
    diff = abs(m_h - HIGGS_MASS_PDG_2025_GEV)
    sigma_h = diff / HIGGS_MASS_PDG_2025_UNCERTAINTY_GEV
    print(f"m_H (TTT, 厳密値) = {m_h} GeV")
    print(f"m_H (PDG 2025)    = {HIGGS_MASS_PDG_2025_GEV} +/- {HIGGS_MASS_PDG_2025_UNCERTAINTY_GEV} GeV")
    print(f"差 = {diff:.3f} GeV ({sigma_h:.2f}σ)")


if __name__ == "__main__":
    report()
