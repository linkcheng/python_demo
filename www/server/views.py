#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


def index(req):
    return HttpResponse('hello')


def add(req):
    a = req.GET.get('a', 0)
    b = req.GET.get('b', 0)
    c = int(a) + int(b)
    return HttpResponse(str(c))


def add2(req, a, b):
    c = a + b
    return HttpResponse(str(c))


def home(req):
    return render(req, 'home.html')
