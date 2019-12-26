#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import os
import sys
import csv
import re
import getopt
from enum import Enum
import collections

class xdr_csv:
    def __init__(self, xdr_path):
        if not (os.path.exists(xdr_path) and os.path.isdir(xdr_path)):
            print "XDR_DEFINE CSV File's Path is Not Exist.Please Check!"
            print "Path : " + xdr_path
            sys.exit()
        self.xdr_path = xdr_path
        #存放XDR具体内容:{"dr_gsm_ln" : ["field1","field2",...]}
        self.xdr_content = dict()
        #存放XDR索引:{fieldnum : ["dr_type1","dr_type2",...]}
        self.xdr_index = dict()
        #存放话单匹配正则
        self.xdr_regstr = list()

    def sortListByAnother(self, a, b, r=False):
        ziped = zip(b, a)
        ziped.sort(reverse=r)
        return list(zip(*ziped)[1])

    def analyseCsv(self):
        filelist = os.listdir(self.xdr_path)
        filelist.sort()
        if len(filelist) == 0:
            print "There's no XDR_DEFINE CSV File in the Path.Please Check!"
            sys.exit()

        field_index = dict()  #临时存放对应的索引
        for fi in filelist:
            xdrFlag = os.path.split(
                os.path.realpath(fi))[1].split('.')[0].split('_')[1]

            fi = os.path.join(self.xdr_path, fi)
            with open(fi) as f:
                try:
                    csvrd = csv.DictReader(f)
                    # dictreader特性，第一行为标题，作为key值，数据从第二行开始
                    # 按设计要求，第二行为话单匹配正则，xdr_dr_type为regstr，xdr_field_name为具体正则
                    # 第三行开始为正式数据记录
                    # 如果匹配正则有多行，正式数据顺延
                    # 话单正则也可以单独放一个csv文件
                    for row in csvrd:
                        xdr_type = row["XDR_DR_TYPE"].lower() + '_' + xdrFlag
                        fieldname = row["XDR_FIELD_NAME"]
                        index = row["XDR_FIELD_INDEX"]
                        if xdr_type == "comment":
                            #comment row
                            pass
                        elif xdr_type == "regstr" + '_' + xdrFlag:
                            #print fieldname
                            self.xdr_regstr.append(fieldname)
                        else:
                            if not self.xdr_content.has_key(xdr_type):
                                self.xdr_content[xdr_type] = list()
                                field_index[xdr_type] = list()
                            self.xdr_content[xdr_type].append(fieldname.upper())
                            field_index[xdr_type].append(int(index))
                except:
                    print "The CSV File is invalid .Please Check!"
                    sys.exit()

        for key in self.xdr_content.keys():
            self.xdr_content[key] = self.sortListByAnother(
                self.xdr_content[key], field_index[key])
            field_num = len(self.xdr_content[key])
            if not self.xdr_index.has_key(field_num):
                self.xdr_index[field_num] = list()
            self.xdr_index[field_num].append(key)

    def viewXdrDefine(self, xdr_type, regstr=r'.*'):
        mat = "\t{:4}{:}"
        hasFlag = False
        for key in self.xdr_content.keys():
            if re.search(xdr_type, key, flags=re.IGNORECASE):
                hasFlag = True
                print "XDR_TYPE : " + key + "\tField Number : " + str(
                    len(self.xdr_content[key]))
                i = 1
                for field in self.xdr_content[key]:
                    #print "\t\t" + i + "" + field
                    if re.search(regstr, field, flags=re.IGNORECASE):
                        print mat.format(str(i) + ".", field)
                    i = i + 1
                print "\n"
        if not hasFlag:
            print "There's no dr_type that fills the bill."


class xdr_analyse:
    def __init__(self, xdr_index, xdr_content, xdr_regstr):
        self.xdr_index = xdr_index
        self.xdr_content = xdr_content
        self.xdr_regstr = xdr_regstr
        #解析文件得到的XDR
        # seq从1开始
        # {seq:[ #话单符合字段数的各个dr_type
        #         [ #dr_type对应的详细字段和值
        #          ['xdrlen','dr_type'],['field1','value1'],['field2','value2']
        #         ],
        #         [ #dr_type对应的详细字段和值
        #          ['xdrlen','dr_type'],['field1','value1'],['field2','value2']
        #         ]
        #        ]
        # }
        self.xdrDecode = collections.OrderedDict()
        #修改的XDR
        self.xdrModify = list()

    def analyseXdrFile(self, fi):
        # [("dr_type",xdr1),("dr_type",xdr2)]
        # 如果话单中没有获取，dr_type为None
        contentList = list()
        with open(fi, 'r') as fd:
            xdrlist = fd.readlines()
            for xdr in xdrlist:
                flag = False
                for regstr in self.xdr_regstr:
                    #print regstr
                    res = re.search(regstr, xdr)
                    if res:
                        grp_t = res.groups()
                        if len(grp_t) == 0:
                            xdr_content = res.group()
                            #xdr_content = eval(repr(xdr_content).replace('\\\\', '\\'))
                            contentList.append(("None", xdr_content))
                        elif len(grp_t) == 1:
                            xdr_content = grp_t[0]
                            #xdr_content = eval(repr(xdr_content).replace('\\\\', '\\'))
                            contentList.append(("None", xdr_content))
                        else:
                            xdr_content = grp_t[1]
                            #xdr_content = eval(repr(xdr_content).replace('\\\\', '\\'))
                            contentList.append((grp_t[0], xdr_content))
                        flag = True
                        break
                if not flag:
                    contentList.append(("None", xdr))
                #if re.search(r'obbs:S:1.3:{{', xdr):
                #    res = re.search(r'}},dr_[_\w]+;(.*)}}', xdr)
                #    if res:
                #        xdr_content = res.group(1)
                #        #xdr_content = eval(repr(xdr_content).replace('\\\\', '\\'))
                #        contentList.append(xdr_content)
                #elif re.search(r'SDS[0-9]{{', xdr):
                #    res = re.search(r'}},dr_[_\w]+,dr_[_\w]+;(.*)}}', xdr)
                #    if res:
                #        xdr_content = res.group(1)
                #        #xdr_content = eval(repr(xdr_content).replace('\\\\', '\\'))
                #        contentList.append(xdr_content)
                #else:
                #    contentList.append(xdr)
        return contentList

    def decodeXdr(self, xdrList):
        # xdrList : [("dr_type",xdr1),("dr_type",xdr2)]
        for i, xdr in enumerate(xdrList,1):
            xdr_type_d = xdr[0]
            values = xdr[1].split(';')
            xdrLen = len(values) - 1

            if self.xdr_index.has_key(xdrLen):
                tmpL = list()
                for xdr_type in self.xdr_index[xdrLen]:
                    resXdr = list()
                    keyvalueL = [xdrLen, xdr_type + "|" + xdr_type_d]
                    resXdr.append(keyvalueL)
                    keys = self.xdr_content[xdr_type]
                    resXdr.extend([[key, values[j]] for j, key in enumerate(keys)])
                    tmpL.append(resXdr)
                self.xdrDecode[i] = tmpL
            else:
                print "There's no XDR_DIFINE Which can fit the bill.\nIn the Line : " + str(
                    i) + " .Field Number : " + str(xdrLen)
                sys.exit()

    def printOne(self, xdrL, regstr, xdr_seq, dr_type):
        mat = "{:4}{:>28}\t:\t{:}"
        lenXdrL = len(xdrL)

        for y, xdr in enumerate(xdrL, 1):
            for i, field in enumerate(xdr):
                if i == 0:
                    xdr_type = field[1].split('|')[0]
                    xdr_type_d = field[1].split('|')[1]
                    if xdr_type_d != "None":
                        if not re.search(r'^' + xdr_type_d + r'_.*', xdr_type, flags=re.IGNORECASE):
                            if lenXdrL == 1:
                                print "XDR " + str(xdr_seq) + ": There's no XDR_DIFINE Which can fit the bill.\nDefault type gived is [" + xdr_type_d + "]"
                            break
                    if lenXdrL > 1 and not re.search(dr_type, xdr_type, flags=re.IGNORECASE):
                        break
                    print "\nXDR " + str(
                        xdr_seq) + " - " + str(
                        y) + ": " + xdr_type + "\tField Number : " + str(
                            field[0])
                else:
                    outstr = mat.format(str(i) + ".", field[0], field[1])
                    #print "\t\t" + field[0] + "\t:\t" + field[1]
                    if re.search(regstr, field[0], flags=re.IGNORECASE):
                        print outstr

    def outPrint(self, regstr, dr_type, xdr_seq=-1):
        xdr_num = len(self.xdrDecode)
        if xdr_num == 0:
            print "There's no xdr decoded."
            sys.exit()
        if xdr_seq == -1:
            for i, xdrL in self.xdrDecode.items():
                self.printOne(xdrL, regstr, i, dr_type)
        elif xdr_seq <= xdr_num:
            self.printOne(self.xdrDecode[xdr_seq], regstr, xdr_seq, dr_type)
        else:
            print "Total " + str(xdr_num) + " Xdr in The File."
            sys.exit()

    def outPut(self, out_path):
        fd = open(out_path, 'w')
        mat = "{:4}{:>28}\t:\t{:}"
        for i, xdrL in self.xdrDecode.items():
            for j, xdr in enumerate(xdrL, 1):
                for k, field in enumerate(xdr):
                    if k == 0:
                        fd.write("XDR " + str(i) + " - " + str(j)+ ": " + field[1].split('|')[0] + "\tField Number : " + str(
                            field[0]) + '\n')
                    else:
                        outstr = mat.format(str(k) + ".", field[0], field[1])
                        fd.write(outstr + '\n')
                fd.write('\n')
            fd.write('\n')
        fd.close()
        print "OutPut Decode File Successfull.Path : " + out_path

    def setOneXdrFields(self, keyValue, xdr_seq_r):
        for kv in keyValue:
            #由于第一个是dr_type,正式话单从第二个开始,这里不需要减1
            k = int(kv[0])
            v = kv[1]
            if len(self.xdrDecode[xdr_seq_r][0]) > k + 1:
                self.xdrDecode[xdr_seq_r][0][k][1] = v
        xdrstr = ""
        for i, value in enumerate(self.xdrDecode[xdr_seq_r][0]):
            if i == 0:
                pass
            else:
                xdrstr = xdrstr + value[1] + ";"
        xdrstr = xdrstr + "\n"
        print xdrstr

    def setXdrFields(self, keyValue, xdr_seq=-1):
        xdr_num = len(self.xdrDecode)
        if xdr_num == 0:
            print "There's no xdr decoded."
            sys.exit()
        if xdr_seq == -1:
            for i in range(1, xdr_num + 1):
                self.setOneXdrFields(keyValue, i)
        elif xdr_seq <= xdr_num:
            self.setOneXdrFields(keyValue, xdr_seq)
        else:
            print "Total " + str(xdr_num) + " Xdr in The File."
            sys.exit()


def convEnv(path):
    #path = '$DATA01/decodei/$(DATA02)/de_gsm_local_d'
    #print path
    if re.search(r'^~', path):
        value = os.environ.get('HOME')
        if value:
            path = re.sub(r'^~', value, path, 1)

    while (True):
        #res = re.search(r'\$[\(]?([A-Za-z0-9_]+)[\)]?',path)
        res = re.search(r'\$[\(]?(\w+)[\)]?', path)
        if res:
            env = res.group(1)
            #print env
            #path = re.sub(r'\$[\(\)A-Za-z0-9]+',os.environ.get(env),path,1)
            value = os.environ.get(env)
            if value:
                path = re.sub(r'\$[\(\)\w]+', value, path, 1)
            else:
                break
        else:
            break
        #break
    return re.sub(r'//', '/', path)


def printHelp():
    ex = os.path.split(os.path.realpath(__file__))[1]
    print '\nusage: \n' + ex + ' -m action [-f inFile] [-r regstr] [-n seq] [-o [outFile]] [-s modifylist] [-t dr_type] [-h]'
    print '''
arguments:
  -h                            show this help message and exit.
  -m action                     action mode, d : decode xdr; u : update xdr field; v : view the xdr define.
  -f inFile                     input file. it needs when action mode in [d|u].
  -r regstr                     a regulation string.it well be used in action [d|v].when in action [d], it takes effect on print mode only.
  -n seq                        sequence no of the xdr in inFile.optional argument.default deal all xdrs.
  -o, [--output=filepath]       output flag.default path is the same with inFile.it can be given by using [output].
                                optional argument.it works when action in [d].default only print mode.
  -s modifylist                 modify fields string.like "15:13;4:11" , 15/4 means the field index in the dr_type define; 13/11 means the new value.
                                it needs when action mode in [u].
  -t dr_type                    a regulation string.it means the dr_type you want to view.
                                it mostly needs when action mode in [v].
                                Also it can be used in Mode [d] which can only print the matched.

for example:
    xdrviewalone.py -m v -t dr_ggprs -r user_number
    xdrviewalone.py -m d -f ./tmp/test_ggprs_rating_2g_200k_cell_002
    xdrviewalone.py -m d -f ./tmp/test_ggprs_rating_2g_200k_cell_002 -r user_number
    xdrviewalone.py -m d -f ./tmp/test_ggprs_rating_2g_200k_cell_002 -o
    xdrviewalone.py -m d -f ./tmp/test_ggprs_rating_2g_200k_cell_002 -o --output=./t.xdr
    xdrviewalone.py -m d -f ./tmp/B2019042800274.dat -n 4
    xdrviewalone.py -m u -f ./tmp/test_ggprs_rating_2g_200k_cell_002 -s "151:123"
    xdrviewalone.py -m u -f ./tmp/test_ggprs_rating_2g_200k_cell_002 -s "151:123;147:1"
    xdrviewalone.py -m u -f ./tmp/B2019042800274.dat -s "3:123;5:111" -n 2

'''


def main(argv):
    exec_path = os.path.split(os.path.realpath(__file__))[0]
    cur_path = os.getcwd()

    xdr_path = os.path.join(exec_path, 'xdr_define')
    if not os.path.exists(os.path.join(xdr_path, 'xdr_regstr.csv')):
        printHelp()
        sys.exit(1)
    xdrcsv = xdr_csv(xdr_path)
    xdrcsv.analyseCsv()
    xdrfunc = xdr_analyse(xdrcsv.xdr_index, xdrcsv.xdr_content, xdrcsv.xdr_regstr)

    #d : decode xdr
    #u : update xdr field
    #v : view the xdr define
    mode = ""
    regstr = ".*"
    dr_type = ""
    modifyStr = list()
    seq = -1
    outFlag = False
    inFile = r''
    outFile = r''
    mstr = ""
    try:
        opts, args = getopt.getopt(argv[1:], "hom:r:n:s:t:f:", ["output="])
    except getopt.GetoptError:
        print "Your input ERROR! Please Check!"
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        elif opt == "-m":
            mode = arg
        elif opt == "-f":
            inFile = arg
            outFile = arg + '.xdr'
        elif opt == "-r":
            regstr = arg
        elif opt == "-n":
            if re.search(r'[0-9]+', arg):
                seq = int(arg)
        elif opt == "-o":
            outFlag = True
        elif opt == "--output":
            if len(arg) > 0:
                outFile = arg
        elif opt == "-s":
            mstr = arg
        elif opt == "-t":
            dr_type = arg

    inFile = convEnv(inFile)
    outFile = convEnv(outFile)
    if len(inFile) > 0 and re.search(r'^\.', inFile):
        inFile = os.path.join(cur_path, inFile)
    if len(outFile) > 0 and re.search(r'^\.', outFile):
        outFile = os.path.join(cur_path, outFile)

    if re.search(r'[du]',
                 mode) and os.path.exists(inFile) and os.path.isfile(inFile):
        contentList = xdrfunc.analyseXdrFile(inFile)
        xdrfunc.decodeXdr(contentList)
        if mode == "d":
            if outFlag:
                xdrfunc.outPut(outFile)
            else:
                if dr_type == "":
                    dr_type = r'.*'
                xdrfunc.outPrint(regstr, dr_type, seq)
        elif mode == "u":
            #mstr : "15:13;4:11"
            for kvs in mstr.split(';'):
                kv = kvs.split(':')
                k = kv[0]
                if re.search(r'[0-9]+', k) and len(kv) > 1:
                    v = kv[1]
                    modifyStr.append((int(k), v))
                else:
                    print "Your Input ERROR!\nmodifylist error."
                    printHelp()
                    sys.exit(2)
            if len(modifyStr) == 0:
                print "Your Input ERROR!\nmodifylist error."
                printHelp()
                sys.exit(2)
            xdrfunc.setXdrFields(modifyStr, seq)
    elif re.search(r'[v]', mode) and len(dr_type) > 0:
        xdrcsv.viewXdrDefine(dr_type, regstr)
    else:
        print "Your Input ERROR!\naction mode error or inFile has no such file or no dr_type."
        printHelp()
        sys.exit(2)

    #xdr.viewXdrDefine(r'gprs', r'.*')

    ##fi = r'./tmp/test_ggprs_rating_2g_200k_cell_002'
    #fi = r'./tmp/B2019042800274.dat'
    #xdr_a = xdr_analyse(xdr.xdr_index, xdr.xdr_content)
    #contentList = xdr_a.analyseXdrFile(fi)

    #xdr_a.decodeXdr(contentList)
    #xdr_a.outPrint(r'.*', -1)
    #xdr_a.outPut(r'./tmp/tmp.xdr')
    #xdr_a.setXdrFields([(15,'13'),(4,"11")],-1)


if __name__ == "__main__":
    main(sys.argv)
