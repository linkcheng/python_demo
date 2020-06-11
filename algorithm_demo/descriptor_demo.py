#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@module: descriptor_demo
@date: 2020-06-11 
"""


class Field:
    def __init__(self):
        print(f'Field __init__')

    def __get__(self, instance, owner):
        print(f'Field __get__ {instance}, {owner}')
        return self.value

    def __set__(self, instance, value):
        print(f'Field __set__ {instance}, {value}')
        self.value = value

    def __del__(self):
        self.value = None
        del self.value


class NonDataField:
    def __init__(self):
        print(f'Field __init__')

    def __get__(self, instance, owner):
        print(f'Field __get__ {instance}, {owner}')
        return "NonDataField"


class Model:
    age = Field()
    non_data = NonDataField()

    def __init__(self, name):
        self.name = name
        self.age = 1

    def __getattribute__(self, item):
        print(f'Model __getattribute__ {self} {item}')
        return object.__getattribute__(self, item)

    def __getattr__(self, item):
        print(f'Model __getattr__ {item}')
        return self.age


if __name__ == '__main__':
    obj = Model("hello")
    print(f'\nModel={Model}')
    print(f'obj={obj}\n')
    print(f'Model.__dict__ {Model.__dict__}\n')
    print(f'obj.__dict__ {obj.__dict__}\n')
    print(f'obj.age={obj.age}\n')
    print(f'obj.non_data={obj.non_data}\n')
    print(f'obj.name={obj.name}\n')
    print(f'obj.invalid={obj.invalid}\n')
