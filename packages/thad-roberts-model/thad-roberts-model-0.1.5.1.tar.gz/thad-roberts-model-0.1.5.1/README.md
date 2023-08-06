# Thads Roberts Model Library
## The idea
Thads Roberts Model Library was built to check the properties, validity and level of confidence of Thads Roberts Model particles masses equations presented here:

https://vortex.institute/wp-content/uploads/2020/03/The-Boundaries-of-Fluid-Quantization-Draft-2020-03-30.pdf

and developed by organization called Vortex Institute (https://vortex.institute).
The model is also sometimes called as Non-Viscous Quantum Fluid Theory.

For the purpose of this library we will name Ramanujan-Soldner constant with RS abbreviation, and N real solution to the simple vortex equation as RSSVE_N.
The idea is to calculate values of RS+3+Pi predicted by each equation with error range, and confront it with exact RS+3+Pi value.
Particle masses are taken from NIST 2018 standard with symmetric error as a max of asymmetric errors if asymmetry is present.
Numerical calculations error problem was solved by applying Decimal class as a number representation. 

## Code form

It is standard pypi.org package.

## How to install

You can install last version from pypi.org using pip:

`pip install thad_roberts_model`

## How to use it?
Currently Library prints analytical report when:

```
from thad_roberts_model import *

ThadRobertsModel().verify()
```

is called.

## Results discussion

Above report shows that Thads Roberts Model is in agreement with physical mass data in the error range, but confidence level of equality with RS+3+Pi value is low for all except one equation.
Only one equation for NEUTRON, PROTON, ELECTRON triplet gives 6 digit accuracy for RS+3+Pi constant in base 10 system, which is very good result, but this is the only equation with such a good agreement.
One equation gives 2 digits accuracy, and three other equations give 1 digit accuracy.
There is also a question regarding reliability of mass measurement due to renormalization problem, but it is not a topic for this library.
Due to big errors of mass measurement and renormalization problem it will be very difficult to verify experimentally Thads Roberts Model masses equations except for the NEUTRON, PROTON, ELECTRON triplet.

## Versioning strategy
[revolutionary].[API].[code].[doc]
