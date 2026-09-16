import numpy as np
# CODATA/PDG-level constants
me=1.0; mmu=206.7682830; mp=1836.15267343; mtau=3477.23; mpi=273.13
alpha=1/137.035999177; c=299792458.0; a0=5.29177210903e-11
tau_mu=2.1969811e-6; tau_pi=2.6033e-8
red=lambda m,M: m*M/(m+M)
# 1 in a bound pair the lighter partner carries fraction M/(m+M) of orbital kinetic energy (equal |p|)
share=mp/(me+mp); assert abs(share-0.999456)<1e-6
share_mu=mp/(mmu+mp); assert abs(share_mu-0.8988)<1e-3
# 2 orbital radius ~ 1/reduced mass : electron (lightest charged) makes the largest orbits
radii={n:a0*red(me,mp)/red(m,mp) for n,m in {"e":me,"pi-":mpi,"mu":mmu,"tau":mtau}.items()}
assert max(radii,key=radii.get)=="e"
assert abs(radii["e"]/radii["mu"]-185.94)<0.05
# 3 muonic hydrogen still orbits ~1e12 times before decay -> "orbital" is not unique to the electron
T_H=2*np.pi*a0/(alpha*c); assert abs(T_H-1.5198e-16)<1e-19
T_mu=T_H*red(me,mp)/red(mmu,mp); n_orb=tau_mu/T_mu
assert 2.6e12<n_orb<2.8e12
T_pi=T_H*red(me,mp)/red(mpi,mp); assert tau_pi/T_pi>1e10
# 4 equilateral bipyramids: pole-pole distance vs edge (=1); only n=5 has poles nearly bonded
pole={}
for n in (3,4,5):
    R=1/(2*np.sin(np.pi/n)); pole[n]=2*np.sqrt(1-R**2)
assert abs(pole[3]-1.63299)<1e-4 and abs(pole[4]-np.sqrt(2))<1e-9 and abs(pole[5]-1.05146)<1e-4
assert min(pole,key=lambda n:abs(pole[n]-1))==5
# 5 closure defect around the pole axis if pole distance were forced to 1 (regular tetrahedra)
defect={n:360-n*np.degrees(np.arccos(1/3)) for n in (3,4,5,6)}
assert abs(defect[5]-7.3561)<1e-3 and defect[5]==min(abs(d) for d in defect.values())
print("all 5 blocks PASS")
print({k:f"{v:.3e}" for k,v in radii.items()}, f"orbits(mu-p)={n_orb:.2e}", pole, {k:round(v,3) for k,v in defect.items()})
