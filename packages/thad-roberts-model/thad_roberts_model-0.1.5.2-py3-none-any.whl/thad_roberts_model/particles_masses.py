from .measurement import *

class PartliclesMasses:
    "NIST 2018 values with symmetric error as a max of asymmetric errors"
    HIGGS         = Measurement("125.18", "0.16", "1000")
    Z_BOSON       = Measurement("91.1876", "0.0021", "1000")
    W_BOSON       = Measurement("80.379", "0.012", "1000")
    PROTON        = Measurement("938.27208816", "0.00000029")
    NEUTRON       = Measurement("939.56542052", "0.00000054")
    ELECTRON      = Measurement("0.51099895000", "0.00000000015")
    DOWN_QUARK    = Measurement("4.7", "0.5")
    UP_QUARK      = Measurement("2.2", "0.5")
    CHARM_QUARK   = Measurement("1.275", "0.035", "1000")
    STRANGE_QUARK = Measurement("95", "9")
    MUON          = Measurement("105.6583755", "0.0000023")
    TOP_QUARK     = Measurement("172.76", "0.3", "1000")
    TAU           = Measurement("1776.86", "0.12")
    BOTTOM_QUARK  = Measurement("4.18", "0.04", "1000")