"""
Rebuilding P2 in the correct framework.
Block 1: the pure Volterra wedge disclination has NO bulk shear -> Cheng's
         shear must be interface-mediated.  Establish this first.
Block 2: split the disclination energy into volumetric and deviatoric parts.
         Show the ratio carries a factor B/(2G) = 1/(2 * Pugh) EXACTLY.
Block 3: energy minimisation -> x_t/x_s = C * (G/B), exponent q = 1 DERIVED.
Block 4: calibrate C on gold, predict diamond.
Block 5: an independent test of q = 1 from Yu et al.'s OWN two materials.
Block 6: the rotation mode is a GRADIENT mode -> size dependent -> P4.
"""
import math, numpy as np
from scipy.integrate import quad

MAT = {"Au":dict(C11=192.9,C12=163.8,C44=41.5),
       "Si":dict(C11=165.7,C12=63.9, C44=79.6),
       "diamond":dict(C11=1079.,C12=124.,C44=578.)}
def hill(C11,C12,C44):
    B=(C11+2*C12)/3.; GV=(C11-C12+3*C44)/5.
    GR=5*(C11-C12)*C44/(4*C44+3*(C11-C12)); return B,0.5*(GV+GR)
for k,p in MAT.items():
    p["B"],p["G"]=hill(p["C11"],p["C12"],p["C44"]); p["pugh"]=p["G"]/p["B"]
    # nu derived from the SAME Hill B,G -- internal consistency, no extra input
    p["nu"]=(3*p["B"]-2*p["G"])/(2*(3*p["B"]+p["G"]))
print("  Poisson ratios derived from the same Hill B,G (no extra input):")
for k,p in MAT.items():
    print(f"    {k:>9}: B={p['B']:7.1f}  G={p['G']:7.1f}  nu={p['nu']:.4f}  G/B={p['pugh']:.4f}")
assert abs(MAT["Au"]["nu"]-0.42)<0.01 and abs(MAT["diamond"]["nu"]-0.07)<0.01
print("    (reproduce the literature 0.42 / 0.07 used since 2026-09-11)")

print("="*76)
print("BLOCK 1 — the pure wedge disclination has NO bulk shear stress")
print("="*76)
print("""
  de Wit / Volterra wedge disclination, strength omega, plane strain,
  cylinder of radius R, with A = mu*omega / [2*pi*(1-nu)] and L = ln(r/R):

      sigma_rr     = A * L
      sigma_thth   = A * (1 + L)
      sigma_zz     = nu * (sigma_rr + sigma_thth) = nu*A*(1 + 2L)
      sigma_r-th   = 0          <-- IDENTICALLY ZERO, axisymmetric

  So in the idealised continuum the deficit is accommodated with NO shear
  at all: purely radial/hoop (tensile-compressive) plus the axial response.

  => Cheng et al.'s measured shear (22.5%) and rotation/bending (32.5%)
     CANNOT come from the bulk Volterra field.  They come from the object
     being FIVE DISCRETE SECTORS with real interfaces, not a continuum with
     a smeared disclination.  This is why they report that it is neither
     Ino-type uniform strain nor de Wit-type 1/r.
  => v1's mistake was deeper than the choice of modulus: it treated the
     three modes as three bulk elastic channels.  Two of them are interface
     channels.
""")

print("="*76)
print("BLOCK 2 — volumetric / deviatoric split carries B/(2G) exactly")
print("="*76)
print("""
  Standard split:  w = w_vol + w_dev ,  w_vol = p^2/(2B) ,  w_dev = s:s/(4G)
  so for ANY stress field
        W_dev / W_vol = [B / (2G)] * <s:s> / <p^2>
                      = [1 / (2 * Pugh)] * <s:s> / <p^2>
  The Pugh ratio appears as an EXACT prefactor, not an empirical correlation.
  Yu et al. found G/B correlates with the strain concentration; this is why.
""")
def ratio_geom(nu, n=20001):
    """<s:s>/<p^2> over the cross-section, area-weighted. A cancels."""
    u = np.linspace(1e-9,1.0,n); L = np.log(u); w = u   # area weight r dr
    p  = (1+nu)*(1+2*L)/3.0
    srr = L      - (1+nu)*(1+2*L)/3.0
    sth = (1+L)  - (1+nu)*(1+2*L)/3.0
    szz = (1+2*L)*(2*nu-1)/3.0
    ss  = srr**2+sth**2+szz**2
    num = np.trapezoid(ss*w,u); den = np.trapezoid(p**2*w,u)
    return num/den
print(f"  {'material':>9} {'nu':>6} {'<s:s>/<p^2>':>13} {'Pugh G/B':>10} {'W_dev/W_vol':>13}")
for k,p in MAT.items():
    g = ratio_geom(p["nu"]); r = g/(2*p["pugh"])
    p["geom"], p["WdWv"] = g, r
    print(f"  {k:>9} {p['nu']:>6.3f} {g:>13.4f} {p['pugh']:>10.4f} {r:>13.4f}")
print(f"""
  The geometric factor <s:s>/<p^2> varies only mildly with nu
  ({min(p['geom'] for p in MAT.values()):.3f} to {max(p['geom'] for p in MAT.values()):.3f}), so W_dev/W_vol is dominated by 1/(2*Pugh):
     gold    {MAT['Au']['WdWv']:.2f}   (shear-dominated energy budget)
     silicon {MAT['Si']['WdWv']:.2f}
     diamond {MAT['diamond']['WdWv']:.2f}   (volumetric-dominated)
  => In gold the deviatoric channel carries {MAT['Au']['WdWv']:.0f}x the volumetric energy;
     in diamond it carries only {MAT['diamond']['WdWv']:.2f}x.  Opposite regimes.
""")

print("="*76)
print("BLOCK 3 — the exponent is DERIVED, not guessed")
print("="*76)
print("""
  Let the deficit split as  omega = x_t + x_s + x_r  and let each channel
  store quadratic energy  (1/2) k_i x_i^2 .  Minimising at fixed omega:
        x_i  proportional to  1 / k_i
  For the two bulk-modulus-bearing channels the stiffnesses are
        k_t ~ B   (dilatational: bond-length change)
        k_s ~ G   (deviatoric: shear)
  hence
        x_t / x_s  =  k_s / k_t  =  C * (G / B)      with C purely geometric.

  So the exponent is q = 1 EXACTLY.  v1 scanned p in [1/2, 1] over a guessed
  form; here the form follows from quadratic elasticity, and the only unknown
  left is the single geometric constant C.
""")

print("="*76)
print("BLOCK 4 — calibrate C on gold, predict diamond")
print("="*76)
xt_xs_Au = 0.66/0.33
Cgeo = xt_xs_Au/MAT["Au"]["pugh"]
print(f"\n  gold measured (Cheng et al.):  x_t/x_s = 0.66/0.33 = {xt_xs_Au:.3f}")
print(f"  gold Pugh = {MAT['Au']['pugh']:.4f}   ->   C = {Cgeo:.3f}")
print(f"\n  {'material':>9} {'Pugh':>8} {'x_t/x_s':>9} {'tensile %':>11} {'shear %':>9} {'rot %':>7}")
for k in ("Au","Si","diamond"):
    p=MAT[k]; r=Cgeo*p["pugh"]; rest=67.5
    print(f"  {k:>9} {p['pugh']:>8.3f} {r:>9.2f} {rest*r/(1+r):>11.1f} {rest/(1+r):>9.1f} {32.5:>7.1f}")
print("""
  (rotation held at gold's 32.5% -- Block 6 explains why that is the one
   share this framework cannot fix, and turns it into a separate prediction)
""")

print("="*76)
print("BLOCK 5 — an INDEPENDENT test of q = 1, from Yu et al.'s own data")
print("="*76)
print("""
  Yu et al. plot bond-length distributions with a display range of +-2% of
  the bulk bond length.  Reading the boundary contours off Figs. S2 and S4:
      diamond (bulk 1.53 A, range 1.500-1.560): boundaries are RED,
              ~1.554-1.560 A  ->  anomaly ~ +1.6 to +2.0%,  call it +1.8%
      silicon (bulk 2.34 A, range 2.296-2.390): boundaries are YELLOW,
              ~2.362-2.371 A  ->  anomaly ~ +0.9 to +1.3%,  call it +1.1%
""")
an_d, an_s = 1.8, 1.1
print(f"  measured anomaly ratio   diamond/Si = {an_d/an_s:.2f}")
print(f"  Pugh ratio               diamond/Si = {MAT['diamond']['pugh']/MAT['Si']['pugh']:.2f}")
print(f"  agreement                            {100*abs(an_d/an_s-MAT['diamond']['pugh']/MAT['Si']['pugh'])/(MAT['diamond']['pugh']/MAT['Si']['pugh']):.0f}% discrepancy")
print("""
  => The dilatational (bond-length) anomaly scales roughly LINEARLY with
     G/B across Yu et al.'s own two materials, which is what q = 1 requires.

  HONESTY: this is a colour read off a contour plot, precision maybe +-0.3%,
  so the test is weak -- but it is INDEPENDENT of gold and it points the
  right way.  Extracting the real numbers needs the main text or the raw
  data (ryu@tsinghua.edu.cn).
  Do NOT push this to absolute scaling: Yu's observable is a boundary-local
  bond length in a ~3 nm DFT cell, Cheng's is a sector-averaged strain in a
  26-52 nm particle.  Only the within-Yu ratio is a fair test.
""")

print("="*76)
print("BLOCK 6 — the rotation mode is a GRADIENT mode -> P4")
print("="*76)
print("""
  The tensile and shear channels store energy in the strain itself, so their
  stiffnesses are moduli (B and G) and are SIZE INDEPENDENT.
  The rotation/bending channel stores energy in the strain GRADIENT
  (curvature kappa ~ x_r / R), so its stiffness carries a length:
        k_r  ~  (modulus) * (length)^2 / R^2
  i.e. k_r DECREASES as R grows -> bending gets relatively cheaper in
  larger particles -> x_r should GROW with size, while x_t/x_s stays fixed.

  PREDICTION P4 (new, and this is the one that is cheap to test):
      in a size series of fivefold twinned particles of ONE material,
        * x_t / x_s  is CONSTANT (set by G/B alone)
        * the rotation/bending share GROWS with particle size
      Cheng et al. already have two sizes (26.0 and 52.5 nm) and report a
      single partition, so either their two sizes are too close to resolve
      it, or the share is stated for one of them.  Lin et al., Adv. Mater.
      (2026) is a SIZE-DEPENDENT 4D-STEM study of exactly these particles
      -- P4 is directly testable against it, and it may already be answered.

  This also explains why the rotation share is the one v1 could not fix from
  moduli: it is not a modulus-controlled quantity at all.
""")
print("ALL CHECKS COMPLETE")

print("="*76)
print("BLOCK 7 — the tension between Block 1 and Block 3, stated openly")
print("="*76)
print("""
  Block 1 says the shear is INTERFACE-mediated (the bulk Volterra field has
  none).  Block 3 then uses the BULK shear modulus G as the shear channel's
  stiffness.  Those two statements are not obviously compatible.  Two readings:

  (a) The interface only LOCALISES the shear; the shear strain field still
      lives in the adjoining bulk and therefore still costs G, up to a
      geometric factor absorbed into C.  Then k_s ~ G is right.

  (b) The interface resists sliding by its OWN structure (tied to gamma_tb
      and the boundary's atomic reconstruction), not by bulk G.  Then k_s
      involves gamma_tb and the framework changes: the partitioning would
      depend on the twin-boundary energy, not only on G/B.

  WHICH ONE?  Yu et al.'s result is evidence for (a): they found that a
  purely BULK ratio (G/B) predicts the strain concentration across diamond
  and silicon.  If (b) dominated, bulk moduli should not have worked at all.
  So (a) is the defensible first approximation -- but (b) is a real
  alternative and it is TESTABLE: under (b) the partitioning correlates with
  gamma_tb as well as with G/B, and the two can be separated by choosing a
  material pair with similar G/B but very different gamma_tb.

  This is the sharpest open question in the rebuilt framework, and it is
  the reason the diamond numbers below are stated as a RANGE-free single
  prediction with an explicit assumption, not as a result.
""")
print("="*76)
print("SUMMARY — what P2 became")
print("="*76)
print("""
  WITHDRAWN (v1 P2): "diamond tensile > 45%, shear < 22.5%" from a guessed
      monotone dependence on the directional ratio E/G.  Wrong control
      parameter AND wrong framework (three bulk channels).

  REBUILT (P2'):  x_t / x_s = C * (G/B),  exponent q = 1 DERIVED from
      quadratic elasticity;  C = 12.72 calibrated on gold's 0.66/0.33.
      diamond:  x_t/x_s = 15.4    -> tensile 63.4%, shear 4.1%
      silicon:  x_t/x_s =  8.65   -> tensile 60.5%, shear 7.0%
      (rotation share held at gold's 32.5%; see P4)
      Assumptions, each separately falsifiable:
        A1  tensile <-> volumetric, shear <-> deviatoric (needs Cheng's
            definitions to confirm; Sci Adv is open access)
        A2  reading (a) of Block 7: interface shear costs bulk G
        A3  rotation share size-independent -- KNOWN to be wrong (P4),
            so the percentages move even if the RATIO 15.4 holds

  NEW (P4):  x_t/x_s constant in a size series, rotation share GROWS with
      size.  Directly testable against Lin et al., Adv. Mater. (2026).

  NEW (explanation, not prediction):  Yu et al.'s empirical G/B correlation
      follows from  W_dev/W_vol = [1/(2 G/B)] * <s:s>/<p^2>  exactly.
      This is the part that needed no new assumption at all.
""")
print("ALL CHECKS COMPLETE (7 blocks)")
