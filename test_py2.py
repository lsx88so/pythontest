#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sys, re

def getReplaceStr(xdr):
    repStr = r''
    for i in range(1, 4 + 1):
        if i == 3:
            repStr = repStr + xdr
        else:
            repStr = repStr + '\\' + str(i)
    return repStr

print getReplaceStr(" test ")

regstr = r'obbs:S:1.3:{{.*?}},(dr_[_\w]+);(.*)}}'
regstr1 = r'(obbs:S:1.3:{{.*?}},)(dr_[_\w]+;)(.*)(}})'
regstr2 = r'(obbs:S:1.3:{{.*?}},dr_[_\w]+;.*}})'

fi = r'./xdrview/tmp/test_ggprs_rating_2g_200k_cell_002'

with open(fi,'r') as f:
    line = f.readline()
    ma = re.search(regstr2,line)
    if ma:
        print ma.group()
        print len(ma.groups())
        #print ma.group(0)
        #print ma.group(1)
        #print ma.group(2)
        res = re.sub(regstr1,getReplaceStr(" test "),line)
        print res

for i in range(1, 1):
    print i
