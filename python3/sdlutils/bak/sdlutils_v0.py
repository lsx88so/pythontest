#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, copy, os, chardet
from sdlbase import sdlNode

class sdlDefine:
    def __init__(self, root_name, sdl_file):
        self.root = None
        self.root_name = root_name
        self.sdl_file = sdl_file

    def getSdlFile(self):
        exec_path = os.path.split(os.path.realpath(__file__))[0]
        if not os.path.exists(self.sdl_file):
            return None
        #raw = open(self.sdl_file, 'rb').read()
        #result = chardet.detect(raw)
        #encoding = result['encoding']
        with open(self.sdl_file, 'r', encoding="gbk") as fi:
            return fi.readlines()
    
    def getNodeByName(self, nodeList, searchDict, field_name):
        regBasic = r'^(int|string|float|xdr)'
        if re.search(regBasic, field_name):
            #print("getbasic")
            return sdlNode(field_name=field_name, field_type=field_name, field_length=0)
        if field_name in searchDict:
            index = searchDict[field_name]
            #print("getdict")
            return copy.deepcopy(nodeList[index])
        #print("getNode " + field_name + " None")
        return None

    def analyseSdlDefine(self):
        sdlLineList = self.getSdlFile()
        #print("start")
        if not sdlLineList:
            return None
        
        #print("start")
        regStruct = r'^struct\s*([0-9a-zA-Z_]+)'
        regStructEnd = r'};?'
        regMap = r'^map\s+aimap\s*<\s*([0-9a-zA-Z_]+)\s*\,\s*([0-9a-zA-Z_]+)\s*>\s+([0-9a-zA-Z_]+)\s*;'
        regList = r'^list\s+vector\s*<\s*([0-9a-zA-Z_]+)\s*>\s+([0-9a-zA-Z_]+)\s*;'
        regBasic = r'^(int|string|float|xdr)<?([0-9]*)>?\s*([0-9a-zA-Z_]+)\s*;'
        regOther = r'^([0-9a-zA-Z_]+)\s*([0-9a-zA-Z_]+)\s*;'

        nodeList = []
        searchDict = dict()
        flagStruct = False
        FlagStructEnd = True

        sdlNodeTmp = sdlNode()
        #print("sdlLineList length : " + str(len(sdlLineList)))
        for line in sdlLineList:
            line = re.sub(r'//.*|\n|\r', "", line).strip()
            #print("line length : " + str(len(line)))
            if len(line) == 0:
                #print("line 0")
                continue
            
            #print("line : " + line)
            if re.search(regStructEnd, line) and flagStruct and not FlagStructEnd:
                flagStruct = False
                FlagStructEnd = True
                #print("regStructEnd")
            elif re.search(regStruct, line):
                #print("regStruct")
                flagStruct = True
                FlagStructEnd = False
                mat = re.search(regStruct, line)
                sdlNodeTmp.field_type="struct"
                sdlNodeTmp.field_length=0
                sdlNodeTmp.field_name=mat.group(1)
            elif re.search(regMap, line):
                #print("regMap")
                flagStruct = False
                mat = re.search(regMap, line)
                sdlNodeTmp.field_type="map"
                sdlNodeTmp.field_length=0
                sdlNodeTmp.field_name=mat.group(3)
                key = mat.group(1)
                value = mat.group(2)
                #print("key : " + key + " value : " + value)
                nodeTmp1 = self.getNodeByName(nodeList, searchDict, key)
                if not nodeTmp1:
                    return None
                sdlNodeTmp.insertNode(nodeTmp1)

                nodeTmp2 = self.getNodeByName(nodeList, searchDict, value)
                if not nodeTmp2:
                    return None
                sdlNodeTmp.insertNode(nodeTmp2)
            elif re.search(regList, line):
                #print("regList")
                flagStruct = False
                mat = re.search(regList, line)
                sdlNodeTmp.field_type="list"
                sdlNodeTmp.field_length=0
                sdlNodeTmp.field_name=mat.group(2)
                key = mat.group(1)
                nodeTmp = self.getNodeByName(nodeList, searchDict, key)
                if not nodeTmp:
                    return None
                sdlNodeTmp.insertNode(nodeTmp)
            elif flagStruct:
                if re.search(regBasic, line):
                    #print("regBasic")
                    mat = re.search(regBasic, line)
                    field_length = mat.group(2)
                    if not field_length:
                        field_length = 0
                    nodeTmp= sdlNode(field_type=mat.group(1), field_length=field_length, field_name=mat.group(3))
                    sdlNodeTmp.insertNode(nodeTmp)
                elif re.search(regOther, line):
                    #print("regOther")
                    mat = re.search(regOther, line)
                    key = mat.group(1)
                    nodeTmp = self.getNodeByName(nodeList, searchDict, key)
                    if not nodeTmp:
                        return None
                    sdlNodeTmp.insertNode(nodeTmp)
            else:
                #print("continue")
                continue
            
            #print("FlagStructEnd : " + str(FlagStructEnd) + " flagStruct : "  + str(flagStruct))
            if FlagStructEnd and not flagStruct and not sdlNodeTmp.Empty():
                #print("insert")
                flagStruct = False
                FlagStructEnd = True
                nodeList.append(sdlNodeTmp)
                searchDict[sdlNodeTmp.field_name] = len(nodeList) - 1
                sdlNodeTmp = sdlNode()

        self.root = self.getNodeByName(nodeList, searchDict, self.root_name)

class sdlContent:
    def __init__(self, parent=None):
        pass
