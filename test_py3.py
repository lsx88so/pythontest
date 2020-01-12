#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, os

a = '01-24~01-30'
b = '01-19,01-23'
c = '01-24~01-30, 01-19,01-23'

print(a.split(','))
print(a.split(',')[0].split('~'))