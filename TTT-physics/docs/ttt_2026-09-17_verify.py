"""TTT 検証スクリプト 2026-09-17（OπO の飽和・電荷構成・g 因子・S³ 幾何）
全ブロック assert 通過で終了する。依存: numpy, sympy
"""
import itertools, math
from collections import Counter
from fractions import Fraction as Fr
import numpy as np, sympy as sp

def cube(n): return list(itertools.product(range(n), repeat=3))

# --- Block 1: 角殻（中心六角数）と立方数 ---------------------------------
H = lambda k: 3*k*(k-1)+1
assert [H(k) for k in range(1,7)] == [1,7,19,37,61,91]
for n in range(1,12): assert sum(H(k) for k in range(1,n+1)) == n**3
assert 216-125 == 91 == H(6)
for n in range(1,12): assert len([p for p in cube(n) if max(p)==n-1]) == H(n)
print("B1 角殻: 1+7+19+37+61=125, +91=216  OK")

# --- Block 2: 偶奇分割（6^3 = 108+108）-----------------------------------
for n in range(2,9):
    P = Counter(sum(p)%2 for p in cube(n))
    assert (P[0]==P[1]) == (n%2==0)
P5 = Counter(sum(p)%2 for p in cube(5)); assert (P5[0],P5[1]) == (63,62)
assert sum((2,2,2))%2 == 0                      # 余りの1は中心点
sh91 = Counter(sum(p)%2 for p in cube(6) if max(p)==5); assert (sh91[0],sh91[1]) == (45,46)
assert 63+45 == 62+46 == 108
c = (2.5,2.5,2.5)
for par in (0,1):
    pts = [p for p in cube(6) if sum(p)%2==par]
    d = Counter(sum((p[i]-c[i])**2 for i in range(3)) for p in pts)
    assert [d[k] for k in sorted(d)] == [4,12,12,16,24,12,12,12,4]
    inner = [p for p in pts if sum((p[i]-2.5)**2 for i in range(3))==0.75]
    assert len({sum((a[i]-b[i])**2 for i in range(3)) for a,b in itertools.combinations(inner,2)}) == 1  # 正四面体
E6 = {p for p in cube(6) if sum(p)%2==0}; O6 = set(cube(6))-E6
assert {(5-y,x,z) for x,y,z in E6} == O6        # C4 は入れ替える
assert {(y,z,x) for x,y,z in E6} == E6          # C3<111> は保つ
assert {(5-x,5-y,z) for x,y,z in E6} == E6      # C2 は保つ
print("B2 偶奇: 125=63:62(差=中心), 91=45:46, 216=108:108, 各108は四面体孔中心, 入替はC4  OK")

# --- Block 3: fcc 四面体孔中心クラスターと 216 --------------------------
N=8
fcc = [(x,y,z) for x in range(-N,N+1) for y in range(-N,N+1) for z in range(-N,N+1) if (x+y+z)%2==0]
d = Counter(round(sum((p[i]-.5)**2 for i in range(3)),6) for p in fcc)
cum = list(itertools.accumulate(d[k] for k in sorted(d)))[:11]
assert cum == [4,16,28,44,68,80,104,140,152,180,216]
assert sorted(set(cum) & {k**3 for k in range(1,7)}) == [216]   # 途中の殻対応はない
print("B3 fcc四面体孔中心: 216 で閉じる, 累積の共通値は216のみ  OK")

# --- Block 4: 結合の数え上げ（表面/体積） -------------------------------
for n in range(1,15):
    bonds = 3*n*n*(n-1)
    assert Fr(bonds, n**3) == 3*(1-Fr(1,n))
print("B4 結合/点 = 3(1-A^(-1/3)), a_S/a_V = 1  OK")

# --- Block 5: 電荷構成（O=+1/6, π=-1/3） -------------------------------
O, PI = Fr(1,6), Fr(-1,3)
assert 2*O+PI == 0 and 6*O+6*PI == -1
u, dq = 4*O, PI
assert u == Fr(2,3) and dq == Fr(-1,3)
assert 2*u+dq == 1 and u+2*dq == 0
assert (8*O+PI) + (6*O+6*PI) == 0               # 水素 = 14O+7π = 7 OπO
print("B5 電荷表: u=4O, d=π, p=1OπO+6O, n=2OπO, e=6O+6π, H=7OπO  OK")

# --- Block 6: g 因子 ------------------------------------------------------
A,B,E,cc = sp.symbols('A B E c', positive=True)
mu = (3*cc**2/(2*E))*A + (-3*cc**2/E)*(-B)       # リング(+1)と軸(-2)逆回転, 各 E/3
g0 = sp.simplify(2*(E/cc**2)*mu/(-(A-B)))
assert sp.simplify(g0 - 3*(A+2*B)/(B-A)) == 0
assert sp.solve(sp.Eq(g0,2), A) == [] or all(s.is_negative for s in sp.solve(sp.Eq(g0,2),A))
x = sp.Symbol('x')
gS3 = 3/(2+x)                                    # S³, J_R 枝, x = 閉じ込め場の実効 cos2η
assert gS3.subs(x,0) == sp.Rational(3,2)          # クリフォード
assert gS3.subs(x,-sp.Rational(1,2)) == 2         # 位相三等分(60°,120°)
assert gS3.subs(x,-sp.Rational(1,3)) == sp.Rational(9,5)   # 面積(エネルギー)三等分=四面体角
for th in (60,120):
    assert sp.nsimplify((1-sp.cos(sp.pi*th/180))/2) in (sp.Rational(1,4),sp.Rational(3,4))
print("B6 g: R³逆回転のみでは2不可, S³クリフォード3/2, 位相三等分2, エネルギー三等分9/5  OK")

# --- Block 7: 双極＋差1 → 黄金比 ----------------------------------------
X = sp.Symbol('X', positive=True)
assert sp.solve(sp.Eq(X-1/X,1),X) == [(1+sp.sqrt(5))/2]
phi = (1+5**.5)/2
worst = lambda v: min(q*q*abs(v-round(v*q)/q) for q in range(2,3000))
assert worst(phi) > worst(2**.5) > worst(math.e) > worst(math.pi)
print("B7 x·(1/x)=1 かつ x-1/x=1 → φ, 最も有理近似されにくい  OK")

# --- Block 8: r⊗ω = 1 ⊕ 3 ⊕ 5 --------------------------------------------
rng = np.random.default_rng(0); r, w = rng.normal(size=3), rng.normal(size=3)
T = np.outer(r,w); tr = np.trace(T)/3*np.eye(3); asym = (T-T.T)/2; sym = (T+T.T)/2 - tr
assert np.allclose(tr+asym+sym, T) and abs(np.trace(sym))<1e-12
assert np.isclose(np.trace(T), r@w)
print("B8 r⊗ω = スカラー(1)+回転(3)+歪み(5)  OK")

# --- Block 9: 否定結果の数値 ---------------------------------------------
me, mp, mn = 0.51099895, 938.27208816, 939.56542052
assert abs(mp/me - round(mp/me)) > 0.1                     # 1836.15 は整数でない
D = mn-mp-me; assert abs(D-0.78233) < 1e-4
hc, rp = 197.3269804, 0.8409
conf = math.sqrt((hc*math.pi/rp)**2+me*me)-me; assert conf/D > 900   # 閉じ込め 942倍
ahc = hc/137.035999
U_uni = 0.6*ahc/(math.sqrt(5/3)*rp); U_gau = ahc/(2*math.sqrt(math.pi)*rp/math.sqrt(3))
U_exp = 5*ahc/(32*rp/math.sqrt(12))
assert 0.79 < U_uni < U_gau < U_exp < 0.93               # 形状で18%動く＝一致は偶然扱い
mmu=105.6583755; red=lambda m: m*mp/(m+mp); assert 185 < red(mmu)/red(me) < 187
assert abs(137.035999177-137) > 0.03                      # 137=125+12 は棄却
print("B9 否定: 質量比非整数, 閉じ込め942倍, 電荷自己エネルギー0.80-0.93MeV(形状依存), ミュオン軌道186倍  OK")
print("\nALL BLOCKS PASSED")
