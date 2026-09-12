import numpy as np, itertools, math
P=np.load('p7.npy'); P-=P.mean(0)
d=np.linalg.norm(P[:,None,:]-P[None,:,:],axis=-1)
nn=np.sort(d,axis=1)[:,1]
cn=[int(np.sum(d[i]<1.30*nn[i]))-1 for i in range(7)]
poles=[i for i in range(7) if cn[i]==max(cn)]; eqs=[i for i in range(7) if i not in poles]
print("=== LJ7 大域最小の実測パラメータ（sigma単位） ===")
print("  近接数:",cn," 極:",poles," 赤道:",eqs)
pp=d[poles[0],poles[1]]
eqeq=sorted(d[i,j] for i,j in itertools.combinations(eqs,2))[:5]
eqpo=[d[i,p] for i in eqs for p in poles]
c=P[poles].mean(0); req=np.mean([np.linalg.norm(P[i]-c) for i in eqs])
print("  極-極 = %.4f   (文書 1.6000)"%pp)
print("  赤道最近接 平均 = %.4f  (文書 1.0748)"%np.mean(eqeq))
print("  赤道-極 平均   = %.4f  (文書 1.2149)"%np.mean(eqpo))
print("  r_eq = %.4f  r_ax = %.4f  (文書 0.9143 / 0.8000)"%(req,pp/2))
print("  極-極 / 赤道最近接 = %.4f"%(pp/np.mean(eqeq)))

print("\n=== 文書の幾何の内部整合（r_eq=0.9143, r_ax=0.8000） ===")
rq,rx=0.9143,0.8
print("  2 r_eq sin36        = %.4f  (文書 1.0748) OK"%(2*rq*math.sin(math.radians(36))))
print("  sqrt(r_eq^2+r_ax^2) = %.4f  (文書 1.2149) OK"%math.sqrt(rq**2+rx**2))
E=np.array([[rq*math.cos(2*math.pi*k/5),rq*math.sin(2*math.pi*k/5),0] for k in range(5)])
Q=np.array([[0,0,rx],[0,0,-rx]])
def ang(a,b,cc):
    u=a-b; v=cc-b
    return math.degrees(math.acos(np.clip(u@v/np.linalg.norm(u)/np.linalg.norm(v),-1,1)))
print("  赤道1-赤道0-赤道4 = %7.2f  (文書 108.0)"%ang(E[1],E[0],E[4]))
print("  上極-赤道0-下極   = %7.2f  (文書  82.4)"%ang(Q[0],E[0],Q[1]))
print("  上極-赤道0-赤道1  = %7.2f  (文書  63.8 はこれ)"%ang(Q[0],E[0],E[1]))
print("  ** 極での角: 赤道0-極-赤道1 = %7.2f / 赤道0-極-赤道2 = %7.2f"%(ang(E[0],Q[0],E[1]),ang(E[0],Q[0],E[2])))
print("  -> 108 deg は 4配位の赤道原子の面内角。5配位の極の角は 52.7 / 85.3 近辺で 108 ではない")

print("\n=== 正二十面体は「重層五角双錐」か ===")
phi=(1+math.sqrt(5))/2
I=[]
for s1 in(1,-1):
    for s2 in(1,-1):
        I+=[[0,s1,s2*phi],[s1,s2*phi,0],[s1*phi,0,s2]]
I=np.array(I,float); I/=np.linalg.norm(I,axis=1,keepdims=True)
k=np.argmax(I[:,2]); top=I[k]
dist=np.array([np.linalg.norm(v-top) for v in I])
cls=sorted(set(np.round(dist,4)))
print("  頂点0からの距離:",cls,"(文書 0 / 1.0515 / 1.7013 / 2.0000)")
edge=cls[1]
up=I[np.isclose(dist,cls[1],atol=1e-6)]; lo=I[np.isclose(dist,cls[2],atol=1e-6)]
print("  上五角形の中心からの距離 = %.4f (文書 0.8944)"%np.mean([np.linalg.norm(v-up.mean(0)) for v in up]))
azi=lambda Q: np.sort(np.degrees(np.arctan2(Q[:,1],Q[:,0]))%72)
print("  上五角形 方位(mod 72) =",np.round(azi(up),2))
print("  下五角形 方位(mod 72) =",np.round(azi(lo),2))
print("  -> 二つの五角形は 36 deg ずれ（五角逆プリズム）。単純な「赤道面の二重化」ではない")
bot=I[np.argmin(I[:,2])]
print("  下極-上五角形 距離 = %.4f  vs 辺長 %.4f -> 非結合"%(np.mean([np.linalg.norm(v-bot) for v in up]),edge))
print("  => {上極+上五角形+下極} は五角双錐ではない（両極が同じ五角形に結合しない）")

print("\n=== Tersoff g(theta) 再計算 ===")
cc,dd,h=3.8049e4,4.3484,-0.57058
g =lambda t: 1+cc**2/dd**2-cc**2/(dd**2+(math.cos(math.radians(t))-h)**2)
g2=lambda t: 1+cc**2/dd**2-cc**2/(dd**2+(math.cos(math.radians(t))+1/3)**2)
print("   theta     文書の主張     実際(h=-0.57058)      h=-1/3 版")
for t,cl in ((109.4712,"1.0 (最小)"),(108,"~1.0"),(63.8,"~1e4"),(82.4,"~1e3"),(120,"—"),(124.79,"—")):
    print("  %9.4f  %-12s %14.4e  %14.4e"%(t,cl,g(t),g2(t)))
print("  -> 4つ全部誤り。実際 g(108)=%.3e は g(109.47)=%.3e より大きく「108はほぼ最適」も偽"%(g(108),g(109.4712)))

print("\n=== 全辺等長の五角双錐は存在しない（7.356 deg の座標版） ===")
dih=math.degrees(math.acos(1/3))
print("  5個の正四面体を共有辺のまわり: 隙間 %.6f deg / 1個 %.6f deg"%(360-5*dih,(360-5*dih)/5))
k1=2*math.sin(math.radians(36))
print("  5回対称を課すと eqeq=%.5f r, pole-eq=sqrt(r^2+h^2/4)"%k1)
print("  h=eqeq とすると pole-eq=%.6f r に対し h=%.6f r -> 食い違い %.3f%%"
      %(math.sqrt(1+k1**2/4),k1,100*(k1/math.sqrt(1+k1**2/4)-1)))
