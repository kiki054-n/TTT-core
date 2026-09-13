"""
Cheng et al. FULL TEXT now in hand.  Three consequences:
  (1) their own stress equation CONFIRMS the deviatoric reading (v4 section 2)
  (2) the exp-vs-MD "two-point lever" (v4 section 3) is CONFOUNDED -> withdraw q=0.232
  (3) v4's claim "Yu et al. not cited" is WRONG -- ref 24 IS Yu's group
"""
import math
print("="*78); print("BLOCK 1 - Cheng's own stress formula contains no bulk modulus"); print("="*78)
print("""
  Methods, verbatim:      sigma = E/(1+nu) * (e_xx - e_yy)

  But  E/(1+nu) = 2G  identically.  So Cheng's own stress measure is

        sigma = 2 G (e_xx - e_yy)

  -- the PURE DEVIATORIC combination, with the bulk modulus B absent.
  v4 section 2 (A1 refuted; tensile channel is deviatoric, cost ~ G) is
  confirmed not by inference but by their own equation.
""")
E_e,nu_e,E_s,nu_s = 88.0,0.415,110.0,0.36
exx_e,eyy_e,exx_s,eyy_s = 0.0058,-0.0061,0.0067,-0.0075
G_e,G_s = E_e/(2*(1+nu_e)), E_s/(2*(1+nu_s))
s_e = 2*G_e*(exx_e-eyy_e); s_s = 2*G_s*(exx_s-eyy_s)
print(f"  G_exp = E/(2(1+nu)) = {G_e:.2f} GPa      G_sim = {G_s:.2f} GPa")
print(f"  sigma_exp = {s_e:.4f} GPa   sigma_sim = {s_s:.4f} GPa")
print(f"  sigma_sim/sigma_exp = {s_s/s_e:.3f}      (paper states ~1.58)  -> arithmetic reproduced")

print("="*78); print("BLOCK 2 - the tensile angle IS e_xx - e_yy in radians"); print("="*78)
for tag,(a,b,rep) in {"exp":(exx_e,eyy_e,0.66),"sim":(exx_s,eyy_s,0.68)}.items():
    d=(a-b); print(f"  {tag}: e_xx-e_yy = {d:.5f} rad = {math.degrees(d):.3f} deg   reported tensile share {rep:.2f} deg"
                   f"   -> {100*(math.degrees(d)/rep-1):+.0f} %")
print("""
  For the EXPERIMENT the identity  delta_t = e_xx - e_yy  holds to 3 %.
  For the SIMULATION it is 20 % off -- consistent with the quoted values
  being EDGE values while the 0.66/0.68 deg are DOMAIN AVERAGES, and with
  the simulation's much shallower averaging depth (see Block 3).
  Either way: the angle-closing observable is the deviatoric difference.
""")

print("="*78); print("BLOCK 3 - WITHDRAW the q = 0.232 fit: the lever is confounded"); print("="*78)
print("""
  v4 used (exp nu=0.415) vs (MD nu=0.36) as a controlled elastic lever.
  The full text forbids this.  Methods, verbatim:

    "The simulations used an LJ potential for Au-Au interactions, which
     reproduced surface tension reasonably well but still existed an ~15 %
     deviation in Young's modulus and Poisson's ratio."

    "strain fields in simulations were extracted from a narrow region of
     ~3 atomic layers near the surface, whereas the experimental strain
     values were averaged across a much larger depth"

    sigma_sim/sigma_exp = (f_sim/h_sim)/(f_exp/h_exp) ~ 1.58  ->  h_sim/h_exp = 0.67

    "we further average the tensile values in simulation over around 10
     atomic layers and the discrepancy for 0 truncation drops from around
     11 to 6 %"

  So (a) nu_sim = 0.36 is a DEFECT of the potential, not a second material,
  and (b) the exp/MD difference is attributed by the authors to AVERAGING
  DEPTH and SURFACE STRESS, not to elasticity.
  => v4 section 3's numerical falsification of q=1 is WITHDRAWN.
     P2' still dies, but on the STRUCTURAL argument of Block 1 alone
     (no B in the governing equation), which is the stronger ground anyway.
""")

print("="*78); print("BLOCK 4 - shape, not size, is the strong control"); print("="*78)
print("""
  Results, verbatim trends with INCREASING truncation depth TD = R/L:
     (i)   decrease in edge-localised tensile strain
     (ii)  increase in shear strain at the vertices
     (iii) DECREASE in rotation strain, with inverted rotation near
           truncated areas
  and separately: "particle size plays a minor role in determining the
  equilibrium strain distribution" (26.0 vs 52.5 nm), while size IS
  relevant to the FLUCTUATIONS ("larger particles exhibiting reduced
  variability").

  TD = 0 is the idealised sharp pentagon, TD = 1 the stellated limit.
""")

print("="*78); print("BLOCK 5 - reconciling Cheng and Lin: the size effect is SHAPE-MEDIATED"); print("="*78)
print("""
  Lin et al. 2026 (abstract): crossover at ~35 nm, "which is also correlated
  to a transition from modified-Wulff particles to pentagonal bipyramids".

  A modified-Wulff decahedron is the TRUNCATED shape (higher TD);
  the pentagonal bipyramid is the sharp limit (TD -> 0).
  So Lin's large particles are LOW-TD, small particles HIGH-TD.

  Apply Cheng's trend (iii):  rotation DECREASES with increasing TD
        => low TD (large particles)  ->  MORE rotation
        => high TD (small particles) ->  LESS rotation

  This is P4's DIRECTION (rotation share grows with size) -- but the
  mechanism is NOT a strain-gradient length scale.  It is SHAPE.
  Size enters only because the equilibrium morphology changes with size.

  => P4 is replaced by P4':
       the rotation share is controlled by truncation depth, not by R
       directly; any apparent size dependence in one-material size series
       is mediated by the TD(size) relation.
     This is why Cheng (fixed shape, two sizes) sees no size effect while
     Lin (size series that crosses a morphology transition) does.
     FALSIFIABLE: measure a size series at FIXED TD -> partition should be
     flat; measure a TD series at FIXED size -> partition should move.
     Cheng has already done the second half (Fig. 3 G-I).
""")

print("="*78); print("BLOCK 6 - prior art I had not checked (my error pattern again)"); print("="*78)
print("""
  v4 section 4.2 proposed elastic ANISOTROPY as the residual's control
  parameter and called it "new".  Cheng's own reference list:

   ref 22  C. L. Johnson, E. Snoeck, M. Ezcurdia, B. Rodriguez-Gonzalez,
           I. Pastoriza-Santos, L. M. Liz-Marzan, M. J. Hytch,
           "EFFECTS OF ELASTIC ANISOTROPY ON STRAIN DISTRIBUTIONS IN
            DECAHEDRAL GOLD NANOPARTICLES", Nat. Mater. 7, 120 (2008)
   ref 57  F. Niekiel, E. Spiecker, E. Bitzek, "INFLUENCE OF ANISOTROPIC
           ELASTICITY ON THE MECHANICAL PROPERTIES OF FIVEFOLD TWINNED
           NANOWIRES", J. Mech. Phys. Solids 84, 358 (2015)
   ref 14  S. Patala, L. D. Marks, M. Olvera de la Cruz, "ELASTIC STRAIN
           ENERGY EFFECTS IN FACETED DECAHEDRAL NANOPARTICLES",
           J. Phys. Chem. C 117, 1485 (2013)

  => P5 is almost certainly already occupied, by ref 22 above all.
     Read ref 22 BEFORE writing another word about anisotropy.
""")

print("="*78); print("BLOCK 7 - CORRECTION to v4: Cheng DOES cite Yu's group"); print("="*78)
print("""
  v4 section 1 stated: "Yu et al. への言及: なし".  That is WRONG.

   ref 24  H. Wu, R. YU, J. ZHU, W. Chen, Y. Li, T. Wang,
           "Size-dependent strain in fivefold twins of gold",
           Struct. Sci. (Acta Cryst. B) 77, 93 (2021)

  Wu + Yu + Zhu are three of the four authors of the 2017 DIAMOND paper
  (Yu, Wu, Wang, Zhu).  Cheng cites them as the source of the claim that
  "tensile strain [is] the dominant accommodation mechanism, with only
  minor contributions from lattice bending", i.e. exactly the position
  Cheng's hybrid result partially vindicates.

  What is genuinely absent from Cheng: DIAMOND, SILICON, the Pugh ratio,
  and the 2017 diamond paper.  The gold-side link to Yu's group is already
  made in the literature; the DIAMOND-side link is not.
  => the unoccupied ground is narrower than v4 claimed, but it is still
     unoccupied, and it is exactly where P3 lives.
""")
print("ALL BLOCKS COMPLETE")
