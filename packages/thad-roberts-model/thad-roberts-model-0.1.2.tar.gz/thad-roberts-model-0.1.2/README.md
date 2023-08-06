# Thads Roberts Model Library
Thads Roberts Model Library was built to check the properties, validity and level of confidence of Thads Roberts Model particles masses equations presented here:

https://vortex.institute/wp-content/uploads/2020/03/The-Boundaries-of-Fluid-Quantization-Draft-2020-03-30.pdf

For the purpose of this library we will name Ramanujan-Soldner constant with RS abbreviation, and N real solution to the simple vortex equation as RSSVE_N.
The idea is to calculate values of RS+3+Pi predicted by each equation witch error range, and confront it witch exact RS+3+Pi value.
Particle masses are taken from NIST 2018 standard with symmetric error as a max of asymmetric errors if asymmetry is present.
Numerical calculations error problem was solved by applying Decimal class as a number representation. 

Currently Library prints analytical report when:

```
from thad_roberts_model import *

ThadRobertsModel().verify()
```

is called.

Above report shows that Thads Roberts Model is in agreement with physical mass data in the error range, but confidence level of this agreement is very low.
Only one equation with NEUTRON, PROTON and ELECTRON gives 6 digit accuracy for RS+3+Pi constant in base 10 system.
One equation gives 2 digits accuracy, and three other equations give 1 digit accuracy.
There is also other unrelated question regarding reliability of mass measurement due to renormalization problem, but it is not a topic for this library.