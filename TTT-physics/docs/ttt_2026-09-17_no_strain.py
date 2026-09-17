"""電子の「歪み(5)ゼロ」条件と g=2 の同時解（S³ / スピン球面）
スピン1/2 の状態は球面上で ℓ=0(1) と ℓ=1(3) しか持たず ℓ=2(5) を持てない（ρ=(1+n·σ)/2）。
"""
import sympy as sp
fb,u,fr,fa = sp.symbols('f_b u f_r f_a', real=True)
P2 = lambda x: (3*x**2-1)/2
P4 = lambda x: (35*x**4-30*x**2+3)/8
# 配置: リング芯=北極(エネルギー f_r, 電荷+1), 軸芯=南極(f_a, 電荷-2), 閉じ込め場の対(f_b, 電荷0)を cosθ=±u
# J_R（単位 Eρ/c）と μ_R（単位 cρ）: 光速運動では μ はエネルギー配分に依らない
S  = (fr+fa)/2 - fb*u/2
mu = (sp.Rational(1,2) - 1)/2                      # (μ_ring - μ_axis)/2 = -1/4
g  = sp.simplify(2*mu/(-1*S))                      # g = 2mμ/(qS), m=E/c², q=-1
assert sp.simplify(g.subs({fr:sp.Rational(1,3),fa:sp.Rational(1,3),fb:sp.Rational(1,3),u:sp.Rational(1,2)}) - 2) == 0  # 前回の解を再現
E2 = (fr+fa)*1 + fb*P2(u)                          # エネルギーの ℓ=2
sol = sp.solve([sp.Eq(g.subs(fr+fa,1-fb),2), sp.Eq(E2.subs(fr+fa,1-fb),0)], [fb,u], dict=True)
sol = [s for s in sol if 0<s[fb]<=1 and -1<=s[u]<=1]
print('歪みゼロ ∧ g=2 の解:', sol)
assert len(sol)==1 and sol[0][fb]==sp.Rational(3,4) and sol[0][u]==-sp.Rational(1,3)
s=sol[0]
print('  閉じ込め場の配分 =',s[fb],'  リング+軸 =',1-s[fb])
print('  位置 cosθ = ±1/3 → θ =', [sp.N(sp.acos(v)*180/sp.pi,7) for v in (sp.Rational(1,3),-sp.Rational(1,3))],'度（正四面体角）')
# 前回の位相三等分解は歪みゼロを満たすか
E2_old = E2.subs({fr:sp.Rational(1,3),fa:sp.Rational(1,3),fb:sp.Rational(1,3),u:sp.Rational(1,2)})
print('前回(位相三等分)のエネルギー ℓ=2 =', E2_old); assert E2_old != 0
# 電荷の ℓ=2
Q2 = 1*1 + (-2)*1 + 0
print('電荷の ℓ=2 =', Q2, '（ゼロでない）'); assert Q2 == -1
# 電荷の ℓ=2 をゼロにする電荷配分（総電荷-1）
qra,qb = sp.symbols('q_ra q_b')
qs = sp.solve([sp.Eq(qra + qb*P2(sp.Rational(1,3)),0), sp.Eq(qra+qb,-1)],[qra,qb]); print('電荷ℓ=2ゼロの配分:', qs)
# 次の階数 ℓ=4
E4 = (1-s[fb]) + s[fb]*P4(sp.Rational(1,3)); print('エネルギー ℓ=4 =', E4)
print('OK')
