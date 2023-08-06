"""

                 ▄▀▀▄▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄  
                █   █   █ ▐  ▄▀   ▐ █   █   █ █   █   █ █      █ 
                ▐  █▀▀█▀    █▄▄▄▄▄  ▐  █▀▀▀▀  ▐  █▀▀█▀  █      █ 
                 ▄▀    █    █    ▌     █       ▄▀    █  ▀▄    ▄▀ 
                █     █    ▄▀▄▄▄▄    ▄▀       █     █     ▀▀▀▀   
                ▐     ▐    █    ▐   █         ▐     ▐            
                           ▐        ▐                            
                  ▄▀▀▄ ▄▀▄  ▄▀▀█▄   ▄▀▀▄ ▀▄  ▄▀▄▄▄▄   ▄▀▀▄ ▀▀▄    
                 █  █ ▀  █ ▐ ▄▀ ▀▄ █  █ █ █ █ █    ▌ █   ▀▄ ▄▀    
                 ▐  █    █   █▄▄▄█ ▐  █  ▀█ ▐ █      ▐     █      
                   █    █   ▄▀   █   █   █    █            █      
                 ▄▀   ▄▀   █   ▄▀  ▄▀   █    ▄▀▄▄▄▄▀     ▄▀       
                 █    █    ▐   ▐   █    ▐   █     ▐      █        
                 ▐    ▐            ▐        ▐            ▐

"""

# Copyright 2020 Erik Soma
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__all__ = ['cast', 'CallingModule']

# python
import collections
import functools
import importlib.abc
import inspect
import logging
import sys
import weakref
# repromancy
import _repromancy # warning: terrifying enchantments contained herein

LOG_NAME = 'repromancy'
log = logging.getLogger(LOG_NAME)

class CallingModule:
    pass

def cast(target):
    targets = [_target(target, depth=1)]
    while targets:
        target = targets.pop()
        for k, v in target.chain_to.items():
            try:
                is_already_casted_on = v in _casted_on
            except TypeError:
                continue
            if is_already_casted_on:
                if __debug__:
                    location = target.module
                    if target.qualname:
                        location = f'{location}.{target.qualname}'
                    log.info(
                        f'{v} has already been casted on, but encountered it '
                        f'again as {location}.{k}'
                    )
                continue
            original_repr = repr(v)
            chain_target = _reprect(target, k, v)
            if chain_target:
                log.info(f'{original_repr} casted to {v!r}')
                _casted_on.add(v)
                targets.append(chain_target)
                
_BUILTIN_PACKAGES = set(sys.builtin_module_names + ('builtins',))
                
def _target(obj, depth=0):
    # get the necessary information for performing repromancy on the target
    # object, turning it into a _Target
    if obj is CallingModule:
        target = _target_calling_module(depth + 1)
    elif inspect.ismodule(obj):
        target = _target_module(obj)
    elif inspect.isclass(obj):
        target = _target_class(obj)
    elif inspect.isfunction(obj):
        target = _target_function(obj)
    elif inspect.ismethod(obj):
        target = _target_method(obj)
    elif isinstance(obj, object):
        target = _target_object(obj)
    else:
        raise TypeError(f'invalid target {obj}')
    if target.package in _BUILTIN_PACKAGES:
        raise ValueError(f'{obj!r} is builtin')
    return target
                
def _target_calling_module(depth=0):
    # looks up the call stack to find the module in which this function was
    # called
    # use depth to adjust how many frames to look up the stack
    call_frame = inspect.currentframe().f_back
    for i in range(depth):
        call_frame = call_frame.f_back
    call_globals = call_frame.f_globals
    return _Target(
        _package_from_module_name(call_globals["__name__"]),
        call_globals["__name__"],
        None,
        _chain_to_from_globals(call_globals)
    )
    
def _target_module(module):
    return _Target(
        _package_from_module_name(module.__name__),
        module.__name__,
        None,
        _chain_to_from_module(module)
    )
    
def _target_class(cls):
    return _Target(
        _package_from_module_name(cls.__module__),
        cls.__module__,
        cls.__qualname__,
        _chain_to_from(cls),
    )
    
def _target_function(func):
    return _Target(
        _package_from_module_name(func.__module__),
        func.__module__,
        func.__qualname__,
        _chain_to_from(func),
    )
    
def _target_method(method):
    return _Target(
        _package_from_module_name(method.__module__),
        method.__module__,
        method.__qualname__,
        _chain_to_from(method),
    )
    
def _target_object(obj):
    return _Target(
        _package_from_module_name(obj.__class__.__module__),
        obj.__class__.__module__,
        repr(obj),
        _chain_to_from(obj),
    )
    
def _chain_to_from(thing):
    return {
        k: getattr(thing, k)
        for k in dir(thing)
        if (
            # its possible for something to be returned by dir, but for it to
            # not be accessible through getattr, for example when using
            # __slots__ and something it hasn't been assigned yet
            hasattr(thing, k) and
            # ignore dunders
            not (k.startswith('__') and k.endswith('__'))
        )
    }
    
def _chain_to_from_module(module):
    chain_to = _chain_to_from(module)
    if hasattr(module, "__all__"):
        chain_to = { k: v for k, v in chain_to.items() if k in module.__all__}
    return chain_to
    
def _chain_to_from_globals(module_dict):
    chain_to = {
        k: v
        for k, v in module_dict.items()
        if (not (k.startswith('__') and k.endswith('__')))
    }
    if "__all__" in module_dict:
        chain_to = {
            k: v
            for k, v in chain_to.items()
            if k in module_dict["__all__"]
        }
    return chain_to
    
def _package_from_module_name(module_name):
    return module_name.split('.')[0]
                
# we keep track of anything we've casted repromancy on so we don't try to do it
# again
#
# it may seem better to stick a hidden value on the object, but if that object
# is using slots that's impossible and if it has slots with a __dict__ we don't
# want to force the creation of a dict just for repromancy
_casted_on = weakref.WeakSet()
                
# calculated state information about something we've casted repromancy on
_Target = collections.namedtuple(
    "_Target",
    ['package', 'module', 'qualname', 'chain_to']
)
      
def _reprect(target, key, value):
    # casts repromancy on the value such that it will act like it was created
    # within the context of target.key
    if target.qualname is None:
        qualname_prefix = ''
    else:
        qualname_prefix = target.qualname + '.'
        
    if inspect.ismodule(value):
        return _reprect_module(target, qualname_prefix, key, value)
    elif inspect.isclass(value):
        return _reprect_class(target, qualname_prefix, key, value)
    elif inspect.isfunction(value):
        return _reprect_function(target, qualname_prefix, key, value)

def _reprect_module(target, qualname_prefix, key, module):
    original_module_package = module.__package__
    original_module_name = module.__name__
    
    module_package = _package_from_module_name(module.__name__)
    
    if module_package != target.package:
        log.debug(f'{module} is not in {target.package}')
        return None
        
    try:
        module.__package__ = f'{target.package}'
        module.__spec__.name = module.__name__ = f'{target.module}.{key}'
    except AttributeError as ex:
        log.warn(f'{module} is immune to repromancy: {ex}')
        return None

    sys.modules[module.__spec__.name] = module
    _module_specs[module.__spec__.name] = module.__spec__
    
    # monkey patch the module's loader to reset this repr data on reload
    original_exec_module = module.__loader__.exec_module
    def exec_module(module):
        module.__package__ = original_module_package
        module.__spec__.name = module.__name__ = original_module_name
        return original_exec_module(module)
    module.__loader__.exec_module = exec_module
        
    return _target_module(module)
    
def _reprect_class(target, qualname_prefix, key, cls):
    cls_package = _package_from_module_name(cls.__module__)
    
    if cls_package != target.package:
        log.debug(f'{cls} is not in {target.package}')
        return None
        
    try:
        cls.__module__ = target.module
        cls.__qualname__ = f'{qualname_prefix}{key}'
        cls.__name__ = key
    except TypeError as ex:
        log.warn(f'{cls} is immune to repromancy: {ex}')
        return None
        
    if inspect.isclass(cls) and not issubclass(cls, _Repr):
        cls_type = cls.__class__
        if (not cls_type is type and
            not issubclass(cls_type__, _ReprClass)):
            cls_type.__bases__ = cls_type.__bases__[:-1] + (_ReprClass, type)
        try:
            cls.__bases__ += (_Repr,)
        except TypeError:
            _wrap_class_repr(cls)
            
    

    return _target_class(cls)
    
def _reprect_function(target, qualname_prefix, key, function):
    function_package = _package_from_module_name(function.__module__)
    
    if function_package != target.package:
        log.debug(f'{function} is not in {target.package}')
        return None
        
    function.__module__ = target.module
    function.__qualname__ = f'{qualname_prefix}{key}'
    function.__name__ = key
    
    return _target_function(function)
    
class _ReprLoader(importlib.abc.Loader):
    
    def find_spec(self, fullname, path, target=None):
        spec = _module_specs.get(fullname)
        if spec:
            spec.name = fullname
        return spec
        
_module_specs = {}
        
sys.meta_path.append(_ReprLoader())

# this gets patched into the a repromancy'd class's __class__.__bases__, see
# _cls_full_name on why this is necessary
class _ReprClass(type):
    
    def __repr__(cls):
        return f'<class \'{_cls_full_name(cls)}\'>'
        
# this gets patched into a repromancy'd class's __bases__, see _cls_full_name
# on why this is necessary
class _Repr(metaclass=_ReprClass):
    
    def __repr__(self):
        repr = ' '.join(object.__repr__(self).split(' ')[1:])
        return f'<{_cls_full_name(self.__class__)} {repr}'
        
# objects that inherit directly from object cannot have their bases changed,
# so rather than patching in the _Repr class we have to edit the repr after
# the fact by using a wrapper
def _wrap_class_repr(obj):
    original_repr = obj.__repr__
    @functools.wraps(obj.__repr__)
    def wrapped_repr(self, *args, **kwargs):
        repr = original_repr(self, *args, **kwargs)
        if repr.startswith('<{self.package}.{self.__qualname__} '):
            repr = ' '.join(repr.split(' ')[1:])
            repr = f'<{_cls_full_name(self.__class__)} {repr}'
        return repr
    obj.__repr__ = wrapped_repr
        
# the default repr for types and objects is usually okay, but it starts to
# break down when we're dealing with classes that are created as part of an
# instance
#
# for example, we have a class A in which a new class is created on
# instantiation called B, the default repr for that B would be something like:
# module.A.__init__.<locals>.B
#
# which is marginally useful, but repromancy can do better by using the A
# instance's repr as the qualname for that B class:
# module.<module.A object at 0x0000016AB1B281D0>.B
#
# there is that redundant "module.<module..." part though
#
# we can, then eliminate the module when the qualified name is an instance,
# which is what this function ultimately does
#
# for the truly curious, you may wonder how we deal with classes that inherit
# directly from type, to know the answer is true terror, but if you have the
# nerves required to bare witness to such sacrilege seek ~_repromancy.c~
def _cls_full_name(cls):
    if cls.__qualname__.startswith('<'):
        return cls.__qualname__
    return f'{cls.__module__}.{cls.__qualname__}'
