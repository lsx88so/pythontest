#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import os
import sys
import csv
import re
import getopt
#from enum import Enum
import collections

class regdef:
    def __init__(self):
        self.regstr = r'.*'
        self.gnum = 0
        self.i_dr = 0
        self.i_xdr = 0

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
        #存放话单匹配正则 regdef
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
                        if xdr_type == "comment" + '_' + xdrFlag:
                            #comment row
                            pass
                        elif xdr_type == "regstr" + '_' + xdrFlag:
                            #print fieldname
                            if re.search(r'^\d\|\d\|\d$',row["XDR_FIELD_TYPE"]):
                                tmpL = row["XDR_FIELD_TYPE"].split('|')
                                reg = regdef()
                                reg.regstr = fieldname
                                reg.gnum = int(tmpL[0])
                                reg.i_dr = int(tmpL[1])
                                reg.i_xdr = int(tmpL[2])
                                if reg.gnum == 0 or reg.gnum == 1:
                                    self.xdr_regstr.append(reg)
                                elif reg.i_xdr == 0:
                                    pass
                                elif reg.i_xdr == reg.i_dr:
                                    pass
                                elif reg.gnum < reg.i_dr or reg.gnum < reg.i_xdr:
                                    pass
                                else:
                                    self.xdr_regstr.append(reg)
                        else:
                            if not self.xdr_content.has_key(xdr_type):
                                self.xdr_content[xdr_type] = list()
                                field_index[xdr_type] = list()
                            self.xdr_content[xdr_type].append(fieldname.upper())
                            field_index[xdr_type].append(int(index))
                except Exception as e:
                    print "The CSV File is invalid.Please Check!"
                    print e
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
    def __init__(self, xdrcsv):
        self.xdr_index = xdrcsv.xdr_index
        self.xdr_content = xdrcsv.xdr_content
        self.xdr_regstr = xdrcsv.xdr_regstr
        #解析文件得到的XDR
        # seq从1开始
        # {seq:[ #话单符合字段数的各个dr_type列表
        #         #第一个元素，本条话单一些属性信息列表
        #         ['xdrlen','dr_type_default',reg_def,'xdr_ori']
        #         第二个元素开始，每种dr_type的一个dict
        #         {
        #          'dr_type1':[['field1','value1'],['field2','value2']]
        #         ,
        #          'dr_type2':[['field1','value1'],['field2','value2']]
        #         }
        #      ]
        # }
        self.xdrDecode = collections.OrderedDict()

    def analyseXdrFile(self, fi):
        # 返回 [("dr_type1", reg_def1, xdrstr1, xdr1),("dr_type2", reg_def2, xdrstr2, xdr2)]
        # 如果话单中没有获取，dr_type为None
        contentList = list()
        with open(fi, 'r') as fd:
            xdrlist = fd.readlines()
            for xdr in xdrlist:
                flag = False
                for i, regd in enumerate(self.xdr_regstr):
                    #print regstr
                    res = re.search(regd.regstr, xdr)
                    if res:
                        grps = res.groups()
                        grp_len = len(grps)
                        if grp_len != regd.gnum:
                            continue

                        xdr_type = "None"
                        if grp_len == 0:
                            xdr_content = res.group()
                            #xdr_content = eval(repr(xdr_content).replace('\\\\', '\\'))
                            #contentList.append(("None", regd, xdr_content))
                        elif grp_len == 1:
                            xdr_content = grps[0]
                            #xdr_content = eval(repr(xdr_content).replace('\\\\', '\\'))
                            #contentList.append(("None", regd, xdr_content))
                        else:
                            xdr_content = grps[regd.i_xdr - 1]
                            #xdr_content = eval(repr(xdr_content).replace('\\\\', '\\'))
                            if regd.i_dr != 0:
                                xdr_type = grps[regd.i_dr - 1]
                        
                        contentList.append((xdr_type, regd, xdr, xdr_content))
                        flag = True
                        break
                if not flag:
                    regd = regdef()
                    contentList.append(("None", regd, xdr, xdr))
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
        # xdrList : [("dr_type1", reg_def1, xdrstr1, xdr1),("dr_type2", reg_def2, xdrstr2, xdr2)]
        for i, xdr in enumerate(xdrList,1):
            xdr_type_d = xdr[0]
            regd = xdr[1]
            xdrstr = xdr[2]
            values = xdr[3].split(';')
            xdrLen = len(values) - 1

            if self.xdr_index.has_key(xdrLen):
                tmpL = list()
                keyvalueL = [xdrLen, xdr_type_d, regd, xdrstr]
                tmpL.append(keyvalueL)
                resXdr = dict()
                for xdr_type in self.xdr_index[xdrLen]:
                    #print "xdr_type :" + xdr_type
                    keys = self.xdr_content[xdr_type]
                    resXdr[xdr_type] = [[key, values[j]] for j, key in enumerate(keys)]
                tmpL.append(resXdr)
                self.xdrDecode[i] = tmpL
            else:
                print "There's no XDR_DIFINE Which can fit the bill.\nIn the Line : " + str(
                    i) + " .Field Number : " + str(xdrLen)
                sys.exit()

    def outDecodeOne(self, xdrL, regstr, xdr_seq, dr_type):
        #     [ #话单符合字段数的各个dr_type列表
        #         #第一个元素，本条话单一些属性信息列表
        #         ['xdrlen','dr_type_default',reg_def,'xdr_ori']
        #         第二个元素开始，每种dr_type的一个dict
        #         {
        #          'dr_type1':[['field1','value1'],['field2','value2']]
        #         ,
        #          'dr_type2':[['field1','value1'],['field2','value2']]
        #         }
        #      ]

        mat = "{:4}{:>28}\t:\t{:}"
        
        if xdrL[0][1] == "None":
            reg_dr_type = r'.*'
        else:
            reg_dr_type = r'^' + xdrL[0][1] + r'_.*'
        
        if len(dr_type) > 0:
            reg_dr_type = dr_type
        
        flag = False
        res = ""
        for i, key in enumerate(xdrL[1].keys(), 1):
            if re.search(reg_dr_type, key, flags=re.IGNORECASE):
                flag = True
                #print "\nXDR " + str(xdr_seq) + " - " + str(i) + ": " + key + "\tField Number : " + str(xdrL[0][0])
                res = res + "\nXDR " + str(xdr_seq) + " - " + str(i) + ": " + key + "\tField Number : " + str(xdrL[0][0]) + "\n"
                for j, field in enumerate(xdrL[1][key], 1):
                    outstr = mat.format(str(j) + ".", field[0], field[1])
                    #print "\t\t" + field[0] + "\t:\t" + field[1]
                    if re.search(regstr, field[0], flags=re.IGNORECASE):
                        #print outstr
                        res = res + outstr + "\n"
                #res = res + "\n"    
        
        if not flag:
            #print "XDR " + str(xdr_seq) + ": There's no kind which meets requirements.\nDefault type gived is [" \
            #    + xdrL[0][1] + "]\tField Number : " + str(xdrL[0][0]) + "\tAnd [" + str(len(xdrL[1])) + "] kinds which find in XDR_DIFINE."
            res = res + "\nXDR " + str(xdr_seq) + ": There's no kind which meets requirements.\nDefault type gived is [" \
                + xdrL[0][1] + "]\tField Number : " + str(xdrL[0][0]) + "\tAnd [" + str(len(xdrL[1])) + "] kinds which find in XDR_DIFINE."
        return res

    def outDecode(self, regstr, dr_type, out_path, xdr_seq=-1, outFlag=False):
        xdr_num = len(self.xdrDecode)
        if xdr_num == 0:
            print "There's no xdr decoded."
            sys.exit()

        if xdr_seq > xdr_num:
            print "Total " + str(xdr_num) + " Xdr in The File."
            sys.exit()

        out_start = 1
        out_end = xdr_num + 1
        if xdr_seq > 0:
            out_start = xdr_seq
            out_end = xdr_seq + 1

        if outFlag:
            with open(out_path, 'w') as f:
                for i in range(out_start, out_end):
                    f.write(self.outDecodeOne(self.xdrDecode[i], regstr, i, dr_type) + "\n")
                print "OutPut Decode File Successfull.Path : " + out_path
        else:
            for i in range(out_start, out_end):
                print self.outDecodeOne(self.xdrDecode[i], regstr, i, dr_type)

    def setOneXdrFields(self, keyValue, xdr_seq_r):
        xdrkey = self.xdrDecode[xdr_seq_r][1].keys()[0]
        for kv in keyValue:
            #由于第一个是dr_type,正式话单从第二个开始,这里不需要减1
            k = int(kv[0])
            v = kv[1]
            if len(self.xdrDecode[xdr_seq_r][1][xdrkey]) >= k:
                self.xdrDecode[xdr_seq_r][1][xdrkey][k - 1][1] = v
        xdrstr = ""
        for value in self.xdrDecode[xdr_seq_r][1][xdrkey]:
            xdrstr = xdrstr + value[1] + ";"
        #xdrstr = xdrstr + "\n"
        #print xdrstr
        return xdrstr

    def getReplaceStr(self, regd, xdr):
        repStr = ''
        for i in range(1, regd.gnum + 1):
            if i == regd.i_xdr:
                repStr = repStr + xdr
            else:
                repStr = repStr + '\\' + str(i)
        if regd.gnum == 0 or regd.gnum == 1:
            repStr = xdr
        return repStr
    
    def updateXdrFields(self, keyValue, outPath, xdr_seq=-1, outFlag=False, outtype=0):
        xdr_num = len(self.xdrDecode)
        if xdr_num == 0:
            print "There's no xdr decoded."
            sys.exit()

        if xdr_seq > xdr_num:
            print "Total " + str(xdr_num) + " Xdr in The File."
            sys.exit()

        out_start = 1
        out_end = xdr_num + 1
        if xdr_seq > 0:
            out_start = xdr_seq
            out_end = xdr_seq + 1

        if outFlag:
            with open(outPath, 'w') as f:
                for i in range(out_start, out_end):
                    if outtype == 0:
                        xdr_u = self.setOneXdrFields(keyValue, i)
                        repStr = self.getReplaceStr(self.xdrDecode[i][0][2], xdr_u)
                        xdr_new = re.sub(self.xdrDecode[i][0][2].regstr, repStr, self.xdrDecode[i][0][3])
                        f.write(xdr_new + "\n")
                    else:
                        f.write(self.setOneXdrFields(keyValue, i) + "\n")
                print "OutPut Update File Successfull.Path : " + outPath
        else:
            for i in range(out_start, out_end):
                if outtype == 0:
                    xdr_u = self.setOneXdrFields(keyValue, i)
                    repStr = self.getReplaceStr(self.xdrDecode[i][0][2], xdr_u)
                    xdr_new = re.sub(self.xdrDecode[i][0][2].regstr, repStr, self.xdrDecode[i][0][3])
                    #print self.xdrDecode[i][0][3]
                    print xdr_new
                else:
                    print self.setOneXdrFields(keyValue, i)

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
    print '\nusage: \n' + ex + ' -a action -i inFile [-r regstr] [-n seq] [-o] [-u modifylist] [-t dr_type] [-h] [--output=filepath] [--outtype=0|1]'
    print '''
arguments:
  -h                            show this help message and exit.
  -a action                     action mode, d : decode xdr; u : update xdr field; v : view the xdr define.
  -i inFile                     input file. it needs when action mode in [d|u].
  -r regstr                     a regulation string.it well be used in action [d|v].when in action [d], it takes effect on print mode only.
  -n seq                        sequence no of the xdr in inFile.optional argument.default deal all xdrs.
  -o, [--output=filepath]       output flag.default path is the same with inFile.it can be given by using [output].
                                optional argument.it works when action in [d|u].
  --outtype=0|1                 can be used in mode [u].0 : output content besides xdr; 1 : only output xdr.default 0.
  -u modifylist                 modify fields string.like "15:13;4:11" , 15/4 means the field index in the dr_type define; 13/11 means the new value.
                                it needs when action mode in [u].
  -t dr_type                    a regulation string.it means the dr_type you want to view.
                                it mostly needs when action mode in [v].
                                Also it can be used in Mode [d] which can only print the matched.

for example:
    xdrviewalone.py -a v -t dr_ggprs -r user_number
    xdrviewalone.py -a d -i ./tmp/test_ggprs_rating_2g_200k_cell_002
    xdrviewalone.py -a d -i ./tmp/test_ggprs_rating_2g_200k_cell_002 -r user_number
    xdrviewalone.py -a d -i ./tmp/test_ggprs_rating_2g_200k_cell_002 -o
    xdrviewalone.py -a d -i ./tmp/test_ggprs_rating_2g_200k_cell_002 -o --output=./t.xdr
    xdrviewalone.py -a d -i ./tmp/B2019042800274.dat -n 4
    xdrviewalone.py -a u -i ./tmp/test_ggprs_rating_2g_200k_cell_002 -u "151:123"
    xdrviewalone.py -a u -i ./tmp/test_ggprs_rating_2g_200k_cell_002 -u "151:123;147:1"
    xdrviewalone.py -a u -i ./tmp/B2019042800274.dat -s "3:123;5:111" -n 2

'''


def main(argv):
    exec_path = os.path.split(os.path.realpath(__file__))[0]
    cur_path = os.getcwd()

    xdr_path = os.path.join(exec_path, 'xdr_define')
    if not os.path.exists(os.path.join(xdr_path, 'xdr_regstr.csv')):
        print "There's no file : xdr_regstr.csv in the path: %s" % xdr_path
        printHelp()
        sys.exit(1)
    xdrcsv = xdr_csv(xdr_path)
    xdrcsv.analyseCsv()
    xdrfunc = xdr_analyse(xdrcsv)

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
    outtype = 0
    try:
        opts, args = getopt.getopt(argv[1:], "hoa:r:n:u:t:i:", ["output=","outtype="])
    except getopt.GetoptError:
        print "Your input ERROR! Please Check!"
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        elif opt == "-a":
            mode = arg
        elif opt == "-i":
            inFile = arg
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
        elif opt == "--outtype":
            if re.search(r'[0-9]+', arg):
                outtype = int(arg)
        elif opt == "-u":
            mstr = arg
        elif opt == "-t":
            dr_type = arg
    
    if len(outFile) == 0:
        outFile = inFile + '.decode'
        if mode  == 'u':
            outFile = inFile + '.update'

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
            xdrfunc.outDecode(regstr, dr_type, outFile, seq, outFlag)
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
            xdrfunc.updateXdrFields(modifyStr, outFile, seq, outFlag, outtype)
    elif re.search(r'[v]', mode) and len(dr_type) > 0:
        xdrcsv.viewXdrDefine(dr_type, regstr)
    else:
        print "Your Input ERROR!\naction mode error or inFile has no such file or no dr_type."
        printHelp()
        sys.exit(2)

    #for key in xdrcsv.xdr_index.keys():
    #    print "Key : " + str(key) + "\t\tValues : " + str(len(xdrcsv.xdr_index[key]))
    #    #print "Values : " + str(len(xdrcsv.xdr_index[key]))
    #    #print xdrcsv.xdr_index[key]


if __name__ == "__main__":
    main(sys.argv)
