
# this is actually part of the test_target_calling_module test
__all__ = []

import repromancy
import pytest
import re
import sys

def test_target_calling_module():
    target = repromancy._target(repromancy.CallingModule)
    assert(target.package == 'test_targeting')
    assert(target.module == 'test_targeting')
    assert(target.qualname is None)
    assert(target.chain_to == {})
    
def test_target_module(emptyham):
    target = repromancy._target(emptyham)
    assert(target.package == 'emptyham')
    assert(target.module == 'emptyham')
    assert(target.qualname is None)
    assert(target.chain_to == {})
    
def test_target_type():
    class Type(type):
        pass
    target = repromancy._target(Type)
    assert(target.package == 'test_targeting')
    assert(target.module == 'test_targeting')
    assert(target.qualname == 'test_target_type.<locals>.Type')
    assert(target.chain_to == {
        "mro": Type.mro
    })
    
def test_target_class():
    class Class:
        pass
    target = repromancy._target(Class)
    assert(target.package == 'test_targeting')
    assert(target.module == 'test_targeting')
    assert(target.qualname == 'test_target_class.<locals>.Class')
    assert(target.chain_to == {})
    
def test_target_function():
    def function():
        pass
    target = repromancy._target(function)
    assert(target.package == 'test_targeting')
    assert(target.module == 'test_targeting')
    assert(target.qualname == 'test_target_function.<locals>.function')
    assert(target.chain_to == {})
    
def test_target_object():
    class Object:
        pass
    obj = Object()
    target = repromancy._target(obj)
    assert(target.package == 'test_targeting')
    assert(target.module == 'test_targeting')
    assert(re.match(
        r'<test_targeting\.test_target_object\.<locals>\.Object '
        r'object at 0x[\da-fA-F]+>',
        target.qualname,
    ))
    assert(target.chain_to == {})
    
def test_target_method():
    class Object:
        def thing(self):
            pass
    obj = Object()
    target = repromancy._target(obj.thing)
    assert(target.package == 'test_targeting')
    assert(target.module == 'test_targeting')
    assert(target.qualname == 'test_target_method.<locals>.Object.thing')
    assert(target.chain_to == {})
    
@pytest.mark.parametrize("target", [
    None,
    bool, True, False,
    int, -100, 0, 999,
    float, -101.1, 0.0, 999.9,
    str, 'hello world',
    bytes, b'hello world',
    object, type,
    repr, min, max, print,
    sys,
])
def test_target_builtin(target):
    with pytest.raises(ValueError):
        repromancy._target(target)
