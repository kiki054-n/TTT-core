from fractions import Fraction as F
# Frank-Kasper coordination statistics per unit cell: {CN: count}
FK={"bcc (not FK, all-tet)":{14:2},"A15":{12:2,14:6},"C15":{12:16,16:8},"C14":{12:8,16:4},
    "Z (Zr4Al3)":{12:3,14:2,15:2},"sigma":{12:10,14:16,15:4},"mu (W6Fe7)":{12:7,14:2,15:2,16:2}}
dual_hydrate_framework={"A15":46,"C15":136,"Z (Zr4Al3)":40,"sigma":172}   # clathrate-hydrate duals (sI, sII, HS-I, TS-I)
known={"bcc (not FK, all-tet)":"CaH6, YH6 (synthesised)","A15":"La4H23, Eu8H46 (synthesised)","C15":"Li2CaH17 predicted (Chem. Mater. 2024)",
       "C14":"?","Z (Zr4Al3)":"not found in search","sigma":"not found in search","mu (W6Fe7)":"not found in search"}
rows=[]
for k,cn in FK.items():
    N=sum(cn.values()); Zb=F(sum(z*n for z,n in cn.items()),N)
    H=sum((z-2)*n for z,n in cn.items())//2 if all(True for _ in cn) else None
    H=F(sum((2*z-4)*n for z,n in cn.items()),4)          # each tetrahedral void shared by 4 atoms
    if k in dual_hydrate_framework: assert H==dual_hydrate_framework[k]
    f12=F(cn.get(12,0),N)
    rows.append((k,N,Zb,H,H/N,f12,known[k]))
assert rows[1][3]==46 and rows[2][3]==136
for r in rows: print(f"{r[0]:22s} atoms {r[1]:2d}  Zbar {float(r[2]):.3f}  H/cell {r[3]}  H/M {float(r[4]):.3f}  CN12(dodecahedral H20 cage) fraction {float(r[5]):.2f}  | {r[6]}")
