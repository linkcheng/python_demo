#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
