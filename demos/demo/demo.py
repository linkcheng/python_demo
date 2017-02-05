# -*- coding: utf-8 -*-
# !/usr/bin/python


def analyse(word):
    rules = {
        'des': ['north', 'south', 'east', 'west'],
        'verb': ['go', 'stop'],
        'noun': ['door', 'bear'],
    }

    for k, v in rules.items():
        if word in v:
            return k
    else:
        return 'error'

if '__main__' == __name__:
    print(analyse('north'))
