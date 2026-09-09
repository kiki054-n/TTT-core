
# Final TTT C60 curvature model
# Key insight: bistable potential needed
# sp2 well at 120° (graphene) and sp3 well at 109.47° (diamond)
# C60 sits between: 108° and 120° mixture
# Strain per atom = 0.4 eV * (R60/R)^2
# Total strain = N*E ~ 24 eV = 12 pentagons * 2 eV (topological invariant)
# This 12 corresponds to 37-model outer shell S3=12 (icosahedron vertices)

import numpy as np
R60=3.55
def curvature_per_atom(N):
    R=R60*np.sqrt(N/60)
    return 0.4*(R60/R)**2

for N in [60,240,540,960]:
    print(N, curvature_per_atom(N), N*curvature_per_atom(N))
