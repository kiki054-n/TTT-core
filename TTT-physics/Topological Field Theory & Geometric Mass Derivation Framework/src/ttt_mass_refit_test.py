import math, itertools, random
pi = math.pi
alpha = 1/137.035999084
alpha_MZ = 1/127.952
alpha_s = 0.1179
me = 0.51099895000

exp = {"muon":105.6583755,"tau":1776.86,"up":2.16,"down":4.67,"strange":93.4,
       "charm":1270.0,"bottom":4180.0,"top":172690.0,
       "W":80377.0,"Z":91187.6,"H":125250.0}
R = {k: v/me for k,v in exp.items()}

print("="*70)
print("1. 修正 G3 ── タウを小出の関係式から解く")
print("="*70)
# (me+mmu+mtau) = (2/3)(sqrt me+sqrt mmu+sqrt mtau)^2  ->  solve for sqrt(mtau)=c
a, b = math.sqrt(me), math.sqrt(exp["muon"])
s = a + b
# c^2 - 4 s c + 3(a^2+b^2) - 2 s^2 = 0
A, B, C = 1.0, -4*s, 3*(a*a+b*b) - 2*s*s
disc = B*B - 4*A*C
c = (-B + math.sqrt(disc))/2
m_tau_koide = c*c
print(f"  小出解      m_tau = {m_tau_koide:.4f} MeV")
print(f"  実測        m_tau = {exp['tau']:.2f} ± 0.12 MeV")
print(f"  差 = {m_tau_koide-exp['tau']:+.4f} MeV = {(m_tau_koide/exp['tau']-1)*100:+.4f}%  ≈ {abs(m_tau_koide-exp['tau'])/0.12:.1f} sigma")
print(f"  旧実装 m_mu*(1+sqrt2 cos(2pi/9))^2 = {R['muon']*(1+math.sqrt(2)*math.cos(2*pi/9))**2:.2f} (比) vs 実測 {R['tau']:.2f}")

print()
print("="*70)
print("2. 修正 G2 ── v は導出されていない。標準模型の関係式で W, Z を出す")
print("="*70)
v = 246.21965 * 1000  # MeV, 入力（TTT からは導出されていない）
sin2 = 0.23122; sin_w = math.sqrt(sin2); cos_w = math.sqrt(1-sin2)
e_MZ = math.sqrt(4*pi*alpha_MZ)
g = e_MZ/sin_w
mW = g*v/2
mZ = mW/cos_w
print(f"  v/m_e = {v/me:,.0f}  （リポジトリのコメントの 481450 とほぼ一致。式は 5738 を返していた）")
print(f"  m_W  予測 {mW/1000:8.3f} GeV   実測 {exp['W']/1000:8.3f}   差 {(mW/exp['W']-1)*100:+.2f}%")
print(f"  m_Z  予測 {mZ/1000:8.3f} GeV   実測 {exp['Z']/1000:8.3f}   差 {(mZ/exp['Z']-1)*100:+.2f}%")
print(f"  m_H  ── 導出なし。旧コードの sqrt(2.427) は実測比 m_H/m_W = {exp['H']/exp['W']:.4f} の二乗 {(exp['H']/exp['W'])**2:.4f} を書き写したもの")

print()
print("="*70)
print("3. 修正後の全体判定")
print("="*70)
rows = [
 ("electron","1（基準）",1.0,R["muon"]*0+1.0,"定義"),
 ("muon","3/2a + (1/4)ln(1/a) - 6.788 a/pi", 3/(2*alpha)+0.25*math.log(1/alpha)-6.788*(alpha/pi), R["muon"],"手置き1個"),
 ("tau","小出の関係式を解く", m_tau_koide/me, R["tau"],"借用（小出1981）"),
 ("up","(pi/2)(1+as/pi)*2.58", (pi/2)*(1+alpha_s/pi)*2.58, R["up"],"手置き1個"),
 ("down","up + pi*1.57", (pi/2)*(1+alpha_s/pi)*2.58 + pi*1.57, R["down"],"手置き1個"),
 ("strange","6pi^3 (1-as/2pi)", 6*pi**3*(1-alpha_s/(2*pi)), R["strange"],"手置きなし"),
 ("charm","6pi^5/sqrt3 (1+as/pi)", 6*pi**5/math.sqrt(3)*(1+alpha_s/pi), R["charm"],"手置き1個"),
 ("bottom","6pi^5 sqrt2 (1-0.08as/pi)", 6*pi**5*math.sqrt(2)*(1-0.08*alpha_s/pi), R["bottom"],"手置き2個"),
 ("top","1/(a^2 sqrt2)(1-a/pi)", (1/(alpha**2*math.sqrt(2)))*(1-alpha/pi), R["top"],"手置き1個"),
 ("W","v * e(MZ)/(2 sin_w)", mW/me, R["W"],"v と sin2 が入力"),
 ("Z","m_W/cos_w", mZ/me, R["Z"],"同上"),
 ("H","導出なし", float('nan'), R["H"],"実測の書き写し"),
]
print(f"{'粒子':<9}{'理論比':>14}{'実験比':>14}{'差':>10}   {'自由な数'}")
for name, f, t, x, note in rows:
    if t != t:
        print(f"{name:<9}{'—':>14}{x:>14.2f}{'—':>10}   {note}")
    else:
        print(f"{name:<9}{t:>14.2f}{x:>14.2f}{(t/x-1)*100:>9.2f}%   {note}")

print()
print("="*70)
print("4. 帰無対照 ── 6pi^n × 単純因子 の語彙は何を当てられるか")
print("="*70)
factors = {"1":1,"sqrt2":math.sqrt(2),"1/sqrt2":1/math.sqrt(2),"sqrt3":math.sqrt(3),
           "1/sqrt3":1/math.sqrt(3),"2":2,"1/2":0.5,"pi":pi,"1/pi":1/pi,
           "sqrt2pi":math.sqrt(2)*pi,"3":3,"1/3":1/3,"sqrt5":math.sqrt(5),"phi":(1+math.sqrt(5))/2}
vocab = []
for n in range(1,10):
    for fn, fv in factors.items():
        vocab.append((f"6pi^{n} x {fn}", 6*pi**n*fv))
# QCD 補正 (1 +- k as/pi), k in 0..2 を許す
def reachable(target, tol=0.01):
    for name, val in vocab:
        for k in (0.0,0.5,1.0,2.0,-0.5,-1.0,-2.0):
            if abs(val*(1+k*alpha_s/pi)/target - 1) <= tol:
                return name
    return None

targets = {"strange":R["strange"],"charm":R["charm"],"bottom":R["bottom"],"top":R["top"],"tau":R["tau"]}
print("  実際の標的（許容 1%）:")
for k,v in targets.items():
    r = reachable(v)
    print(f"    {k:<9}{v:>12.2f}  ->  {r if r else '到達不可'}")

random.seed(1)
lo, hi = math.log(100), math.log(400000)
hits = 0; N = 2000
for _ in range(N):
    t = math.exp(random.uniform(lo,hi))
    if reachable(t): hits += 1
print(f"\n  無作為な標的 {N} 個（100〜400000 の対数一様）のうち到達可能: {hits} ({100*hits/N:.1f}%)")
print(f"  語彙サイズ: {len(vocab)} 式 x 7 補正 = {len(vocab)*7} 通り")
