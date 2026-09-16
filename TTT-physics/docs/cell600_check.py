import numpy as np, itertools, re
src=open("h_capacity.py").read()
# reuse definitions up to block 3
exec(src.split("# ---- block 3")[0].replace('"time_limit":15','"time_limit":120'))
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
D=np.linalg.norm(C[:,None,:]-C[None,:,:],axis=2)/edge
vals=np.unique(np.round(D[np.triu_indices(600,1)],6))[:6]
print("smallest site-site distances / metal edge:",vals)
print("d thresholds where a distance class reaches 2.1 A:",[round(RHH/v,4) for v in vals])
fcc_r={"tet-tet":1/np.sqrt(2),"tet-oct":np.sqrt(3)/(2*np.sqrt(2)),"oct-oct":1.0}
print("fcc thresholds:",{k:round(RHH/v,4) for k,v in fcc_r.items()})
def mis_status(P,thr):
    N=len(P); A=[]
    Dm=np.linalg.norm(P[:,None]-P[None],axis=2); I,J=np.where(np.triu(Dm<thr-1e-9,1))
    M=lil_matrix((len(I),N))
    for k,(i,j) in enumerate(zip(I,J)): M[k,i]=1; M[k,j]=1
    r=milp(c=-np.ones(N),constraints=LinearConstraint(M.tocsr(),-np.inf,1),integrality=np.ones(N),bounds=Bounds(0,1),options={"time_limit":240,"mip_rel_gap":0})
    return -r.fun, r.status, getattr(r,"mip_gap",None), r.mip_dual_bound if hasattr(r,"mip_dual_bound") else None
for d in (3.0,3.3,3.6):
    v,st,gap,bd=mis_status(C*(d/edge),RHH); print(d,"H/M",v/120,"status",st,"gap",gap,"dual bound H/M",None if bd is None else -bd/120,flush=True)
