"""
Yu, Wu, Wang, Zhu (ACS AMI 9 (2017) 4253) SI gives the controlling parameter:
Pugh's ratio G/B.  They quote diamond 1.21 and silicon 0.68.
Block 1: reproduce their two numbers exactly (validates constants + method)
Block 2: place GOLD in their series  -> links Yu 2017 (DFT) to Cheng 2025 (expt)
Block 3: extend the series to other materials = a prediction ladder
Block 4: the corner rehybridisation numbers from the SI
"""
import math
C = {  # C11, C12, C44 in GPa, room temperature standard values
 "diamond": (1079.,124.,578.),  "c-BN": (820.,190.,480.),
 "SiC(3C)": (390.,142.,256.),   "Si": (165.7,63.9,79.6),
 "Ge": (128.9,48.3,67.1),       "Ni": (246.5,147.3,124.7),
 "Cu": (168.4,121.4,75.4),      "Ag": (124.,93.4,46.1),
 "Au": (192.9,163.8,41.5),      "Al": (108.2,61.3,28.5),
 "Pt": (346.7,250.7,76.5),      "Pb": (49.5,42.3,14.9),
}
def hill(C11,C12,C44):
    B  = (C11+2*C12)/3.0
    GV = (C11-C12+3*C44)/5.0
    GR = 5*(C11-C12)*C44/(4*C44+3*(C11-C12))
    G  = 0.5*(GV+GR)
    A  = 2*C44/(C11-C12)
    return B,G,A

print("="*76)
print("BLOCK 1 — reproduce Yu et al.'s Pugh ratios (validation)")
print("="*76)
for k,q in (("diamond",1.21),("Si",0.68)):
    B,G,A = hill(*C[k])
    print(f"\n  {k}: B={B:.1f} GPa, G(Hill)={G:.1f} GPa,  G/B = {G/B:.4f}   "
          f"SI quotes {q}")
    assert abs(G/B - q) < 0.006, (k, G/B, q)
print("\n  Both reproduced to better than 0.006.  Constants and Hill averaging")
print("  match what Yu et al. used.  G(Hill) also equals the mu we have been")
print("  using since 2026-09-11 (diamond 535, Au 27) -- consistent throughout.")

print("\n"+"="*76)
print("BLOCK 2 — place GOLD in their series: this links the two papers")
print("="*76)
rows=[]
for k in ("Au","Si","diamond"):
    B,G,A = hill(*C[k]); rows.append((k,B,G,G/B,A))
print(f"\n  {'material':>9} {'B(GPa)':>8} {'G(GPa)':>8} {'G/B':>7} {'Zener A':>8}")
for k,B,G,r,A in rows:
    print(f"  {k:>9} {B:>8.1f} {G:>8.1f} {r:>7.3f} {A:>8.3f}")
gb = {k:r for k,_,_,r,_ in rows}
print(f"""
  Yu et al.'s finding (SI section 4, verbatim):
    "The strain concentration at the twin boundaries can also be observed,
     but significantly smaller than that in diamond.  Note that the Pugh's
     ratios G/B of diamond and silicon are 1.21 and 0.68, respectively,
     confirming the strong correlation between the strain concentration and
     the ratio of shear modulus to bulk modulus."

  So: HIGHER G/B  ->  STRONGER localisation of strain AT the twin boundaries.
  The ordering is
       diamond {gb['diamond']:.3f}  >>  Si {gb['Si']:.3f}  >>  Au {gb['Au']:.3f}
  with gold a further factor {gb['Si']/gb['Au']:.1f} below silicon.

  => Extended to gold, Yu et al.'s correlation says gold should show the
     WEAKEST boundary localisation of the three: the deficit spreads into
     the sector interior instead.

  And that is exactly what Cheng et al. (2025) measured for gold:
     a MIXED accommodation (45.0 : 22.5 : 32.5) distributed through the
     sector, tensile peaking at the sector CENTRE (mean 0.88%), and the
     option "dump the deficit into one boundary" explicitly REJECTED.

  The two papers have never been connected (different communities: DFT/
  materials vs 4D-STEM/nanoparticles).  Pugh's ratio connects them into a
  single monotone series.
""")

print("="*76)
print("BLOCK 3 — the prediction ladder (a testable ordering)")
print("="*76)
allr = sorted(((k,)+hill(*v) for k,v in C.items()), key=lambda x: -x[2]/x[1])
print(f"\n  {'material':>9} {'B(GPa)':>8} {'G(GPa)':>8} {'G/B':>7}  expected boundary localisation")
for k,B,G,A in allr:
    r=G/B
    tag = ("very strong" if r>1.0 else "strong" if r>0.7 else
           "moderate" if r>0.45 else "weak" if r>0.2 else "very weak")
    mark = "  <- Yu 2017" if k in ("diamond","Si") else ("  <- Cheng 2025" if k=="Au" else "")
    print(f"  {k:>9} {B:>8.1f} {G:>8.1f} {r:>7.3f}  {tag}{mark}")
print(f"""
  PREDICTION P3 (new, from Yu et al.'s own correlation):
    the degree to which the 7.356 deg deficit localises at the twin
    boundaries is monotone in G/B.  Anchors: diamond 1.21 (strong, DFT),
    Si 0.68 (weaker, DFT), Au 0.157 (weakest, experiment).
    Falsifiable on any other fivefold-twinned material -- c-BN and SiC
    should behave like diamond; Ag, Al, Pb like gold; Ni and Ge in between.
    Ge (G/B = {hill(*C['Ge'])[1]/hill(*C['Ge'])[0]:.3f}) is the cheapest new DFT test: same structure
    as Si and diamond, G/B between Si and the metals.
""")

print("="*76)
print("BLOCK 4 — the corner rehybridisation: a mechanism metals cannot use")
print("="*76)
d_bulk, d_corner = 1.53, 1.245
single, double, triple = 1.54, 1.34, 1.20
print(f"""
  SI section 1, diamond with ideal (100) surfaces:
    bulk C-C bond            {d_bulk} A
    bond at the five corners {d_corner} A   -> contraction {100*(1-d_corner/d_bulk):.1f}%
    reference lengths: single {single} / double {double} / TRIPLE {triple} A
    1.245 A is {100*(d_corner/triple-1):.1f}% above the triple-bond length
  Yu et al.: "C(triple)C bonds are formed normal to the twin boundaries.
  Thus the total bond order is four at the corners, with the dangling bonds
  fully compensated."

  Silicon, same model: outermost Si-Si {2.33} A vs bulk {2.34} A
    -> contraction only {100*(1-2.33/2.34):.2f}%   (diamond: {100*(1-d_corner/d_bulk):.1f}%)

  => This is a FOURTH absorption mechanism, absent from the scale series:
        (e) chemical rehybridisation at the corners (sp3 -> sp1, bond order 4)
     It is available only to covalent materials with accessible multiple
     bonding.  Gold cannot do it at all.  Silicon barely does it.
     So the deficit's fate depends not only on SIZE (the R* axis) but on
     whether the BONDING can rehybridise -- a materials axis.
""")
print("ALL CHECKS COMPLETE")
