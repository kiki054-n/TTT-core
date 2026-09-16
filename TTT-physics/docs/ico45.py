import numpy as np, itertools
phi=(1+5**.5)/2; u=np.ones(3)/np.sqrt(3)
def cyc(p):
    out=[]
    for s in itertools.product([1,-1],repeat=3):
        q=np.array(p)*s
        for k in range(3): out.append(np.roll(q,k))
    return out
uniq=lambda L:[p for i,p in enumerate(L) if not any(np.allclose(p,q) for q in L[:i])]
ico=uniq(cyc((0,1,phi)))
dod=uniq([np.array(p,float) for p in itertools.product([1,-1],repeat=3)]+cyc((0,1/phi,phi)))
assert len(ico)==12 and len(dod)==20
edges=[(a,b) for a,b in itertools.combinations(ico,2) if np.isclose(np.linalg.norm(a-b),2)]
assert len(edges)==30
mid=uniq([(a+b)/2 for a,b in edges])        # icosidodecahedron (30)
faces=[f for f in itertools.combinations(range(12),3) if all(np.isclose(np.linalg.norm(ico[i]-ico[j]),2) for i,j in itertools.combinations(f,2))]
fc=uniq([sum(ico[i] for i in f)/3 for f in faces]); assert len(faces)==20
# (1,1,1) must be a C3 axis of this icosahedron (a face-centre direction)
assert any(np.allclose(np.cross(c,u),0) for c in fc)
sets={"ico vertices":ico,"dod vertices":dod,"edge mids":mid,"face centres":fc}
pts=uniq(ico+dod+mid+fc+[np.zeros(3)])
ang=lambda d: np.degrees(np.arccos(np.clip(abs(d@u)/np.linalg.norm(d),0,1)))
hits=[]; allang=set()
for a,b in itertools.combinations(pts,2):
    d=b-a; x=ang(d); allang.add(round(x,6))
    if abs(x-45)<1e-9: hits.append((a,b))
# position vectors themselves (from centre)
pos_hits=[(k,p) for k,S in sets.items() for p in S if abs(ang(p)-45)<1e-9]
print("points:",len(pts)," distinct angles:",len(allang)," 45-deg pair directions:",len(hits)," from-centre hits:",len(pos_hits))
# exactness check in Q(sqrt5): represent a hit direction and verify cos^2 = 1/2 with high precision (mpmath)
import mpmath as mp; mp.mp.dps=50
P=mp.mpf(1+mp.sqrt(5))/2
if hits:
    a,b=hits[0]; d=b-a
    # recover exact coords as rationals in {1,phi}: solve d_i = r + s*phi with small rationals
    def rec(x):
        for den in (1,2,3,4,6):
            for s in range(-12,13):
                r=x*den-s*phi
                if abs(r-round(r))<1e-9: return (round(r),s,den)
    ex=[rec(xi) for xi in d]; print("exact coords (r,s,den) for r+s*phi over den:",ex)
    D=[mp.mpf(r)/den+mp.mpf(s)/den*P for r,s,den in ex]
    c2=(sum(D))**2/(3*sum(x*x for x in D)); print("cos^2 exact-ish:",mp.nstr(c2,40))
    print("sample pair a,b:",np.round(a,4),np.round(b,4))
# Q values reachable near 2/3
Q=sorted({round(1/(3*np.cos(np.radians(x))**2),6) for x in allang if x<89.9})
print("Q in [0.5,1]:",[q for q in Q if 0.5<=q<=1])

# ---- characterise hits and test the azimuth (mass ratios, Brannen delta)
me,mmu,mtau=0.51099895,105.6583755,1776.93
def label(p):
    for k,S in sets.items():
        if any(np.allclose(p,q) for q in S): return k
    return "centre"
fc111=[c for c in fc if np.allclose(np.cross(c,u),0) and c@u>0][0]
res=[]
for a,b in hits:
    d=b-a
    if d@u<0: d=-d
    la,lb=label(a),label(b)
    s2=np.sort(d**2); r=(s2[1]/s2[0], s2[2]/s2[0])
    s=np.abs(d); mu=s.sum()/3; c=(s/mu-1)/np.sqrt(2)
    dd=[x for x in np.linspace(0,2*np.pi/3,120001) if np.allclose(np.sort(np.cos(x+2*np.pi*np.arange(3)/3)),np.sort(c),atol=2e-4)]
    res.append((la,lb,round(np.linalg.norm(b-a),4),tuple(np.round(r,3)),round(dd[0],5) if dd else None))
for x in res: print(x)
print("target ratios:",round(mmu/me,3),round(mtau/me,3)," target delta 0.222226")

print("---- signed azimuth")
for a,b in hits:
    d=b-a
    if d@u<0: d=-d
    mu=d.sum()/3; c=(d/mu-1)/np.sqrt(2)          # c_k = cos(delta + 2pi k/3) in some order
    # delta from projection angle
    e1=np.array([1,-1,0])/np.sqrt(2); e2=np.array([1,1,-2])/np.sqrt(6)
    best=min((abs(np.sort(np.cos(x+2*np.pi*np.arange(3)/3))-np.sort(c)).max(),x) for x in np.linspace(0,2*np.pi/3,240001))
    print("face?",np.allclose(np.cross(b,u),0) or np.allclose(np.cross(a,u),0),"dot a.u<0:",a@u<0,"|a-b|",round(np.linalg.norm(a-b),4),
          "c:",np.round(np.sort(c),5),"delta:",round(best[1],6),"fit err",f"{best[0]:.1e}")
