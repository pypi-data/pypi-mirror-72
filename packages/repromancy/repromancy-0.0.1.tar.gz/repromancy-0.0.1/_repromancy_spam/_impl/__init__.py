
from . import ham

class EggType(type):
    pass

class Egg:
    
    def __init__(self):
    
        class YolkType(type):
            pass
        self.YolkType = YolkType
    
        class Yolk:
            pass
        self.Yolk = Yolk
        
        def crack(self):
            pass
        self.crack = crack
        
    def roll(self):
        pass
        
egg = Egg()

def count_eggs():
    pass
