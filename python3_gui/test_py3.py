#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, os, copy, datetime

print(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))

a = '01-24~01-30'
b = '01-19,01-23'
c = '01-24~01-30, 01-19,01-23'

print(a.split(','))
print(a.split(',')[0].split('~'))

c = [1,2]
a = [1,2,3,c]
b = a[3]
d = copy.copy(a)
print(a,b,c,d)
b[1] = 1
print(a,b,c,d)
c[1] = 3
print(a,b,c,d)
x = 1
y = x
print(x,y)
y = 3
print(x,y)
