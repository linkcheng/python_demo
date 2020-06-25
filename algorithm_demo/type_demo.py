#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: type_demo 
@date: 2020-06-23 
"""

from abc import ABCMeta, abstractmethod
from collections import OrderedDict


class Demo:
    def __new__(cls, *args, **kwargs):
        print(f"__new__, {args, kwargs}")
        return object.__new__(cls)

    def __init__(self, *args, **kwargs):
        print(f"Demo __init__, {args, kwargs}")


class MyType(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        print(f'__prepare__ {name}, {bases}')
        return OrderedDict(a=1)

    def __new__(cls, *args, **kwargs):
        print(f"__new__, {args, kwargs}")
        return type.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"__init__, {args, kwargs}")

    def __call__(cls, *args, **kwargs):
        print(f"__call__, {args, kwargs}")
        obj = cls.__new__(cls, *args, **kwargs)
        obj.__init__(*args, **kwargs)
        return obj


class Foo(metaclass=MyType):
    def __init__(self):
        self.name = 'name'


def meth(self):
    print(f"Calling method={self.attr}")


class MyMeta(type):
    @classmethod
    def __prepare__(cls, name, baseClasses):
        return {'meth': meth}

    def __new__(cls, name, baseClasses, classdict):
        return type.__new__(cls, name, baseClasses, classdict)


def _check_methods(C, *methods):
    print(f"_check_methods C={C}, methods={methods}")
    mro = C.__mro__
    print(mro)
    for method in methods:
        for B in mro:
            if method in B.__dict__:
                if B.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented
    return True


class MySized(metaclass=ABCMeta):
    __slots__ = ()

    @abstractmethod
    def __len__(self):
        return 0

    @classmethod
    def __subclasshook__(cls, C):
        print(f"cls={cls}, C={C}")
        if cls is MySized:
            return _check_methods(C, "__len__")
        return NotImplemented


class Test(metaclass=MyMeta):
    attr = 'an attribute'

    def __init__(self):
        pass

    def __len__(self):
        return 0


a = Test()

isinstance(a, MySized)  # True


if __name__ == '__main__':
    pass
