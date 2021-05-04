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

def insertSpace(inStr):
    strLen = len(inStr)
    if strLen % 2 != 0:
        inStr = inStr.zfill(strLen + 1)
    text_list = re.findall(".{2}",inStr)
    new_text = " ".join(text_list)
    return new_text

def calcTag(cl, pc, tagv):
    #tagClass = {"00": "UNIVERSAL", "01": "APPLICATION", "10": "CONTEXT_SPECIFIC", "11": "PRIVATE"}
    #tagType = {"0": "PRIMITIVE", "1": "CONSTRUCTED"}
    tag = 0
    if cl == 0:
        tag = tag | 0x0
    elif cl == 1:
        tag = tag | 0x40
    elif cl == 2:
        tag = tag | 0x80
    elif cl == 3:
        tag = tag | 0xC0
    else:
        return None
    
    if pc == 0:
        tag = tag | 0x0
    elif pc == 1:
        tag = tag | 0x20
    else:
        return None
    
    if tagv < 31:
        tag = tag | tagv
    else:
        tag = tag | 0x1F
        vBin = bin(tagv).lstrip('0b')[::-1]
        
        vBinLen = len(vBin)
        vBinT = vBinLen // 7
        if vBinT > 7:
            return None
        tmpBin = ""
        for i in range(vBinT + 1):
            if i == vBinT and i == 0:
                tmpBin = "0" + vBin[i * 7:][::-1].zfill(7) + tmpBin
            elif i == vBinT and i != 0:
                tmpBin = "1" + vBin[i * 7:][::-1].zfill(7) + tmpBin
            elif i == 0:
                tmpBin = "0" + vBin[0:7][::-1] + tmpBin
            else:
                tmpBin = "1" + vBin[i * 7:(i + 1) * 7][::-1] + tmpBin
        tmpBin = bin(tag).lstrip('0b') + tmpBin
        tag = int(tmpBin, 2)
    return hex(tag).lstrip("0x").upper()

#=============================================================================================================
# ASN.1以8位为单位存储，BER规范的格式是TLV三元组<Tag, Length, Value>
# T是Tag，L是整个类型的长度，V是类型的Value，它还可以是TLV或TLV组合
#
# Tag是一个或若干个八位组
# 最开始的8位，第7、6位指明Tag的类型，或操作，Universal:00（0x0）, APPLICATION:01（0x40）, CONTEXT_SPECIFIC:10（0x80）, PRIVATE:11（0xc0）
# 第5位指明该类型以primitive方式编码还是constructed方式编码，或操作，PRIMITIVE:0（0x0）, CONSTRUCTED:1（0x20）
# PRIMITIVE方式时，后面的Value就是值，CONSTRUCTED方式时，后面的Value是由TLV组成
# 后5位不全为1时，则表示tagvalue，全为1时，直到后面8位组的最高位为0，该tagvalue才结束
# tagvalue为各个8位组去掉最高位，由后7位依次组合而成
# 基本类型的Tag的值，例如INTEGER的Tag值是2,SEQUENCE型类Tag值是16
#
# Length指明Value部分所占8位组的个数（即字节数），分2类，定长和不定长。
# 定长分短和长形式，最高位为0，表示短形式，低7位表示长度；最高位为1，表示长形式，低7位表示的长度字段包含的字节数
# 不定长，长度字段固定为0x80，在Value字段结束后，以2个0x00结尾
# 算法上优先判断不定长，然后再分短和长形式
#
# 根据Length获取value
# BITSTRING，V中第一个八位取值0-7，表示在这个V后面补的0的个数，如果BITSTRING的值为空，则编码时，长度为1，补充的八位组为全0
# value值的reverse，就是一个字节里的高4位和低4位互换
#=============================================================================================================
class nodeData:
    '''
    各个参数默认值都为None

    :param asnFileHeader: 数据域，文件头，16进制大写字符串

    :param asnRecordHeader: 数据域，记录头，16进制大写字符串

    :param asnOffset: 数据域，当前结点的偏移量，类型int

    :param asnTag: 数据域，tag标签，16进制大写字符串

    :param asnTag_class: 数据域，tag类别，枚举：UNIVERSAL，APPLICATION，CONTEXT_SPECIFIC, PRIVATE

    :param asnTag_type: 数据域，结点值类型，枚举：PRIMITIVE，CONSTRUCTED

    :param asnTag_value: 数据域，tag值，类型int

    :param asnLength: 数据域，长度原始串，16进制大写字符串

    :param asnLength_t: 数据域，长度类型，类型int，0:不定长，1:长形式，2:短形式

    :param asnLength_b: 数据域，长类型占用字节数，类型int，长形式使用

    :param asnLength_v: 数据域，结点值所占字节数，类型int

    :param asnValue: 数据域，结点值原始串，16进制大写字符串，包含反序列值，如:125F|21F5
    '''
    def __init__(self):
        self.asnFileHeader = None
        self.asnRecordHeader = None
        self.asnOffset = None
        self.asnTag = None
        self.asnTag_class = None
        self.asnTag_type = None
        self.asnTag_value = None
        self.asnLength = None
        self.asnLength_t = None
        self.asnLength_b = None
        self.asnLength_v = None
        self.asnValue = None
    
    def __deepcopy__(self, memo):
        if memo is None:
            memo = {}
        result = self.__class__()
        memo[id(self)] = result
        result.asnFileHeader = self.asnFileHeader
        result.asnRecordHeader = self.asnRecordHeader
        result.asnOffset = self.asnOffset
        result.asnTag = self.asnTag
        result.asnTag_class = self.asnTag_class
        result.asnTag_type = self.asnTag_type
        result.asnTag_value = self.asnTag_value
        result.asnLength = self.asnLength
        result.asnLength_t = self.asnLength_t
        result.asnLength_b = self.asnLength_b
        result.asnLength_v = self.asnLength_v
        result.asnValue = self.asnValue
        return result

    def __len__(self):
        if self.asnTag is not None:
            return 1
        return 0
    
    def __str__(self):
        attrdict = ",".join("{}={}".format(k, getattr(self, k)) for k in self.__dict__.keys())
        return "[{}:{}]".format(self.__class__.__name__, attrdict)

class asn1Aanlyse:
    '''
    ASN.1分析类

    :param byteStream: 待分析的bit流

    :attribute root: 根结点，tag值固定为root，具体的分析结果为其子节点，默认：None
    '''
    universal_dict = {
        "0": "RESERVE",
        "1": "BOOLEAN",
        "2": "INTEGER",
        "3": "BIT STRING",
        "4": "OCTET STRING",
        "5": "NULL",
        "6": "OBJECT IDENTIFIER",
        "7": "ObjectDescripion",
        "8": "EXTERNAL,INSTANCE OF",
        "9": "REAL",
        "10": "ENUMERATED",
        "11": "EMBEDDED PDV",
        "12": "UFT8String",
        "13": "RELATIVE-OID",
        "14": "RESERVE",
        "15": "RESERVE",
        "16": "SEQUENCE,SEQUENCE OF",
        "17": "SET,SET OF",
        "18": "NumericString",
        "19": "PrintableString",
        "20": "TeletexString,T61String",
        "21": "VideotexString",
        "22": "IA5String",
        "23": "UTCTime",
        "24": "GeneralizedTime",
        "25": "GraphicString",
        "26": "VisibleString,ISO646String",
        "27": "GeneralString",
        "28": "UniversalString",
        "29": "CHARACTER STRING",
        "30": "BMPString",
        "31": "RESERVE"
    }

    tagClass = {"00": "UNIVERSAL", "01": "APPLICATION", "10": "CONTEXT_SPECIFIC", "11": "PRIVATE"}
    tagType = {"0": "PRIMITIVE", "1": "CONSTRUCTED"}

    def __init__(self, byteStream, fileHeadLen=0, recordHeadLen=0, loglevel="error", logmode=1, logpath=None):
        self.root = None
        self.__byteStream = byteStream
        self.__fileHeadLen = fileHeadLen
        self.__recordHeadLen = recordHeadLen
        filename = logpath + r"asn1analyse.log" if logpath else None
        self.__log = Logger(level=loglevel, logmode=logmode, filename=filename, logname='asn1Aanalyse', fmt=r'[%(name)s - %(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')

    def setLogLevel(self, loglevel):
        self.__log.setLogLevel(loglevel)
    
    def setHeaderLen(self, fileHeadLen, recordHeadLen):
        self.__fileHeadLen = fileHeadLen
        self.__recordHeadLen = recordHeadLen
    
    def printAsn1Tree(self, inNode=None, indent=0, prefix="", flag=False, debug=False):
        """
        打印ASN.1分析树

        :param inNode: SDL定义树的根结点，默认为该实例的root，保持为空就好

        :param indent: 初始缩进空格数，默认为0，保持为空就好

        :param prefix: 初始前缀，默认为空，保持为空就好

        :param flag: 当值为Ture时，各级结点下面都输出'|'

        :param debug: 当值为Ture时，输出完整信息，默认只输出TAG
        """
        if not inNode:
            inNode = self.root
            nodeName = inNode.data.asnTag
        elif not debug:
            nodeName = inNode.data.asnTag
        else:
            nodeName = inNode.data.asnTag + ": " + str(inNode.data.asnValue) if inNode.data.asnValue else inNode.data.asnTag
            nodeName = nodeName + " [ TagValue: " + str(inNode.data.asnTag_value) + "," + "Offset: " + str(inNode.data.asnOffset)
            nodeName = nodeName + "," + inNode.data.asnTag_class + "," + inNode.data.asnTag_type + " ]"
            nodeName = nodeName + " [ Length: " + str(inNode.data.asnLength_v) + " ]"

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
            self.printAsn1Tree(inNode=obj, indent=indent + 1, prefix=prefix, flag=flag, debug=debug)
    
    def __getTagAndValue(self, byteList):
        inL = list(byteList)
        if len(inL) == 1:
            return hex(inL[0]).lstrip("0x").upper().zfill(2), inL[0]
        if len(inL) > 1:
            tagL = []
            valueL = []
            for i, byte in enumerate(byteList):
                tagL.append(hex(byte).split('x')[-1].upper().zfill(2))
                if i > 0:
                    valueL.append(bin(byte).split('b')[-1].zfill(8)[1:])
            return "".join(tagL), int("".join(valueL), 2)
        return None, None

    def __getValue(self, byteList):
        inL = list(byteList)
        if len(inL) == 1:
            bHex = hex(inL[0]).lstrip("0x").upper().zfill(2)
            return bHex, bHex[1] + bHex[0], inL[0]
        if len(inL) > 1:
            valueL = []
            reserveL = []
            for byte in byteList:
                bHex = hex(byte).lstrip("0x").upper().zfill(2)
                valueL.append(bHex)
                reserveL.append(bHex[1] + bHex[0])
            return "".join(valueL), "".join(reserveL), int("".join(valueL), 16)
        return None, None, None

    def __analyseOneTag(self, inBytes, startPos=0, fileOffset=True, recordOffset=True):
        self.__log.logger.debug("------asn1 one tag in------")
        currPos = startPos
        recordHeadPos = currPos
        if fileOffset:
            currPos = currPos + self.__fileHeadLen
        if recordOffset:
            recordHeadPos = currPos
            currPos = currPos + self.__recordHeadLen
        nextPos = currPos + 1
        if len(inBytes) < nextPos:
            self.__log.logger.error("asn1 file error:no.1. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
            return None, None
        currByte = inBytes[currPos]
        currBin = bin(currByte).split('b')[-1].zfill(8)
        asn1Node = treeNode(data=nodeData())
        asn1Node.data.asnOffset = currPos
        if fileOffset and self.__fileHeadLen > 0:
            asn1Node.data.asnFileHeader = inBytes[0:self.__fileHeadLen]
        if recordOffset and self.__recordHeadLen > 0:
            asn1Node.data.asnRecordHeader = inBytes[recordHeadPos:currPos]

        # tag
        asn1Node.data.asnTag_class = self.tagClass[currBin[:2]]
        asn1Node.data.asnTag_type = self.tagType[currBin[2]]
        if currBin[3:] == "11111":
            currByte = inBytes[nextPos]
            currBin = bin(currByte).split('b')[-1].zfill(8)
            nextPos = nextPos + 1
            if len(inBytes) < nextPos:
                self.__log.logger.error("asn1 file error:no.2. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
                return None, None
            while currBin[0] == '1':
                currByte = inBytes[nextPos]
                currBin = bin(currByte).split('b')[-1].zfill(8)
                nextPos = nextPos + 1
                if len(inBytes) < nextPos:
                    self.__log.logger.error("asn1 file error:no.3. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
                    return None, None
            asn1Node.data.asnTag, asn1Node.data.asnTag_value = self.__getTagAndValue(inBytes[currPos:nextPos])
        else:
            asn1Node.data.asnTag = hex(currByte).split('x')[-1].upper()
            asn1Node.data.asnTag_value = int(currBin[3:])
        currPos = nextPos
        currByte = inBytes[currPos]
        currBin = bin(currByte).split('b')[-1].zfill(8)
        nextPos = nextPos + 1
        if len(inBytes) < nextPos:
            self.__log.logger.error("asn1 file error:no.4. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
            return None, None
        
        # length
        self.__log.logger.debug("tag after - currPos: " + str(currPos) + "   nextPos: " + str(nextPos))
        asn1Node.data.asnLength = hex(currByte).split('x')[-1].upper().zfill(2)
        if asn1Node.data.asnLength == "80":
            asn1Node.data.asnLength_t = 0
        elif currBin[0] == "1":
            asn1Node.data.asnLength_t = 1
            asn1Node.data.asnLength_b = int("".join(currBin[1:]), 2)
            nextPos = nextPos + asn1Node.data.asnLength_b
            if len(inBytes) < nextPos:
                self.__log.logger.error("asn1 file error:no.5. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
                return None, None
            _, _, asn1Node.data.asnLength_v = self.__getValue(inBytes[currPos + 1:nextPos])
            asn1Node.data.asnLength, _, _ = self.__getValue(inBytes[currPos:nextPos])
        else:
            asn1Node.data.asnLength_t = 2
            asn1Node.data.asnLength_v = int("".join(currBin[1:]), 2)
        currPos = nextPos
        currByte = inBytes[currPos]
        nextPos = nextPos + 1
        if len(inBytes) < nextPos:
            self.__log.logger.error("asn1 file error:no.6. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
            return None, None
        
        # value
        self.__log.logger.debug("length after - currPos: " + str(currPos) + "   nextPos: " + str(nextPos))
        if asn1Node.data.asnTag_type == "PRIMITIVE":
            if asn1Node.data.asnLength_v is not None:
                nextPos = nextPos + asn1Node.data.asnLength_v - 1
                if len(inBytes) >= nextPos:
                    v, vr, _ = self.__getValue(inBytes[currPos:nextPos])
                    asn1Node.data.asnValue = v + "|" + vr
                else:
                    self.__log.logger.error("asn1 file error:no.7. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
                    return None, None
            else:
                while currByte != "0" or inBytes[nextPos] != 0:
                    currByte = inBytes[nextPos]
                    nextPos = nextPos + 1
                nextPos = nextPos + 1
                if len(inBytes) >= nextPos:
                    v, vr, _ = self.__getValue(inBytes[currPos:nextPos - 2])
                    asn1Node.data.asnValue = v + "|" + vr
                else:
                    self.__log.logger.error("asn1 file error:no.8. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
                    return None, None
                asn1Node.data.asnLength_v = nextPos - currPos
        else:
            if asn1Node.data.asnLength_v is not None:
                nextPos = nextPos + asn1Node.data.asnLength_v - 1
                if len(inBytes) < nextPos:
                    self.__log.logger.error("asn1 file error:no.9. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
                    return None, None
                tmpNext, childNode = self.__analyseOneTag(inBytes, startPos=currPos, fileOffset=False, recordOffset=False)
                if tmpNext is not None:
                    asn1Node.insertNode(childNode)
                    while tmpNext < nextPos:
                        tmpNext, childNode = self.__analyseOneTag(inBytes, startPos=tmpNext, fileOffset=False, recordOffset=False)
                        asn1Node.insertNode(childNode)
                    if tmpNext > nextPos:
                        self.__log.logger.error("asn1 file error:no.10. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
                        return None, None
                else:
                    self.__log.logger.error("asn1 file error:no.11. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
                    return None, None
            else:
                while currByte != "0" or inBytes[nextPos] != 0:
                    nextPos, childNode = self.__analyseOneTag(inBytes, startPos=currPos, fileOffset=False, recordOffset=False)
                    asn1Node.insertNode(childNode)
                    currPos = nextPos
                    if len(inBytes) < nextPos:
                        self.__log.logger.error("asn1 file error:no.12. inLen: " + str(len(inBytes)) + ", nextPos: " + str(nextPos))
                        return None, None
                    currByte = inBytes[nextPos]
                    nextPos = nextPos + 1
                asn1Node.data.asnLength_v = nextPos - currPos
        self.__log.logger.debug("------asn1 one tag out------")
        return nextPos, asn1Node

    def anakyseAsn(self):
        if type(self.__byteStream) == bytes and len(self.__byteStream) > 2:
            self.root = treeNode(data=nodeData())
            self.root.data.asnTag = "root"
            nextPos, asn1Node = self.__analyseOneTag(self.__byteStream, 0)
            if nextPos is not None:
                self.root.insertNode(asn1Node)
                while nextPos < len(self.__byteStream):
                    nextPos, asn1Node = self.__analyseOneTag(self.__byteStream, 0, fileOffset=False, recordOffset=True)
                    self.root.insertNode(asn1Node)
                if nextPos == len(self.__byteStream):
                    return True
        self.root = None
        return False

    def __getByteStream(self, inNode, fileHeader=False, recordHeader=False):
        retL = []
        if fileHeader:
            if inNode.data.asnFileHeader:
                retL.append(inNode.data.asnFileHeader.upper())
            else:
                retL.append("F" * self.__fileHeadLen)
        if recordHeader:
            if inNode.data.asnRecordHeader:
                retL.append(inNode.data.asnRecordHeader.upper())
            else:
                retL.append("F" * self.__recordHeadLen)
        retL.append(inNode.data.asnTag.upper())
        retL.append(inNode.data.asnLength.upper())

        if len(inNode.children) == 0:
            retL.append(inNode.data.asnValue.split('|')[0].upper())
        else:
            for child in inNode.children:
                tmpL = self.__getByteStream(child, fileHeader=False, recordHeader=False)
                retL.extend(tmpL)

        if inNode.data.asnLength_t == 0:
            retL.append("0000")
        return retL

    def convToByteStream(self, nodeList, withHeader=False):
        retL = []
        first = True
        for node in nodeList:
            if withHeader and first:
                tmpL = self.__getByteStream(node, fileHeader=True, recordHeader=True)
                first = False
            elif withHeader and not first:
                tmpL = self.__getByteStream(node, fileHeader=False, recordHeader=True)
            else:
                tmpL = self.__getByteStream(node, fileHeader=False, recordHeader=False)
            retL.extend(tmpL)
        if len(retL) > 0:
            return bytes.fromhex("".join(retL))
        return None
    
    def saveByteStream(self):
        retL = []
        first = True
        for node in self.root.children:
            if first:
                tmpL = self.__getByteStream(node, True, True)
                first = False
            else:
                tmpL = self.__getByteStream(node, False, True)
            retL.extend(tmpL)
        if len(retL) > 0:
            return bytes.fromhex("".join(retL))
        return None

    def __splitTag(self, tag):
        # Tag是一个或若干个八位组
        # 最开始的8位，第7、6位指明Tag的类型，或操作，Universal:00（0x0）, APPLICATION:01（0x40）, CONTEXT_SPECIFIC:10（0x80）, PRIVATE:11（0xc0）
        # 第5位指明该类型以primitive方式编码还是constructed方式编码，或操作，PRIMITIVE:0（0x0）, CONSTRUCTED:1（0x20）
        # PRIMITIVE方式时，后面的Value就是值，CONSTRUCTED方式时，后面的Value是由TLV组成
        # 后5位不全为1时，则表示tagvalue，全为1时，直到后面8位组的最高位为0，该tagvalue才结束
        # tagvalue为各个8位组去掉最高位，由后7位依次组合而成
        # 基本类型的Tag的值，例如INTEGER的Tag值是2,SEQUENCE型类Tag值是16
        asnTag_class = None
        asnTag_type = None
        asnTag_value = None
        if tag and re.search(r'[A-F0-9]+', tag.upper()):
            binStr = bin(int(tag, base=16))[2:]
            binLen = len(binStr)
            binStr = binStr.zfill(int((binLen + 7) / 8) * 8)
            binLen = len(binStr)
            asnTag_class = self.tagClass[binStr[:2]]
            asnTag_type = self.tagType[binStr[2]]
            if binStr[3:8] == "11111":
                if binLen < 9:
                    return None, None, None
                i = 8
                while binStr[i] == '1':
                    i = i + 8
                    if binLen < i:
                        return None, None, None
                if i + 8 != binLen:
                    return None, None, None

                valueL = []
                for j in range(8, binLen):
                    if j % 8 != 0:
                        valueL.append(binStr[j])
                asnTag_value = int("".join(valueL), base=2)
            else:
                asnTag_value = int(binStr[3:], base=2)
        return asnTag_class, asnTag_type, asnTag_value

    def __calcTagLength(self, lenType, vLen):
        # lenType:
        # 0: 不定长
        # 1: 定长
        # Length指明Value部分所占8位组的个数（即字节数），分2类，定长和不定长。
        # 定长分短和长形式，最高位为0，表示短形式，低7位表示长度；最高位为1，表示长形式，低7位表示的长度字段包含的字节数
        # 不定长，长度字段固定为0x80，在Value字段结束后，以2个0x00结尾
        # 算法上优先判断不定长，然后再分短和长形式
        asnLength = None
        asnLength_t = None
        asnLength_b = None
        asnLength_v = None
        if lenType == 0:
            asnLength = "80"
            asnLength_t = 0
            asnLength_v = vLen
        elif lenType == 1 and vLen <= 127:
            asnLength_t = 2
            asnLength_v = vLen
            asnLength = hex(vLen)[2:].zfill(2)
        elif lenType == 1 and vLen > 127:
            asnLength_t = 1
            asnLength_v = vLen
            asnLength_b = int((vLen + 255)/256)
            asnLength = hex(int("1" + bin(asnLength_b)[2:].zfill(7), base=2))[2:].zfill(2) + hex(vLen)[2:].zfill(asnLength_b * 2)
        return asnLength, asnLength_t, asnLength_b, asnLength_v

    def __resetTagLenth(self, startNode):
        if startNode.parent and startNode.parent.data.asnTag != "root":
            tmpLen = 0
            for n in startNode.parent.children:
                tmpLen = tmpLen + n.data.asnLength_v
            if tmpLen > 0:
                lenType = 0
                if startNode.parent.data.length_t in [1, 2]:
                    lenType = 1
                asnLength, asnLength_t, asnLength_b, asnLength_v = self.__calcTagLength(lenType, tmpLen)
                startNode.parent.data.asnLength = asnLength
                startNode.parent.data.asnLength_t = asnLength_t
                startNode.parent.data.asnLength_b = asnLength_b
                startNode.parent.data.asnLength_v = asnLength_v
                self.__resetTagLenth(startNode.parent)
    
    def __resetOffset(self, inNode=None):
        if inNode is None:
            inNode = self.root.children[0]
        if inNode.parent.data.asnTag == "root" and inNode.index == 0:
            inNode.data.Offset = self.__fileHeadLen + self.__recordHeadLen
        elif inNode.parent.data.asnTag == "root" and inNode.index != 0:
            prevNode = inNode.parent.children[inNode.index - 1]
            inNode.data.Offset = self.__recordHeadLen + len(prevNode.data.asnTag) + len(prevNode.data.asnLength) + prevNode.data.asnLength_v
            if prevNode.data.asnLength_t == 0:
                inNode.data.Offset = inNode.data.Offset + 3
        elif inNode.index == 0:
            prevNode = inNode.parent
            inNode.data.Offset = len(prevNode.data.asnTag) + len(prevNode.data.asnLength)
        else:
            prevNode = inNode.parent.children[inNode.index - 1]
            inNode.data.Offset = len(prevNode.data.asnTag) + len(prevNode.data.asnLength) + prevNode.data.asnLength_v
            if prevNode.data.asnLength_t == 0:
                inNode.data.Offset = inNode.data.Offset + 3
        
        for i in range(len(inNode.children)):
            self.__resetTagLenth(inNode.children[i])

    def modifyContent(self, inNode, nodeTag, action, valueDict):
        '''
        对目标树进行改动

        :param inNode: 待操作的树

        :param nodeTag: 目标结点的Tag值

        :param action: 操作方式，0:添加，1:复制，2:修改，3:删除
        0: 添加一个新的TLV结构，作为目标结点的子节点，针对constructed类型结点
        1: 复制目标结点，作为其父结点的子节点
        2: 修改目标结点的值，针对primitive类型结点
        3: 删除目标结点

        :param valueDict: 值的字典，0和2模式需要
        action为0时，{"tag":"", "length_type":0/1, "value":""}，length_type：0 不定长；1 定长
        action为1时，{"value":""}
        value为16进制字符串
        '''
        if inNode and nodeTag and action in [0, 1, 2, 3]:
            destNode = inNode.search(nodeTag)
            if destNode:
                if action == 0 and valueDict:
                    tag = valueDict.get("tag")
                    lenType = valueDict.get("length_type")
                    value = valueDict.get("value")
                    if tag and lenType and value:
                        asnTag_class, asnTag_type, asnTag_value = self.__splitTag(tag)
                        tmpLen = len(value)
                        asnLength, asnLength_t, asnLength_b, asnLength_v = self.__calcTagLength(lenType, tmpLen)
                        if asnTag_class and asnLength:
                            tmpNode = treeNode(data=nodeData())
                            tmpNode.data.asnTag = tag
                            tmpNode.data.asnTag_class = asnTag_class
                            tmpNode.data.asnTag_type = asnTag_type
                            tmpNode.data.asnTag_value = asnTag_value
                            tmpNode.data.asnLength = asnLength
                            tmpNode.data.asnLength_t = asnLength_t
                            tmpNode.data.asnLength_b = asnLength_b
                            tmpNode.data.asnLength_v = asnLength_v
                            destNode.insertNode(tmpNode)
                if action == 1:
                    tmpNode = copy.deepcopy(destNode)
                    destNode.parent.insertNode(tmpNode)
                if action == 2 and valueDict:
                    value = valueDict.get("value")
                    if value is not None:
                        lenType = 0
                        if destNode.data.length_t in [1, 2]:
                            lenType = 1
                        tmpLen = len(value)
                        asnLength, asnLength_t, asnLength_b, asnLength_v = self.__calcTagLength(lenType, tmpLen)
                        destNode.data.asnLength = asnLength
                        destNode.data.asnLength_t = asnLength_t
                        destNode.data.asnLength_b = asnLength_b
                        destNode.data.asnLength_v = asnLength_v
                        destNode.data.asnValue = value
                if action == 3:
                    parent = destNode.parent
                    parent.removeNode(destNode)
                    destNode = parent.children[-1]
                self.__resetTagLenth(destNode)
                self.__resetOffset()
                        