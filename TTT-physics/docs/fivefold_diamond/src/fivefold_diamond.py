"""
Condensed-matter track: quantifying the 5-fold twin predictions for diamond.
Uses ONLY published elastic constants + the exact geometric deficit.
Block 1: the exact identity (re-verify)
Block 2: direction-dependent E and G for the actual 5-fold crystallography
Block 3: isotropic disclination energy density  (re-verify 2026-09-11)
Block 4: crossover radius R*, parametric in gamma_tb
Block 5: the cross-material prediction  R*(diamond) / R*(Au)
"""
import math, itertools, numpy as np
np.set_printoptions(precision=5, suppress=True)

print("="*78); print("BLOCK 1 — the exact geometric deficit"); print("="*78)
dih = math.degrees(math.acos(1/3))
defic = 360 - 5*dih
per   = 72 - dih
tet   = math.degrees(math.acos(-1/3))
print(f"\n  tetrahedron dihedral  arccos(1/3)   = {dih:.6f} deg")
print(f"  5 x dihedral                        = {5*dih:.6f} deg")
print(f"  total deficit  omega                = {defic:.6f} deg = {math.radians(defic):.6f} rad")
print(f"  per boundary   72 - dihedral        = {per:.6f} deg")
print(f"  identity check  109.47... - 108     = {tet-108:.6f} deg")
assert abs(per - (tet-108)) < 1e-9
assert abs(defic - 5*per) < 1e-9
OMEGA = math.radians(defic)
print(f"  => omega = {OMEGA:.6f} rad  (exact, no material input)")

print("\n"+"="*78)
print("BLOCK 2 — direction-dependent moduli in the 5-fold crystallography")
print("="*78)
# cubic elastic constants (GPa), room temperature, standard references
MAT = {
  "Au":      dict(C11=192.9, C12=163.8, C44=41.5,  mu=27.0,  nu=0.42, V_at=16.96e-30),
  "diamond": dict(C11=1079., C12=124.,  C44=578.,  mu=535.0, nu=0.07, V_at=5.673e-30),
}
def compliance(C11,C12,C44):
    d = (C11-C12)*(C11+2*C12)
    S11 = (C11+C12)/d; S12 = -C12/d; S44 = 1.0/C44
    return S11,S12,S44
def E_dir(n, C11,C12,C44):
    n = np.array(n,dtype=float); n/=np.linalg.norm(n)
    S11,S12,S44 = compliance(C11,C12,C44)
    H = 2*(S11-S12-S44/2)
    J = n[0]**2*n[1]**2 + n[1]**2*n[2]**2 + n[2]**2*n[0]**2
    return 1.0/(S11 - H*J)
def G_dir(n, m, C11,C12,C44):
    n = np.array(n,dtype=float); n/=np.linalg.norm(n)
    m = np.array(m,dtype=float); m/=np.linalg.norm(m)
    assert abs(np.dot(n,m)) < 1e-9, "n must be perpendicular to m"
    S11,S12,S44 = compliance(C11,C12,C44)
    H = 4*(S11-S12-S44/2)
    return 1.0/(S44 + H*sum(n[i]**2*m[i]**2 for i in range(3)))

DIRS = [((0,0,1),"<001>"), ((1,1,0),"<110>"), ((1,1,1),"<111>"), ((1,1,-2),"<11-2>")]
print("\n  Zener anisotropy A = 2*C44/(C11-C12):")
for k,p in MAT.items():
    A = 2*p["C44"]/(p["C11"]-p["C12"])
    print(f"    {k:>8}: A = {A:.4f}")
    p["A"] = A
assert abs(MAT["diamond"]["A"]-1.2105) < 2e-3 and abs(MAT["Au"]["A"]-2.8522) < 2e-3
print("    (both reproduce the 2026-09-11 values)")

print("\n  Young's modulus E (GPa) by direction:")
hdr = "    {:>9}".format("") + "".join(f"{lab:>10}" for _,lab in DIRS)
print(hdr)
for k,p in MAT.items():
    row = f"    {k:>9}" + "".join(f"{E_dir(n,p['C11'],p['C12'],p['C44']):>10.1f}" for n,_ in DIRS)
    print(row)

# the twin boundary is {111}; the disclination line is <110>; the in-boundary
# direction perpendicular to the line is <11-2>.  That is the shear channel.
print("\n  shear modulus G on the twin-boundary plane {111} along <11-2> (GPa):")
for k,p in MAT.items():
    g = G_dir((1,1,1),(1,1,-2),p['C11'],p['C12'],p['C44'])
    p["G_tb"] = g
    print(f"    {k:>9}: G = {g:>8.1f}")
print("\n  radial tensile channel: E along <11-2> (in the plane normal to <110>):")
for k,p in MAT.items():
    e = E_dir((1,1,-2),p['C11'],p['C12'],p['C44'])
    p["E_rad"] = e
    print(f"    {k:>9}: E = {e:>8.1f}")

print("\n  the ratio that controls tensile-vs-shear partitioning:")
for k,p in MAT.items():
    p["ratio"] = p["E_rad"]/p["G_tb"]
    print(f"    {k:>9}: E<11-2> / G{{111}}<11-2> = {p['ratio']:.4f}")
r = MAT["diamond"]["ratio"]/MAT["Au"]["ratio"]
print(f"\n  diamond / Au  = {r:.4f}")
print(f"  => the stiffness ratio between the two accommodation channels differs")
print(f"     by a factor {r:.2f} between the materials.  The Au partitioning")
print(f"     (45.0 : 22.5 : 32.5) therefore CANNOT be assumed for diamond.")

print("\n"+"="*78)
print("BLOCK 3 — isotropic disclination energy density (re-verify)")
print("="*78)
print(f"\n  W/L = mu*omega^2*R^2 / [16*pi*(1-nu)]   (de Wit, wedge disclination)")
print(f"  volume density w = mu*omega^2 / [16*pi^2*(1-nu)]   (R cancels)")
print(f"\n  {'':>9} {'mu(GPa)':>8} {'nu':>6} {'MJ/m^3':>9} {'meV/atom':>10}")
for k,p in MAT.items():
    w = p["mu"]*1e9*OMEGA**2/(16*math.pi**2*(1-p["nu"]))
    mev = w*p["V_at"]/1.602176634e-19*1e3
    p["w"], p["mev"] = w, mev
    print(f"  {k:>9} {p['mu']:>8.1f} {p['nu']:>6.2f} {w/1e6:>9.2f} {mev:>10.3f}")
assert abs(MAT["diamond"]["w"]/1e6 - 60.05) < 0.5
assert abs(MAT["diamond"]["mev"] - 2.126) < 0.02
print(f"\n  diamond / Au = {MAT['diamond']['mev']/MAT['Au']['mev']:.2f}x   (2026-09-11: 4.13)")
print(f"  controls: graphite->diamond ~20 meV/atom, hexagonal diamond 20-30 meV/atom")
print(f"  -> the disclination costs ~1/10 of those, consistent with 5-fold twins")
print(f"     being observed in CVD and detonation nanodiamond.")
print(f"\n  NOTE: diamond is Zener 1.21 (nearly isotropic), Au is 2.85.")
print(f"  The isotropic de Wit formula is therefore MORE reliable for diamond")
print(f"  than for Au -- diamond is the cleaner test case for the theory.")

print("\n"+"="*78)
print("BLOCK 4 — crossover radius R*, parametric in gamma_tb")
print("="*78)
print("""
  strain energy per unit length :  mu*omega^2*R^2 / [16*pi*(1-nu)]
  twin-boundary energy per unit length : 5 * gamma_tb * R
  equal at   R* = 80*pi*(1-nu)*gamma_tb / (mu*omega^2)
""")
def Rstar(mu_GPa, nu, gamma):
    return 80*math.pi*(1-nu)*gamma/(mu_GPa*1e9*OMEGA**2)
print(f"  {'gamma (J/m^2)':>14} {'R* diamond (nm)':>17} {'R* Au (nm)':>12}")
for g in (0.02,0.03,0.05,0.09,0.13,0.20,0.30):
    rd = Rstar(MAT['diamond']['mu'], MAT['diamond']['nu'], g)*1e9
    ra = Rstar(MAT['Au']['mu'],      MAT['Au']['nu'],      g)*1e9
    print(f"  {g:>14.2f} {rd:>17.3f} {ra:>12.3f}")
for g,exp in ((0.03,0.795),(0.05,1.325),(0.09,2.385)):
    assert abs(Rstar(535,0.07,g)*1e9 - exp) < 0.01
print("\n  (the 0.03 / 0.05 / 0.09 rows reproduce the 2026-09-11 values exactly)")
print("\n  LITERATURE STILL NEEDED: gamma_tb for the diamond coherent {111} twin.")
print("  Could not retrieve a value here (paywalls).  Standard relation for the")
print("  diamond structure: gamma_CTB ~ gamma_ISF / 2, so an ISF value fixes it.")

print("\n"+"="*78)
print("BLOCK 5 — the cross-material prediction (gamma ratio is the only input)")
print("="*78)
pref = ((1-MAT['diamond']['nu'])/(1-MAT['Au']['nu'])) * (MAT['Au']['mu']/MAT['diamond']['mu'])
print(f"""
  R*(dia)/R*(Au) = [gamma_dia/gamma_Au] * [(1-nu_dia)/(1-nu_Au)] * [mu_Au/mu_dia]
                 = [gamma_dia/gamma_Au] * {(1-MAT['diamond']['nu'])/(1-MAT['Au']['nu']):.4f} * {MAT['Au']['mu']/MAT['diamond']['mu']:.6f}
                 = [gamma_dia/gamma_Au] * {pref:.5f}
""")
print(f"  {'gamma_dia/gamma_Au':>20} {'R*(dia)/R*(Au)':>16}")
for gr in (1,2,3,4,5,8):
    print(f"  {gr:>20} {gr*pref:>16.3f}")
print(f"""
  => Even if diamond's twin boundary were EIGHT times more expensive than
     gold's, its 5-fold crossover radius would still be {8*pref:.2f}x gold's.
     The shear modulus ratio (535/27 = {535/27:.1f}) dominates everything.

  PRE-REGISTERED PREDICTION (P1):
     the boundary-dominated regime for 5-fold twinned diamond ends at a
     radius roughly ONE ORDER OF MAGNITUDE SMALLER than for gold.
     With gamma_Au = 0.032 J/m^2:  R*(Au) = {Rstar(27,0.42,0.032)*1e9:.1f} nm.
     With gamma_dia/gamma_Au = 4:  R*(dia) = {Rstar(27,0.42,0.032)*1e9*4*pref:.1f} nm.

  This is testable against what is already observed:
     - Cheng et al. 2025 measured Au pentagonal prisms at 26.0 and 52.5 nm
       edge length -- ABOVE R*(Au) ~ {Rstar(27,0.42,0.032)*1e9:.0f} nm, i.e. strain-dominated,
       which is why they see MIXED accommodation rather than a clean boundary.
     - detonation nanodiamond is typically 4-5 nm, i.e. also at or above
       a diamond R* of a few nm -> strain-dominated as well.
     - CVD diamond 5-fold twins are far larger -> deep in strain-dominated.
  So the prediction is NOT that diamond behaves like the small-R limit; it is
  that diamond's crossover sits an order of magnitude lower, so essentially
  ALL observed 5-fold diamond is strain-dominated.  That has a consequence:
  the accommodation should be dominated by the elastically SOFTEST channel,
  and Block 2 says which one that is.
""")
print("ALL CHECKS COMPLETE")

print("\n"+"="*78)
print("BLOCK 6 — the partitioning prediction, stated at the level it can be")
print("="*78)
EG_Au, EG_di = MAT["Au"]["ratio"], MAT["diamond"]["ratio"]
print(f"""
  Cheng et al. 2025 measured, for Au, per sector boundary (total 1.471 deg):
      tensile 0.66 deg (45.0%)   shear 0.33 deg (22.5%)   rot/bend 0.48 deg (32.5%)
  so within the tensile/shear pair,  x_t / x_s = 0.66/0.33 = 2.00.

  NOTE what this rules out.  The naive "softest channel takes the most"
  rule  x_i ~ 1/k_i  would give  x_t/x_s = G/E = {1/EG_Au:.3f}  for Au, i.e. shear
  dominating 4:1.  The measurement is the OPPOSITE (2:1 the other way).
  So the geometric closure coefficients, not the moduli alone, set the split,
  and I do not have Cheng et al.'s definitions to fix them (paywalled).
  => no first-principles partitioning prediction is available here.

  What IS available is the DIRECTION, which needs only monotonicity:
      Au      : E<11-2> / G{{111}}<11-2> = {EG_Au:.4f}   (shear {EG_Au:.2f}x softer than tensile)
      diamond : E<11-2> / G{{111}}<11-2> = {EG_di:.4f}   (shear only {EG_di:.2f}x softer)
      ratio   : {EG_Au/EG_di:.3f}
  In diamond the shear channel is RELATIVELY STIFFER.  Under any model in
  which a relatively stiffer channel takes relatively less of the deficit:
""")
print("  PRE-REGISTERED PREDICTION (P2), directional and model-free:")
print("      diamond's tensile share > 45.0%   AND   shear share < 22.5%")
print("\n  and with a one-parameter monotone form x_t/x_s ~ (E/G)^(-p), calibrated")
print("  on Au and holding the rotation share at 32.5% for want of a model:")
print(f"\n  {'p':>5} {'x_t/x_s':>9} {'tensile %':>11} {'shear %':>9}")
for p in (0.5, 0.75, 1.0):
    r = 2.00*(EG_Au/EG_di)**p
    tot = 67.5
    print(f"  {p:>5.2f} {r:>9.2f} {tot*r/(1+r):>11.1f} {tot/(1+r):>9.1f}")
print(f"\n  => quantitative range: tensile 49-54%, shear 14-19%  (Au: 45.0 / 22.5)")
print("     assumptions stated: (i) monotone in E/G, (ii) rotation share held,")
print("     (iii) exponent p in [1/2, 1].  All three are falsifiable separately.")

print("\n"+"="*78)
print("BLOCK 7 — a consistency check the model already passes")
print("="*78)
RA = Rstar(27,0.42,0.032)*1e9
print(f"""
  R*(Au) with gamma_Au = 0.032 J/m^2  ->  {RA:.1f} nm
  Cheng et al. measured Au pentagonal prisms of edge length 26.0 and 52.5 nm,
  i.e. {26.0/RA:.1f}x and {52.5/RA:.1f}x above R*.
  Above R* the strain term dominates the twin-boundary term, so the deficit
  should NOT be dumped into one boundary -- it should spread into the bulk as
  a mixed elastic field.  That is exactly what they measured, and it is why
  option (c) "one non-twin boundary" was rejected for Au.
  The R* estimate was not tuned to this; it follows from mu, nu, omega, gamma.
""")
print("ALL CHECKS COMPLETE (7 blocks)")
