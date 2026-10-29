#!/usr/bin/env python3
"""
verify_navel_tetra.py
Machine verification for:
  "Navel-Tetra Lattice-Occupancy Model: Nucleon, Electron and Higgs Mass Ratios"
  Kawakami Naoyuki (川上真潔), 2026-10-29

Every number quoted in the paper is recomputed here and fixed with an assert.
Inputs: CODATA 2022 mass ratios, PDG 2025 Higgs mass, NIST/CODATA thermochemistry.
Run:  python3 verify_navel_tetra.py
License: MIT
"""
from fractions import Fraction as F
import math

PASS = []
def check(name, cond):
    assert cond, name
    PASS.append(name)

# ---------------------------------------------------------------------------
# Measured inputs
# ---------------------------------------------------------------------------
MP_ME = 1836.152673426      # CODATA 2022, proton/electron mass ratio
MN_ME = 1838.68366200       # CODATA 2022, neutron/electron mass ratio
MA_ME = 7294.29954171       # CODATA 2022, alpha (He-4 nucleus)/electron mass ratio
ME_MEV = 0.51099895069      # CODATA 2022, electron mass energy [MeV]
MH_GEV, MH_ERR = 125.20, 0.11   # PDG 2025 world average (error incl. scale factor 1.4)
MH_ATLAS, MH_ATLAS_ERR = 125.11, 0.11
MH_CMS, MH_CMS_ERR = 125.38, 0.14
MH_OLD = 125.25             # PDG 2022/2023 average (+-0.17)

# ---------------------------------------------------------------------------
# Block 1: generation counts vs. cubic capacities (lattice wall)
# ---------------------------------------------------------------------------
gens = [2 * 3**n for n in range(5)]          # 2, 6, 18, 54, 162
caps = [(n + 1)**3 for n in range(5)]        # 1, 8, 27, 64, 125
check("B1 births = 2,6,18,54,162", gens == [2, 6, 18, 54, 162])
check("B1 capacities = 1,8,27,64,125", caps == [1, 8, 27, 64, 125])
overflow_index = [n for n in range(1, 5) if gens[n] > caps[n]]
check("B1 first overflow after genesis is at 5^3", overflow_index == [4])
OVER = gens[4] - caps[4]
check("B1 overflow = 37", OVER == 37)
check("B1 37 = 4^3 - 3^3", OVER == 4**3 - 3**3)
check("B1 spare at 4^3 = 10", caps[3] - gens[3] == 10)
# 125 decompositions and the cube identity
check("B1 3^3+4^3+5^3 = 6^3", 27 + 64 + 125 == 216)
check("B1 91 = 3^3+4^3 = 6^3-5^3 = 7*13", 27 + 64 == 91 == 216 - 125 == 7 * 13)
check("B1 shell of 125 = 98", 125 - 27 == 98)
check("B1 108 midpoint of 91 and 125, = 6^3/2", (91 + 125) // 2 == 108 == 216 // 2)
check("B1 17 + 17 + 91 = 125", 91 + 2 * 17 == 125)
check("B1 37 = 34 + 3", OVER == 34 + 3)

# ---------------------------------------------------------------------------
# Block 2: compression factor from the central quarter cell
# ---------------------------------------------------------------------------
lam = F(501, 500)                 # (125 + 1/4)*4 / (125*4)
check("B2 (125+1/4)*4 = 501", (F(125) + F(1, 4)) * 4 == 501)
check("B2 lambda = 501/500", lam == F(125 * 4 + 1, 125 * 4))

# ---------------------------------------------------------------------------
# Block 3: nucleon/electron mass ratio
#   m_N/m_e = 125*16 - [125*lam^2 + 34*lam + 3]
# ---------------------------------------------------------------------------
compressed = 125 * lam**2 + 34 * lam + 3
mN_model = 125 * 16 - compressed
mN_model_f = float(mN_model)
mN_meas = (MP_ME + MN_ME) / 2
check("B3 compressed 162 -> 162.5685", abs(float(compressed) - 162.5685) < 1e-9)
check("B3 m_N/m_e (model) = 1837.4315", abs(mN_model_f - 1837.4315) < 1e-9)
dev_N = (mN_model_f - mN_meas) / mN_meas
check("B3 nucleon mean deviation ~ +0.0007%", 0.6e-5 < dev_N < 0.8e-5)

# Intermediate readings (for the record)
all_two = 125 * 16 - 162 * lam**2
three_free = 125 * 16 - (159 * lam**2 + 3)
check("B3 all-two-stage reading -0.0036%", abs((float(all_two) - mN_meas) / mN_meas + 3.6e-5) < 0.2e-5)
check("B3 3-uncompressed reading -0.0030%", abs((float(three_free) - mN_meas) / mN_meas + 3.0e-5) < 0.2e-5)

# ---------------------------------------------------------------------------
# Block 4: proton / neutron split  (n - p = m_e + (5/3) u,  u = m_N/2000)
# ---------------------------------------------------------------------------
u = mN_model_f / 2000            # model unit in electron masses
delta = 1 + (5 / 3) * u
mp_model = mN_model_f - delta / 2
mn_model = mN_model_f + delta / 2
check("B4 u = 0.918716 m_e", abs(u - 0.918716) < 1e-6)
check("B4 n-p model 2.53119 vs meas 2.53099",
      abs(delta - 2.531193) < 1e-5 and abs((MN_ME - MP_ME) - 2.530989) < 1e-5)
dev_p = (mp_model - MP_ME) / MP_ME
dev_n = (mn_model - MN_ME) / MN_ME
check("B4 proton +0.0007%", 0.6e-5 < dev_p < 0.8e-5)
check("B4 neutron +0.0007%", 0.6e-5 < dev_n < 0.8e-5)

# Q value of free-neutron beta decay
Q_meas_me = MN_ME - MP_ME - 1                      # in m_e
Q_meas_mev = Q_meas_me * ME_MEV
check("B4 Q_beta = 0.78233 MeV", abs(Q_meas_mev - 0.782333) < 1e-5)
Q_in_proton_units = Q_meas_me / (MP_ME / 2000)
check("B4 Q in proton/2000 units = 1.6676 ~ 5/3 (0.06%)",
      abs(Q_in_proton_units - 1.66758) < 1e-4 and abs(Q_in_proton_units / (5 / 3) - 1) < 7e-4)

# twist accounting: icosahedron -> pentagonal bipyramid, measured in triangular-bipyramid units
ico = dict(V=12, F=20, E=30); pbp = dict(V=7, F=10, E=15); tbp = dict(V=5, F=6, E=9)
check("B4 Euler V-E+F=2 for all three", all(d["V"] - d["E"] + d["F"] == 2 for d in (ico, pbp, tbp)))
released = {k: ico[k] - pbp[k] for k in ico}
check("B4 released twist band = (5,10,15)", released == dict(V=5, F=10, E=15))
check("B4 released/triangle-unit = 5/3 for V(per 3), F, E",
      F(released["V"], 3) == F(released["F"], tbp["F"]) == F(released["E"], tbp["E"]) == F(5, 3))

# ---------------------------------------------------------------------------
# Block 5: helium-4
#   M_alpha/m_e = 2 m_p + 2 m_n - (60 u + 1/4)
# ---------------------------------------------------------------------------
B_meas_me = 2 * MP_ME + 2 * MN_ME - MA_ME
B_meas_mev = B_meas_me * ME_MEV
check("B5 He-4 binding = 28.2957 MeV", abs(B_meas_mev - 28.29566) < 2e-4)
frac = B_meas_me / (2 * MP_ME + 2 * MN_ME)
check("B5 binding fraction 0.7534%", abs(frac * 100 - 0.75341) < 1e-4)
check("B5 60 = 3 tetra x 5 x 4", 3 * 5 * 4 == 60 and 20 * 3 == 12 * 5 == 60)
B_model_60 = 60 * u
deficit = B_meas_me - B_model_60
check("B5 deficit in m_e ~ 0.250 (= 2/8)", abs(deficit - 0.25) < 0.003)
Ma_model = 2 * mp_model + 2 * mn_model - (60 * u + 0.25)
dev_a = (Ma_model - MA_ME) / MA_ME
check("B5 He-4 model 7294.353, +0.0007%", abs(Ma_model - 7294.353) < 0.01 and 0.6e-5 < dev_a < 0.8e-5)

# electron-scale deviation is per nucleon (independent of nucleus)
dev_e_he = 7940 / MA_ME
dev_e_N = 2000 / mN_meas
check("B5 2000/m_N = 1.08848 and 7940/M_alpha = 1.08852", abs(dev_e_N - 1.08848) < 1e-5 and abs(dev_e_he - 1.08852) < 1e-5)
check("B5 162 = 125 + 37", 125 + OVER == 162)

# ---------------------------------------------------------------------------
# Block 6: Higgs / electron
#   m_H/m_e = (125*8 - 20)(125*16)/8 = 245000
# ---------------------------------------------------------------------------
ratio_H = F((125 * 8 - 20) * (125 * 16), 8)
check("B6 m_H/m_e = 245000", ratio_H == 245000)
mH_pred = 245000 * ME_MEV / 1000
check("B6 m_H prediction 125.1947 GeV", abs(mH_pred - 125.19474) < 1e-5)
pulls = {k: (mH_pred - v) / e for k, (v, e) in
         {"PDG2025": (MH_GEV, MH_ERR), "ATLAS2023": (MH_ATLAS, MH_ATLAS_ERR), "CMS2020": (MH_CMS, MH_CMS_ERR)}.items()}
check("B6 pulls -0.05, +0.77, -1.32 sigma",
      abs(pulls["PDG2025"] + 0.048) < 0.01 and abs(pulls["ATLAS2023"] - 0.770) < 0.01 and abs(pulls["CMS2020"] + 1.323) < 0.01)
meas_ratio = MH_GEV * 1000 / ME_MEV
check("B6 measured m_H/m_e = 245010", abs(meas_ratio - 245010.3) < 1)
check("B6 alternative (centre-quarter) reading 125.25 differs by 55 MeV", abs((MH_OLD - mH_pred) * 1000 - 55.26) < 0.1)

# ---------------------------------------------------------------------------
# Block 7: chemistry (qualitative appendix) -- standard enthalpies, kJ/mol, 298 K
# ---------------------------------------------------------------------------
dHf = {"C(g)": 716.68, "H(g)": 217.998, "CH4": -74.87, "C2H4": 52.47, "C2H2": 226.73, "C2H6": -84.0}
at = {
    "CH4": dHf["C(g)"] + 4 * dHf["H(g)"] - dHf["CH4"],
    "C2H4": 2 * dHf["C(g)"] + 4 * dHf["H(g)"] - dHf["C2H4"],
    "C2H2": 2 * dHf["C(g)"] + 2 * dHf["H(g)"] - dHf["C2H2"],
    "C2H6": 2 * dHf["C(g)"] + 6 * dHf["H(g)"] - dHf["C2H6"],
}
ne = {"CH4": 10, "C2H4": 16, "C2H2": 14, "C2H6": 18}
per_e = {k: at[k] / ne[k] for k in at}
r_CH4 = per_e["CH4"] / per_e["C2H2"]
r_C2H4 = per_e["C2H4"] / per_e["C2H2"]
check("B7 per-electron CH4/C2H2 = 1.418 (sqrt2 +0.25%)", abs(r_CH4 - 1.4177) < 2e-3)
check("B7 per-electron C2H4/C2H2 = 1.200", abs(r_C2H4 - 1.2000) < 1e-3)
# sigma : average pi from average bond enthalpies (two textbook sets)
for s, d, t in [(347, 614, 839), (346, 602, 835)]:
    pi_avg = (t - s) / 2
    check(f"B7 pi_avg/sigma ~ 1/sqrt2 for set {s}", abs(pi_avg / s - 1 / math.sqrt(2)) < 3e-3)
# diamond vs graphite, silicon
graphite, diamond = 716.68, 716.68 - 1.895
check("B7 graphite/diamond cohesive ratio 1.00265", abs(graphite / diamond - 1.00265) < 2e-5)
for si in (450.0, 452.7):
    check(f"B7 C/Si cohesive ratio {si}", 1.57 < diamond / si < 1.59)

print(f"All {len(PASS)} checks passed.")
print()
print(f"m_N/m_e model {mN_model_f:.4f}  meas {mN_meas:.4f}  dev {dev_N*100:+.5f}%")
print(f"m_p/m_e model {mp_model:.4f}  meas {MP_ME:.4f}  dev {dev_p*100:+.5f}%")
print(f"m_n/m_e model {mn_model:.4f}  meas {MN_ME:.4f}  dev {dev_n*100:+.5f}%")
print(f"M_a/m_e model {Ma_model:.4f}  meas {MA_ME:.4f}  dev {dev_a*100:+.5f}%")
print(f"m_H pred {mH_pred:.5f} GeV ; pulls {pulls}")
print(f"Q_beta {Q_meas_mev:.6f} MeV = {Q_in_proton_units:.5f} (proton/2000) vs 5/3")
print(f"He-4 binding {B_meas_mev:.4f} MeV, deficit vs 60u = {deficit:.4f} m_e")
print(f"per-electron atomization: { {k: round(v, 2) for k, v in per_e.items()} }")
