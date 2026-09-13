"""
Cheng et al. 2025 (Sci Adv 11, eaea9781) has now been OBTAINED.
Its actual numbers are used here to TEST the P2' prediction x_t/x_s = C*(G/B), q=1.
"""
import math
import numpy as np

print("="*78); print("BLOCK 0 - what Cheng et al. actually report"); print("="*78)
print("""
  Material: gold pentagonal prisms (FCC).  Sizes 26.0 and 52.5 nm edge length,
  four populations with truncation depths TD = 0.094, 0.184, 0.185, 0.373.

  Partition of the 7.356 deg angular deficit (normalised to 1.47 deg / domain):
                        EXPERIMENT (n=10)      MD / Lennard-Jones
      tensile              45.0 %  (0.66 deg)     0.68 deg
      shear                22.5 %  (0.33 deg)     0.30 deg
      rotational           32.5 %  (0.48 deg)     0.49 deg
      elastic input      E=88.0 GPa, nu=0.415   E=110 GPa, nu=0.36
      surface energy     1.52 J/m^2 {100}       1.609 J/m^2

  Mean tensile strain 0.97 % before heating -> 0.23 % after (relaxation).
  "Particle size plays a minor role in determining the equilibrium strain
   distribution" ... size is "more relevant to the fluctuations".
  Diamond / silicon / Pugh ratio / Yu et al.: NOT mentioned.
""")

print("="*78); print("BLOCK 1 - A1 is REFUTED by Cheng's own definition"); print("="*78)
print("""
  Cheng's tensile observable is the dimensionless ratio

        a_x / a_y  =  sqrt(2) * (1 + e_xx) / (1 + e_yy)

  a_x = lattice constant along the ANGULAR axis, a_y along the RADIAL axis.
  A purely hydrostatic in-plane dilation has e_xx = e_yy and CANCELS out of
  this ratio exactly.  So what closes the angular gap is the DIFFERENCE
  e_xx - e_yy -- a deviatoric normal-strain mode, not a volumetric one.

  v3's assumption A1 ("tensile <-> volumetric, shear <-> deviatoric") is
  therefore WRONG.  Both of Cheng's strain channels are deviatoric:
      tensile channel : e_theta-theta - e_rr   (deviatoric, normal)
      shear   channel : e_r-theta              (deviatoric, off-diagonal)
      rotation channel: rigid lattice rotation (ZERO strain energy)
  The bulk modulus B does not control the competition between them.
""")

print("="*78); print("BLOCK 2 - the quantitative test of q = 1"); print("="*78)
def GB_from_nu(nu): return 3*(1-2*nu)/(2*(1+nu))
exp = dict(tag="Cheng exp",  nu=0.415, xt=0.66, xs=0.33, xr=0.48)
sim = dict(tag="Cheng MD/LJ",nu=0.360, xt=0.68, xs=0.30, xr=0.49)
for d in (exp,sim):
    d["GB"]=GB_from_nu(d["nu"]); d["r"]=d["xt"]/d["xs"]
    print(f"  {d['tag']:>12}: nu={d['nu']:.3f}  G/B={d['GB']:.4f}  x_t/x_s={d['r']:.3f}"
          f"  x_r/(x_t+x_s)={d['xr']/(d['xt']+d['xs']):.3f}")
lev  = sim["GB"]/exp["GB"]; obs = sim["r"]/exp["r"]
print(f"\n  lever on G/B        : x{lev:.3f}")
print(f"  observed change in ratio: x{obs:.3f}")
print(f"  q = 1 predicts          : x{lev:.3f}   -> MISMATCH of {100*(lev/obs-1):.0f} %")
q = math.log(obs)/math.log(lev)
print(f"  best-fit exponent q = {q:.3f}   (NOT 1)")
C1 = exp["r"]/exp["GB"]
print(f"\n  with q=1 calibrated on the experiment, C = {C1:.2f}")
print(f"  -> predicts for the MD point  x_t/x_s = {C1*sim['GB']:.2f}, observed {sim['r']:.2f}")
print("  => P2' with q=1 is FALSIFIED by the only internal control that exists.")

print("="*78); print("BLOCK 3 - what the weak exponent does to the diamond prediction"); print("="*78)
MAT = {"Au":dict(C11=192.9,C12=163.8,C44=41.5),
       "Si":dict(C11=165.7,C12=63.9, C44=79.6),
       "diamond":dict(C11=1079.,C12=124.,C44=578.)}
def hill(C11,C12,C44):
    B=(C11+2*C12)/3.; GV=(C11-C12+3*C44)/5.
    GR=5*(C11-C12)*C44/(4*C44+3*(C11-C12)); return B,0.5*(GV+GR)
for k,p in MAT.items():
    p["B"],p["G"]=hill(p["C11"],p["C12"],p["C44"]); p["pugh"]=p["G"]/p["B"]
Cq = exp["r"]/exp["GB"]**q
print(f"  two-point fit:  x_t/x_s = {Cq:.3f} * (G/B)^{q:.3f}\n")
print(f"  {'material':>9} {'G/B(Hill)':>10} {'q=1 (v3)':>10} {'q=0.23':>9}")
for k in ("Au","Si","diamond"):
    p=MAT[k]
    print(f"  {k:>9} {p['pugh']:>10.3f} {C1*p['pugh']:>10.2f} {Cq*p['pugh']**q:>9.2f}")
print("""
  v3 predicted diamond x_t/x_s = 15.4 (tensile 63 %, shear 4 %).
  The two-point fit predicts ~3.1 -- i.e. almost the SAME as gold.
  The dramatic material contrast in v3 was an artefact of q = 1.
""")

print("="*78); print("BLOCK 4 - why weak dependence is the CORRECT expectation"); print("="*78)
print("""
  Closing an angular deficit is a purely GEOMETRIC (trace-free, in-plane)
  constraint.  Write the in-plane strain as
        e = (1/2) tr(e) I  +  e'      (e' deviatoric)
  Only e' changes angles.  Both of Cheng's strain channels are components of
  the SAME deviatoric tensor e', differing only by a 45 deg rotation of axes:
        tensile channel  ~ (e'_xx - e'_yy)/2
        shear   channel  ~  e'_xy
  In an ISOTROPIC solid these two are degenerate: they cost the identical
  modulus G, so their ratio is fixed by GEOMETRY alone and is completely
  independent of B (and of G).  => x_t/x_s should be a near-universal number.

  Cheng's two points (2.00 vs 2.27 across a 1.7x change in G/B) are exactly
  that: near-universality with a weak residual.
  The residual must come from ELASTIC ANISOTROPY, which breaks the
  degeneracy of the two deviatoric channels.  The relevant control parameter
  is therefore NOT G/B but the anisotropy of the two shear moduli:
        C44   (shear on {100}<010>)   vs   (C11 - C12)/2   (tetragonal shear)
  i.e. the Zener ratio A = 2 C44 / (C11 - C12).
""")
print(f"  {'material':>9} {'C44':>7} {'(C11-C12)/2':>12} {'Zener A':>8}")
for k in ("Au","Si","diamond"):
    p=MAT[k]; Cp=(p["C11"]-p["C12"])/2.; A=p["C44"]/Cp
    p["A"]=A
    print(f"  {k:>9} {p['C44']:>7.1f} {Cp:>12.1f} {A:>8.3f}")
print("""
  Gold A = 2.85 (strongly anisotropic), silicon A = 1.56, diamond A = 1.21.
  Au(LJ, fcc) is also anisotropic but with different constants -- which is
  plausibly the whole origin of the 2.00 -> 2.27 shift.
""")
print("="*78); print("BLOCK 5 - P4 (size dependence) is now in trouble"); print("="*78)
print("""
  v3's P4: the rotation share should GROW with particle size, because
  rotation is a strain-GRADIENT (bending) mode whose stiffness falls as
  1/R^2 while the strain channels are size-independent.

  Cheng et al. state the opposite for the MEAN:
      "Particle size plays a minor role in determining the equilibrium
       strain distribution"
  across 26.0 -> 52.5 nm (a factor 2.0), and instead attribute the size
  effect to the FLUCTUATIONS, with "larger particles exhibiting reduced
  variability".

  Two possible readings:
   (i) P4 is simply wrong: the rotation is NOT a bulk gradient mode but an
       interface/twin-boundary accommodation, whose cost per unit boundary
       area is size-independent -> the share is size-independent.
  (ii) A factor 2.0 in R is too small a lever: if the rotation share grows
       like x_r ~ 1 + (l/R)^2 with l a few nm, the change over 26->52 nm is
       a few percent, inside their scatter.  Then P4 survives but needs a
       much wider size range.
  Reading (ii) is testable: Lin et al. 2026 is a size-dependent 4D-STEM study.
  If Lin also finds a size-independent mean partition over a wide range,
  reading (i) wins and P4 must be withdrawn.

  Note what DOES show a size effect in Cheng: the variance.  A gradient
  mode with a length scale l would also reduce scatter in large particles
  (more averaging volume), so the variance result is NOT evidence for P4
  -- it is generic.
""")
print("ALL BLOCKS COMPLETE")
