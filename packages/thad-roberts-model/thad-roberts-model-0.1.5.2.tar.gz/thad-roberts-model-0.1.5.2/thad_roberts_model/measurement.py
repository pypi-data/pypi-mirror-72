import math
from decimal import *

getcontext().prec = 28

class Measurement():
    '''
    Class for measurement with error and multiplier.
    It has API to work correctly in equations expressions in python. 
    '''
    def __init__(self, value, error, multiplier = "1"):
        self.value = Decimal(value) * Decimal(multiplier)
        self.absolute_error = Decimal(error) * Decimal(multiplier)
        assert self.absolute_error >= Decimal("0"), "Absolute error should be greater or equal to 0"
        if self.value == Decimal("0"): 
            self.relatvive_error = Decimal("0")
        else:
            #TODO: Fix division by 0 problem correctly, see tests
            self.relatvive_error = abs(self.absolute_error/self.value)
        
    def recalc_absolute(self):
        #TODO: Fix division by 0 problem correctly, see tests
        self.absolute_error = abs(self.relatvive_error * self.value)
    
    def recalc_relative(self):
        self.relatvive_error = abs(self.absolute_error/self.value)

        
    def __add__(self, other):
        self.value += other.value
        self.absolute_error += other.absolute_error
        self.recalc_relative()
        return self
    
    def __sub__(self, other):
        self.value -= other.value
        self.absolute_error += other.absolute_error
        self.recalc_relative()
        return self

    def __mul__(self, other):
        self.value *= other.value
        self.relatvive_error += other.relatvive_error
        self.recalc_absolute()
        return self
    
    def __truediv__(self, other):
        self.value = self.value/other.value
        self.relatvive_error += other.relatvive_error
        self.recalc_absolute()
        return self    
    
    def __pow__(self, other):
        self.value **= other.value
        self.relatvive_error *= abs(other.value)
        self.recalc_absolute()
        return self
    
    def __neg__(self):
        self.value = -self.value
        return self
        
    def __pos__(self):
        self.value = self.value
        return self
    
    def __eq__(self, other):
        if self.absolute_error != Decimal("0"):
            if (self.value + self.absolute_error >= other.value - other.absolute_error) and (other.value + other.absolute_error >= self.value - self.absolute_error):
                return True
            else: return False
        else:
            return self.value == other.value
    
    def __ne__(self, other):
        return bool(~(self == other))
        
    def __str__(self):
        if self.absolute_error == Decimal("0"):
            return "%.7f" % self.value
        return "[ %.7f, +/- %.7f, +/- %10.7f %%]" %(self.value, self.absolute_error, Decimal('100') * self.relatvive_error)
    def mulit_line_str(self):
        return "[    %.7f    ] = VALUE\n(+/- %.7f, +/- %9.7f %%) = SYMMETRIC ERROR" %(self.value, self.absolute_error, Decimal('100') * self.relatvive_error)

def v(value):
    '''Function returning constant value as an exact measurement in equations where it is necessary'''
    return Measurement(value, error = '0')
