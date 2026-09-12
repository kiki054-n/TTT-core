import numpy as np, math
from scipy.optimize import minimize
np.random.seed(5)
def LJg(x):
    P=x.reshape(-1,3); N=len(P)
    diff=P[:,None,:]-P[None,:,:]
    d2=np.sum(diff**2,axis=-1); np.fill_diagonal(d2,np.inf)
    inv6=d2**-3; inv12=inv6**2
    E=0.5*np.sum(4*(inv12-inv6))
    coef=0.5*(4*(-12*inv12+6*inv6)/d2)*2
    G=np.sum(coef[:,:,None]*diff,axis=1)*2
    return E,G.ravel()
for N,lit in ((4,-6.000000),(5,-9.103852),(6,-12.712062),(7,-16.505384),(13,-44.326801)):
    best=None; nr=200 if N<10 else 600
    for _ in range(nr):
        x0=np.random.normal(scale=0.55*N**(1/3),size=3*N)
        r=minimize(LJg,x0,jac=True,method='L-BFGS-B',options={'maxiter':4000})
        if best is None or r.fun<best.fun: best=r
    print("LJ%-2d E=%11.6f E/N=%9.6f  (文献 E=%.6f E/N=%.6f)"%(N,best.fun,best.fun/N,lit,lit/N))
    if N==7: np.save('p7.npy',best.x.reshape(7,3))
print("文書: LJ7 E/N=-2.007 / LJ13 E/N=-3.394")
