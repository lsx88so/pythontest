#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, copy, os, json
from sdlbase import sdlNode
try: import cchardet as chardet
except ImportError: import chardet
try: import cpickle as pickle
except ImportError: import pickle

class sdlDefine:
    '''
    data:
    :key field_type: 数据域，数据类型，类型string
    :key field_name: 数据域，字段名，类型string
    :key field_length: 数据域，字段定义的长度，类型string
    :key field_value: 数据域，字段值，类型string
    :key field_seq: 对应树的真实子节点序号，类型int
    :key field_note: 备注信息，如记录子节点类型，类型string
    '''
    def __init__(self, root_name, sdl_file, sdl_dump_path):
        self.root = None
        self.root_name = root_name
        self.sdl_file = sdl_file
        self.sdl_dump_path = sdl_dump_path

    def printSdlTree(self, inNode=None, indent=0, prefix="", flag=False):
        """print tree to string"""
        if not inNode:
            inNode = self.root
        nodeLength = inNode.data["field_length"] if inNode.data["field_length"] else 0
        nodeType = inNode.data["field_type"]
        if inNode.data["field_type"] == "int":
            nodeType = nodeType + nodeLength
        nodeName = nodeType + "_" + str(inNode.index)  + "_" + inNode.data["field_name"]

        if flag and indent == 0:
            tab = prefix
            prefix = prefix + "|    "
        elif flag and indent > 0:
            tab = prefix[0:len(prefix)-2] + "|\n" + prefix[0:len(prefix)-2] + "|- "
            prefix = prefix + "|    "
        else:
            tab = '    ' * (indent - 1) + ' |- ' if indent > 0 else ''
            prefix = ""
        print('%s%s' % (tab, nodeName))
        
        for obj in inNode.children:
            self.printSdlTree(inNode=obj, indent=indent + 1, prefix=prefix, flag=flag)
    
    def dumpSdlDefine(self):
        with open(self.sdl_dump_path, 'wb') as fi:
            pickle.dump(self.root, fi)

    def loadSdlDefine(self):
        with open(self.sdl_dump_path, 'rb') as fi:
            self.root = pickle.load(fi)

    def getSdlFile(self):
        exec_path = os.path.split(os.path.realpath(__file__))[0]
        if not os.path.exists(self.sdl_file):
            return None
        raw = open(self.sdl_file, 'rb').read()
        result = chardet.detect(raw)
        encoding = result['encoding']
        with open(self.sdl_file, 'r', encoding=encoding) as fi:
            return fi.readlines()
    
    def getNodeByName(self, nodeList, searchDict, field_name):
        regBasic = r'^(int|string|float|xdr)'
        if re.search(regBasic, field_name):
            #print("getbasic")
            nodeData = {
                "field_type" : field_name,
                "field_name" : field_name,
                "field_length" : 0
            }
            return sdlNode(data=nodeData)
        if field_name in searchDict:
            index = searchDict[field_name]
            #print("getdict")
            #return copy.deepcopy(nodeList[index])
            nodeTmp1 = copy.deepcopy(nodeList[index])
            if nodeTmp1.data["field_type"] == "map":
                nodeData = {
                    "field_type" : "list",
                    "field_name" : "maplist",
                    "field_length" : 0
                }
                nodeTmp2 = sdlNode(data=nodeData)
                nodeTmp2.insertNode(nodeTmp1)
                return nodeTmp2
            return nodeTmp1
        #print("getNode " + field_name + " None")
        return None

    def analyseSdlDefine(self):
        sdlLineList = self.getSdlFile()
        #print("start")
        if not sdlLineList:
            return -1
        
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

        nodeData = {
            "field_type" : None,
            "field_name" : None,
            "field_length" : None
            #"field_value" : None,
            #"field_seq" : None
        }
        sdlNodeTmp = sdlNode(data=nodeData)
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
                sdlNodeTmp.data["field_name"] = mat.group(1)
                sdlNodeTmp.data["field_type"] = "struct"
                sdlNodeTmp.data["field_length"] = 0
            elif re.search(regMap, line):
                #print("regMap")
                flagStruct = False
                mat = re.search(regMap, line)
                sdlNodeTmp.data["field_name"] = mat.group(3)
                sdlNodeTmp.data["field_type"] = "map"
                sdlNodeTmp.data["field_length"] = 0
                
                key = mat.group(1)
                value = mat.group(2)
                #print("key : " + key + " value : " + value)
                nodeTmp1 = self.getNodeByName(nodeList, searchDict, key)
                if not nodeTmp1:
                    return -2
                sdlNodeTmp.insertNode(nodeTmp1)

                nodeTmp2 = self.getNodeByName(nodeList, searchDict, value)
                if not nodeTmp2:
                    return -2
                sdlNodeTmp.insertNode(nodeTmp2)
            elif re.search(regList, line):
                #print("regList")
                flagStruct = False
                mat = re.search(regList, line)
                sdlNodeTmp.data["field_name"] = mat.group(2)
                sdlNodeTmp.data["field_type"] = "list"
                sdlNodeTmp.data["field_length"] = 0

                key = mat.group(1)
                nodeTmp = self.getNodeByName(nodeList, searchDict, key)
                if not nodeTmp:
                    return -2
                sdlNodeTmp.insertNode(nodeTmp)
            elif flagStruct:
                if re.search(regBasic, line):
                    #print("regBasic")
                    mat = re.search(regBasic, line)
                    field_length = mat.group(2)
                    if not field_length:
                        field_length = 0
                    
                    nodeData = {
                        "field_type" : mat.group(1),
                        "field_name" : mat.group(3).upper(),
                        "field_length" : field_length
                    }
                    nodeTmp = sdlNode(data=nodeData)
                    sdlNodeTmp.insertNode(nodeTmp)
                elif re.search(regOther, line):
                    #print("regOther")
                    mat = re.search(regOther, line)
                    key = mat.group(1)
                    value = mat.group(2)
                    nodeTmp = self.getNodeByName(nodeList, searchDict, key)
                    if nodeTmp.data["field_type"] != "map":
                        nodeTmp.data["field_name"] = value.upper()
                    if not nodeTmp:
                        return -2
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
                searchDict[sdlNodeTmp.data["field_name"]] = len(nodeList) - 1
                nodeData = {
                    "field_type" : None,
                    "field_name" : None,
                    "field_length" : None
                }
                sdlNodeTmp = sdlNode(data=nodeData)

        self.root = self.getNodeByName(nodeList, searchDict, self.root_name)
        self.root.index=0
        return 0

class sdlContent:
    def __init__(self, xdr_content, regkey=r'obbs:S:1.3:', root_name="obbs:J:1.3:"):
        self.xdr_content = xdr_content
        self.regkey = regkey
        self.root_name = root_name

    def printXdrTree(self, inNode=None, indent=0, prefix="", flag=False, isseq=False):
        """print tree to string"""
        if not inNode:
            inNode = self.xdrNode
        
        nodeName = inNode.data["field_value"] if inNode.data["field_value"] else inNode.data["field_name"]
        # '\\\\\\1' = r'\\\1'
        nodeName = re.sub(r'([\\\{\}\[\]\(\),\'\"])', r'\\\1', nodeName).replace('\r','\\r').replace('\n','\\n')
        if inNode.data["field_length"] is not None:
            nodeLength = inNode.data["field_length"] if inNode.data["field_length"] else 0
            nodeType = inNode.data["field_type"]
            if inNode.data["field_type"] == "int":
                nodeType = nodeType + str(nodeLength)
            if inNode.data["field_type"] not in ["struct", "list", "map"]:
                nodeName = nodeType + "_" + str(inNode.index)  + "_" + inNode.data["field_name"] + " : " + nodeName
            else:
                nodeName = nodeType + "_" + str(inNode.index)  + "_" + inNode.data["field_name"]
        
        
        if isseq and inNode.data["field_seq"] is not None:
            nodeseq = inNode.data["field_seq"]
            nodeName = nodeName + " [" + str(nodeseq) + "]"
            
        if flag and indent == 0:
            tab = prefix
            prefix = prefix + "|    "
        elif flag and indent > 0:
            tab = prefix[0:len(prefix)-2] + "|\n" + prefix[0:len(prefix)-2] + "|- "
            prefix = prefix + "|    "
        else:
            tab = '    ' * (indent - 1) + ' |- ' if indent > 0 else ''
            prefix = ""
        print('%s%s' % (tab, nodeName))
        
        for obj in inNode.children:
            self.printXdrTree(inNode=obj, indent=indent + 1, prefix=prefix, flag=flag, isseq=isseq)

    def getIndexForChar(self, srcStr, nChar, nStart=0):
        retIndex = srcStr.find(nChar, nStart)
        #print("ret :  " + srcStr[retIndex])
        if retIndex != -1 and retIndex != nStart and srcStr[retIndex - 1] == '\\':
            retIndex = self.getIndexForChar(srcStr, nChar, retIndex + 1)
        return retIndex

    def getMinNumIndex(self, numL):
        ret = 0
        for i, n in enumerate(numL):
            if (n < numL[ret] or numL[ret] == -1) and n != -1:
                ret = i
        return ret, numL[ret]

    def getMachineBinStr(self, strNum):
        '''
        Return a 64bit binary string which the number saved in machine
        '''
        intNum = int(strNum)
        binStr = bin(intNum).split('b')[1]
        if len(binStr) < 9:
            hexStr = hex(intNum & 0xFF)
        elif len(binStr) > 8 and len(binStr) < 17:
            hexStr = hex(intNum & 0xFFFF)
        elif len(binStr) > 16 and len(binStr) < 33:
            hexStr = hex(intNum & 0xFFFFFFFF)
        elif len(binStr) > 16 and len(binStr) < 65:
            hexStr = hex(intNum & 0xFFFFFFFFFFFFFFFF)
        else:
            return None
        
        hexNum = int(hexStr, base=16)
        return bin(hexNum).split('b')[1].zfill(64)

    def getNodeSeq(self, sdl_node):
        # 对于struct类型，{}内的前几个字段是属于marker字段，用于解码时确定struct元素的个数
        # {1,7,7,0,0,109}
        # markernum：1表示有1个usedmaker和1个marker字段
        # usedmarker：7用于表示哪些字段是在使用的，7用二进制表示为0000 0111，表示前3个字段是有值的
        # marker：7用于表示哪些字段是没有被设置成null的，如果usedmarker位是1，marker是0，那么这个字段是null，sjson不输出
        childrenLen = len(sdl_node.children)
        if sdl_node.data["field_type"] == "struct" and childrenLen > 0:
            markerNum = int(sdl_node.children[0].data["field_value"])
            if markerNum > 0:
                markerStr = ""
                for i in range(markerNum):
                    markerStr = markerStr + self.getMachineBinStr(sdl_node.children[2 * markerNum - 2 * i].data["field_value"])

                markerStr = markerStr[::-1]
                startIndex = 0
                for j, _ in enumerate(sdl_node.children):
                    if j < markerNum * 2 + 1:
                        if j == 0:
                            sdl_node.children[j].data["field_length"] = 16
                            sdl_node.children[j].data["field_name"] = "_MarkerNum"
                        elif j % 2 == 1:
                            sdl_node.children[j].data["field_length"] = 64
                            sdl_node.children[j].data["field_name"] = "_UsedMarker"
                        else:
                            sdl_node.children[j].data["field_length"] = 64
                            sdl_node.children[j].data["field_name"] = "_Marker"
                        sdl_node.children[j].data["field_type"] = "int"
                        continue
                    #print("j : " + str(j))
                    pos = markerStr.find('1', startIndex)
                    #print("pos : " + str(pos))
                    sdl_node.children[j].data["field_seq"] = pos
                    startIndex = pos + 1
                    #self.getNodeSeq(sdl_node.children[j])
        
        for k, _ in enumerate(sdl_node.children):
            self.getNodeSeq(sdl_node.children[k])

    def analyseSdlContent(self):
        # '{' '}' '[' ']' '(' ')' ',' '\\' '\"' '\'' '\r' '\n'
        regstr = self.regkey + r'{({.*})}'
        mat = re.search(regstr, self.xdr_content)
        if not mat:
            return -1
        
        content = mat.group(1)
        #print(content)

        nodeData = {
            "field_type" : None,
            "field_name" : self.root_name,
            "field_length" : None,
            "field_value" : None,
            "field_seq" : None,
            "field_note": None
        }
        self.xdrNode = sdlNode(data=nodeData)

        #searchContext = "{" 
        #numList = [m.start() for m in re.finditer(searchContext, content)]
        #print(numList)

        currPos = 0
        currNode = self.xdrNode
        strLen = len(content)

        nodeData = {
                "field_type" : None,
                "field_name" : None,
                "field_length" : None,
                "field_value" : None,
                "field_seq" : None,
                "field_note": None
            }
        tmpNode = sdlNode(data=nodeData)

        while currPos < strLen:
            currChar = content[currPos]
            flagNextNode = False
            if currChar == '{':
                tmpNode.data["field_type"] = "struct"
                tmpNode.data["field_name"] = "struct"
                flagNextNode = True
            elif currChar == '[':
                tmpNode.data["field_type"] = "list"
                tmpNode.data["field_name"] = "list"
                flagNextNode = True
            elif currChar == '(':
                tmpNode.data["field_type"] = "map"
                tmpNode.data["field_name"] = "map"
                flagNextNode = True
            elif currChar not in ('}',']',')',','):
                i_s = self.getIndexForChar(content, '}', currPos)
                i_l = self.getIndexForChar(content, ']', currPos)
                i_m = self.getIndexForChar(content, ')', currPos)
                i_n = self.getIndexForChar(content, ',', currPos)
                typeTuple = (i_s, i_l, i_m, i_n)
                minTypeIndex, nextPos = self.getMinNumIndex(typeTuple)
                #print("currPos : " + str(currPos) + "   nextPos : " + str(nextPos))
                #print(currChar)
                if nextPos == -1:
                    return -1
                valueStr = content[currPos:nextPos]
                currPos = nextPos - 1
                tmpNode.data["field_type"] = "value"
                tmpNode.data["field_name"] = "value"
                # '\\1' = r'\1'
                tmpNode.data["field_value"] = re.sub(r'\\([\\\{\}\[\]\(\),\'\"])', r'\1', valueStr).replace('\\r','\r').replace('\\n','\n')
                flagNextNode = False
            elif content[currPos] == ',' and content[currPos - 1] == ',' :
                tmpNode.data["field_type"] = "value"
                tmpNode.data["field_name"] = "value"
                flagNextNode = False
            elif content[currPos] in ('}',']',')'):
                currNode = currNode.parent
                currPos = currPos + 1
                continue
            else:
                currPos = currPos + 1
                continue
                      
            if not currNode:
                print("error")
                return -2

            currNode.insertNode(tmpNode)
            if flagNextNode:
                currNode = tmpNode
                
            currPos = currPos + 1
            nodeData = {
                "field_type" : None,
                "field_name" : None,
                "field_length" : None,
                "field_value" : None,
                "field_seq" : None,
                "field_note": None
            }
            tmpNode = sdlNode(data=nodeData)
        
        #self.xdrNode.children[0].data["field_name"] = "MXdr::SXdr"
        self.getNodeSeq(self.xdrNode.children[0])

        return 0

    def unionDefAndContent(self, sdldef, sdlContentNode=None):
        if sdldef == None:
            return -1
        if sdlContentNode == None:
            sdlContentNode = self.xdrNode.children[0]

        if sdlContentNode.data["field_type"] == sdldef.data["field_type"] \
            or (sdlContentNode.data["field_type"] == "value" and re.search(r'^int|string|float|xdr', sdldef.data["field_type"])):
            sdlContentNode.data["field_name"] = sdldef.data["field_name"]
            sdlContentNode.data["field_length"] = sdldef.data["field_length"]
            sdlContentNode.data["field_type"] = sdldef.data["field_type"]
        else:
            return -1
        
        if sdlContentNode.data["field_type"] == "struct":
            childrenLen = len(sdlContentNode.children)
            if childrenLen == 0:
                return -1
            
            markerNum = int(sdlContentNode.children[0].data["field_value"])
            childrenLenReal = childrenLen - markerNum * 2 - 1
            if childrenLenReal > len(sdldef.children):
                return -1
            
            if childrenLenReal > 0:
                for i, _ in enumerate(sdlContentNode.children):
                    if i < markerNum * 2 + 1:
                        continue
                    node_seq = sdlContentNode.children[i].data["field_seq"]
                    ret = self.unionDefAndContent(sdldef.children[node_seq], sdlContentNode.children[i])
                    if ret != 0:
                        return ret
        elif sdlContentNode.data["field_type"] == "list":
            sdlContentNode.data["field_note"] = sdldef.children[0].data["field_type"] + ":" + sdldef.children[0].data["field_name"]
            for i, _ in enumerate(sdlContentNode.children):
                ret = self.unionDefAndContent(sdldef.children[0], sdlContentNode.children[i])
                if ret != 0:
                    return ret
        elif sdlContentNode.data["field_type"] == "map":
            for i, _ in enumerate(sdlContentNode.children):
                ret = self.unionDefAndContent(sdldef.children[i], sdlContentNode.children[i])
                if ret != 0:
                    return ret
        return 0

    def toDict(self, inNode=None, retDict=None, retList=None):
        if inNode == None:
            inNode = self.xdrNode.children[0]
        nodeType = inNode.data["field_type"]
        if nodeType == "int":
            nodeType = nodeType + str(inNode.data["field_length"])
        
        key = nodeType + "_" + str(inNode.index)  + "_" + inNode.data["field_name"]
        
        if nodeType == "struct":
            #print("struct : " + inNode.data["field_name"])
            value = {}
            for node in inNode.children:
                self.toDict(node, retDict=value, retList=retList)
        elif nodeType == "list":
            #print("list : " + inNode.data["field_name"])
            value = []
            for node in inNode.children:
                self.toDict(node, retDict=retDict, retList=value)

            #print("---" + inNode.data["field_name"] + "   " + str(len(inNode.children)))
            if len(inNode.children) > 0 and inNode.children[0].data["field_type"] == "map":
                valueTmp = []
                for v in value:
                    valueTmp.extend(v)
                value = valueTmp
        elif nodeType == "map":
            #print("map : " + inNode.data["field_name"])
            value = []
            for node in inNode.children:
                self.toDict(node, retDict=retDict, retList=value)
        else:
            if nodeType in ["int16", "int32"]:
                value = int(inNode.data["field_value"]) if inNode.data["field_value"] else 0
            else:
                value = str(inNode.data["field_value"]) if inNode.data["field_value"] else ""
        
        #print("key : " + key + "   value : " + str(value))
        if inNode.parent.data["field_type"] in ["list", "map"]:
            retList.append(value)
        else:
            #print("nodename : " + inNode.data["field_name"])
            if nodeType == "list":
                if len(inNode.data["field_note"]) > 0:
                    nextType = inNode.data["field_note"].split(':')[0]
                    nextName = inNode.data["field_note"].split(':')[1]
                    if nextType == "map":
                        key =  "map_" + str(inNode.index)  + "_MXdr::" + nextName
                    key1 = key + "_size"
                    value1 = int(len(value) / 2) if nextType == "map" else len(value)
                    retDict[key1] = value1
                    if value1 == 0:
                        value = None
            elif inNode.data["field_name"] == "SXdr":
                key =  "struct_" + str(inNode.index)  + "_MXdr::SXdr"
            retDict[key] = value
