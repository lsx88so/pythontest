#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os, sys, csv, re, collections
from logger import Logger
try: import cchardet as chardet
except ImportError: import chardet

def convEnv(path):
    if re.search(r'^~', path):
        value = os.environ.get('HOME')
        if value:
            path = re.sub(r'^~', value, path, 1)

    while (True):
        res = re.search(r'\$[\(]?(\w+)[\)]?', path)
        if res:
            env = res.group(1)
            value = os.environ.get(env)
            if value:
                path = re.sub(r'\$[\(\)\w]+', value, path, 1)
            else:
                break
        else:
            break
    return re.sub(r'//', '/', path)

def sortListByAnother(a, b, r=False):
    #ziped = zip(b, a) ->py2
    #ziped.sort(reverse=r) ->py2
    #return list(zip(*ziped)[1]) ->py2
    #tmpList = sorted(zip(a, b), key=lambda x: x[0], reverse=True)
    tmpList = sorted(zip(b, a), key=lambda x: x[0])
    return [x[1] for x in tmpList]

class regdef:
    # 获取话单的匹配规则
    def __init__(self):
        self.regstr = r'.*'
        # 分组个数
        self.gnum = 0
        # dr_type所在的分组
        self.i_dr = 0
        # xdr话单内容所在的分组
        self.i_xdr = 0

class xdrDefine:
    fieldtype_relations = {
        '1': "int",
        '2':"number",
        '3':"reverse",
        '4':"varchar2",
        '5':"datetime"
    }

    def __init__(self, xdr_path, loglevel="error", logmode=1, logpath=None):
        self.__xdr_path = xdr_path
        #存放XDR具体内容:{"dr_gsm_ln" : ["field1","field2",...]}
        self.__xdr_define = dict()
        #存放XDR的字段类型:{"dr_gsm_ln" : [field1_type,field2_type,...]}
        self.__xdr_field_type = dict()
        #存放XDR索引:{fieldnum : ["dr_type1","dr_type2",...]}
        self.__def_index = dict()
        #存放话单匹配正则 regdef
        self.__xdr_regstr = list()
        #解析文件得到的XDR
        # seq从0开始
        # {seq:[  第一个元素(0)，本条话单一些属性信息列表
        #         ['xdrlen','dr_type_default',reg_def,'xdr_ori','xdr_new'],
        #         第二个元素(1)，本条话单的各个字段值列表
        #         ['value1','value2',...],
        #         第三个元素(2)，本条话单可以匹配到话单类型列表
        #         ['dr_type1','dr_type2',...]
        #      ]
        # }
        self.__xdrDecode = collections.OrderedDict()
        filename = logpath + r"xdrdefine.log" if logpath else None
        self.__log = Logger(level=loglevel, logmode=logmode, filename=filename, logname='xdrDefine', fmt=r'[%(name)s - %(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')

    def setLogLevel(self, loglevel):
        self.__log.setLogLevel(loglevel)

    def getXdrDefine(self):
        return self.__xdr_define, self.__xdr_field_type

    def getXdrContent(self):
        return self.__xdrDecode

    def isXdrDefineOk(self):
        '''判断xdr定义是否可用'''
        if len(self.__xdr_define) == 0 or len(self.__xdr_regstr) == 0 or len(self.__def_index) ==0:
            return False
        return True
    
    def printXdrDefine(self, xdr_type, regstr=r'.*'):
        fmat = "\t{:>5}{:<30}{:>15}"
        hasFlag = False
        for key in self.__xdr_define.keys():
            if re.search(xdr_type, key, flags=re.IGNORECASE):
                hasFlag = True
                print("XDR_TYPE : " + key + "\tField Number : " + str(len(self.__xdr_define[key])))
                i = 1
                for i, field in enumerate(self.__xdr_define[key]):
                    if re.search(regstr, field, flags=re.IGNORECASE):
                        print(fmat.format(str(i) + ".", field, self.fieldtype_relations.get(self.__xdr_field_type[key][i], "reserve")))
                    i = i + 1
                print("\n")
        if not hasFlag:
            print("There's no dr_type that fills the bill.")

    def __printOneXdr(self, oneXdr, regstr, xdr_seq, dr_type):
        # seq从0开始
        # {seq:[  第一个元素(0)，本条话单一些属性信息列表
        #         ['xdrlen','dr_type_default',reg_def,'xdr_ori','xdr_new'],
        #         第二个元素(1)，本条话单的各个字段值列表
        #         ['value1','value2',...],
        #         第三个元素(2)，本条话单可以匹配到话单类型列表
        #         ['dr_type1','dr_type2',...]
        #      ]
        # }

        mat = "{:4}{:>28}\t:\t{:}"
        
        if oneXdr[0][1] == "None":
            reg_dr_type = r'.*'
        else:
            reg_dr_type = r'^' + oneXdr[0][1] + r'_.*'
        
        if len(dr_type) > 0:
            reg_dr_type = dr_type
        
        flag = False
        res = ""
        for i, fit_dr_type in enumerate(oneXdr[2], 1):
            if re.search(reg_dr_type, fit_dr_type, flags=re.IGNORECASE):
                flag = True
                res = res + "\nXDR " + str(xdr_seq) + " - " + str(i) + ": " + fit_dr_type + "\tField Number : " + str(oneXdr[0][0]) + "\n"
                fieldList = self.__xdr_define[fit_dr_type]
                for j, field in enumerate(fieldList, 1):
                    outstr = mat.format(str(j) + ".", field, oneXdr[1][j])
                    if re.search(regstr, field, flags=re.IGNORECASE):
                        res = res + outstr + "\n"  
        
        if not flag:
           res = res + "\nXDR " + str(xdr_seq) + ": There's no kind which meets requirements.\nDefault type gived is [" \
                + oneXdr[0][1] + "]\tField Number : " + str(oneXdr[0][0]) + "\tAnd [" + str(len(oneXdr[1])) + "] kinds which find in XDR_DIFINE."
        return res

    def printXdrList(self, regstr=r'.*', dr_type=r'.*', xdr_seq=0, outFlag=False, out_path=None):
        xdr_num = len(self.__xdrDecode)
        if xdr_num == 0:
            print("There's no xdr decoded.")
            return

        if xdr_seq > xdr_num:
            print("Total " + str(xdr_num) + " Xdr in The File.")
            return

        out_start = 0
        out_end = xdr_num
        if xdr_seq > 0:
            out_start = xdr_seq - 1
            out_end = xdr_seq

        if outFlag and not out_path:
            with open(out_path, 'w') as f:
                for i in range(out_start, out_end):
                    f.write(self.__printOneXdr(self.__xdrDecode[i], regstr, i, dr_type) + "\n")
                print("Write Decode File Successfull.Path : " + out_path)
        else:
            for i in range(out_start, out_end):
                print(self.__printOneXdr(self.__xdrDecode[i], regstr, i, dr_type))
    
    def __getRegstr(self, regDictList=None):
        # regd:
        # {"regStr":"str", "groupNum":num, "indexDrType":num, "indexXDR":num}
        for regd in regDictList:
            reg = regdef()
            reg.regstr = regd["regStr"]
            reg.gnum = regd["groupNum"]
            reg.i_dr = regd["indexDrType"]
            reg.i_xdr = regd["indexXDR"]
            if reg.i_xdr == 0 or reg.i_xdr == reg.i_dr or reg.gnum < reg.i_dr or reg.gnum < reg.i_xdr:
                continue
            self.__xdr_regstr.append(reg)

        filelist = os.listdir(self.__xdr_path)
        filelist.sort()

        for fi in filelist:
            fp = os.path.join(self.__xdr_path, fi)
            if os.path.isdir(fp) or fi.split('.')[-1] != 'csv':
                continue
            xdrFlag = os.path.split(os.path.realpath(fp))[1].split('.')[0].split('_')[-1]
            raw = open(fp, 'rb').read()
            result = chardet.detect(raw)
            encoding = result['encoding']
            with open(fp, 'r', encoding=encoding) as f:
                csvrd = csv.DictReader(f)
                for row in csvrd:
                    xdr_type = row["XDR_DR_TYPE"].lower()
                    if xdr_type == "regstr" and re.search(r'^\d\|\d\|\d$',row["XDR_FIELD_TYPE"]):
                        tmpL = row["XDR_FIELD_TYPE"].split('|')
                        reg = regdef()
                        reg.regstr = row["XDR_FIELD_NAME"]
                        reg.gnum = int(tmpL[0])
                        reg.i_dr = int(tmpL[1])
                        reg.i_xdr = int(tmpL[2])
                        if reg.i_xdr == 0 or reg.i_xdr == reg.i_dr or reg.gnum < reg.i_dr or reg.gnum < reg.i_xdr:
                            continue
                        self.__xdr_regstr.append(reg)

    def analyseXdrDefine(self, regDictList=None):
        if not (os.path.exists(self.__xdr_path) and os.path.isdir(self.__xdr_path)):
            self.__log.logger.error("XDR_DEFINE CSV File's Path is Not Exist.Please Check!")
            self.__log.logger.error("Path : " + self.__xdr_path)
            return False
        filelist = os.listdir(self.__xdr_path)
        filelist.sort()
        if len(filelist) == 0:
            self.__log.logger.error("There's no XDR_DEFINE CSV File in the Path.Please Check!")
            return False

        #临时存放对应的索引
        field_index = dict()
        for fi in filelist:
            fp = os.path.join(self.__xdr_path, fi)
            if os.path.isdir(fp) or fi.split('.')[-1] != 'csv':
                continue
            xdrFlag = os.path.split(os.path.realpath(fp))[1].split('.')[0].split('_')[-1]
            raw = open(fp, 'rb').read()
            result = chardet.detect(raw)
            encoding = result['encoding']
            #print(fp)
            with open(fp, 'r', encoding=encoding) as f:
                try:
                    csvrd = csv.DictReader(f)
                    # dictreader特性，第一行为标题，作为key值，数据从第二行开始
                    # 按设计要求，xdr_dr_type分regstr、comment，其它都作为正常话单字段处理
                    # 若为regstr，则xdr_field_name为具体正则，具体配置方式看样例
                    # 话单获取正则也可以单独放一个csv文件
                    for row in csvrd:
                        xdr_type = row["XDR_DR_TYPE"].lower() + '_' + xdrFlag
                        fieldname = row["XDR_FIELD_NAME"]
                        index = row["XDR_FIELD_INDEX"]
                        fieldtype = row["XDR_FIELD_TYPE"]
                        if xdr_type == "comment" + '_' + xdrFlag:
                            #comment row
                            pass
                        elif xdr_type == "regstr" + '_' + xdrFlag:
                            pass
                            #if re.search(r'^\d\|\d\|\d$',row["XDR_FIELD_TYPE"]):
                            #    tmpL = row["XDR_FIELD_TYPE"].split('|')
                            #    reg = regdef()
                            #    reg.regstr = fieldname
                            #    reg.gnum = int(tmpL[0])
                            #    reg.i_dr = int(tmpL[1])
                            #    reg.i_xdr = int(tmpL[2])
                            #    if reg.gnum == 0 or reg.gnum == 1:
                            #        self.__xdr_regstr.append(reg)
                            #    elif reg.i_xdr == 0:
                            #        pass
                            #    elif reg.i_xdr == reg.i_dr:
                            #        pass
                            #    elif reg.gnum < reg.i_dr or reg.gnum < reg.i_xdr:
                            #        pass
                            #    else:
                            #        self.__xdr_regstr.append(reg)
                        else:
                            if xdr_type not in self.__xdr_define:
                                self.__xdr_define[xdr_type] = list()
                                self.__xdr_field_type[xdr_type] = list()
                                field_index[xdr_type] = list()
                            self.__xdr_define[xdr_type].append(fieldname.upper())
                            self.__xdr_field_type[xdr_type].append(fieldtype)
                            field_index[xdr_type].append(int(index))
                except Exception as e:
                    self.__log.logger.error("The CSV File is invalid.Please Check!")
                    self.__log.logger.error(e)
                    self.__xdr_define.clear()
                    self.__xdr_field_type.clear()
                    #self.__xdr_regstr.clear()
                    self.__def_index.clear()
                    return False

        for key in self.__xdr_define.keys():
            self.__xdr_define[key] = sortListByAnother(self.__xdr_define[key], field_index[key])
            self.__xdr_field_type[key] = sortListByAnother(self.__xdr_field_type[key], field_index[key])
            field_num = len(self.__xdr_define[key])
            if field_num not in self.__def_index:
                self.__def_index[field_num] = list()
            self.__def_index[field_num].append(key)
        
        self.__getRegstr(regDictList)
        return True
    
    def __analyseXdrStr(self, xdrStr):
        # 返回 [("dr_type1", reg_def1, xdrstr1, xdr1),("dr_type2", reg_def2, xdrstr2, xdr2)]
        # 如果话单中没有获取，dr_type为None
        contentList = list()
        xdrlist = xdrStr.split('\n')
        for xdr in xdrlist:
            if len(xdr) == 0:
                continue
            flag = False
            for i, regd in enumerate(self.__xdr_regstr):
                res = re.search(regd.regstr, xdr)
                if res:
                    grps = res.groups()
                    grp_len = len(grps)
                    if grp_len != regd.gnum:
                        continue
                    xdr_type = "None"
                    if grp_len == 0:
                        xdr_content = res.group()
                    elif grp_len == 1:
                        xdr_content = grps[0]
                    else:
                        xdr_content = grps[regd.i_xdr - 1]
                        if regd.i_dr != 0:
                            xdr_type = grps[regd.i_dr - 1]
                    
                    contentList.append((xdr_type, regd, xdr, xdr_content))
                    flag = True
                    break
            if not flag:
                regd = regdef()
                contentList.append(("None", regd, xdr, xdr))
        return contentList

    def analyseXdrContent(self, xdrStr):
        self.__xdrDecode.clear()
        #print(self.__def_index)
        xdrList = self.__analyseXdrStr(xdrStr)
        # xdrList : [("dr_type1", reg_def1, xdrstr1, xdr1),("dr_type2", reg_def2, xdrstr2, xdr2)]
        #print(len(xdrList))
        for i, xdr in enumerate(xdrList):
            xdr_type_d = xdr[0]
            regd = xdr[1]
            xdrstr = xdr[2]
            values = xdr[3].split(';')
            xdrLen = len(values) - 1

            if xdrLen in self.__def_index:
                tmpL = list()
                keyvalueL = [xdrLen, xdr_type_d, regd, xdrstr, xdrstr]
                tmpL.append(keyvalueL)
                tmpL.append(values)
                fitDrTypeList = list()
                for xdr_type in self.__def_index[xdrLen]:
                    #keys = self.__xdr_define[xdr_type][0]
                    #resXdr[xdr_type] = [[key, values[j]] for j, key in enumerate(keys)]
                    fitDrTypeList.append(xdr_type)
                tmpL.append(fitDrTypeList)
                self.__xdrDecode[i] = tmpL
            else:
                self.__log.logger.error("There's no XDR_DIFINE Which can fit the bill. In the Line : " + str(i) + " .Field Number : " + str(xdrLen))
                return False
        return True

    def __setOneXdrFields(self, keyValue, xdr_seq):
        # seq从0开始
        # {seq:[  第一个元素(0)，本条话单一些属性信息列表
        #         ['xdrlen','dr_type_default',reg_def,'xdr_ori','xdr_new'],
        #         第二个元素(1)，本条话单的各个字段值列表
        #         ['value1','value2',...],
        #         第三个元素(2)，本条话单可以匹配到话单类型列表
        #         ['dr_type1','dr_type2',...]
        #      ]
        # }
        # keyvalue : {'field_index1':new_value,...}
        xdrLen = self.__xdrDecode[xdr_seq][0][0]
        for k, v in keyValue.items():
            k = int(k)
            v = v
            if xdrLen >= k:
                self.__xdrDecode[xdr_seq][1][k] = v
        xdrstr = ""
        for value in self.__xdrDecode[xdr_seq][1]:
            xdrstr = xdrstr + value + ";"
        return xdrstr

    def __getReplaceStr(self, regd, xdr):
        repStr = ''
        for i in range(1, regd.gnum + 1):
            if i == regd.i_xdr:
                repStr = repStr + xdr
            else:
                repStr = repStr + '\\' + str(i)
        if regd.gnum == 0 or regd.gnum == 1:
            repStr = xdr
        return repStr
    
    def updateXdrFields(self, keyValue, xdr_seq=0):
        # keyvalue : {'field_index1':new_value,...}
        xdr_num = len(self.__xdrDecode)
        if xdr_num == 0:
            self.__log.logger.error("There's no xdr decoded.")
            return False

        if xdr_seq > xdr_num:
            self.__log.logger.error("Total " + str(xdr_num) + " Xdr in The File.")
            return False

        out_start = 0
        out_end = xdr_num
        if xdr_seq > 0:
            out_start = xdr_seq -1
            out_end = xdr_seq

        for i in range(out_start, out_end):
            xdr_str = self.__setOneXdrFields(keyValue, i)
            repStr = self.__getReplaceStr(self.__xdrDecode[i][0][2], xdr_str)
            xdr_new = re.sub(self.__xdrDecode[i][0][2].regstr, repStr, self.__xdrDecode[i][0][3])
            self.__xdrDecode[i][0][4] = xdr_new
        return True

    def getNewXdrList(self, xdr_seq=0):
        xdr_num = len(self.__xdrDecode)
        retList = []
        if xdr_num == 0:
            self.__log.logger.error("There's no xdr decoded.")
        elif xdr_seq > xdr_num:
            self.__log.logger.error("Total " + str(xdr_num) + " Xdr in The File.")
        else:
            out_start = 0
            out_end = xdr_num
            if xdr_seq > 0:
                out_start = xdr_seq -1
                out_end = xdr_seq

            for i in range(out_start, out_end):
               newXdr = ';'.join(self.__xdrDecode[i][1])
               retList.append(newXdr)
        return retList
    
    def getNewSdlList(self, xdr_seq=0):
        xdr_num = len(self.__xdrDecode)
        retList = []
        if xdr_num == 0:
            self.__log.logger.error("There's no xdr decoded.")
        elif xdr_seq > xdr_num:
            self.__log.logger.error("Total " + str(xdr_num) + " Xdr in The File.")
        else:
            out_start = 0
            out_end = xdr_num
            if xdr_seq > 0:
                out_start = xdr_seq -1
                out_end = xdr_seq
    
            for i in range(out_start, out_end):
               retList.append(self.__xdrDecode[i][0][4])
        return retList

    def restoreFromOri(self):
        oriList = []
        for i in range(len(self.__xdrDecode)):
            oriList.append(self.__xdrDecode[i][0][3])

        oriStr = '\n'.join(oriList)
        self.__xdrDecode.clear()
        return self.analyseXdrContent(oriStr)