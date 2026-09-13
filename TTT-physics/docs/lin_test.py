import math
print("="*78); print("BLOCK A - Lin's k parameter IS Cheng's tensile ratio, and its limit is BCT"); print("="*78)
print("""
  Lin et al. (arXiv 2507.14781), Eq. 1:

        k = d_220/d_002 = (1/sqrt2) * (1+eps_220)/(1+eps_002) = tan(theta)

  where 2*theta is the interplanar angle between the (111) twinned directions.
  Cheng et al., Methods:

        a_x/a_y = sqrt2 * (1+e_xx)/(1+e_yy)

  Same observable (reciprocal vs real space, 220 vs 002 ordering).
  But LIN GIVES IT A GEOMETRIC MEANING CHENG DOES NOT:
""")
k_fcc, k_bct = 0.7071, 0.7265
for tag,k in (("ideal fcc",k_fcc),("5-twinned bct",k_bct)):
    print(f"    {tag:>14}: k = {k:.4f}  ->  2*theta = {2*math.degrees(math.atan(k)):.3f} deg")
print(f"""
  So the BCT limit is EXACTLY the state in which the normal-strain channel
  closes the whole gap by itself:  72.000 deg x 5 = {72*5} deg.
  => the tensile/normal channel has a SATURATION LIMIT and that limit is BCT.
  This is a geometric identity, not a fit.  Neither Cheng nor v5 had it.
""")

print("="*78); print("BLOCK B - P4 and P4' are both DEAD"); print("="*78)
print("""
  Lin, verbatim:
    "The NPs exhibit SIZE-INDEPENDENT spatial patterns of gamma and R to
     close the 7.35 deg geometric gap"
    "The alternating patterns in gamma and R maps across five grains sustain
     for all the NPs, confirming the SIZE-INDEPENDENCE of the gap closing
     mechanism."
  and for d > 35 nm the summed (R + gamma) plateaus at ~7.35 deg, while for
  d < 35 nm it fluctuates around 7.35 deg by ~1 deg.

  => P4  (rotation share grows with R, gradient mechanism): REFUTED.
  => P4' (rotation share set by truncation depth TD): ALSO REFUTED --
     Lin's particles DO change shape across the crossover (rounded
     modified-Wulff -> faceted pentagonal bipyramid) and the gamma/R gap
     closing still does not change.  The shape route is closed too.

  What IS size dependent in Lin: the NORMAL strain DISTRIBUTION, and the
  bct/fcc balance:
      d < 35 nm : homogeneous bct across the particle (~10 % fcc)
      d ~ 35 nm : fcc emerges at twin boundaries and edges, mostly one grain
      d > 35 nm : fcc near all five boundaries and edges, bct inside grains
                  "the normalized population of fcc-like phase never
                   exceeds 40 %"
      heterogeneity swaps character: small = INTER-grain, large = INTRA-grain

  NOTE an internal tension in Lin worth flagging: if gamma + R already sums
  to 7.35 deg, the normal strain has nothing left to close -- yet k > 0.7071
  everywhere means the normal channel IS contributing.  Cheng's accounting
  (tensile 45 %, shear 22.5 %, rotation 32.5 %) and Lin's (gamma + R = 7.35)
  are therefore NOT the same partition.  Resolving that needs Lin's figures.
  DO NOT quote a combined partition until it is resolved.
""")

print("="*78); print("BLOCK C - a REAL disagreement between the two papers"); print("="*78)
print("""
  Off-centre disclination (Gryaznov et al. 1999):
    CHENG: MD shows reproducing the observed strain variation "would require
           more than 35 % off-center displacement, which is inconsistent
           with our experimental observations"  -> REJECTED
    LIN:   "when we build models with the center shift and keep all other
           factors identical, the grain with significantly distorted k can
           be reproduced"                                    -> REQUIRED

  Same material, same technique (4D-STEM), opposite conclusions on the same
  hypothesis, in papers that do not cite each other (Lin's preprint is
  July 2025, Cheng published Oct 2025, Lin's journal version Apr 2026).
  This is an OPEN, NAMED controversy -- and unlike everything else in this
  track, it is not occupied by either group.
""")

print("="*78); print("BLOCK D - Lin gives the interface energies -> a NUMERICAL TEST OF P1"); print("="*78)
print("""
  Lin quotes (Au vs Ag, mJ/m^2):
        stacking fault   32   vs  16
        twin boundary    15   vs   8
        grain boundary  364   vs 790
""")
omega = math.radians(360-5*math.degrees(math.acos(1/3.)))
print(f"  omega = {omega:.6f} rad  ({math.degrees(omega):.6f} deg)")
def Rstar(gamma, mu, nu):
    return 80*math.pi*(1-nu)*gamma/(mu*omega**2)
cases = [("Au", 0.015, 31.10e9, 0.415), ("Ag", 0.008, 30.3e9, 0.37)]
for tag,g,mu,nu in cases:
    R = Rstar(g,mu,nu)
    print(f"  {tag}: gamma_tb={g*1000:.0f} mJ/m^2, mu={mu/1e9:.1f} GPa, nu={nu:.3f}  ->  R* = {R*1e9:.2f} nm")
print("""
  P1 says R* is where the disclination elastic energy  mu w^2 R^2/[16 pi(1-nu)]
  equals the five twin boundaries' cost  5 gamma_tb R.

  PROBLEM: R*(Au) ~ 4 nm, but fivefold Au particles are elastically strained
  and defect-free at 20-55 nm (both Lin and Cheng), only relaxing by partial
  dislocations when heated to 1200 C.  An order of magnitude out.

  DIAGNOSIS: P1's balance has only TWO of the three terms.  The reason the
  decahedron exists at all is its LOWER SURFACE energy (Marks / Ino).
  Omitting the surface term makes R* meaningless as a stability threshold.
  => P1 must be reformulated with the surface term, or withdrawn.
  Lin says as much in words: Au's stability comes from its LOW twin-boundary
  cost relative to competing metals -- a three-way comparison, not two-way.
""")
print("ALL BLOCKS COMPLETE")
