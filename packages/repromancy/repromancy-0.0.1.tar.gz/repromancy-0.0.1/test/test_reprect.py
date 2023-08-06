
import pickle
import pytest
import re
import repromancy
import sys

@pytest.fixture
def spam_target(spam):
    return repromancy._target(spam)
    
def test_reprect_module_not_in_package(emptyham, spam_target):
    assert(emptyham.__package__ == '')
    assert(emptyham.__name__ == 'emptyham')
    assert(emptyham.__spec__.name == 'emptyham')
    chain_target = repromancy._reprect(spam_target, 'emptyham', emptyham)
    assert(emptyham.__package__ == '')
    assert(emptyham.__name__ == 'emptyham')
    assert('emptyham' in sys.modules)
    assert(
        repr(emptyham) ==
        f'<module \'emptyham\' from {emptyham.__file__!r}>'
    )
    assert(chain_target is None)

def test_reprect_module(spam, spam_target):
    assert(spam.ham.__package__ == '_repromancy_spam._impl')
    assert(spam.ham.__name__ == '_repromancy_spam._impl.ham')
    assert(spam.ham.__spec__.name == '_repromancy_spam._impl.ham')
    chain_target = repromancy._reprect(spam_target, 'ham', spam.ham)
    assert(spam.ham.__package__ == '_repromancy_spam')
    assert(spam.ham.__name__ == '_repromancy_spam.ham')
    assert('_repromancy_spam.ham' in sys.modules)
    assert(
        repr(spam.ham) ==
        f'<module \'_repromancy_spam.ham\' from {spam.ham.__file__!r}>'
    )
    assert(chain_target.package == '_repromancy_spam')
    assert(chain_target.module == '_repromancy_spam.ham')
    assert(chain_target.qualname is None)
    assert(chain_target.chain_to == {
        "Public": spam.ham.Public,
    })
    
def test_reprect_class_not_in_package(spam_target):
    class BadEgg:
        pass
    assert(BadEgg.__module__ == 'test_reprect')
    assert(
        BadEgg.__qualname__ ==
        'test_reprect_class_not_in_package.<locals>.BadEgg'
    )
    assert(BadEgg.__name__ == 'BadEgg')
    chain_target = repromancy._reprect(spam_target, 'BadEgg', BadEgg)
    assert(BadEgg.__module__ == 'test_reprect')
    assert(
        BadEgg.__qualname__ ==
        'test_reprect_class_not_in_package.<locals>.BadEgg'
    )
    assert(BadEgg.__name__ == 'BadEgg')
    assert(chain_target is None)
    
def test_reprect_class(spam, spam_target):
    assert(spam.Egg.__module__ == '_repromancy_spam._impl')
    assert(spam.Egg.__qualname__ == 'Egg')
    assert(spam.Egg.__name__ == 'Egg')
    chain_target = repromancy._reprect(spam_target, 'Egg', spam.Egg)
    assert(spam.Egg.__module__ == '_repromancy_spam')
    assert(spam.Egg.__qualname__ == 'Egg')
    assert(spam.Egg.__name__ == 'Egg')
    assert(repr(spam.Egg) == '<class \'_repromancy_spam.Egg\'>')
    pickle.loads(pickle.dumps(spam.Egg))
    assert(chain_target.package == '_repromancy_spam')
    assert(chain_target.module == '_repromancy_spam')
    assert(chain_target.qualname  == 'Egg')
    assert(chain_target.chain_to == {
        "roll": spam.Egg.roll,
    })
    
def test_reprect_class_of_instance(spam, spam_target):
    assert(spam.egg.Yolk.__module__ == '_repromancy_spam._impl')
    assert(spam.egg.Yolk.__qualname__ == 'Egg.__init__.<locals>.Yolk')
    assert(spam.egg.Yolk.__name__ == 'Yolk')
    repromancy._reprect(spam_target, 'Egg', spam.Egg)
    egg_target = repromancy._target(spam.egg)
    chain_target = repromancy._reprect(egg_target, 'Yolk', spam.egg.Yolk)
    assert(spam.egg.Yolk.__module__ == '_repromancy_spam')
    assert(re.match(
        r'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.Yolk',
        spam.egg.Yolk.__qualname__
    ))
    assert(spam.egg.Yolk.__name__ == 'Yolk')
    assert(re.match(
        r'<class \'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.Yolk\'>',
        repr(spam.egg.Yolk)
    ))
    assert(chain_target.package == '_repromancy_spam')
    assert(chain_target.module == '_repromancy_spam')
    assert(re.match(
        r'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.Yolk',
        chain_target.qualname
    ))
    assert(chain_target.chain_to == {})
    
def test_reprect_type_class(spam, spam_target):
    assert(spam.EggType.__module__ == '_repromancy_spam._impl')
    assert(spam.EggType.__qualname__ == 'EggType')
    assert(spam.EggType.__name__ == 'EggType')
    chain_target = repromancy._reprect(spam_target, 'EggType', spam.EggType)
    assert(spam.EggType.__module__ == '_repromancy_spam')
    assert(spam.EggType.__qualname__ == 'EggType')
    assert(spam.EggType.__name__ == 'EggType')
    assert(repr(spam.EggType) == '<class \'_repromancy_spam.EggType\'>')
    pickle.loads(pickle.dumps(spam.EggType))
    assert(chain_target.package == '_repromancy_spam')
    assert(chain_target.module == '_repromancy_spam')
    assert(chain_target.qualname  == 'EggType')
    assert(set(chain_target.chain_to.keys()) == set(["mro"]))
    
def test_reprect_type_class_of_instance(spam, spam_target):
    assert(spam.egg.YolkType.__module__ == '_repromancy_spam._impl')
    assert(spam.egg.YolkType.__qualname__ == 'Egg.__init__.<locals>.YolkType')
    assert(spam.egg.YolkType.__name__ == 'YolkType')
    repromancy._reprect(spam_target, 'Egg', spam.Egg)
    egg_target = repromancy._target(spam.egg)
    chain_target = repromancy._reprect(
        egg_target, 'YolkType', spam.egg.YolkType
    )
    assert(spam.egg.YolkType.__module__ == '_repromancy_spam')
    assert(re.match(
        r'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.YolkType',
        spam.egg.YolkType.__qualname__
    ))
    assert(spam.egg.YolkType.__name__ == 'YolkType')
    assert(re.match(
        r'<class \'<_repromancy_spam.Egg object at '
        r'0x[\da-fA-F]+>\.YolkType\'>',
        repr(spam.egg.YolkType)
    ))
    assert(chain_target.package == '_repromancy_spam')
    assert(chain_target.module == '_repromancy_spam')
    assert(re.match(
        r'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.YolkType',
        chain_target.qualname
    ))
    assert(set(chain_target.chain_to.keys()) == set(["mro"]))
   
def test_reprect_function(spam, spam_target):
    assert(spam.count_eggs.__module__ == '_repromancy_spam._impl')
    assert(spam.count_eggs.__qualname__ == 'count_eggs')
    assert(spam.count_eggs.__name__ == 'count_eggs')
    chain_target = repromancy._reprect(
        spam_target, 'count_eggs', spam.count_eggs
    )
    assert(spam.count_eggs.__module__ == '_repromancy_spam')
    assert(spam.count_eggs.__qualname__ == 'count_eggs')
    assert(spam.count_eggs.__name__ == 'count_eggs')
    assert(re.match(
        r'<function \'_repromancy_spam.count_eggs\' at 0x[\da-fA-F]+>',
        repr(spam.count_eggs)
    ))
    assert(chain_target.package == '_repromancy_spam')
    assert(chain_target.module == '_repromancy_spam')
    assert(chain_target.qualname == 'count_eggs')
    assert(chain_target.chain_to == {})
   
def test_reprect_function_of_instance(spam, spam_target):
    assert(spam.egg.crack.__module__ == '_repromancy_spam._impl')
    assert(spam.egg.crack.__qualname__ == 'Egg.__init__.<locals>.crack')
    assert(spam.egg.crack.__name__ == 'crack')
    repromancy._reprect(spam_target, 'Egg', spam.Egg)
    egg_target = repromancy._target(spam.egg)
    chain_target = repromancy._reprect(egg_target, 'crack', spam.egg.crack)
    assert(spam.egg.crack.__module__ == '_repromancy_spam')
    assert(re.match(
        r'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.crack',
        spam.egg.crack.__qualname__
    ))
    assert(spam.egg.crack.__name__ == 'crack')
    print(spam.egg.crack)
    assert(re.match(
        r'<function \'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.crack\' '
        r'at 0x[\da-fA-F]+>',
        repr(spam.egg.crack)
    ))
    assert(chain_target.package == '_repromancy_spam')
    assert(chain_target.module == '_repromancy_spam')
    assert(re.match(
        r'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\.crack',
        chain_target.qualname
    ))
    assert(chain_target.chain_to == {})
        
def test_reperect_method(spam, spam_target):
    assert(spam.Egg.roll.__module__ == '_repromancy_spam._impl')
    assert(spam.Egg.roll.__qualname__ == 'Egg.roll')
    assert(spam.Egg.roll.__name__ == 'roll')
    Egg_target = repromancy._reprect(spam_target, 'Egg', spam.Egg)
    chain_target = repromancy._reprect(Egg_target, 'roll', spam.Egg.roll)
    assert(spam.Egg.roll.__module__ == '_repromancy_spam')
    assert(spam.Egg.roll.__qualname__ == 'Egg.roll')
    assert(spam.Egg.roll.__name__ == 'roll')
    assert(re.match(
        r'<function \'_repromancy_spam.Egg.roll\' at 0x[\da-fA-F]+>',
        repr(spam.Egg.roll)
    ))
    assert(chain_target.package == '_repromancy_spam')
    assert(chain_target.module == '_repromancy_spam')
    assert(chain_target.qualname == 'Egg.roll')
    assert(chain_target.chain_to == {})
        
def test_reperect_method_of_instance(spam, spam_target):
    assert(spam.egg.roll.__module__ == '_repromancy_spam._impl')
    assert(spam.egg.roll.__qualname__ == 'Egg.roll')
    assert(spam.egg.roll.__name__ == 'roll')
    repromancy._reprect(spam_target, 'Egg', spam.Egg)
    egg_target = repromancy._target(spam.egg)
    chain_target = repromancy._reprect(egg_target, 'roll', spam.egg.roll)
    assert(spam.egg.roll.__module__ == '_repromancy_spam._impl')
    assert(spam.egg.roll.__qualname__ == 'Egg.roll')
    assert(spam.egg.roll.__name__ == 'roll')
    assert(re.match(
        r'<bound method '
        r'\'<function \'_repromancy_spam._impl.Egg.roll\' at 0x[\da-fA-F]+>\' '
        r'of '
        r'\'<_repromancy_spam.Egg object at 0x[\da-fA-F]+>\'',
        repr(spam.egg.roll)
    ))
    assert(chain_target is None)
