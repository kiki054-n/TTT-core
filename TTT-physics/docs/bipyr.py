import numpy as np, itertools, math
from scipy.optimize import minimize
np.random.seed(3)

print("=== 双錐族 B_n（n角双錐）の骨組み ===")
for n in range(3,9):
    V=n+2; E=3*n; F=2*n
    reg = " <- 正八面体（唯一の正多面体）" if n==4 else ""
    print("  B_%d: 頂点%2d 辺%2d 面%2d  対称性 D_%dh%s"%(n,V,E,F,n,reg))

def vecs_bipyr(n):
    V=[[math.cos(2*math.pi*k/n),math.sin(2*math.pi*k/n),0] for k in range(n)]
    V+=[[0,0,1],[0,0,-1]]
    V=np.array(V,float); return V/np.linalg.norm(V,axis=1,keepdims=True)

print("\n=== 中心からの単位ベクトルとしての性質 ===")
for n in (3,4,5,6):
    V=vecs_bipyr(n); m=len(V)
    dots=sorted(set(round(V[i]@V[j],4) for i,j in itertools.combinations(range(m),2)))
    Mten=sum(np.outer(v,v) for v in V)
    iso=np.allclose(Mten,(m/3)*np.eye(3),atol=1e-9)
    print("  B_%d (%d本): |sum v|=%.4f  内積の種類=%s  等方タイトフレーム=%s"%(n,m,np.linalg.norm(V.sum(0)),dots,iso))
print("  -> どの双錐も全対等内積は不可能（軸-軸=-1 と 軸-赤道=0 が必ず別クラス）")

print("\n=== 正四面体二面角の閉じない話（決定的な数） ===")
dih=math.degrees(math.acos(1/3.0))
print("  正四面体の二面角 = arccos(1/3) = %.6f deg"%dih)
for k in (3,4,5,6):
    tot=k*dih
    print("   %d個を1辺のまわりに: %10.6f deg  -> 隙間 %+.6f deg"%(k,tot,360-tot))
print("  -> 5個は %.4f deg 閉じない（五角双錐＝五回双晶・十面体粒子のくさび欠損）"%(360-5*dih))
sa=3*math.acos(1/3.0)-math.pi
print("  頂点まわり: 正四面体の立体角 = %.6f sr, 20個 = %.6f sr vs 4pi = %.6f sr -> 不足 %.6f sr (%.2f%%)"
      %(sa,20*sa,4*math.pi,4*math.pi-20*sa,100*(4*math.pi-20*sa)/(4*math.pi)))
print("  Mackay二十面体の動径収縮: R/a = sin(2pi/5) = %.6f -> %.2f%% 短い"%(math.sin(2*math.pi/5),100*(1-math.sin(2*math.pi/5))))

print("\n=== トムソン問題: 双錐は解か ===")
def UG(x):
    P=x.reshape(-1,3); nn=np.linalg.norm(P,axis=1,keepdims=True); Q=P/nn
    diff=Q[:,None,:]-Q[None,:,:]; dm=np.linalg.norm(diff,axis=-1); np.fill_diagonal(dm,np.inf)
    U=0.5*np.sum(1.0/dm)
    gq=-np.sum(diff/dm[:,:,None]**3,axis=1)
    gp=(gq-np.sum(gq*Q,axis=1,keepdims=True)*Q)/nn
    return U,gp.ravel()
for n,lit in ((3,6.474691),(5,32.716949)):
    V=vecs_bipyr(n); N=len(V)
    best=1e9
    for _ in range(40):
        r=minimize(UG,np.random.normal(size=3*N),jac=True,method='L-BFGS-B',options={'maxiter':3000})
        best=min(best,r.fun)
    u=UG(V.ravel())[0]
    print("  N=%d  双錐 U=%.6f   大域最小 U=%.6f   差 %+.2e  (文献 %.6f)"%(N,u,best,u-best,lit))

print("\n=== 5配位サイトの局所エネルギー（k2汎関数、目標内積を振る） ===")
def E(V,c):
    return sum((V[i]@V[j]-c)**2 for i,j in itertools.combinations(range(len(V)),2))
tbp=vecs_bipyr(3); sqp=np.array([[1,0,0],[0,1,0],[-1,0,0],[0,-1,0],[0,0,1]],float)
pent5=np.array([[math.cos(2*math.pi*k/5),math.sin(2*math.pi*k/5),0] for k in range(5)],float)
for c,lab in ((-0.25,"c=-1/4 (4次元単体)"),(-1/3,"c=-1/3 (四面体)"),(-0.2,"c=-1/5")):
    print("  %-22s 三方両錐=%.4f 四角錐=%.4f 正五角形=%.4f"%(lab,E(tbp,c),E(sqp,c),E(pent5,c)))
print("  -> 目標内積を何に置いても三方両錐が最小（配置の順位は c に依らない）")

print("\n=== FCC/ダイヤ格子との接続 ===")
print("  FCC の空隙: 四面体サイト 8個/セル、八面体サイト 4個/セル = 2:1")
print("  八面体 = B_4 なので、双錐族の結晶学的メンバーはすでにダイヤ格子の中にある")
print("  B_5 は結晶学的禁止（5回軸）-> 5回双晶・十面体/二十面体粒子としてのみ現れる")
