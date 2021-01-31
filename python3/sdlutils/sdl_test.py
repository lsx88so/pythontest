#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from sdlbase import sdlNode
import sdlutils
import xdrutils
import asn1utils
#from sdlutils import sdlDefine
#from sdlutils import sdlContent
#import pickle, json, re

if __name__ == "__main__":
    #a = "5F8136"
    #aL = list(a)
    #alL = [ aL[x * 2:x * 2 + 2] for x in range(len(aL)//2)]
    ##print(a[0:6][::-1])
    #print(alL)
    #print("F" * 3)
    #res = asn1utils.sumTag(1, 0, 182)
    #print(res)
    #print(asn1utils.insertSpace(res))

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
    
    #xdrdef = xdrutils.xdrDefine(r'/Users/liusx/Develop/VSCode/pythontest/python2/xdrview/xdr_define')
    #with open(r'/Users/liusx/Develop/VSCode/pythontest/python3/sdlutils/example/test.xdr') as f:
    #    xdrList = f.readlines()
    #xdrdef.analyseXdrDefine()
    ##xdrdef.printXdrDefine("dr_ggprs_ln")
    #xdrdef.analyseXdrContent(xdrList[0])
    #xdrdef.printXdrList()

    sdldefine = sdlutils.sdlDefine("SXdr",r'/Users/liusx/Develop/VSCode/pythontest/python3/sdlutils/example/xdr_def.sdl',r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/test.s')
    sdldefine.getSdlDefine(fromDumpFile=False)
    #sdldefine.printDefTree()

    #with open(r'/Users/liusx/Develop/VSCode/pythontest/python3/sdlutils/example/test3.cdr') as f:
    with open(r'/Users/liusx/Develop/VSCode/pythontest/python2/xdrview/tmp/test_ggprs_rating_2g_200k_cell_002') as f:
        xdrList = f.readlines()
    sdlcontent = sdlutils.sdlContent(xdrList[0],sdldefine)
    sdlcontent.getSdlFromSjson()
    sdlcontent.printSdlTree(isseq=True)
    
    #with open(r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/test1.json', 'r') as fo:
    #    content = fo.read()
    #sdlcontent = sdlutils.sdlContent(content,sdldefine)
    #print(sdlcontent.getSdlFromJson(debugFlag=True))
    #sdlcontent.getSdlFromJson()
    ##sdlcontent.printSdlTree(isseq=False)
    #sdlcontent.printSdlTree(isseq=True)

    #jsonPath = r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/test1.json'
    #ret = sdlcontent.convSdlToJson()
    ##ret = sdlcontent.convSdlToJson(wFlag=True, wPath=jsonPath)
    #print(ret)

    #sjsonPath = r'/Users/liusx/Develop/VSCode/pythontest/python3/tmp/test1.sjson'
    #ret = sdlcontent.convSdlToSjson()
    #ret = sdlcontent.convSdlToSjson(wFlag=True, wPath=sjsonPath)
    #print(ret)

    #retstr = sdlutils.addSdlHead(ret)
    #with open(sjsonPath, 'w') as fi:
    #    fi.write(retstr + '\n')

    #testcdr = r'/Users/liusx/Develop/VSCode/pythontest/python3/sdlutils/example/test3.cdr.json'
    #with open(testcdr, 'r') as fi:
    #    sdlstr = fi.read()
    #retstr = sdlutils.addSdlHead(sdlstr)
    #print(retstr)
