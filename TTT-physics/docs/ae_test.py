"""
Test (A): does the TTT fixed-vocabulary alpha survive the electron a_e test?
alpha^-1(TTT) = 136395767/995328  (exact rational)
"""
from fractions import Fraction as F
from scipy.optimize import brentq

# ---------- QED coefficients (Aoyama-Kinoshita-Nio, Atoms 7 (2019) 28) ----------
A1_2  = 0.5
A1_4  = -0.328478965579193378
A1_6  =  1.181241456587
A1_8  = -1.9122457649264
A1_10_AHKN   = 6.737   ; A1_10_AHKN_e   = 0.159   # AHKN 2018 revised
A1_10_VOLKOV = 5.891   ; A1_10_VOLKOV_e = 0.061   # Volkov 2024, PRD 110 036001

A2_4_mu  =  5.19738667e-7 ; A2_4_tau  =  1.83790e-9
A2_6_mu  = -7.37394162e-6 ; A2_6_tau  = -6.5830e-8 ; A3_6 = 1.909e-13
A2_8_mu  =  9.1617e-4     ; A2_8_tau  =  7.429e-6
A2_10_mu = -0.00382

A_HAD = 1.693e-12 ; A_HAD_e = 0.012e-12          # hadronic
A_EW  = 0.03053e-12; A_EW_e  = 0.00023e-12       # electroweak

PI = 3.14159265358979323846

def coeffs(A1_10):
    return [
        A1_2,
        A1_4  + A2_4_mu  + A2_4_tau,
        A1_6  + A2_6_mu  + A2_6_tau + A3_6,
        A1_8  + A2_8_mu  + A2_8_tau,
        A1_10 + A2_10_mu,
    ]

def a_e_theory(alpha, A1_10):
    x = alpha/PI
    return sum(c*x**(n+1) for n, c in enumerate(coeffs(A1_10))) + A_HAD + A_EW

# ---------- inputs ----------
AE_EXP, AE_EXP_E = 1.15965218059e-3, 0.00000000013e-3   # Fan et al. PRL 130, 071801 (2023)
TTT = F(136395767, 995328)
ainv_TTT = float(TTT)

DETERMS = {
    "a_e + QED (AHKN 2018)   ": (137.0359991663, 0.0000000155),
    "a_e + QED (Volkov 2024)  ": (137.0359991595, 0.0000000155),
    "CODATA 2022              ": (137.035999177,  0.000000021),
    "CODATA 2018              ": (137.035999084,  0.000000021),
    "Cs recoil (Parker 2018)  ": (137.035999046,  0.000000027),
    "Rb recoil (Morel 2020)   ": (137.035999206,  0.000000011),
}

print("alpha^-1 (TTT, exact) =", TTT, "=", repr(ainv_TTT))
print()

# ---------- self-check: does our series reproduce the published extraction? ----------
print("=== 0. coefficient-table self-check (invert the series for alpha) ===")
for lbl, A10 in (("AHKN 2018 ", A1_10_AHKN), ("Volkov 2024", A1_10_VOLKOV)):
    f = lambda a: a_e_theory(a, A10) - AE_EXP
    a = brentq(f, 1/138., 1/136., xtol=1e-22, rtol=1e-15)
    pub = DETERMS["a_e + QED (%s)   " % "AHKN 2018" if "AHKN" in lbl else "a_e + QED (Volkov 2024)  "][0]
    print(f"  {lbl}: our alpha^-1 = {1/a:.10f}   published = {pub:.10f}   diff = {1/a-pub:+.2e}")
print()

# ---------- forward test ----------
print("=== 1. FORWARD: a_e computed from the TTT alpha ===")
alpha_TTT = 1.0/ainv_TTT
for lbl, A10, A10e in (("AHKN 2018 ", A1_10_AHKN, A1_10_AHKN_e),
                       ("Volkov 2024", A1_10_VOLKOV, A1_10_VOLKOV_e)):
    ae = a_e_theory(alpha_TTT, A10)
    # theory uncertainty: A1^(10) + hadronic + EW
    s_th = ((A10e*(alpha_TTT/PI)**5)**2 + A_HAD_e**2 + A_EW_e**2)**0.5
    d  = ae - AE_EXP
    s  = (AE_EXP_E**2 + s_th**2)**0.5
    print(f"  {lbl}: a_e(theory) = {ae:.14e}")
    print(f"              a_e(exp)    = {AE_EXP:.14e}   diff = {d:+.3e}")
    print(f"              sigma_exp = {AE_EXP_E:.2e}  sigma_theory = {s_th:.2e}  total = {s:.2e}"
          f"   -> {abs(d)/s:.2f} sigma")
print()

# ---------- inverse test ----------
print("=== 2. INVERSE: the TTT rational vs every alpha determination ===")
for lbl,(v,e) in DETERMS.items():
    d = ainv_TTT - v
    print(f"  {lbl}  {v:.9f}({int(round(e*1e9)):2d})   diff = {d:+.3e}   -> {abs(d)/e:5.2f} sigma"
          f"   {'consistent' if abs(d)/e < 2 else ('tension' if abs(d)/e < 5 else 'EXCLUDED')}")
print()

# ---------- equivalence of the two routes ----------
print("=== 3. are the two routes independent? (sensitivity) ===")
ae0 = a_e_theory(alpha_TTT, A1_10_VOLKOV)
h = alpha_TTT*1e-9
dlog = (a_e_theory(alpha_TTT+h, A1_10_VOLKOV)-a_e_theory(alpha_TTT-h, A1_10_VOLKOV))/(2*h)*alpha_TTT/ae0
print(f"  d ln a_e / d ln alpha = {dlog:.6f}   (exactly 1 would mean a_e carries no information beyond alpha)")
v,e = DETERMS["a_e + QED (Volkov 2024)  "]
rel = (ainv_TTT - v)/v
print(f"  predicted forward shift  delta a_e = -a_e * {dlog:.4f} * {rel:.3e} = {-ae0*dlog*rel:+.3e}")
print(f"  measured forward shift                                            = {ae0-AE_EXP:+.3e}")
print(f"  sigma from forward route = {abs(ae0-AE_EXP)/AE_EXP_E:.2f},  from inverse route = {abs(ainv_TTT-v)/e:.2f}")

# ---------- 4. when does this test become lethal? ----------
print()
print("=== 4. required measurement precision for 5-sigma exclusion ===")
def s_ainv(s_ae): return ainv_TTT*s_ae/AE_EXP
print(f"  current sigma(alpha^-1) from a_e = {s_ainv(AE_EXP_E):.3e}")
for name in ("a_e + QED (Volkov 2024)  ", "a_e + QED (AHKN 2018)   ", "Rb recoil (Morel 2020)   "):
    v,_ = DETERMS[name]
    d = abs(ainv_TTT-v); need = d/5.0
    print(f"  vs {name}: need sigma(a_e) <= {AE_EXP_E*need/s_ainv(AE_EXP_E):.2e}"
          f"  (measurement must improve x{s_ainv(AE_EXP_E)/need:.2f})")
s_th = ((A1_10_VOLKOV_e*(alpha_TTT/PI)**5)**2 + A_HAD_e**2 + A_EW_e**2)**0.5
print(f"  theory floor: sigma_th(a_e)={s_th:.2e} -> sigma(alpha^-1)={s_ainv(s_th):.2e}"
      f"  => a perfect measurement would judge at {abs(ainv_TTT-137.0359991595)/s_ainv(s_th):.1f} sigma")
