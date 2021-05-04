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
    补码的计算，返回输入数字使用机器码表示的合适位长（最长64位）的二进制，失败返回None

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

def getMachineInt(strBin, bitLen=None):
    '''
    补码的反向计算，返回机器码对应的int值，失败返回None

    :param bitLen: 指定数字存储的长度，范围（8，16，32，64），默认为None，根据输入数字的长度来适配
    '''
    positiveFlag = True
    if bitLen and len(strBin) == bitLen and strBin[0] == "1":
        positiveFlag = False
    if not bitLen:
        if (len(strBin) == 8 or len(strBin) == 16 or len(strBin) == 32 or len(strBin) == 64) and strBin[0] == "1":
            positiveFlag = False
    
    if not positiveFlag:
        #数字减1
        intNum = int(strBin, base=2) - 1
        # 返回串开头为0b
        strBinTmp = bin(intNum)[2:]
        # 取反
        #reserveStr = reverse(strBinTmp)
        binary_out = list(strBinTmp)
        for epoch,i in enumerate(strBinTmp):
            if i == "0":
                binary_out[epoch] = "1"
            else:
                binary_out[epoch] = "0"
        reserveStr = "".join(binary_out)
        resInt = -int(reserveStr,2)
    else:
        resInt = int(strBin, base=2)

    return resInt

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
def addSdlHead_v6(sdlstr):
    regJson = r'obbs:J:[\d][.][\d]:{'
    regSjson = r'obbs:S:[\d][.][\d]:{'
    jFlag = False
    sFlag = False
    for testline in sdlstr.split('\n'):
        if re.search(regJson, testline):
            jFlag = True
            break
        if re.search(regSjson, testline):
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

def addSdlHead_v8(sdlstr):
    regJson = r'SDJ0{'
    regSjson = r'SDS0{'
    jFlag = False
    sFlag = False
    for testline in sdlstr.split('\n'):
        if re.search(regJson, testline):
            jFlag = True
            break
        if re.search(regSjson, testline):
            sFlag = True
            break
    
    inStr = sdlstr
    retStr = ""
    typeFlag = ""
    newSdlList = []

    if jFlag:
        typeFlag = "J"
        oneSdlList = []
        regJson1 = r'.*?(SDJ0\{.*)'

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
                sessionId = genRandomStr()
                newSdl = sessionId + oneSdl + '\n'
                newSdlList.append(newSdl)
                oneSdlList.clear()
                if i != len(lines) - 1:
                    oneSdlList.append(mat.group(1))
                    oneBegin = True
    if sFlag:
        regSjson1 = r'.*?(SDS0\{.*\}$)'
        typeFlag = "S"
        for line in inStr.split('\n'):
            if len(line) == 0:
                continue
            mat = re.search(regSjson1, line)
            if mat:
                oneSdl = mat.group(1)
                sessionId = genRandomStr()
                newSdl = sessionId + oneSdl
                newSdlList.append(newSdl)
            else:
                newSdlList.clear()
                break
    if len(newSdlList) > 0:
        retStr = '\n'.join(newSdlList)

    return retStr

class nodeData:
    '''
    各个参数默认值都为None

    :param field_type: 数据域，数据类型，类型string

    :param field_name: 数据域，字段名，类型string

    :param field_next: 数据域，记录第一个子节点数据类型和字段名，中间以冒号隔开，类型string

    :param field_length: 数据域，字段定义的长度，类型int

    :param field_value: 数据域，字段值，类型string

    :param field_seq: 对应SDL DEF树的真实子节点序号，类型int

    :param field_useflag: 标记是否使用，针对content树来说，类型bool

    :param field_note: 其余描述，供外围接口使用，类型string
    '''
    def __init__(self, field_type=None, field_name=None, field_next=None, field_length=None, field_value=None, field_seq=None, field_useflag=False, field_note=None):
        self.field_type = field_type
        self.field_name = field_name
        self.field_next = field_next
        self.field_length = field_length
        self.field_value = field_value
        self.field_seq = field_seq
        self.field_useflag = field_useflag
        self.field_note = field_note
    
    def __deepcopy__(self, memo):
        if memo is None:
            memo = {}
        result = self.__class__()
        memo[id(self)] = result
        result.field_type = self.field_type
        result.field_name = self.field_name
        result.field_next = self.field_next
        result.field_length = self.field_length
        result.field_value = self.field_value
        result.field_seq = self.field_seq
        result.field_useflag = self.field_useflag
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
        self.__log = Logger(level=loglevel, logmode=logmode, filename=filename, logname='sdlDefine', fmt=r'[%(name)s - %(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')

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

    def __getSdlDefFile(self, inFile=None):
        inFile = self.__sdl_file if not inFile else inFile
        exec_path = os.path.split(os.path.realpath(__file__))[0]
        if not os.path.exists(inFile):
            return None
        raw = open(inFile, 'rb').read()
        result = chardet.detect(raw)
        encoding = result['encoding']
        with open(inFile, 'r', encoding=encoding) as fi:
            return fi.readlines()
    
    def __getNodeByName(self, nodeList, searchDict, field_name):
        """通过结构名称，从保存的列表里查找结构"""
        regBasic = r'^(int|string|float|xdr)'
        if re.search(regBasic, field_name):
            self.__log.logger.debug("getbasic" + field_name)
            ndata = nodeData(field_type=field_name, field_name=field_name, field_length=0)
            return treeNode(data=ndata)
        if field_name in searchDict:
            index = searchDict[field_name]
            self.__log.logger.debug("getdict" + field_name)
            nodeTmp1 = copy.deepcopy(nodeList[index])
            if nodeTmp1.data.field_type == "map":
                ndata = nodeData(field_type="list", field_name="maplist", field_length=0)
                nodeTmp2 = treeNode(data=ndata)
                nodeTmp2.insertNode(nodeTmp1)
                return nodeTmp2
            return nodeTmp1
        self.__log.logger.error("getNode " + field_name + " None")
        return None

    def __getSdlIncludeDefine(self, includeFile, nodeList, searchDict):
        """
        获取SDL定义树
        返回值:
        0 : 子文件分析成功
        -1: 输入的SDL定义文件为空
        -2: 输入的SDL定义文件存在错误，引用的结构必须要在之前定义过.
        """
        sdlLineList = self.__getSdlDefFile(includeFile)
        self.__log.logger.debug("---include file: " + includeFile)
        ret = 0
        if not sdlLineList:
            ret = -1
        else:
            self.__log.logger.debug("---include start---")
            regStruct = r'^struct\s*([0-9a-zA-Z_]+)'
            regStructEnd = r'};?'
            regMap = r'^map\s+aimap\s*<\s*([0-9a-zA-Z_]+)\s*\,\s*([0-9a-zA-Z_]+)\s*>\s+([0-9a-zA-Z_]+)\s*;'
            regList = r'^list\s+vector\s*<\s*([0-9a-zA-Z_]+)\s*>\s+([0-9a-zA-Z_]+)\s*;'
            regBasic = r'^(int|string|float|xdr)<?([0-9]*)>?\s*([0-9a-zA-Z_]+)\s*;'
            regInclude = r'^#\s*include\s*[<"\']([0-9A-Za-z_.-]+)[>"\']'
            regOther = r'^([0-9a-zA-Z_:]+)\s*([0-9a-zA-Z_]+)\s*;'

            flagStruct = False
            FlagStructEnd = True

            ndata = nodeData()
            sdlNodeTmp = treeNode(data=ndata)
            self.__log.logger.debug("include sdlLineList length : " + str(len(sdlLineList)))
            for line in sdlLineList:
                line = re.sub(r'//.*|\n|\r', "", line).strip()
                self.__log.logger.debug("include line length : " + str(len(line)))
                if len(line) == 0:
                    self.__log.logger.debug("include continue.line length : 0")
                    continue
                
                self.__log.logger.debug("include line : " + line)
                if re.search(regInclude, line):
                    self.__log.logger.debug("---include regInclude start---")
                    mat = re.search(regInclude, line)
                    includeFile = os.path.join(os.path.split(includeFile)[0], mat.group(1))
                    ret = self.__getSdlIncludeDefine(includeFile, nodeList, searchDict)
                    if ret != 0:
                        break
                elif re.search(regStructEnd, line) and flagStruct and not FlagStructEnd:
                    flagStruct = False
                    FlagStructEnd = True
                    self.__log.logger.debug("---include regStructEnd---")
                elif re.search(regStruct, line):
                    self.__log.logger.debug("---include regStruct start---")
                    flagStruct = True
                    FlagStructEnd = False
                    mat = re.search(regStruct, line)
                    sdlNodeTmp.data.field_name = mat.group(1)
                    sdlNodeTmp.data.field_type = "struct"
                    sdlNodeTmp.data.field_length = 0
                elif re.search(regMap, line):
                    self.__log.logger.debug("---include regMap start---")
                    flagStruct = False
                    mat = re.search(regMap, line)
                    sdlNodeTmp.data.field_name = mat.group(3)
                    sdlNodeTmp.data.field_type = "map"
                    sdlNodeTmp.data.field_length = 0

                    key = mat.group(1)
                    value = mat.group(2)
                    self.__log.logger.debug("include key : " + key + " value : " + value)
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
                    self.__log.logger.debug("---include regList start---")
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
                        self.__log.logger.debug("---include regBasic start---")
                        mat = re.search(regBasic, line)
                        field_length = mat.group(2)
                        if not field_length:
                            field_length = 0

                        ndata = nodeData(field_type=mat.group(1), field_name=mat.group(3).upper(), field_length=field_length)
                        nodeTmp = treeNode(data=ndata)
                        sdlNodeTmp.insertNode(nodeTmp)
                    elif re.search(regOther, line):
                        self.__log.logger.debug("---include regOther start---")
                        mat = re.search(regOther, line)
                        key = mat.group(1)
                        value = mat.group(2)
                        key = key.split(':')[-1]
                        nodeTmp = self.__getNodeByName(nodeList, searchDict, key)
                        if not nodeTmp:
                            ret = -2
                            break
                        if nodeTmp.data.field_type != "map":
                            nodeTmp.data.field_name = value.upper()
                        sdlNodeTmp.insertNode(nodeTmp)
                else:
                    self.__log.logger.debug("include continue.reg failed.")
                    continue
                
                self.__log.logger.debug("include FlagStructEnd : " + str(FlagStructEnd) + " flagStruct : "  + str(flagStruct))
                if FlagStructEnd and not flagStruct and not sdlNodeTmp.Empty():
                    self.__log.logger.debug("---include insert node---")
                    flagStruct = False
                    FlagStructEnd = True
                    nodeList.append(sdlNodeTmp)
                    searchDict[sdlNodeTmp.data.field_name] = len(nodeList) - 1
                    ndata = nodeData()
                    sdlNodeTmp = treeNode(data=ndata)
        self.__log.logger.info("---include ret: " + str(ret))
        return ret
    
    def getSdlDefine(self, dumpMode=0, debugFlag=False):
        """
        获取SDL定义树
        返回值:
        0 : 成功，将SDL定义树设置到self.root
        -1: 输入的SDL定义文件为空
        -2: 输入的SDL定义文件存在错误，引用的结构必须要在之前定义过.
        -3: 读取SDL定义树的DUMP文件时出错
        -4: 写入DUMP文件失败

        :param dumpMode: 指定获取SDL定义的方式
        0: 先从DUMP文件获取，成功返回，失败则读取SDL定义文件来分析
        1：从SDL定义文件读取，分析后保存到DUMP文件
        2：从保存的SDL定义树DUMP文件读取
        :param debugFlag: 调试开关，当返回值为-4时，保留root的值
        """
        if dumpMode == 2:
            return 0 if self.__loadSdlDefine() else -3
        if dumpMode == 0:
            if self.__loadSdlDefine():
                return 0

        sdlLineList = self.__getSdlDefFile()
        self.__log.logger.debug("---file: " + self.__sdl_file)
        ret = 0
        if not sdlLineList:
            ret = -1
        else:
            self.__log.logger.debug("---start---")
            regStruct = r'^struct\s*([0-9a-zA-Z_]+)'
            regStructEnd = r'};?'
            regMap = r'^map\s+aimap\s*<\s*([0-9a-zA-Z_]+)\s*\,\s*([0-9a-zA-Z_]+)\s*>\s+([0-9a-zA-Z_]+)\s*;'
            regList = r'^list\s+vector\s*<\s*([0-9a-zA-Z_]+)\s*>\s+([0-9a-zA-Z_]+)\s*;'
            regBasic = r'^(int|string|float|xdr)<?([0-9]*)>?\s*([0-9a-zA-Z_]+)\s*;'
            regInclude = r'^#\s*include\s*[<"\']([0-9A-Za-z_.-]+)[>"\']'
            regOther = r'^([0-9a-zA-Z_:]+)\s*([0-9a-zA-Z_]+)\s*;'

            nodeList = []
            searchDict = dict()
            flagStruct = False
            FlagStructEnd = True

            ndata = nodeData()
            sdlNodeTmp = treeNode(data=ndata)
            self.__log.logger.debug("sdlLineList length : " + str(len(sdlLineList)))
            for line in sdlLineList:
                line = re.sub(r'//.*|\n|\r', "", line).strip()
                self.__log.logger.debug("line length : " + str(len(line)))
                if len(line) == 0:
                    self.__log.logger.debug("continue.line length : 0")
                    continue
                
                self.__log.logger.debug("line : " + line)
                if re.search(regInclude, line):
                    self.__log.logger.debug("---regInclude start---")
                    mat = re.search(regInclude, line)
                    includeFile = os.path.join(os.path.split(self.__sdl_file)[0], mat.group(1))
                    ret = self.__getSdlIncludeDefine(includeFile, nodeList, searchDict)
                    if ret != 0:
                        break
                elif re.search(regStructEnd, line) and flagStruct and not FlagStructEnd:
                    flagStruct = False
                    FlagStructEnd = True
                    self.__log.logger.debug("---regStructEnd---")
                elif re.search(regStruct, line):
                    self.__log.logger.debug("---regStruct start---")
                    flagStruct = True
                    FlagStructEnd = False
                    mat = re.search(regStruct, line)
                    sdlNodeTmp.data.field_name = mat.group(1)
                    sdlNodeTmp.data.field_type = "struct"
                    sdlNodeTmp.data.field_length = 0
                elif re.search(regMap, line):
                    self.__log.logger.debug("---regMap start---")
                    flagStruct = False
                    mat = re.search(regMap, line)
                    sdlNodeTmp.data.field_name = mat.group(3)
                    sdlNodeTmp.data.field_type = "map"
                    sdlNodeTmp.data.field_length = 0

                    key = mat.group(1)
                    value = mat.group(2)
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
                        self.__log.logger.debug("---regBasic start---")
                        mat = re.search(regBasic, line)
                        field_length = mat.group(2)
                        if not field_length:
                            field_length = 0

                        ndata = nodeData(field_type=mat.group(1), field_name=mat.group(3).upper(), field_length=field_length)
                        nodeTmp = treeNode(data=ndata)
                        sdlNodeTmp.insertNode(nodeTmp)
                    elif re.search(regOther, line):
                        self.__log.logger.debug("---regOther start---")
                        mat = re.search(regOther, line)
                        key = mat.group(1)
                        value = mat.group(2)
                        key = key.split(':')[-1]
                        nodeTmp = self.__getNodeByName(nodeList, searchDict, key)
                        if not nodeTmp:
                            ret = -2
                            break
                        if nodeTmp.data.field_type != "map":
                            nodeTmp.data.field_name = value.upper()
                        sdlNodeTmp.insertNode(nodeTmp)
                else:
                    self.__log.logger.debug("continue.reg failed.")
                    continue
                
                self.__log.logger.debug("FlagStructEnd : " + str(FlagStructEnd) + " flagStruct : "  + str(flagStruct))
                if FlagStructEnd and not flagStruct and not sdlNodeTmp.Empty():
                    self.__log.logger.debug("---insert node---")
                    flagStruct = False
                    FlagStructEnd = True
                    nodeList.append(sdlNodeTmp)
                    searchDict[sdlNodeTmp.data.field_name] = len(nodeList) - 1
                    ndata = nodeData()
                    sdlNodeTmp = treeNode(data=ndata)
            if ret == 0:
                self.root = self.__getNodeByName(nodeList, searchDict, self.__root_name)
                if self.root:
                    self.root.index=0
                    if not self.__dumpSdlDefine():
                        ret = -4
                        if not debugFlag:
                            self.root = None
        self.__log.logger.info("---main ret: " + str(ret))
        return ret

class sdlContent:
    '''
    话单类，一个实例表示一条话单

    :param xdr_content: 一条话单的字符串

    :param sdlDef: SDL定义树

    :attribute root: 解析完成的话单树根结点，实际的话单为其第一个子节点，和SDL定义树的根结点对应，默认: None
    '''
    def __init__(self, xdr_content, sdlDef, loglevel="error", logmode=1, logpath=None):
        self.__xdr_content = xdr_content
        self.__sdlDef = sdlDef
        self.root = None
        # sdl类型，目前支持V6和V8，0:V6，1:V8，默认：0
        # V6: JSON - obbs:J:1.3:   SJSON - obbs:S:1.3:
        # V8: JSON - SDJ0   SJSON - SDS0
        self.__xdrVersion = 0
        filename = logpath + r"sdlcontent.log" if logpath else None
        self.__log = Logger(level=loglevel, logmode=logmode, filename=filename, logname='sdlContent', fmt=r'[%(name)s - %(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')

    def setLogLevel(self, loglevel):
        self.__log.setLogLevel(loglevel)
    
    def getXdrVersion(self, loglevel):
        return self.__xdrVersion

    def printSdlTree(self, inNode=None, indent=0, prefix="", flag=False, isseq=False):
        """
        打印话单树

        :param inNode: 话单树的根结点，默认为该实例的root，保持为空就好

        :param indent: 初始缩进空格数，默认为0，保持为空就好

        :param prefix: 初始前缀，默认为空，保持为空就好

        :param flag: 当值为Ture时，各级结点下面都输出'|'

        :param isseq: 当值为True时，输出话单字段结点对应在SDL定义结构中的子节点序号
        """
        if not inNode:
            inNode = self.root
        
        nodeName = inNode.data.field_value if inNode.data.field_value is not None else "None"
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

        if isseq:
            nodeuseflag = 1 if inNode.data.field_useflag else 0
            nodeName = nodeName + " [" + str(nodeuseflag) + "]"
            if inNode.data.field_seq is not None:
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

    def __getNodeSeq_v6(self, sdl_node):
        '''根据sdldef，设置xdr结点对应到定义的子结点索引'''
        # 对于struct类型，{}内的前几个字段是属于marker字段，用于解码时确定struct元素的个数
        # {1,7,7,0,0,109}
        # markernum：1表示有1个usedmarker和1个marker字段
        # usedmarker：7用于表示哪些字段是在使用的，7用二进制表示为0000 0111，表示前3个字段是有值的
        # marker：7用于表示哪些字段是没有被设置成null的，如果usedmarker位是1，marker是0，那么这个字段是null，sjson不输出
        childrenLen = len(sdl_node.children)
        self.__log.logger.debug("field name: " + sdl_node.data.field_name + ", field_value: " + (sdl_node.data.field_value if sdl_node.data.field_value else "None"))
        if sdl_node.data.field_type == "struct" and childrenLen > 0:
            self.__log.logger.debug("field name: " + sdl_node.data.field_name + ", field_value: " + (sdl_node.data.field_value if sdl_node.data.field_value else "None"))
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
                    self.__log.logger.debug("j : " + str(j))
                    pos = markerStr.find('1', startIndex)
                    self.__log.logger.debug("pos : " + str(pos))
                    sdl_node.children[j].data.field_seq = pos
                    startIndex = pos + 1
                    #self.__getNodeSeq_v6(sdl_node.children[j])
        
        for k, _ in enumerate(sdl_node.children):
            self.__getNodeSeq_v6(sdl_node.children[k])

    def __getNodeSeq_v8(self, sdl_node):
        '''根据sdldef，设置xdr结点对应到定义的子结点索引'''
        # 对于struct类型，{}内的前1个字段是属于marker字段，用于解码时确定struct元素的个数
        # {bffe,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
        # 440e04327018000:6008400
        # 45c1;5c1
        # marker：16进制字符串，转成二进制来表示字段的状态，意义和V6类似
        # 取消了V6的markernum，合并usedmarker和marker成一个，以分号隔开
        # 如果两者值一样则省略原marker值
        # 字段数多于64时，分多个，以冒号隔开，原marker部分后移，相等时也可省略
        # 当启用的字段数为0时，可以用空表示，当不能省略
        self.__log.logger.debug("nodename: " + sdl_node.data.field_name + ", nodetype: " + sdl_node.data.field_type)
        sdlChildrenLen = len(sdl_node.children)
        if sdl_node.data.field_type == "struct" and sdlChildrenLen > 0 and len(sdl_node.children[0].data.field_value) > 0:
            markerList = sdl_node.children[0].data.field_value.split(';') if sdl_node.children[0].data.field_value != "3fef" else ["1fff"]
            destList = markerList[0].split(':')
            if len(markerList) > 1:
                destList = markerList[1].split(':')
            markerNum = len(destList)
            markerStr = ""
            for i in range(markerNum - 1, -1, -1):
                if len(destList[i]) > 0:
                    markerStr = markerStr + bin(int(destList[i], 16))[2:].zfill(64)
                else:
                    markerStr = markerStr + "0".zfill(64)
            
            markerStr = markerStr[::-1]
            self.__log.logger.debug("markerStr : " + markerStr)
            startIndex = 0
            for j, _ in enumerate(sdl_node.children):
                if j == 0:
                    sdl_node.children[j].data.field_type = "string"
                    sdl_node.children[j].data.field_length = 0
                    sdl_node.children[j].data.field_name = "_Marker"
                    continue
                self.__log.logger.debug("j : " + str(j))
                pos = markerStr.find('1', startIndex)
                self.__log.logger.debug("pos : " + str(pos))
                sdl_node.children[j].data.field_seq = pos
                startIndex = pos + 1
        if sdl_node.data.field_type == "struct" and sdlChildrenLen > 0 and len(sdl_node.children[0].data.field_value) == 0:
            sdl_node.children[0].data.field_type = "string"
            sdl_node.children[0].data.field_length = 0
            sdl_node.children[0].data.field_name = "_Marker"
        
        for k, _ in enumerate(sdl_node.children):
            self.__getNodeSeq_v8(sdl_node.children[k])

    def __getContentFromSjson(self):
        '''
        从SJSON格式的话单，分析获取对应的话单树，失败时，root为None
        0: 成功，设置self.root为该话单树root结点
        -1: 失败，传入的话单，格式不正确
        '''
        # '{' '}' '[' ']' '(' ')' ',' '\\' '\"' '\'' '\r' '\n'
        regstr = r'obbs:S:[\d].[\d]:' + r'{({.*})}'
        mat = re.search(regstr, self.__xdr_content)
        if not mat:
            regstr = r'SDS0' + r'{({.*})}'
            mat = re.search(regstr, self.__xdr_content)
            if not mat:
                self.__log.logger.error("content error.return -1.")
                return -1
            self.__xdrVersion = 1
        else:
            self.__xdrVersion = 0
        
        content = mat.group(1)
        self.__log.logger.debug("xdr content : " + content)

        ndata = nodeData(field_name="SDLTree", field_useflag=True)
        xdrNode = treeNode(data=ndata)

        #numList = [m.start() for m in re.finditer(searchContext, content)]
        #print(numList)

        currPos = 0
        currNode = xdrNode
        strLen = len(content)

        ndata = nodeData(field_useflag=True)
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
                tmpNode.data.field_value = ""
                flagNextNode = False
            elif content[currPos] in ('}',']',')'):
                if self.__xdrVersion == 1 and content[currPos] == '}' and len(currNode.children) == 0:
                    self.__log.logger.debug("for v8, empty node insert.")
                    ndata1 = nodeData(field_useflag=True)
                    tmpNode1 = treeNode(data=ndata1)
                    tmpNode1.data.field_type = "value"
                    tmpNode1.data.field_name = "value"
                    tmpNode1.data.field_value = ""
                    currNode.insertNode(tmpNode1)
                currNode = currNode.parent
                currPos = currPos + 1
                continue
            else:
                currPos = currPos + 1
                continue
                      
            if not currNode:
                self.__log.logger.error("error.parent is none.return -3")
                return -3

            currNode.insertNode(tmpNode)
            if flagNextNode:
                currNode = tmpNode
                
            currPos = currPos + 1
            ndata = nodeData(field_useflag=True)
            tmpNode = treeNode(data=ndata)
        
        #self.printSdlTree()
        #self.root.children[0].data.field_name = "MXdr::SXdr"
        self.root = xdrNode.children[0]
        if self.__xdrVersion == 0:
            self.__getNodeSeq_v6(self.root)
        else:
            self.__getNodeSeq_v8(self.root)

        return 0

    def __unionDefAndSdl(self, sdldef, sdlContentNode=None):
        '''
        将解析的sdl和def关联，形成完整的sdl树
        0: 成功
        -2: 失败，xdr的结构和对应的def结构无法对应
        '''
        if sdldef == None:
            self.__log.logger.error("union: def none.return -2")
            return -2
        if sdlContentNode == None:
            sdlContentNode = self.root

        if sdlContentNode.data.field_type == sdldef.data.field_type \
            or (sdlContentNode.data.field_type == "value" and re.search(r'^int|string|float|xdr', sdldef.data.field_type)):
            sdlContentNode.data.field_name = sdldef.data.field_name
            sdlContentNode.data.field_length = sdldef.data.field_length
            sdlContentNode.data.field_type = sdldef.data.field_type
        else:
            self.__log.logger.error("union: node type error.return -2")
            self.__log.logger.error("node name: " + sdldef.data.field_name)
            self.__log.logger.error("content type: " + sdlContentNode.data.field_type)
            self.__log.logger.error("def type: " + sdldef.data.field_type)
            return -2
        
        if sdlContentNode.data.field_type == "struct":
            childrenLen = len(sdlContentNode.children)
            if childrenLen == 0:
                self.__log.logger.error("union: struct node children len is 0.return -2")
                return -2
            
            if self.__xdrVersion == 0:
                markerNum = int(sdlContentNode.children[0].data.field_value) * 2 + 1
            else:
                markerNum = 1
            
            childrenLenReal = childrenLen - markerNum
            
            if childrenLenReal > len(sdldef.children):
                self.__log.logger.error("union: struct node real children error.return -2")
                return -2
            
            self.__log.logger.debug("union: ori Num: " + str(childrenLen) + ", real Num: " + str(childrenLenReal) + ". sdldef num: " + str(len(sdldef.children)))
            if childrenLenReal > 0:
                for i, _ in enumerate(sdlContentNode.children):
                    if i < markerNum:
                        continue
                    node_seq = sdlContentNode.children[i].data.field_seq
                    self.__log.logger.debug("union: index: " + str(i) + ", def node_seq: " + str(node_seq))
                    ret = self.__unionDefAndSdl(sdldef.children[node_seq], sdlContentNode.children[i])
                    if ret != 0:
                        return ret
        elif sdlContentNode.data.field_type == "list":
            #sdlContentNode.data.field_note = sdldef.children[0].data.field_type + ":" + sdldef.children[0].data.field_name
            sdlContentNode.data.field_next = sdldef.children[0].data.field_type + ":" + sdldef.children[0].data.field_name
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

    def __setDictToSdlTree(self, retNode, inDict, inList=None):
        '''
        将dict结构转成话单树

        :param retNode: 存储话单内容的结点
        
        :param inDict: 输入话单转换成的dict结构

        :param inList: 中间变量，保持为空就好
        '''
        ret = 0
        self.__log.logger.debug("---start---")

        if inList:
            self.__log.logger.debug("---in List---")
            self.__log.logger.debug("List : " + str(inList))
            for node in inList:
                ndata = nodeData(field_useflag=True)
                tmpNode1 = treeNode(data=ndata)
                if isinstance(node, dict):
                    tmpNode1.data.field_type = "struct"
                    tmpNode1.data.field_name = "struct"
                    ret = self.__setDictToSdlTree(retNode=tmpNode1, inDict=node)
                    if ret != 0:
                        break
                    if len(tmpNode1.children) > 0 and tmpNode1.children[0].data.field_name == "maplist":
                        self.__log.logger.debug("---struct maplist---")
                        retNode.moveNode(tmpNode1.children[0])
                    else:
                        retNode.insertNode(tmpNode1)
                elif isinstance(node, list):
                    tmpNode1.data.field_type = "list"
                    tmpNode1.data.field_name = "list"
                    retNode.insertNode(tmpNode1)
                    ret = self.__setDictToSdlTree(retNode=retNode.children[-1], inDict=inDict, inList=node)
                    if ret != 0:
                        break
                else:
                    tmpNode1.data.field_type = "value"
                    tmpNode1.data.field_name = "value"
                    tmpNode1.data.field_length = 0
                    tmpNode1.data.field_value = str(node)
                    retNode.insertNode(tmpNode1)
        else:
            self.__log.logger.debug("---in Dict---")
            for key, value in inDict.items():
                self.__log.logger.debug("key : " + key)

                ndata = nodeData(field_useflag=True)
                tmpNode = treeNode(data=ndata)
                field_name, field_type, field_length = self.__getFieldNameFromKey(key)
                if len(field_name) == 0:
                    ret = -1
                    self.__log.logger.error("field_name is empty.return -1.")
                    break
                if re.search(r'^MXdr::',field_name) and self.__xdrVersion == 0:
                    field_name = field_name.split(':')[2]
                if field_name == "_Val":
                    self.__log.logger.debug("---val maplist---")
                    field_name = "maplist"
                self.__log.logger.debug("field_name : " + field_name)
                self.__log.logger.debug("field_type : " + field_type)
                self.__log.logger.debug("field_length : " + str(field_length))

                tmpNode.data.field_type = field_type
                tmpNode.data.field_name = field_name
                tmpNode.data.field_length = field_length
                if re.search(r'_size$', field_name):
                    self.__log.logger.debug("continue.size key.")
                    continue
                #if isinstance(value, dict):
                if field_type == "struct":
                    self.__log.logger.debug("---struct---")
                    ret = self.__setDictToSdlTree(retNode=tmpNode, inDict=value)
                    if ret != 0:
                        break
                #elif isinstance(value, list):
                elif field_type in ["list", "map"]:
                    self.__log.logger.debug("---list-map---")
                    if value:
                        ret = self.__setDictToSdlTree(retNode=tmpNode, inDict=inDict, inList=value)
                        if ret != 0:
                            break
                    if field_type == "map":
                        childLen = len(tmpNode.children)
                        self.__log.logger.debug("Nodename : " + tmpNode.data.field_name + " len : " + str(childLen))
                        if childLen !=0 and childLen % 2 != 0:
                            self.__log.logger.error("map node's childLen is wrong.return -1.")
                            ret = -1
                            break
                        ndata = nodeData(field_type="map", field_name="map", field_useflag=True)
                        tmpNode1 = treeNode(data=ndata)
                        for i in range(int(childLen / 2)):
                            tmpNode1.moveNode(tmpNode.children[0])
                            tmpNode1.moveNode(tmpNode.children[0])
                            tmpNode.insertNode(tmpNode1)
                            ndata = nodeData(field_type="map", field_name="map", field_useflag=True)
                            tmpNode1 = treeNode(data=ndata)
                        tmpNode.data.field_type = "list"
                else:
                    self.__log.logger.debug("---value---")
                    tmpNode.data.field_value = str(value)
                
                retNode.insertNode(tmpNode)
        return ret

    def __setSdlToDict(self, inNode=None, retDict=None, retList=None):
        '''
        将话单树转换成dict结构

        :param inNode: 待转换话单的起始结点，默认为root
        
        :param retDict: 存储转换完成的dict结构

        :param retList: 中间变量，保持为空就好
        '''
        if inNode == None:
            inNode = self.root
        nodeType = inNode.data.field_type
        if nodeType == "int":
            nodeType = nodeType + str(inNode.data.field_length)
        
        key = nodeType + "_" + str(inNode.index)  + "_" + inNode.data.field_name
        
        if nodeType == "struct":
            self.__log.logger.debug("struct : " + inNode.data.field_name)
            value = {}
            for node in inNode.children:
                self.__setSdlToDict(node, retDict=value, retList=retList)
        elif nodeType == "list":
            self.__log.logger.debug("list : " + inNode.data.field_name)
            if len(inNode.children) > 0 and inNode.children[0].data.field_type == "map" and inNode.parent.data.field_type == "map":
                self.__log.logger.debug("---maplist: " + inNode.data.field_name)
                value = {}
                for node in inNode.children:
                    self.__setSdlToDict(node, retDict=value, retList=retList)
            else:
                value = []
                for node in inNode.children:
                    self.__setSdlToDict(node, retDict=retDict, retList=value)

            self.__log.logger.debug("---" + inNode.data.field_name + "   " + str(len(inNode.children)))
            if len(inNode.children) > 0 and inNode.children[0].data.field_type == "map" and inNode.parent.data.field_type != "map":
                self.__log.logger.debug("---not maplist: " + inNode.data.field_name)
                valueTmp = []
                for v in value:
                    valueTmp.extend(v)
                value = valueTmp
        elif nodeType == "map":
            self.__log.logger.debug("map : " + inNode.data.field_name)
            value = []
            for node in inNode.children:
               self.__setSdlToDict(node, retDict=retDict, retList=value)
        else:
            if nodeType in ["int16", "int32"]:
                value = int(inNode.data.field_value) if inNode.data.field_value else 0
            else:
                value = str(inNode.data.field_value) if inNode.data.field_value else ""
        
        self.__log.logger.debug("key : " + key)
        if inNode.parent.data.field_type in ["list", "map"] and inNode.parent.data.field_name != "maplist":
            retList.append(value)
        else:
            self.__log.logger.debug("nodename : " + inNode.data.field_name)
            if nodeType == "list":
                if len(inNode.data.field_next) > 0:
                    nextType = inNode.data.field_next.split(':')[0]
                    nextName = inNode.data.field_next.split(':')[1]
                    if nextType == "map" and self.__xdrVersion == 0:
                        key =  "map_" + str(inNode.index)  + "_MXdr::" + nextName
                    if nextType == "map" and self.__xdrVersion == 1:
                        key =  "map_" + str(inNode.index)  + "_" + inNode.data.field_name
                    key1 = key + "_size"
                    value1 = int(len(value) / 2) if nextType == "map" else len(value)
                    retDict[key1] = value1
                    if value1 == 0:
                        value = None
            elif nodeType == "map":
                if inNode.parent.data.field_name == "maplist":
                    self.__log.logger.debug("---parent maplist: " + inNode.parent.data.field_name)
                    if self.__xdrVersion == 0:
                        key =  "map_2_MXdr::Val"
                        key1 = "map_2_MXdr::Val_size"
                    if self.__xdrVersion == 1:
                        key =  "map_2__Val"
                        key1 = "map_1__Val_size"
                    value1 = int(len(value) / 2)
                    retDict[key1] = value1
                    if value1 == 0:
                        value = None
            elif inNode.data.field_name == "SXdr":
                key =  "struct_" + str(inNode.index)  + "_MXdr::SXdr"
            elif nodeType == "xdr":
                key =  "xdr_"
            retDict[key] = value

    def __setSdlToStr(self, inNode=None, tmpList=[]):
        '''
        将话单树转换成一个字符串，只保留data的field_value

        :param inNode: 待转换话单的起始结点，默认为root
        
        :param tmpStr: 初始字符串，默认为空，保持为空就好
        '''
        if inNode == None:
            inNode = self.root
        
        self.__log.logger.debug("---start---nodename: " + inNode.data.field_name + ", nodetype: " + inNode.data.field_type)
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
        从SJSON格式的话单，分析获取对应的话单树，失败时，root为None
        0: 成功，设置self.root为该话单树的根结点
        -1: 失败，传入的话单，格式不正确
        -2: 失败，传入的话单和def的结构不匹配

        :param debugFlag: 调试开关，值为True时，对于返回值为-2的情况，保留xdr解析结果，可以调用printSdlTree函数进行打印
        '''
        ret = self.__getContentFromSjson()
        if ret == 0:
            ret = self.__unionDefAndSdl(self.__sdlDef.root)
            if ret != 0 and not debugFlag:
                self.root = None
        return ret
    
    def getSdlFromJson(self, debugFlag=False):
        '''
        从JSON格式的话单，分析获取对应的话单树，失败时，root为None
        0: 成功，设置self.root为该话单树root结点
        -1: 失败，传入的话单，格式不正确
        -2: 失败，传入的话单和def的结构不匹配

        :param debugFlag: 调试开关，值为True时，对于返回值为-2的情况，保留xdr解析结果，可以调用printSdlTree函数进行打印
        '''
        regstr = r'.*?obbs:J:[\d].[\d]:{'
        if not re.search(regstr, self.__xdr_content):
            regstr = r'.*?SDJ0{'
            if not re.search(regstr, self.__xdr_content):
                self.__log.logger.error("xdr content error.need obbs:J:.return -1")
                return -1
            self.__xdrVersion = 1
        else:
            self.__xdrVersion = 0
        
        content = re.sub(regstr, r'{', self.__xdr_content)
        try:
            xdrDict = json.loads(content)
        except:
            self.__log.logger.debug("json load error.maybe the xdr content has some problem.return -1")
            return -1
        
        ndata = nodeData(field_name="SDLTree", field_useflag=True)
        retNode = treeNode(data=ndata)
        ret = self.__setDictToSdlTree(retNode, xdrDict)
        if ret == 0:
            self.root = retNode.children[0]
            try:
                if self.__xdrVersion == 0:
                    self.__getNodeSeq_v6(self.root)
                if self.__xdrVersion == 1:
                    self.__getNodeSeq_v8(self.root)
                ret = self.__unionDefAndSdl(self.__sdlDef.root)
                if ret != 0 and not debugFlag:
                    self.root = None
            except:
                ret = -1
                if not debugFlag:
                    self.root = None
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
            retStr = "obbs:J:1.3:" + retStr if self.__xdrVersion == 0 else "SDJ0" + retStr
        else:
            retStr = json.dumps(retDict, ensure_ascii=False)
            retStr = "obbs:J:1.3:" + retStr if self.__xdrVersion == 0 else "SDJ0" + retStr
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
        retStr = "obbs:S:1.3:{" + "".join(tmpList) + "}\n" if self.__xdrVersion == 0 else "SDS0{" + "".join(tmpList) + "}\n"
        
        if wFlag:
            try:
                with open(wPath, 'w') as fi:
                    fi.write(retStr)
            except Exception as e:
                self.__log.logger.error("json dump to file error.maybe the file path error.info: " + e)
                return None
        return retStr
    
    def __convSdltoDef(self, sdldef, sdlContentNode):
        '''
        将解析的sdl和def关联，形成完整的sdl树
        0: 成功
        -1: 失败，xdr的结构和对应的def结构无法对应
        '''
        if sdldef == None or sdlContentNode == None:
            self.__log.logger.error("def or content is none.return -1")
            return -1

        if sdlContentNode.data.field_type == sdldef.data.field_type:
            sdldef.data.field_seq = sdlContentNode.data.field_seq
            sdldef.data.field_next = sdlContentNode.data.field_next
            sdldef.data.field_useflag = sdlContentNode.data.field_useflag
            sdldef.data.field_note = sdlContentNode.data.field_note
            sdldef.data.field_value = sdlContentNode.data.field_value
        else:
            self.__log.logger.error("node type error.return -1")
            self.__log.logger.error("node name: " + sdldef.data.field_name)
            self.__log.logger.error("content type: " + sdlContentNode.data.field_type)
            self.__log.logger.error("def type: " + sdldef.data.field_type)
            return -1
        
        if sdlContentNode.data.field_type == "struct":
            childrenLen = len(sdlContentNode.children)
            if childrenLen == 0:
                self.__log.logger.error("struct node children len is 0.return -1")
                return -1
            
            if self.__xdrVersion == 0:
                markerNum = int(sdlContentNode.children[0].data.field_value) * 2 + 1
            else:
                markerNum = 1
            
            childrenLenReal = childrenLen - markerNum
            
            if childrenLenReal > len(sdldef.children):
                self.__log.logger.error("struct node real children error.return -1")
                return -1
            
            self.__log.logger.debug("ori Num: " + str(childrenLen) + ", real Num: " + str(childrenLenReal) + ". sdldef num: " + str(len(sdldef.children)))
            if childrenLenReal > 0:
                for i, _ in enumerate(sdlContentNode.children):
                    if i < markerNum:
                        continue
                    node_seq = sdlContentNode.children[i].data.field_seq
                    self.__log.logger.debug("union: index: " + str(i) + ", def node_seq: " + str(node_seq))
                    ret = self.__convSdltoDef(sdldef.children[node_seq], sdlContentNode.children[i])
                    if ret != 0:
                        return ret
        elif sdlContentNode.data.field_type == "list":
            listNodeOri = copy.deepcopy(sdldef.children[0])
            for i, _ in enumerate(sdlContentNode.children):
                if i == 0:
                    ret = self.__convSdltoDef(sdldef.children[0], sdlContentNode.children[i])
                    if ret != 0:
                        return ret
                else:
                    listTmpNode = copy.deepcopy(listNodeOri)
                    ret = self.__convSdltoDef(listTmpNode, sdlContentNode.children[i])
                    if ret != 0:
                        return ret
                    sdldef.insertNode(listTmpNode)
        elif sdlContentNode.data.field_type == "map":
            for i, _ in enumerate(sdlContentNode.children):
                ret = self.__convSdltoDef(sdldef.children[i], sdlContentNode.children[i])
                if ret != 0:
                    return ret
        return 0

    def extendContent(self):
        '''
        将话单树，按照定义树进行扩展，成功返回扩展后的根结点，出错返回None
        '''
        xdrExtendNode = copy.deepcopy(self.__sdlDef.root)
        ret = self.__convSdltoDef(xdrExtendNode, self.root)
        if ret == 0:
            return xdrExtendNode
        return None

    def __sumMarker(self, sdlNode):
        retList = list()
        if sdlNode.data.field_type == "struct" and sdlNode.data.field_useflag:
            childLen = len(sdlNode.children)
            tmpMark = list()
            for node in sdlNode.children:
                tmpMark.append("1" if node.data.field_useflag else "0")
            tmpStr = "".join(tmpMark)
            markNum = int((childLen + 63) / 64)
            if int(tmpStr, 2) != 0:
                used_marker = ""
                marker = ""
                if self.__xdrVersion == 0:
                    ndata = nodeData(field_name="_MarkerNum", field_length=16, field_type="int", field_value=str(markNum), field_useflag=True)
                    retList.append(treeNode(data=ndata))
                for i in range(markNum):
                    start = i * 64
                    end = (i + 1) * 64
                    used_bin_str = tmpStr[start:end] if end < childLen else tmpStr[start:]
                    used_bin_str = used_bin_str[::-1]
                    bin_str = used_bin_str
                    if i == markNum - 1 and sdlNode.parent is None and sdlNode.children[-1].data.field_name == "T_XDR":
                        used_bin_str = "1" + used_bin_str[1:]
                    marker = marker + ":" + hex(int(bin_str, 2))[2:]
                    used_marker = used_marker + ":" + hex(int(used_bin_str, 2))[2:]
                    if self.__xdrVersion == 0:
                        ndata = nodeData(field_name="_UsedMarker", field_length=64, field_type="int", field_value=str(getMachineInt(used_bin_str, 64)), field_useflag=True)
                        retList.append(treeNode(data=ndata))
                        ndata = nodeData(field_name="_Marker", field_length=64, field_type="int", field_value=str(getMachineInt(bin_str, 64)), field_useflag=True)
                        retList.append(treeNode(data=ndata))
                if self.__xdrVersion == 1:
                    value = used_marker.strip(':') if used_marker == marker else used_marker.strip(':') + ";" + marker.strip(':')
                    #value = value.strip(";")
                    ndata = nodeData(field_name="_Marker", field_length=0, field_type="string", field_value=value, field_useflag=True)
                    retList.append(treeNode(data=ndata))
            else:
                if self.__xdrVersion == 0:
                    ndata = nodeData(field_name="_MarkerNum", field_length=16, field_type="int", field_value=str(markNum), field_useflag=True)
                    retList.append(treeNode(data=ndata))
                for i in range(markNum):
                    if self.__xdrVersion == 0:
                        ndata = nodeData(field_name="_UsedMarker", field_length=64, field_type="int", field_value="0", field_useflag=True)
                        retList.append(treeNode(data=ndata))
                        ndata = nodeData(field_name="_Marker", field_length=64, field_type="int", field_value="0", field_useflag=True)
                        retList.append(treeNode(data=ndata))
                if self.__xdrVersion == 1:
                    ndata = nodeData(field_name="_Marker", field_length=0, field_type="string", field_value="", field_useflag=True)
                    retList.append(treeNode(data=ndata))
        return retList

    def shrinkContent(self, extendNode):
        '''
        将扩展的话单树缩小，去除不必要的结点
        '''
        if extendNode.data.field_useflag:
            contentNode = treeNode()
            contentNode.data = extendNode.data
            contentNode.index = extendNode.index
            if extendNode.data.field_type == "struct":
                retList = self.__sumMarker(extendNode)
                for i in range(len(retList)):
                    #contentNode.children.extend(retList)
                    contentNode.insertNode(retList[i])
            for i in range(len(extendNode.children)):
                retNode = self.shrinkContent(extendNode.children[i])
                if retNode:
                    contentNode.insertNode(retNode)
            return contentNode
        return None
    
    def __unsetNodeUseFlag(self, node):
        node.data.field_useflag = False
        node.data.field_value = None
        for i, _ in enumerate(node.children):
            self.__unsetNodeUseFlag(node.children[i])

    def modifyContent(self, inNode, nodeTag, action, value=None):
        '''
        对目标树进行改动

        :param inNode: 待操作的树

        :param nodeTag: 目标结点的Tag值

        :param action: 操作方式，0:添加，1:复制，2:修改，3:删除
        0: 目标结点的父结点为list类型时起作用，复制结点结构，清空数据
        1: 和0类似，区别是保留原始值
        2: 目标结点为int、string等基础类型时起作用，设置本结点和父结点的field_useflag为True
        3: 设置目标结点及其子节点的field_useflag为False

        :param value: 新值，修改方式时需要这个参数
        '''
        if inNode and nodeTag and action in [0, 1, 2, 3]:
            destNode = inNode.search(nodeTag)
            if destNode and destNode.parent and destNode.parent.data.field_useflag:
                if action == 0 and destNode.parent.data.field_type == "list":
                    if destNode.data.field_useflag:
                        tmpNode = copy.deepcopy(destNode)
                        self.__unsetNodeUseFlag(tmpNode)
                        tmpNode.data.field_useflag = True
                        destNode.parent.insertNode(tmpNode)
                    else:
                        destNode.data.field_useflag = True
                if action == 1 and destNode.parent.data.field_type == "list":
                    if destNode.data.field_useflag:
                        tmpNode = copy.deepcopy(destNode)
                        destNode.parent.insertNode(tmpNode)
                    else:
                        destNode.data.field_useflag = True
                if action == 2 and value is not None and destNode.data.field_type not in ["struct", "list", "map"]:
                    destNode.data.field_useflag = True
                    destNode.data.field_value = value
                if action == 3 and destNode.data.field_useflag:
                    if destNode.parent.data.field_type == "list" and len(destNode.parent.children) > 1:
                        destNode.parent.removeNode(destNode)
                    else:
                        if destNode.data.field_type == "list" and len(destNode.children) > 1:
                            for i in range(len(destNode.children)):
                                if i > 0:
                                    destNode.removeNodeByIndex(i)
                        self.__unsetNodeUseFlag(destNode)
