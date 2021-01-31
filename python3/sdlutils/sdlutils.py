#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, copy, os, json, uuid #, base64, random
from treenode import treeNode
from logger import Logger
try: import cchardet as chardet
except ImportError: import chardet
try: import cpickle as pickle
except ImportError: import pickle

def getMachineBinStr(strNum, bitLen=None):
    '''
    返回输入数字使用机器码表示的合适位长（最长64位）的二进制，失败返回None

    :param bitLen: 指定返回二进制的长度，范围（8，16，32，64），默认为None，根据输入数字的长度来适配
    '''
    intNum = int(strNum)
    binStr = bin(intNum).split('b')[1]

    destLen = bitLen
    if bitLen:
        if bitLen == 8:
            hexStr = hex(intNum & 0xFF)
        elif bitLen == 16:
            hexStr = hex(intNum & 0xFFFF)
        elif bitLen == 32:
            hexStr = hex(intNum & 0xFFFFFFFF)
        elif bitLen == 64:
            hexStr = hex(intNum & 0xFFFFFFFFFFFFFFFF)
        else:
            return None
    else:
        if len(binStr) < 9:
            hexStr = hex(intNum & 0xFF)
            destLen = 8
        elif len(binStr) > 8 and len(binStr) < 17:
            hexStr = hex(intNum & 0xFFFF)
            destLen = 16
        elif len(binStr) > 16 and len(binStr) < 33:
            hexStr = hex(intNum & 0xFFFFFFFF)
            destLen = 32
        else:
            hexStr = hex(intNum & 0xFFFFFFFFFFFFFFFF)
            destLen = 64
    
    hexNum = int(hexStr, base=16)
    return bin(hexNum).split('b')[1].zfill(destLen)

def genRandomStr(length=16):
    res=[]
    while len(res) == 0 or res[0] ==0:
        #a = "".join([random.choice("0123456789ABCDEF") for i in range(length)])
        #转为bytes
        #bytes.fromhex("a"))
        #res = a
        res = str(uuid.uuid4())
        res = res.replace('-', '')[:length]
        #res = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2].decode('utf-8').upper().replace('_','').replace('-','')[:length]
    return res.lower()

#=============================================================================================================
#  参考资料
#  00000027S0000bdab0000002741e530e335daaaf0000004c4obbs:S:1.3:{
#  1.   00000027  -- 文件头，每个文件都会有8个字节的文件头，表示这个文件的话单数（16进制），有可能是空格，空格表示话单数未知
#  2.   J -- 话单块的开始，也是表示这块话单的格式，J表示json格式，S为 SJSON，T为STJSON
#  3.   0000bdab -- 话单块的大小，表示这块文件块的长度，8字节16进制，一个文件可能有多个块，块大大小是从"0000bdab"后开始算,这里一个文
#件一块
#  4.   00000027 -- 这块文件中的话单数，8字节的16进制
#  5.   41e530e335daaaf0 -- 话单块里面的每条话单前面都会有16字节16进制的session id，话单一般都是一条一行的
#  6.   000004c4 -- 本条话单的长度，8字节16进制,从"obbs:J:1.3:{(含)"开始到结束
#  7.   obbs:J:1.3:{ -- 话单内容，具体的长度根据前面的8字节算出来
#  5、6、7合起来作为一条话单，就是说一个文件块里会有多5、6、7
#=============================================================================================================
def addSdlHead(sdlstr):
    regJson = r'obbs:J:[\d][.][\d]:{'
    regSjson = r'obbs:S:[\d][.][\d]:{'
    jFlag = False
    sFlag = False
    for testline in sdlstr.split('\n'):
        if re.search(regJson, testline):
            jFlag = True
            break
        if re.search(regJson, testline):
            sFlag = True
            break
    
    inStr = sdlstr
    retStr = ""
    typeFlag = ""
    blockSize = 0
    newSdlList = []

    # 下面这种实现速度有点慢
    #if jFlag:
    #    regJson1 = r'[\s\S]*?(obbs:J:[\d][.][\d]:\{[\s\S]*?\})\s{0,2}.*?obbs:J:'
    #    mat = re.search(regJson1, inStr)
    #    while mat:
    #        oneSdl = mat.group(1)
    #        oneSdlSize = len(oneSdl) + 2
    #        sessionId = genRandomStr()
    #        newSdl = sessionId + hex(oneSdlSize)[2:].zfill(8) + oneSdl + '\n'
    #        newSdlList.append(newSdl)
    #        blockSize = blockSize + oneSdlSize
    #        inStr = inStr[oneSdlSize:-1]
    #        mat = re.search(regJson1, inStr)
    if jFlag:
        typeFlag = "J"
        oneSdlList = []
        regJson1 = r'.*?(obbs:J:[\d][.][\d]:\{.*)'

        oneBegin = False
        lines = inStr.split('\n')
        for i, line in enumerate(lines):
            mat = re.search(regJson1, line)
            if mat:
                if oneBegin:
                    oneBegin = False  
                else:
                    oneBegin = True
                    oneSdlList.append(mat.group(1))
                    continue
            if oneBegin and len(line) > 0:
                oneSdlList.append(line)

            if (not oneBegin or i == len(lines) - 1) and len(oneSdlList) > 0:
                oneSdl = '\n'.join(oneSdlList)
                oneSdlSize = len(oneSdl) + 2
                sessionId = genRandomStr()
                newSdl = sessionId + hex(oneSdlSize)[2:].zfill(8) + oneSdl + '\n'
                newSdlList.append(newSdl)
                blockSize = blockSize + oneSdlSize
                oneSdlList.clear()
                if i != len(lines) - 1:
                    oneSdlList.append(mat.group(1))
                    oneBegin = True
    if sFlag:
        regSjson1 = r'.*?(obbs:S:[\d][.][\d]:\{.*\}$)'
        typeFlag = "S"
        for line in inStr.split('\n'):
            if len(line) == 0:
                continue
            mat = re.search(regSjson1, line)
            if mat:
                oneSdl = mat.group(1)
                oneSdlSize = len(oneSdl) + 1
                sessionId = genRandomStr()
                newSdl = sessionId + hex(oneSdlSize)[2:].zfill(8) + oneSdl
                newSdlList.append(newSdl)
                blockSize = blockSize + oneSdlSize
            else:
                newSdlList.clear()
                break
    if len(newSdlList) > 0:
        fileHeadNum =  hex(len(newSdlList))[2:].zfill(8)
        blockSdlNum = fileHeadNum
        blockSize = blockSize + 8
        retStr = fileHeadNum + typeFlag + hex(blockSize)[2:].zfill(8) + blockSdlNum + '\n'.join(newSdlList)

    return retStr

class nodeData:
    '''
    各个参数默认值都为None

    :param field_type: 数据域，数据类型，类型string

    :param field_name: 数据域，字段名，类型string

    :param field_length: 数据域，字段定义的长度，类型int

    :param field_value: 数据域，字段值，类型string

    :param field_seq: 对应树的真实子节点序号，类型int

    :param field_note: 备注信息，如记录子节点类型，类型string
    '''
    def __init__(self, field_type=None, field_name=None, field_length=None, field_value=None, field_seq=None, field_note=None):
        self.field_type = field_type
        self.field_name = field_name
        self.field_length = field_length
        self.field_value = field_value
        self.field_seq = field_seq
        self.field_note = field_note
    
    def __deepcopy__(self, memo):
        if memo is None:
            memo = {}
        result = self.__class__()
        memo[id(self)] = result
        result.field_type = self.field_type
        result.field_name = self.field_name
        result.field_length = self.field_length
        result.field_value = self.field_value
        result.field_seq = self.field_seq
        result.field_note = self.field_note
        return result

    def __len__(self):
        if any([self.field_type, self.field_name, self.field_value, self.field_note]) \
            or self.field_length is not None or self.field_seq is not None:
            return 1
        return 0
    
    def __str__(self):
        attrdict = ",".join("{}={}".format(k, getattr(self, k)) for k in self.__dict__.keys())
        return "[{}:{}]".format(self.__class__.__name__, attrdict)

class sdlDefine:
    '''
    SDL定义类，一个实例表示一种SDL结构

    :param root_name: 该SDL结构的根结点结构名称，以便确定根结点

    :param sdl_file: SDL定义文件路径

    :param sdl_dump_file: SDL定义树DUMP文件路径（包含文件名）

    :attribute root: SDL定义树根结点，默认: None
    '''
    def __init__(self, root_name, sdl_file, sdl_dump_file, loglevel="error", logmode=1, logpath=None):
        self.root = None
        self.__root_name = root_name
        self.__sdl_file = sdl_file
        self.__sdl_dump_file = sdl_dump_file
        filename = logpath + r"sdldefine.log" if logpath else None
        self.__log = Logger(level=loglevel, logmode=logmode, filename=filename, logname='sdlDefine', fmt=r'[%(name)s - %(funcName)s] - %(levelname)s: %(message)s')

    def setLogLevel(self, loglevel):
        self.__log.setLogLevel(loglevel)
    
    def printDefTree(self, inNode=None, indent=0, prefix="", flag=False):
        """
        打印SDL定义树

        :param inNode: SDL定义树的根结点，默认为该实例的root，保持为空就好

        :param indent: 初始缩进空格数，默认为0，保持为空就好

        :param prefix: 初始前缀，默认为空，保持为空就好

        :param flag: 当值为Ture时，各级结点下面都输出'|'
        """
        if not inNode:
            inNode = self.root
        nodeLength = inNode.data.field_length if inNode.data.field_length else 0
        nodeType = inNode.data.field_type
        if inNode.data.field_type == "int":
            nodeType = nodeType + nodeLength
        nodeName = nodeType + "_" + str(inNode.index)  + "_" + inNode.data.field_name

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
            self.printDefTree(inNode=obj, indent=indent + 1, prefix=prefix, flag=flag)
        
    def __dumpSdlDefine(self):
        try:
            with open(self.__sdl_dump_file, 'wb') as fi:
                pickle.dump(self.root, fi)
                return True
        except Exception as e:
            self.__log.logger.error("sdl dump error.info: " + e)
            return False

    def __loadSdlDefine(self):
        exec_path = os.path.split(os.path.realpath(__file__))[0]
        if os.path.exists(self.__sdl_dump_file):
            with open(self.__sdl_dump_file, 'rb') as fi:
                self.root = pickle.load(fi)
                return True
        return False

    def __getSdlDefFile(self):
        exec_path = os.path.split(os.path.realpath(__file__))[0]
        if not os.path.exists(self.__sdl_file):
            return None
        raw = open(self.__sdl_file, 'rb').read()
        result = chardet.detect(raw)
        encoding = result['encoding']
        with open(self.__sdl_file, 'r', encoding=encoding) as fi:
            return fi.readlines()
    
    def __getNodeByName(self, nodeList, searchDict, field_name):
        """通过结构名称，从保存的列表里查找结构"""
        regBasic = r'^(int|string|float|xdr)'
        if re.search(regBasic, field_name):
            #print("getbasic" + field_name)
            self.__log.logger.debug("getbasic" + field_name)
            ndata = nodeData(field_type=field_name, field_name=field_name, field_length=0)
            return treeNode(data=ndata)
        if field_name in searchDict:
            index = searchDict[field_name]
            #print("getdict" + field_name)
            nodeTmp1 = copy.deepcopy(nodeList[index])
            if nodeTmp1.data.field_type == "map":
                ndata = nodeData(field_type="list", field_name="maplist", field_length=0)
                nodeTmp2 = treeNode(data=ndata)
                nodeTmp2.insertNode(nodeTmp1)
                return nodeTmp2
            return nodeTmp1
        #print("getNode " + field_name + " None")
        self.__log.logger.error("getNode " + field_name + " None")
        return None

    def getSdlDefine(self, fromDumpFile, debugFlag=False):
        """
        获取SDL定义树
        返回值:
        0 : 成功，将SDL定义树设置到self.root
        -1: 输入的SDL定义文件为空
        -2: 输入的SDL定义文件存在错误，引用的结构必须要在之前定义过.
        -3: 读取SDL定义树的DUMP文件时出错
        -4: 写入DUMP文件失败

        :param fromDumpFile: 指定是否从SDL定义树的DUMP文件读取
                             False：从SDL定义文件读取，分析后保存到DUMP文件; 
                             True：从保存的SDL定义树DUMP文件读取
        :param debugFlag: 调试开关，当返回值为-4时，保留root的值
        """
        if fromDumpFile:
            return 0 if self.__loadSdlDefine() else -3

        sdlLineList = self.__getSdlDefFile()
        #print("start")
        self.__log.logger.debug("---start1---")
        ret = 0
        if not sdlLineList:
            ret = -1
        else:
            #print("start")
            self.__log.logger.debug("---start2---")
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

            ndata = nodeData()
            sdlNodeTmp = treeNode(data=ndata)
            #print("sdlLineList length : " + str(len(sdlLineList)))
            self.__log.logger.debug("sdlLineList length : " + str(len(sdlLineList)))
            for line in sdlLineList:
                line = re.sub(r'//.*|\n|\r', "", line).strip()
                #print("line length : " + str(len(line)))
                self.__log.logger.debug("line length : " + str(len(line)))
                if len(line) == 0:
                    #print("line 0")
                    self.__log.logger.debug("continue.line length : 0")
                    continue
                
                #print("line : " + line)
                self.__log.logger.debug("line : " + line)
                if re.search(regStructEnd, line) and flagStruct and not FlagStructEnd:
                    flagStruct = False
                    FlagStructEnd = True
                    #print("regStructEnd")
                    self.__log.logger.debug("---regStructEnd---")
                elif re.search(regStruct, line):
                    #print("regStruct")
                    self.__log.logger.debug("---regStruct start---")
                    flagStruct = True
                    FlagStructEnd = False
                    mat = re.search(regStruct, line)
                    sdlNodeTmp.data.field_name = mat.group(1)
                    sdlNodeTmp.data.field_type = "struct"
                    sdlNodeTmp.data.field_length = 0
                elif re.search(regMap, line):
                    #print("regMap")
                    self.__log.logger.debug("---regMap start---")
                    flagStruct = False
                    mat = re.search(regMap, line)
                    sdlNodeTmp.data.field_name = mat.group(3)
                    sdlNodeTmp.data.field_type = "map"
                    sdlNodeTmp.data.field_length = 0

                    key = mat.group(1)
                    value = mat.group(2)
                    #print("key : " + key + " value : " + value)
                    self.__log.logger.debug("key : " + key + " value : " + value)
                    nodeTmp1 = self.__getNodeByName(nodeList, searchDict, key)
                    if not nodeTmp1:
                        ret = -2
                        break
                    sdlNodeTmp.insertNode(nodeTmp1)

                    nodeTmp2 = self.__getNodeByName(nodeList, searchDict, value)
                    if not nodeTmp2:
                        ret = -2
                        break
                    sdlNodeTmp.insertNode(nodeTmp2)
                elif re.search(regList, line):
                    #print("regList")
                    self.__log.logger.debug("---regList start---")
                    flagStruct = False
                    mat = re.search(regList, line)
                    sdlNodeTmp.data.field_name = mat.group(2)
                    sdlNodeTmp.data.field_type = "list"
                    sdlNodeTmp.data.field_length = 0

                    key = mat.group(1)
                    nodeTmp = self.__getNodeByName(nodeList, searchDict, key)
                    if not nodeTmp:
                        ret = -2
                        break
                    sdlNodeTmp.insertNode(nodeTmp)
                elif flagStruct:
                    if re.search(regBasic, line):
                        #print("regBasic")
                        self.__log.logger.debug("---regBasic start---")
                        mat = re.search(regBasic, line)
                        field_length = mat.group(2)
                        if not field_length:
                            field_length = 0

                        ndata = nodeData(field_type=mat.group(1), field_name=mat.group(3).upper(), field_length=field_length)
                        nodeTmp = treeNode(data=ndata)
                        sdlNodeTmp.insertNode(nodeTmp)
                    elif re.search(regOther, line):
                        #print("regOther")
                        self.__log.logger.debug("---regOther start---")
                        mat = re.search(regOther, line)
                        key = mat.group(1)
                        value = mat.group(2)
                        nodeTmp = self.__getNodeByName(nodeList, searchDict, key)
                        if nodeTmp.data.field_type != "map":
                            nodeTmp.data.field_name = value.upper()
                        if not nodeTmp:
                            ret = -2
                            break
                        sdlNodeTmp.insertNode(nodeTmp)
                else:
                    #print("continue")
                    self.__log.logger.debug("continue.reg failed.")
                    continue
                
                #print("FlagStructEnd : " + str(FlagStructEnd) + " flagStruct : "  + str(flagStruct))
                self.__log.logger.debug("FlagStructEnd : " + str(FlagStructEnd) + " flagStruct : "  + str(flagStruct))
                if FlagStructEnd and not flagStruct and not sdlNodeTmp.Empty():
                    #print("insert")
                    self.__log.logger.debug("---insert node---")
                    flagStruct = False
                    FlagStructEnd = True
                    nodeList.append(sdlNodeTmp)
                    searchDict[sdlNodeTmp.data.field_name] = len(nodeList) - 1
                    ndata = nodeData()
                    sdlNodeTmp = treeNode(data=ndata)
            if ret == 0:
                self.root = self.__getNodeByName(nodeList, searchDict, self.__root_name)
                self.root.index=0
                if not self.__dumpSdlDefine():
                    ret = -4
                    self.root = None
        return ret

class sdlContent:
    '''
    话单类，一个实例表示一条话单

    :param xdr_content: 一条话单的字符串

    :param sdlDef: SDL定义树

    :attribute xdrNode: 解析完成的话单树根结点，实际的话单为其第一个子节点，和SDL定义树的根结点对应，默认: None
    '''
    def __init__(self, xdr_content, sdlDef, loglevel="error", logmode=1, logpath=None):
        self.__xdr_content = xdr_content
        self.__sdlDef = sdlDef
        self.xdrNode = None
        filename = logpath + r"sdlcontent.log" if logpath else None
        self.__log = Logger(level=loglevel, logmode=logmode, filename=filename, logname='sdlContent', fmt=r'[%(name)s - %(funcName)s] - %(levelname)s: %(message)s')

    def setLogLevel(self, loglevel):
        self.__log.setLogLevel(loglevel)

    def printSdlTree(self, inNode=None, indent=0, prefix="", flag=False, isseq=False):
        """
        打印话单树

        :param inNode: 话单树的根结点，默认为该实例的xdrNode，保持为空就好

        :param indent: 初始缩进空格数，默认为0，保持为空就好

        :param prefix: 初始前缀，默认为空，保持为空就好

        :param flag: 当值为Ture时，各级结点下面都输出'|'

        :param isseq: 当值为True时，输出话单字段结点对应在SDL定义结构中的子节点序号
        """
        if not inNode:
            inNode = self.xdrNode
        
        nodeName = inNode.data.field_value if inNode.data.field_value else inNode.data.field_name
        # '\\\\\\1' = r'\\\1'
        nodeName = re.sub(r'([\\\{\}\[\]\(\),\'\"])', r'\\\1', nodeName).replace('\r','\\r').replace('\n','\\n')
        if inNode.data.field_length is not None:
            nodeLength = inNode.data.field_length if inNode.data.field_length else 0
            nodeType = inNode.data.field_type
            if inNode.data.field_type == "int":
                nodeType = nodeType + str(nodeLength)
            if inNode.data.field_type not in ["struct", "list", "map"]:
                nodeName = nodeType + "_" + str(inNode.index)  + "_" + inNode.data.field_name + " : " + nodeName
            else:
                nodeName = nodeType + "_" + str(inNode.index)  + "_" + inNode.data.field_name

        if isseq and inNode.data.field_seq is not None:
            nodeseq = inNode.data.field_seq
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
            self.printSdlTree(inNode=obj, indent=indent + 1, prefix=prefix, flag=flag, isseq=isseq)

    def __getIndexForChar(self, srcStr, nChar, nStart=0):
        '''从给定字符串中，从给定的起始位置查找，获取指定字符第一次出现的位置，忽略转义字符'''
        retIndex = srcStr.find(nChar, nStart)
        #print("ret :  " + srcStr[retIndex])
        self.__log.logger.debug("ret :  " + srcStr[retIndex])
        if retIndex != -1 and retIndex != nStart and srcStr[retIndex - 1] == '\\':
            retIndex = self.__getIndexForChar(srcStr, nChar, retIndex + 1)
        return retIndex

    def __getMinNumIndex(self, numL):
        '''获取列表中的最小值，忽略-1的影响，返回对应的索引和值'''
        ret = 0
        for i, n in enumerate(numL):
            if (n < numL[ret] or numL[ret] == -1) and n != -1:
                ret = i
        return ret, numL[ret]

    def __getNodeSeq(self, sdl_node):
        '''根据sdldef，设置xdr结点对应到定义的子结点索引'''
        # 对于struct类型，{}内的前几个字段是属于marker字段，用于解码时确定struct元素的个数
        # {1,7,7,0,0,109}
        # markernum：1表示有1个usedmarker和1个marker字段
        # usedmarker：7用于表示哪些字段是在使用的，7用二进制表示为0000 0111，表示前3个字段是有值的
        # marker：7用于表示哪些字段是没有被设置成null的，如果usedmarker位是1，marker是0，那么这个字段是null，sjson不输出
        childrenLen = len(sdl_node.children)
        if sdl_node.data.field_type == "struct" and childrenLen > 0:
            markerNum = int(sdl_node.children[0].data.field_value)
            if markerNum > 0:
                markerStr = ""
                for i in range(markerNum):
                    markerStr = markerStr + getMachineBinStr(sdl_node.children[2 * markerNum - 2 * i].data.field_value, 64)

                markerStr = markerStr[::-1]
                startIndex = 0
                for j, _ in enumerate(sdl_node.children):
                    if j < markerNum * 2 + 1:
                        if j == 0:
                            sdl_node.children[j].data.field_length = 16
                            sdl_node.children[j].data.field_name = "_MarkerNum"
                        elif j % 2 == 1:
                            sdl_node.children[j].data.field_length = 64
                            sdl_node.children[j].data.field_name = "_UsedMarker"
                        else:
                            sdl_node.children[j].data.field_length = 64
                            sdl_node.children[j].data.field_name = "_Marker"
                        sdl_node.children[j].data.field_type = "int"
                        continue
                    #print("j : " + str(j))
                    self.__log.logger.debug("j : " + str(j))
                    pos = markerStr.find('1', startIndex)
                    #print("pos : " + str(pos))
                    self.__log.logger.debug("pos : " + str(pos))
                    sdl_node.children[j].data.field_seq = pos
                    startIndex = pos + 1
                    #self.__getNodeSeq(sdl_node.children[j])
        
        for k, _ in enumerate(sdl_node.children):
            self.__getNodeSeq(sdl_node.children[k])

    def __getContentFromSjson(self):
        '''
        从SJSON格式的话单，分析获取对应的话单树，失败时，xdrNode为None
        0: 成功，设置self.xdrNode为该话单树root结点
        -1: 失败，传入的话单，格式不正确
        '''
        # '{' '}' '[' ']' '(' ')' ',' '\\' '\"' '\'' '\r' '\n'
        regstr = r'obbs:S:[\d].[\d]:' + r'{({.*})}'
        mat = re.search(regstr, self.__xdr_content)
        if not mat:
            self.__log.logger.error("content error.return -1.")
            return -1
        
        content = mat.group(1)
        #print(content)
        self.__log.logger.debug("xdr content : " + content)

        ndata = nodeData(field_name="SDLTree")
        self.xdrNode = treeNode(data=ndata)

        #numList = [m.start() for m in re.finditer(searchContext, content)]
        #print(numList)

        currPos = 0
        currNode = self.xdrNode
        strLen = len(content)

        ndata = nodeData()
        tmpNode = treeNode(data=ndata)

        while currPos < strLen:
            currChar = content[currPos]
            flagNextNode = False
            if currChar == '{':
                tmpNode.data.field_type = "struct"
                tmpNode.data.field_name = "struct"
                flagNextNode = True
            elif currChar == '[':
                tmpNode.data.field_type = "list"
                tmpNode.data.field_name = "list"
                flagNextNode = True
            elif currChar == '(':
                tmpNode.data.field_type = "map"
                tmpNode.data.field_name = "map"
                flagNextNode = True
            elif currChar not in ('}',']',')',','):
                i_s = self.__getIndexForChar(content, '}', currPos)
                i_l = self.__getIndexForChar(content, ']', currPos)
                i_m = self.__getIndexForChar(content, ')', currPos)
                i_n = self.__getIndexForChar(content, ',', currPos)
                typeTuple = (i_s, i_l, i_m, i_n)
                minTypeIndex, nextPos = self.__getMinNumIndex(typeTuple)
                #print("currPos : " + str(currPos) + "   nextPos : " + str(nextPos))
                #print(currChar)
                self.__log.logger.debug("currChar : " + currChar + "   currPos : " + str(currPos) + "   nextPos : " + str(nextPos))
                if nextPos == -1:
                    self.__log.logger.error("nextPos is -1.return -1")
                    return -1
                valueStr = content[currPos:nextPos]
                currPos = nextPos - 1
                tmpNode.data.field_type = "value"
                tmpNode.data.field_name = "value"
                # '\\1' = r'\1'
                tmpNode.data.field_value = re.sub(r'\\([\\\{\}\[\]\(\),\'\"])', r'\1', valueStr).replace('\\r','\r').replace('\\n','\n')
                flagNextNode = False
            elif content[currPos] == ',' and content[currPos - 1] == ',' :
                tmpNode.data.field_type = "value"
                tmpNode.data.field_name = "value"
                flagNextNode = False
            elif content[currPos] in ('}',']',')'):
                currNode = currNode.parent
                currPos = currPos + 1
                continue
            else:
                currPos = currPos + 1
                continue
                      
            if not currNode:
                #print("error.parent is none")
                self.__log.logger.error("error.parent is none.return -3")
                return -3

            currNode.insertNode(tmpNode)
            if flagNextNode:
                currNode = tmpNode
                
            currPos = currPos + 1
            ndata = nodeData()
            tmpNode = treeNode(data=ndata)
        
        #self.xdrNode.children[0].data.field_name = "MXdr::SXdr"
        self.__getNodeSeq(self.xdrNode.children[0])

        return 0

    def __unionDefAndSdl(self, sdldef, sdlContentNode=None):
        '''
        将解析的sdl和def关联，形成完整的sdl树
        0: 成功
        -1: 失败，xdr的结构和对应的def结构无法对应
        '''
        if sdldef == None:
            #print("union: def none")
            self.__log.logger.error("union: def none.return -2")
            return -2
        if sdlContentNode == None:
            sdlContentNode = self.xdrNode.children[0]

        if sdlContentNode.data.field_type == sdldef.data.field_type \
            or (sdlContentNode.data.field_type == "value" and re.search(r'^int|string|float|xdr', sdldef.data.field_type)):
            sdlContentNode.data.field_name = sdldef.data.field_name
            sdlContentNode.data.field_length = sdldef.data.field_length
            sdlContentNode.data.field_type = sdldef.data.field_type
        else:
            #print("union: node type error")
            #print("node name: " + sdldef.data.field_name)
            #print("content type: " + sdlContentNode.data.field_type)
            #print("def type: " + sdldef.data.field_type)
            self.__log.logger.error("union: node type error.return -2")
            self.__log.logger.error("node name: " + sdldef.data.field_name)
            self.__log.logger.error("content type: " + sdlContentNode.data.field_type)
            self.__log.logger.error("def type: " + sdldef.data.field_type)
            return -2
        
        if sdlContentNode.data.field_type == "struct":
            childrenLen = len(sdlContentNode.children)
            if childrenLen == 0:
                #print("union: struct node children len is 0")
                self.__log.logger.error("union: struct node children len is 0.return -2")
                return -2
            
            markerNum = int(sdlContentNode.children[0].data.field_value)
            childrenLenReal = childrenLen - markerNum * 2 - 1
            if childrenLenReal > len(sdldef.children):
                #print("union: struct node real children error")
                self.__log.logger.error("union: struct node real children error.return -2")
                return -2
            
            if childrenLenReal > 0:
                for i, _ in enumerate(sdlContentNode.children):
                    if i < markerNum * 2 + 1:
                        continue
                    node_seq = sdlContentNode.children[i].data.field_seq
                    ret = self.__unionDefAndSdl(sdldef.children[node_seq], sdlContentNode.children[i])
                    if ret != 0:
                        return ret
        elif sdlContentNode.data.field_type == "list":
            sdlContentNode.data.field_note = sdldef.children[0].data.field_type + ":" + sdldef.children[0].data.field_name
            for i, _ in enumerate(sdlContentNode.children):
                ret = self.__unionDefAndSdl(sdldef.children[0], sdlContentNode.children[i])
                if ret != 0:
                    return ret
        elif sdlContentNode.data.field_type == "map":
            for i, _ in enumerate(sdlContentNode.children):
                ret = self.__unionDefAndSdl(sdldef.children[i], sdlContentNode.children[i])
                if ret != 0:
                    return ret
        return 0

    def __getFieldNameFromKey(self, key):
        field_name = ""
        field_type = ""
        field_length = 0
        if len(key.split('_')) >= 3:
            for i, v in enumerate(key.split('_')):
                if i == 0:
                    field_type = v
                    field_length = 0
                    mat = re.search(r'^int(\d+)', field_type)
                    if mat:
                        field_type = "int"
                        field_length = mat.group(1)
                elif i == 1:
                    pass
                else:
                    field_name = field_name + v + "_"
            field_name = field_name.rstrip('_')
        return field_name, field_type, field_length

    def __setDictToSdl(self, retNode=None, inDict=None, inList=None):
        '''
        将dict结构转成话单树转

        :param retNode: 存储话单的空结点，默认为xdrNode
        
        :param inDict: 输入话单转换成的dict结构

        :param inList: 中间变量，保持为空就好
        '''
        ret = 0
        if retNode == None:
            retNode = self.xdrNode
        #print("---o---")
        self.__log.logger.debug("---start---")

        if inList:
            #print("in List : " + str(inList))
            self.__log.logger.debug("---in List---")
            self.__log.logger.debug("List : " + str(inList))
            for node in inList:
                ndata = nodeData()
                tmpNode1 = treeNode(data=ndata)
                if isinstance(node, dict):
                    tmpNode1.data.field_type = "struct"
                    tmpNode1.data.field_name = "struct"
                    retNode.insertNode(tmpNode1)
                    ret = self.__setDictToSdl(retNode=retNode.children[-1], inDict=node)
                    if ret != 0:
                        break
                elif isinstance(node, list):
                    tmpNode1.data.field_type = "list"
                    tmpNode1.data.field_name = "list"
                    retNode.insertNode(tmpNode1)
                    ret = self.__setDictToSdl(retNode=retNode.children[-1], inDict=inDict, inList=node)
                    if ret != 0:
                        break
                else:
                    tmpNode1.data.field_type = "value"
                    tmpNode1.data.field_name = "value"
                    tmpNode1.data.field_length = 0
                    tmpNode1.data.field_value = str(node)
                    retNode.insertNode(tmpNode1)
        else:
            #print("dict")
            self.__log.logger.debug("---in Dict---")
            for key, value in inDict.items():
                #print("key : " + key + " , value : " + str(value))
                #print("key : " + key)
                self.__log.logger.debug("key : " + key)

                ndata = nodeData()
                tmpNode = treeNode(data=ndata)
                field_name, field_type, field_length = self.__getFieldNameFromKey(key)
                if len(field_name) == 0:
                    ret = -1
                    self.__log.logger.error("field_name is empty.return -1.")
                    break
                if re.search(r'^MXdr::',field_name):
                    field_name = field_name.split(':')[2]

                #print(field_name, field_type, field_length)
                self.__log.logger.debug("field_name : " + field_name)
                self.__log.logger.debug("field_type : " + field_type)
                self.__log.logger.debug("field_length : " + str(field_length))

                tmpNode.data.field_type = field_type
                tmpNode.data.field_name = field_name
                tmpNode.data.field_length = field_length
                if re.search(r'_size$', field_name):
                    #print("continue")
                    self.__log.logger.debug("continue.size key.")
                    continue
                #if isinstance(value, dict):
                if field_type == "struct":
                    #print("struct")
                    self.__log.logger.debug("---struct---")
                    ret = self.__setDictToSdl(retNode=tmpNode, inDict=value)
                    if ret != 0:
                        break
                #elif isinstance(value, list):
                elif field_type in ["list", "map"]:
                    #print("list-map")
                    self.__log.logger.debug("---list-map---")
                    if value:
                        ret = self.__setDictToSdl(retNode=tmpNode, inDict=inDict, inList=value)
                        if ret != 0:
                            break
                    if field_type == "map":
                        childLen = len(tmpNode.children)
                        #print("Nodename : " + tmpNode.data.field_name + " len : " + str(childLen))
                        self.__log.logger.debug("Nodename : " + tmpNode.data.field_name + " len : " + str(childLen))
                        if childLen !=0 and childLen % 2 != 0:
                            self.__log.logger.error("map node's childLen is wrong.return -1.")
                            ret = -1
                            break
                        ndata = nodeData(field_type="map", field_name="map")
                        tmpNode1 = treeNode(data=ndata)
                        for i in range(int(childLen / 2)):
                            tmpNode1.moveNode(tmpNode.children[0])
                            tmpNode1.moveNode(tmpNode.children[0])
                            tmpNode.insertNode(tmpNode1)
                            ndata = nodeData(field_type="map", field_name="map")
                            tmpNode1 = treeNode(data=ndata)
                        tmpNode.data.field_type = "list"
                else:
                    #print("value")
                    self.__log.logger.debug("---value---")
                    tmpNode.data.field_value = str(value)
                
                retNode.insertNode(tmpNode)
        return ret

    def __setSdlToDict(self, inNode=None, retDict=None, retList=None):
        '''
        将话单树转换成dict结构

        :param inNode: 待转换话单的起始结点，默认为xdrNode的第一个子节点
        
        :param retDict: 存储转换完成的dict结构

        :param retList: 中间变量，保持为空就好
        '''
        if inNode == None:
            inNode = self.xdrNode.children[0]
        nodeType = inNode.data.field_type
        if nodeType == "int":
            nodeType = nodeType + str(inNode.data.field_length)
        
        key = nodeType + "_" + str(inNode.index)  + "_" + inNode.data.field_name
        
        if nodeType == "struct":
            #print("struct : " + inNode.data.field_name)
            self.__log.logger.debug("struct : " + inNode.data.field_name)
            value = {}
            for node in inNode.children:
                self.__setSdlToDict(node, retDict=value, retList=retList)
        elif nodeType == "list":
            #print("list : " + inNode.data.field_name)
            self.__log.logger.debug("list : " + inNode.data.field_name)
            value = []
            for node in inNode.children:
                self.__setSdlToDict(node, retDict=retDict, retList=value)

            #print("---" + inNode.data.field_name + "   " + str(len(inNode.children)))
            self.__log.logger.debug("---" + inNode.data.field_name + "   " + str(len(inNode.children)))
            if len(inNode.children) > 0 and inNode.children[0].data.field_type == "map":
                valueTmp = []
                for v in value:
                    valueTmp.extend(v)
                value = valueTmp
        elif nodeType == "map":
            #print("map : " + inNode.data.field_name)
            self.__log.logger.debug("map : " + inNode.data.field_name)
            value = []
            for node in inNode.children:
                self.__setSdlToDict(node, retDict=retDict, retList=value)
        else:
            if nodeType in ["int16", "int32"]:
                value = int(inNode.data.field_value) if inNode.data.field_value else 0
            else:
                value = str(inNode.data.field_value) if inNode.data.field_value else ""
        
        #print("key : " + key + "   value : " + str(value))
        self.__log.logger.debug("key : " + key)
        if inNode.parent.data.field_type in ["list", "map"]:
            retList.append(value)
        else:
            #print("nodename : " + inNode.data.field_name)
            self.__log.logger.debug("nodename : " + inNode.data.field_name)
            if nodeType == "list":
                if len(inNode.data.field_note) > 0:
                    nextType = inNode.data.field_note.split(':')[0]
                    nextName = inNode.data.field_note.split(':')[1]
                    if nextType == "map":
                        key =  "map_" + str(inNode.index)  + "_MXdr::" + nextName
                    key1 = key + "_size"
                    value1 = int(len(value) / 2) if nextType == "map" else len(value)
                    retDict[key1] = value1
                    if value1 == 0:
                        value = None
            elif inNode.data.field_name == "SXdr":
                key =  "struct_" + str(inNode.index)  + "_MXdr::SXdr"
            retDict[key] = value

    def __setSdlToStr(self, inNode=None, tmpList=[]):
        '''
        将话单树转换成一个字符串，只保留data的field_value

        :param inNode: 待转换话单的起始结点，默认为xdrNode的第一个子节点
        
        :param tmpStr: 初始字符串，默认为空，保持为空就好
        '''
        if inNode == None:
            inNode = self.xdrNode.children[0]
        
        self.__log.logger.debug("---start---")
        nodeType = inNode.data.field_type
        if nodeType == "struct":
            self.__log.logger.debug("---struct begin---")
            tmpList.append("{")
        elif nodeType == "list":
            self.__log.logger.debug("---list begin---")
            tmpList.append("[")
        elif nodeType == "map":
            self.__log.logger.debug("---map begin---")
            tmpList.append("(")
        else:
            self.__log.logger.debug("---other begin---")
            self.__log.logger.debug("value: " + inNode.data.field_value)
            value = re.sub(r'([\\\{\}\[\]\(\),\'\"])', r'\\\1', inNode.data.field_value).replace('\r','\\r').replace('\n','\\n')
            self.__log.logger.debug("replaced value: " + value)
            tmpList.append(value)
            tmpList.append(",")
            self.__log.logger.debug("---other end---")
        
        for child in inNode.children:
            self.__setSdlToStr(inNode=child, tmpList=tmpList)
        if inNode.data.field_type == "struct":
            if len(inNode.children) > 0:
                del tmpList[-1]
            tmpList.append("}")
            tmpList.append(",")
            self.__log.logger.debug("---struct end---")
        if inNode.data.field_type == "list":
            if len(inNode.children) > 0:
                del tmpList[-1]
            tmpList.append("]")
            tmpList.append(",")
            self.__log.logger.debug("---list end---")
        if inNode.data.field_type == "map":
            if len(inNode.children) > 0:
                del tmpList[-1]
            tmpList.append(")")
            tmpList.append(",")
            self.__log.logger.debug("---map end---")

    def getSdlFromSjson(self, debugFlag=False):
        '''
        从SJSON格式的话单，分析获取对应的话单树，失败时，xdrNode为None
        0: 成功，设置self.xdrNode为该话单树的根结点
        -1: 失败，传入的话单，格式不正确
        -2: 失败，传入的话单和def的结构不匹配

        :param debugFlag: 调试开关，值为True时，对于返回值为-2的情况，保留xdr解析结果，可以调用printSdlTree函数进行打印
        '''
        ret = self.__getContentFromSjson()
        if ret == 0:
            ret = self.__unionDefAndSdl(self.__sdlDef.root)
            if ret != 0 and not debugFlag:
                self.xdrNode = None
        return ret
    
    def getSdlFromJson(self, debugFlag=False):
        '''
        从JSON格式的话单，分析获取对应的话单树，失败时，xdrNode为None
        0: 成功，设置self.xdrNode为该话单树root结点
        -1: 失败，传入的话单，格式不正确
        -2: 失败，传入的话单和def的结构不匹配

        :param debugFlag: 调试开关，值为True时，对于返回值为-2的情况，保留xdr解析结果，可以调用printSdlTree函数进行打印
        '''
        regstr = r'.*?obbs:J:[\d].[\d]:{'
        if not re.search(regstr, self.__xdr_content):
            self.__log.logger.error("xdr content error.need obbs:J:.return -1")
            return -1
        
        content = re.sub(regstr, r'{', self.__xdr_content)
        try:
            xdrDict = json.loads(content)
        except:
            self.__log.logger.debug("json load error.maybe the xdr content has some problem.return -1")
            return -1
        
        ndata = nodeData(field_name="SDLTree")
        self.xdrNode = treeNode(data=ndata)
        ret = self.__setDictToSdl(inDict=xdrDict)
        if ret == 0:
            self.__getNodeSeq(self.xdrNode.children[0])
            ret = self.__unionDefAndSdl(self.__sdlDef.root)
            if ret != 0 and not debugFlag:
                self.xdrNode = None
        return ret
    
    def convSdlToJson(self, fmtFlag=True, wFlag=False, wPath=None):
        '''
        转换成JSON格式输出，返回json字符串，出错返回None

        :param fmtFlag: 是否格式化输出，默认为True

        :param wFlag: 是否写入文件，方式为覆盖写入，默认为False

        :param wPath: 要写入的json路径，如果vFlag为True，则必须要输入该参数，否则报错返回，默认为None
        '''
        if wFlag and not wPath:
            self.__log.logger.error("when writing file, path should be gived.")
            return None

        retDict = {}
        self.__setSdlToDict(retDict=retDict)
        retStr = None
        if fmtFlag:
            retStr = json.dumps(retDict, indent=3, ensure_ascii=False)
            retStr = "obbs:J:1.3:" + retStr
        else:
            retStr = json.dumps(retDict, ensure_ascii=False)
            retStr = "obbs:J:1.3:" + retStr
        if wFlag:
            try:
                with open(wPath, 'w') as fi:
                    fi.write(retStr)
            except Exception as e:
                self.__log.logger.error("json dump to file error.maybe the file path error.info: " + e)
                return None
        return retStr
    
    def convSdlToSjson(self, wFlag=False, wPath=None):
        '''
        转换成SJSON格式输出，返回sjson字符串，出错返回None

        :param wFlag: 是否写入文件，方式为覆盖写入，默认为False

        :param wPath: 要写入的json路径，如果vFlag为True，则必须要输入该参数，否则报错返回，默认为None
        '''
        if wFlag and not wPath:
            self.__log.logger.error("when writing file, path should be gived.")
            return None
        
        tmpList = []
        self.__setSdlToStr(tmpList=tmpList)
        del tmpList[-1]
        retStr = "obbs:S:1.3:{" + "".join(tmpList) + "}\n"
        
        if wFlag:
            try:
                with open(wPath, 'w') as fi:
                    fi.write(retStr)
            except Exception as e:
                self.__log.logger.error("json dump to file error.maybe the file path error.info: " + e)
                return None
        return retStr
