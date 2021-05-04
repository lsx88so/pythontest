#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from sdlbase import sdlNode
import sdlutils
import xdrutils
import asn1utils
#from sdlutils import sdlDefine
#from sdlutils import sdlContent
import pickle, json, re

if __name__ == "__main__":
    pass
    #vLen = 270
    #asnLength_b = int((vLen + 255)/256)
    #t = hex(int("1" + bin(asnLength_b)[2:].zfill(7), base=2))[2:].zfill(2) + hex(vLen)[2:].zfill(asnLength_b * 2)
    #print(t)
    #asn.1
    #asn1path = r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/asn5f8136.asn'
    #asn1path = r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/asn64_2ceng.asn'
    #asn1path = r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/asn7f72_3ceng.asn'
    #with open(asn1path, 'rb') as fr:
    #    rd = fr.read()
    #    asn1 = asn1utils.asn1Aanlyse(rd, loglevel="error")
    #    if asn1.anakyseAsn():
    #        asn1.printAsn1Tree(debug=True)
    #
    #    asn1path = r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/asn.out'
    #    with open(asn1path, 'wb') as fw:
    #        #fw.write(bytes.fromhex("5F813603323430"))
    #        retByetes = asn1.convToByteStream(asn1.root.children)
    #        fw.write(retByetes)
    
    #xdr
    #xdrdef = xdrutils.xdrDefine(r'/Users/liusx/Develop/VSCode/pythontest/python2/xdrview/xdr_define')
    #with open(r'/Users/liusx/Develop/VSCode/pythontest/python3/sdlutils/example/test.xdr') as f:
    #    xdrList = f.readlines()
    #xdrdef.analyseXdrDefine()
    #xdrdef.printXdrDefine("dr_ggprs_ln")
    #xdrdef.analyseXdrContent(xdrList[0])
    #xdrdef.printXdrList()

    #v8
    #sdldefine = sdlutils.sdlDefine("SXdr",r'/Users/liusx/Develop/VSCode/pythontest/python3/sdlutils/example/xdr_def_v8.sdl',r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/v8/test_v8.s',loglevel="error")
    #sdldefine.getSdlDefine(dumpMode=2)
    #sdldefine.printDefTree()

    #from sjson
    #with open(r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/v8/CMICceshi') as f:
    #with open(r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/v8/pgwcdr_5G.dat') as f:
    #    xdrList = f.readlines()
    #sdlcontent = sdlutils.sdlContent(xdrList[0],sdldefine)
    #sdlcontent.getSdlFromSjson()
    #sdlcontent.printSdlTree(isseq=True)

    #from json
    #with open(r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/v8/test1_v8.json', 'r') as fo:
    #    content = fo.read()
    #sdlcontent = sdlutils.sdlContent(content,sdldefine)
    #print(sdlcontent.getSdlFromJson(debugFlag=True))
    #sdlcontent.getSdlFromJson()
    #sdlcontent.printSdlTree(isseq=False)
    #sdlcontent.printSdlTree(isseq=True)

    #tojson
    #jsonPath = r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/v8/test1_v8.json'
    #ret = sdlcontent.convSdlToJson()
    #ret = sdlcontent.convSdlToJson(wFlag=True, wPath=jsonPath)
    #print(ret)

    #tosjson
    #sjsonPath = r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/v8/test1_v8.sjson'
    #sdlcontent.setLogLevel("debug")
    #ret = sdlcontent.convSdlToSjson()
    #ret = sdlcontent.convSdlToSjson(wFlag=True, wPath=sjsonPath)
    #print(ret)

    #addhead
    #retstr = sdlutils.addSdlHead_v8(ret)
    #with open(sjsonPath, 'w') as fi:
    #    fi.write(retstr + '\n')
    #testcdr = r'/Users/liusx/Develop/VSCode/pythontest/python3/sdlutils/example/test3.cdr.json'
    #with open(testcdr, 'r') as fi:
    #    sdlstr = fi.read()
    #retstr = sdlutils.addSdlHead(sdlstr)
    #print(retstr)

    #conv
    #extSdl = sdlcontent.extendContent()
    #if extSdl:
    #    sdlcontent.printSdlTree(extSdl, isseq=True)
    #    sdlnew = sdlcontent.shrinkContent(extSdl)
    #    if sdlnew:
    #        sdlcontent.printSdlTree(sdlnew, isseq=True)

    #v6
    #sdldefine = sdlutils.sdlDefine("SXdr",r'/Users/liusx/Develop/VSCode/pythontest/python3/sdlutils/example/xdr_def.sdl',r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/test.s')
    #sdldefine.getSdlDefine(dumpMode=2)
    #sdldefine.printDefTree()
    
    #from sjson
    #with open(r'/Users/liusx/Develop/VSCode/pythontest/python3/sdlutils/example/test3.cdr') as f:
    #with open(r'/Users/liusx/Develop/VSCode/pythontest/python2/xdrview/tmp/test_ggprs_rating_2g_200k_cell_002') as f:
    #    xdrList = f.readlines()
    #sdlcontent = sdlutils.sdlContent(xdrList[0],sdldefine)
    #sdlcontent.setLogLevel("debug")
    #sdlcontent.getSdlFromSjson(debugFlag=True)
    #sdlcontent.printSdlTree(isseq=True)
    
    #from json
    #with open(r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/test1.json', 'r') as fo:
    #    content = fo.read()
    #sdlcontent = sdlutils.sdlContent(content,sdldefine)
    #print(sdlcontent.getSdlFromJson(debugFlag=True))
    #sdlcontent.getSdlFromJson()
    ##sdlcontent.printSdlTree(isseq=False)
    #sdlcontent.printSdlTree(isseq=True)

    #tojson
    #jsonPath = r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/test1.json'
    #ret = sdlcontent.convSdlToJson()
    ##ret = sdlcontent.convSdlToJson(wFlag=True, wPath=jsonPath)
    #print(ret)

    #tosjson
    #sjsonPath = r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/test1.sjson'
    #ret = sdlcontent.convSdlToSjson()
    #ret = sdlcontent.convSdlToSjson(wFlag=True, wPath=sjsonPath)
    #print(ret)

    #addhead
    #retstr = sdlutils.addSdlHead_v6(ret)
    #with open(sjsonPath, 'w') as fi:
    #    fi.write(retstr + '\n')
    #testcdr = r'/Users/liusx/Develop/VSCode/pythontest/python3/sdlutils/example/test3.cdr.json'
    #with open(testcdr, 'r') as fi:
    #    sdlstr = fi.read()
    #retstr = sdlutils.addSdlHead(sdlstr)
    #print(retstr)

    #conv
    #extSdl = sdlcontent.extendContent()
    #if extSdl:
    #    sdlcontent.printSdlTree(extSdl, isseq=True)
    #    sdlnew = sdlcontent.shrinkContent(extSdl)
    #    if sdlnew:
    #        sdlcontent.printSdlTree(sdlnew, isseq=True)
