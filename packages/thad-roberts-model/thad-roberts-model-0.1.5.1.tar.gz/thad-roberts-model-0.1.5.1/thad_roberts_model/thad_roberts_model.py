from .measurement import *
from .particles_masses import *

class ThadRobertsModel(PartliclesMasses):
    RS_CONST = v("1.45136923488338105028396848589202744949303228")
    PI_CONST = v(math.pi)
    EQ_CONST = RS_CONST + v("3.0") + PI_CONST
    
    RSSVE_1 = v("0.0854245431533310")
    RSSVE_2 = v("3.667567534854999")
    
    RSSVE_5 = v("0.093474041000289951749648")
    RSSVE_6 = v("3.526755530609707752174473")
    
    RSSVE_CORRECTION = v("1") + ((RSSVE_1**v("2")) * (RSSVE_5**v("2")))/((RSSVE_2**v("2")) * (RSSVE_6**v("2")))
    
    def __init__(self):
        self.equations = {}
    
    def verify(self):
        self.equations[('HIGGS', 'Z_BOSON', 'W_BOSON')] = ((v("3")**v("2"))*(self.HIGGS - self.Z_BOSON))/((((v("2")**v("-1")))*self.W_BOSON)*self.RSSVE_CORRECTION)
        self.equations[('NEUTRON', 'PROTON', 'ELECTRON')] = ((v("3")**v("1"))*(self.NEUTRON - self.PROTON))/((((v("2")**v("0")))*self.ELECTRON)*self.RSSVE_CORRECTION)
        self.equations[('DOWN_QUARK', 'UP_QUARK', 'ELECTRON')] = ((v("3")**v("1"))*(self.DOWN_QUARK - self.UP_QUARK))/((((v("2")**v("1")))*self.ELECTRON)*self.RSSVE_CORRECTION)
        self.equations[('CHARM_QUARK', 'STRANGE_QUARK', 'MUON')] = ((v("3")**v("1"))*(self.CHARM_QUARK - v("2")*self.STRANGE_QUARK))/((((v("2")**v("2")))*self.MUON)*self.RSSVE_CORRECTION)
        self.equations[('TOP_QUARK', 'TAU', 'BOTTOM_QUARK')] = ((v("3")**v("1"))*(self.TOP_QUARK - v("2")*self.TAU))/((((v("2")**v("4")))*self.BOTTOM_QUARK)*self.RSSVE_CORRECTION)
        
        for eq_key, value in self.equations.items():
            print("RS+3+PI calculation for equation", eq_key, ":")
            print("[   ", self.RS_CONST, "= RS+3+PI", "   ]")
            print(value.mulit_line_str())
            print("are equal in measurement error range." if value == self.EQ_CONST else "are not equal in measurement error range.", end = "\n\n")