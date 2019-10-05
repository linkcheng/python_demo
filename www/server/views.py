#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse
from server.models import User


def index(req):
    reps = HttpResponse()
    reps.content = json.dumps({
        'code': '201',
        'key': 'hello'
    })

    return reps


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


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.get_user(username, password)
        if user:
            return render(request, 'home.html')
        else:
            return HttpResponse('用户名或密码错误')
