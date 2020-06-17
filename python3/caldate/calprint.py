#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
A Chinese Calendar Library in Python, Using Table-Searching Method.
Between 1901-2100
'''

import os, sys, re
from urllib import request, error
import sqlite3
import datetime

APPDIR = os.path.abspath(os.path.dirname(__file__))
URL = 'https://www.hko.gov.hk/tc/gts/time/calendar/text/files/T%dc.txt'
DB_FILE = os.path.join(APPDIR, 'db', 'lunarcal.sqlite')

CN_DAY = {u'初二': 2, u'初三': 3, u'初四': 4, u'初五': 5, u'初六': 6,
          u'初七': 7, u'初八': 8, u'初九': 9, u'初十': 10, u'十一': 11,
          u'十二': 12, u'十三': 13, u'十四': 14, u'十五': 15, u'十六': 16,
          u'十七': 17, u'十八': 18, u'十九': 19, u'二十': 20, u'廿一': 21,
          u'廿二': 22, u'廿三': 23, u'廿四': 24, u'廿五': 25, u'廿六': 26,
          u'廿七': 27, u'廿八': 28, u'廿九': 29, u'三十': 30}

CN_MON = {u'正月': 1, u'二月': 2, u'三月': 3, u'四月': 4,
          u'五月': 5, u'六月': 6, u'七月': 7, u'八月': 8,
          u'九月': 9, u'十月': 10, u'十一月': 11, u'十二月': 12,

          u'閏正月': 101, u'閏二月': 102, u'閏三月': 103, u'閏四月': 104,
          u'閏五月': 105, u'閏六月': 106, u'閏七月': 107, u'閏八月': 108,
          u'閏九月': 109, u'閏十月': 110, u'閏十一月': 111, u'閏十二月': 112}

GAN = (u'庚', u'辛', u'壬', u'癸', u'甲', u'乙', u'丙', u'丁', u'戊', u'已')
ZHI = (u'申', u'酉', u'戌', u'亥', u'子', u'丑',
       u'寅', u'卯', u'辰', u'巳', u'午', u'未')
SX = (u'猴', u'鸡', u'狗', u'猪', u'鼠', u'牛',
      u'虎', u'兔', u'龙', u'蛇', u'马', u'羊')

class Festival():
    #国历节日 *表示放假日
    @staticmethod
    def solar_Fstv(solar_month, solar_day, oneOut=False):
        sFtv = [
        "0101#元旦#",
        #"0202#世界湿地日#",
        #"0210#国际气象节#",
        "0214#情人节#",
        #"0301#国际海豹日#",
        #"0303#全国爱耳日#",
        #"0305#学雷锋纪念日#",
        "0308#妇女节#",
        #"0312#植树节# #孙中山逝世纪念日#",
        "0312#植树节#",
        #"0314#国际警察日#",
        #"0315#消费者权益日#",
        #"0317#中国国医节# #国际航海日#",
        #"0321#世界森林日# #消除种族歧视国际日# #世界儿歌日#",
        #"0322#世界水日#",
        #"0323#世界气象日#",
        #"0324#世界防治结核病日#",
        #"0325#全国中小学生安全教育日#",
        #"0330#巴勒斯坦国土日#",
        #"0401#愚人节# #全国爱国卫生运动月(四月)# #税收宣传月(四月)#",
        "0401#愚人节#",
        #"0407#世界卫生日#",
        #"0422#世界地球日#",
        #"0423#世界图书和版权日#",
        #"0424#亚非新闻工作者日#",
        "0501#劳动节#",
        "0504#青年节#",
        #"0505#碘缺乏病防治日#",
        #"0508#世界红十字日#",
        #"0512#国际护士节#",
        #"0515#国际家庭日#",
        #"0517#国际电信日#",
        #"0518#国际博物馆日#",
        #"0520#全国学生营养日#",
        #"0523#国际牛奶日#",
        #"0531#世界无烟日#",
        "0601#儿童节#",
        #"0605#世界环境保护日#",
        #"0606#全国爱眼日#",
        #"0617#防治荒漠化和干旱日#",
        #"0623#国际奥林匹克日#",
        #"0625#全国土地日#",
        #"0626#国际禁毒日#",
        #"0701#中国共·产党诞辰# #香港回归纪念日# #世界建筑日#",
        #"0702#国际体育记者日#",
        #"0707#抗日战争纪念日#",
        #"0711#世界人口日#",
        #"0730#非洲妇女日#",
        "0801#建军节#",
        #"0808#中国男子节(爸爸节)#",
        #"0815#抗日战争胜利纪念#",
        #"0908#国际扫盲日# #国际新闻工作者日#",
        #"0909#毛·泽东逝世纪念#",
        "0910#教师节#",
        #"0914#世界清洁地球日#",
        #"0916#国际臭氧层保护日#",
        #"0918#九·一八事变纪念日#",
        #"0920#国际爱牙日#",
        #"0927#世界旅游日#",
        #"0928#孔子诞辰#",
        #"1001#国庆节# #世界音乐日# #国际老人节#",
        "1001#国庆节#",
        #"1002#国庆节假日# #国际和平与民主自由斗争日#",
        #"1003#国庆节假日#",
        #"1004#世界动物日#",
        #"1006#老人节#",
        #"1008#全国高血压日# #世界视觉日#",
        #"1009#世界邮政日# #万国邮联日#",
        #"1010#辛亥革命纪念日# #世界精神卫生日#",
        #"1013#世界保健日# #国际教师节#",
        #"1014#世界标准日#",
        #"1015#国际盲人节(白手杖节)#",
        #"1016#世界粮食日#",
        #"1017#世界消除贫困日#",
        #"1022#世界传统医药日#",
        #"1024#联合国日#",
        #"1031#世界勤俭日#",
        #"1107#十月社会主义革命纪念日#",
        #"1108#中国记者日#",
        #"1109#全国消防安全宣传教育日#",
        #"1110#世界青年节#",
        #"1111#国际科学与和平周(本日所属的一周)#",
        #"1112#孙中山诞辰纪念日#",
        #"1114#世界糖尿病日#",
        #"1116#国际宽容日#",
        #"1117#国际大学生节# #世界学生节#",
        #"1120#彝族年#",
        #"1121#彝族年# #世界问候日# #世界电视日#",
        #"1122#彝族年#",
        #"1129#国际声援巴勒斯坦人民国际日#",
        #"1201#世界艾滋病日#",
        #"1203#世界残疾人日#",
        #"1205#国际经济和社会发展志愿人员日#",
        #"1208#国际儿童电视日#",
        #"1209#世界足球日#",
        #"1210#世界人权日#",
        #"1212#西安事变纪念日#",
        #"1213#南京大屠杀(1937年)纪念日#",
        #"1220#澳门回归纪念#",
        #"1221#国际篮球日#",
        "1224#平安夜#",
        "1225#圣诞节#",
        #"1226#毛·泽东诞辰纪念日#"
        ]
        #solar_month_str = str(solar_month) if solar_month > 9 else "0" + str(solar_month)
        #solar_day_str = str(solar_day) if solar_day > 9 else "0" + str(solar_day)
        #pattern = r"(" + solar_month_str + solar_day_str + r")([\w+?\#?\(?\)?\d+\s?·?]*)"
        pattern = r'(' + solar_month + solar_day + r')([\w+?\#?\(?\)?\d+\s?·?]*)'
        for solar_fstv_item in sFtv:
            result = re.search(pattern, solar_fstv_item)
            if result is not None:
                if solar_month + solar_day == result.group(1):
                    if oneOut:
                        return result.group(2).split('#')[1].strip()
                    return result.group(2)
        return None

    @staticmethod
    def lunar_Fstv(lunar_month, lunar_day):
        #农历节日 *表示放假日
        #每年单独来算
        lFtv = [
        "0101#春节#",
        "0115#元宵节#",
        "0202#春龙节",
        #"0314#清明节#", #每年不一样，此为2012年，事实上为公历节日
        "0505#端午节#",
        "0707#七夕情人节#",
        "0715#中元节#",
        "0815#中秋节#",
        "0909#重阳节#",
        "1208#腊八节#",
        "1223#小年#",
        "1229#除夕#"   #每年不一样，此为2011年
        ]
        lunar_month_str = str(lunar_month) if lunar_month > 9 else "0" + str(lunar_month)
        lunar_day_str = str(lunar_day) if lunar_day > 9 else "0" + str(lunar_day)
        pattern = r"(" + lunar_month_str + lunar_day_str + r")([\w+?\#?\s?]*)"
        for lunar_fstv_item in lFtv:
            result = re.search(pattern, lunar_fstv_item)
            if result is not None:
                return result.group(2)

    #国历节日 *表示放假日
    @staticmethod
    def weekday_Fstv(solar_month, solar_day, solar_weekday):
        #某月的第几个星期几
        wFtv = [
        "0150#世界防治麻风病日#", #一月的最后一个星期日（月倒数第一个星期日）
        "0520#国际母亲节#",
        "0530#全国助残日#",
        "0630#父亲节#",
        "0730#被奴役国家周#",
        "0932#国际和平日#",
        "0940#国际聋人节# #世界儿童日#",
        "0950#世界海事日#",
        "1011#国际住房日#",
        "1013#国际减轻自然灾害日(减灾日)#",
        "1144#感恩节#"]

        #7，14等应该属于1, 2周，能整除的那天实际属于上一周，做个偏移
        offset = -1 if solar_day % 7 == 0 else 0
        #计算当前日属于第几周，得出来从0开始计周，再向后偏移1
        weekday_ordinal = solar_day // 7 + offset + 1

        #solar_month_str = str(solar_month) if solar_month > 9 else "0" + str(solar_month)
        solar_weekday_str = str(weekday_ordinal) + str(solar_weekday)
        #pattern = r"(" + solar_month_str + solar_weekday_str + r")([\w+?\#?\s?]*)"
        pattern = r"(" + solar_month + solar_weekday_str + r")([\w+?\#?\s?]*)"
        for weekday_fstv_item in wFtv:
            result = re.search(pattern, weekday_fstv_item)
            if result is not None:
                return result.group(2)

    #24节气
    @staticmethod
    def solar_Term(solar_month, solar_day):
        #每年数据不一样，此为2012年内的数据
        stFtv = [
        "0106#小寒#",
        "0120#大寒#",
        "0204#立春#",
        "0219#雨水#",
        "0305#惊蛰#",
        "0320#春分#",
        "0404#清明#",
        "0420#谷雨#",
        "0505#立夏#",
        "0521#小满#",
        "0605#芒种#",
        "0621#夏至#",
        "0707#小暑#",
        "0722#大暑#",
        "0807#立秋#",
        "0823#处暑#",
        "0907#白露#",
        "0922#秋分#",
        "1008#寒露#",
        "1023#霜降#",
        "1107#立冬#",
        "1122#小雪#",
        "1206#大雪#",
        "1221#冬至#",
        ]
        #solar_month_str = str(solar_month) if solar_month > 9 else "0" + str(solar_month)
        #solar_day_str = str(solar_day) if solar_day > 9 else "0" + str(solar_day)
        #pattern = r"(" + solar_month_str + solar_day_str + r")([\w+?\#?]*)"
        pattern = r"(" + solar_month + solar_day + r")([\w+?\#?]*)"
        for solarTerm_fstv_item in stFtv:
            result = re.search(pattern, solarTerm_fstv_item)
            if result is not None:
                return result.group(2)

def initdb():
    try:
        os.mkdir(os.path.join(APPDIR, 'db'))
    except OSError:
        pass

    conn = sqlite3.connect(DB_FILE)
    db = conn.cursor()
    db.execute('''CREATE TABLE IF NOT EXISTS ical (
                    id INTEGER PRIMARY KEY,
                    date TEXT UNIQUE,
                    lunardate TEXT,
                    holiday TEXT,
                    jieqi TEXT,
                    legalday TEXT)''')
    conn.commit()
    db.close()

def compact_sqlite3_db():
    try: 
        conn = sqlite3.connect(DB_FILE)
        conn.execute("VACUUM")
        conn.close()
        return True
    except:
        return False

def query_db(query, args=(), one=False):
    ''' wrap the db query, fetch into one step '''
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def update_db(uSql, args=()):
    conn = sqlite3.connect(DB_FILE)
    db = conn.cursor()
    db.execute(uSql, args)
    conn.commit()
    conn.close()

def getJieQi():
    sql = 'select jieqi from ical where jieqi NOT NULL limit 28'
    res = query_db(sql)
    d = -75
    for row in res:
        print("%d: u'%s', " % (d, row[0]))
        d += 15

def getDataFromHko(year, coding='big5'):
    ret = True
    content = ""
    url = URL % year
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    try:
        reponse = request.urlopen(req)
        #print('Status:', reponse.status, reponse.reason)
        #print('Data:', reponse.read().decode('big5'))
        if reponse.status == 200:
            content = reponse.read().decode(coding)
    except error.HTTPError as e:
        ret = False
        content = e
    return ret, content

def analyseHkoData(content):
    # 2020(庚子 - 肖鼠)年公曆與農曆日期對照表
    #reg_header = r'(\(.*\))'
    # 2020年1月1日          初七        星期三   
    # 2020年1月6日          十二        星期一      小寒  
    reg_content = r'^(\d+)年(\d+)月(\d+)日'
    
    sql_nojq = ('insert or replace into ical (date,lunardate) '
                'values(?,?) ')
    sql_jq = ('insert or replace into ical (date,lunardate,jieqi) '
              'values(?,?,?) ')
    conn = sqlite3.connect(DB_FILE)
    db = conn.cursor()
    for line in content.split('\n'):
        m = re.match(reg_content,line)
        if m:
            fds = line.split()
            # add leading zero to month and day
            if len(m.group(2)) == 1:
                str_m = '0%s' % m.group(2)
            else:
                str_m = m.group(2)
            if len(m.group(3)) == 1:
                str_d = '0%s' % m.group(3)
            else:
                str_d = m.group(3)

            dt = '%s-%s-%s' % (m.group(1), str_m, str_d)
            if len(fds) > 3:  # last field is jieqi
                db.execute(sql_jq, (dt, fds[1], fds[3]))
            else:
                db.execute(sql_nojq, (dt, fds[1]))
    conn.commit()
    conn.close()

def delData(year):
    sql = "delete from ical where date like '%s%%'"  % year
    query_db(sql)

def update_cal(year=0, isDel=False):
    ''' fetch lunar calendar from HongKong Obs, parse it and save to db'''
    ret = False
    if year == 0:
        for y in range(1901, 2101):
            ret, content = getDataFromHko(y)
            if ret:
                if isDel:
                    delData(y)
                analyseHkoData(content)
    else:
        ret, content = getDataFromHko(year)
        if ret:
            if isDel:
                delData(year)
            analyseHkoData(content)
    return ret

def post_process():
    ''' there are several mistakes in HK OBS data, the following date
    do not have a valid lunar date, instead are the weekday names, they
    are all 三十 '''
    sql_update = 'update ical set lunardate=? where date=?'

    HK_ERROR = ('2036-01-27', '2053-12-09', '2056-03-15',
                '2063-07-25', '2063-10-21', '2063-12-19')
    conn = sqlite3.connect(DB_FILE)
    db = conn.cursor()
    for d in HK_ERROR:
        db.execute(sql_update, (u'三十', d))
    conn.commit()
    conn.close()

def update_holiday():
    ''' write chinese traditional holiday to db
    腊八节(腊月初八)     除夕(腊月的最后一天)     春节(一月一日)
    元宵节(一月十五日)   寒食节(清明的前一天)     端午节(五月初五)
    七夕节(七月初七)     中元节(七月十五日)       中秋节(八月十五日)
    重阳节(九月九日)     下元节(十月十五日)
    阳历：
    元旦(1月1日)   情人节(2月14日)   劳动节(5月1日)  
    '''
    sql = 'select * from ical order by date'
    rows = query_db(sql)
    args = []
    m = None
    previd = None
    for r in rows:
        try:
            d = CN_DAY[r['lunardate']]
        except KeyError:
            #print 'debug: %s %s' % (r['date'], r['lunardate'])
            m = CN_MON[r['lunardate']]
            d = 1

        if not m:
            continue

        if m == 12 and d == 8:
            args.append((r['id'], u'腊八'))
        elif m == 1 and d == 1:
            args.append((r['id'], u'春节'))
            args.append((previd, u'除夕'))
        elif m == 1 and d == 15:
            args.append((r['id'], u'元宵'))
        elif m == 5 and d == 5:
            args.append((r['id'], u'端午'))
        elif m == 7 and d == 7:
            args.append((r['id'], u'七夕'))
        elif m == 7 and d == 15:
            args.append((r['id'], u'中元'))
        elif m == 8 and d == 15:
            args.append((r['id'], u'中秋'))
        elif m == 9 and d == 9:
            args.append((r['id'], u'重阳'))
        elif m == 10 and d == 15:
            args.append((r['id'], u'下元'))

        if r['jieqi'] == u'清明':
            args.append((previd, u'寒食'))
        previd = r['id']

    sql_update = 'update ical set holiday=? where id=?'
    conn = sqlite3.connect(DB_FILE)
    db = conn.cursor()
    for arg in args:
        db.execute(sql_update, (arg[1], arg[0]))
    conn.commit()
    conn.close()

def analyseLegalDay(legalstr):
    regstr1 = r'^[0-9][0-9]-[0-9][0-9]$'
    regstr2 = r'^[0-9][0-9]-[0-9][0-9]~[0-9][0-9]-[0-9][0-9]$'
    retL = list()
    splitL1 = legalstr.split(',')
    for sp1 in splitL1:
        if re.search(regstr1, sp1.strip()) or re.search(regstr2, sp1.strip()):
            retL.append(sp1.strip())
        #else:
        #    splitL2 = sp1.split('~')
        #    if re.search(regstr, splitL2[0].strip()) and re.search(regstr, splitL2[1].strip()):
        #        start = int(splitL2[0].strip()[3:4])
        #        end = start = int(splitL2[1].strip()[3:4]) + 1
        #        for i in range(start, end):
        #            
        #            retL.append(sp2.strip())
    return retL

def updateLegalDay():
    regstr = r'^h[\d]{4,4}.txt'
    regline = r'^(\d):([\d\-,~]+):([\d\-,~]*)'
    legalDict = dict()
    fileL = os.listdir(os.path.join(APPDIR, 'db'))
    for f in fileL:
        fpath = os.path.join(APPDIR, 'db', f)
        if os.path.isfile(fpath) and re.search(regstr, f):
            year = f[1:5]
            with open(fpath, 'r') as fi:
                legalDays = list()
                legalAdjust = list()
                lines = fi.readlines()
                for line in lines:
                    ma = re.search(regline, line)
                    if ma:
                        legalDays.extend(analyseLegalDay(ma.group(2)))
                        legalAdjust.extend(analyseLegalDay(ma.group(3)))
                legalDict[year] = [legalDays, legalAdjust]
    #print(legalDict)
    for key, value in legalDict.items():
        uSql = "update ical set legalday=NULL where date like '%s%%'" % (key)
        update_db(uSql)
        for day in value[0]:
            sp = day.split('~')
            uSql = "update ical set legalday='1' where date='%s'" % (key + '-' + sp[0])
            if len(sp) == 2:
                uSql = "update ical set legalday='1' where date >= '%s' and date <= '%s'" % (key + '-' + sp[0], key + '-' + sp[1])
            update_db(uSql)
            #print(uSql)
        for day in value[1]:
            sp = day.split('~')
            uSql = "update ical set legalday='2' where date='%s'" % (key + '-' + sp[0])
            if len(sp) == 2:
                uSql = "update ical set legalday='2' where date >= '%s' and date <= '%s'" % (key + '-' + sp[0], key + '-' + sp[1])
            update_db(uSql)
            #print(uSql)
    print("更新法定节假日完成。")

def getGanzhi(lyear):
    '''generate 干支年份
    Args:
        lyear: four digit lyear, either integer or string
    Return:
        a string, e.g. 庚辰[龙]年
    '''

    g = GAN[int(str(lyear)[-1])]
    z = ZHI[int(lyear) % 12]
    sx = SX[int(lyear) % 12]
    return u'%s%s[%s]' % (g, z, sx)

def getLunarYear(isodate):
    '''find lunar year for a date'''
    sql = ('select date from ical where lunardate="正月" and '
           'date<=? order by date desc limit 1')
    row = query_db(sql, (isodate,), one=True)
    res = 'Unknown'
    if row:
        # print(row[0][:4])
        res = getGanzhi(row[0][:4])
    return res

def getLunarDate(isodate, needM=False):
    ret = None
    sql = 'select lunardate,holiday,jieqi from ical where date=?'
    row = query_db(sql, (isodate,), one=True)
    if row:
        ret = [row[1],row[2],row[0]]
        if needM:
            lunarDay = CN_DAY[row[0]]
            givedT = datetime.datetime.strptime(isodate, "%Y-%m-%d")
            destT = givedT - datetime.timedelta(days=lunarDay - 1)
            destTstr = destT.strftime("%Y-%m-%d")
            row1 = query_db(sql, (destTstr,), one=True)
            ret.append(row1[0])
    return ret

def getWeekDay(isodate, full=False):
    #i = time.strptime(isodate, "%Y-%m-%d").tm_wday
    i = datetime.datetime.strptime(isodate, "%Y-%m-%d").weekday()
    a = '一 二 三 四 五 六 日'.split()
    if full:
        a = '星期一 星期二 星期三 星期四 星期五 星期六 星期日'.split()
    return a[i]

def isExistDate(isodate):
    sql = "select count(*) from ical where date like '%s%%'"  % isodate[:8]
    rows = query_db(sql, one=True)

    ret = False
    if rows:
        #print(rows[0])
        if int(rows[0]) > 0:
            ret = True
    return ret

def outOneMonth(isodate):
    lunarYear = getLunarYear(isodate)
    week = getWeekDay(isodate, True)

    print(isodate[:4] + "年 " + lunarYear + " 当前时间[" + isodate[5:] + " " + week + "]")

    sql = "select date,lunardate,holiday,jieqi,legalday from ical where date like '%s%%'"  % isodate[:8]
    rows = query_db(sql)

    firstL = ""
    for line in '日 一 二 三 四 五 六'.split():
        firstL = firstL + "{:^9}".format(line)
    print(firstL)

    if rows:
        w1 = datetime.datetime.strptime(rows[0][0], "%Y-%m-%d").weekday() + 1
        if w1 == 7:
            w1 = 0
        lineN = (len(rows) + w1) // 7
        yuN = (len(rows) + w1) % 7
        if  yuN > 0:
            lineN = (len(rows) + w1) // 7 + 1
        
        #print(lineN)
        #outL = list()
        d = 0
        for i in range(lineN):
            #tmpL = list()
            oneline = ""
            lunarLine = ""
            jieqiLine = ""
            for j in range(7):
                if (i == 0 and j < w1) or (i == lineN - 1 and j >= yuN):
                    #tmpL.append("{:^10}".format(""))
                    oneline = oneline + "{:^10}".format("")
                    lunarLine = lunarLine + "{:^10}".format("")
                    jieqiLine = jieqiLine + "{:^10}".format("")
                else:
                    #tmpL.append("{:^10}".format(rows[d][0][8:]))
                    oneline = oneline + "{:^10}".format(rows[d][0][8:])
                    lunarFormat = "{:^%d}" % (10 - len(rows[d][1]))
                    jieqiFlag = False
                    if rows[d][2]:
                        lunarLine = lunarLine + lunarFormat.format(rows[d][2])
                        jieqiFlag = True
                    else:
                        #dstr = str(d+1) if d + 1 > 9 else "0" + str(d+1)
                        res = Festival.solar_Fstv(rows[d][0][5:7], rows[d][0][8:10], True)
                        if res:
                            lunarFormat = "{:^%d}" % (10 - len(res))
                            lunarLine = lunarLine + lunarFormat.format(res)
                            jieqiFlag = True
                        elif rows[d][3]:
                            lunarFormat = "{:^%d}" % (10 - len(rows[d][3]))
                            lunarLine = lunarLine + lunarFormat.format(rows[d][3])
                        else:
                            lunarLine = lunarLine + lunarFormat.format(rows[d][1])
                    
                    if rows[d][4]:
                        if int(rows[d][4]) == 1:
                            jieqiLine = jieqiLine + "{:^9}".format('休')
                        else:
                            jieqiLine = jieqiLine + "{:^9}".format('班')
                    elif rows[d][3] and jieqiFlag:
                        lunarFormat = "{:^%d}" % (10 - len(rows[d][3]))
                        jieqiLine = jieqiLine + lunarFormat.format(rows[d][3])
                    else:
                        jieqiLine = jieqiLine + "{:^10}".format("")
                    
                    d = d + 1
            #outL.append(tmpL)
            print(oneline)
            print(lunarLine)
            print(jieqiLine)

def main():
    if not os.path.exists(DB_FILE):
        initdb()
        if update_cal():
            post_process()  # fix error in HK data
            update_holiday()
            compact_sqlite3_db()
    
    #now = datetime.datetime.now().strftime("%Y-%m-%d")
    now = "2020-01-02"
    if not isExistDate(now):
        if update_cal(int(now[:4]), isDel=True):
            post_process()  # fix error in HK data
            update_holiday()
            compact_sqlite3_db()
    if not isExistDate(now):
        print("本程序依赖香港天台农历对照表信息，目前支持1901 - 2100年之间的日历信息显示。")
        print("详细信息请参考：https://www.hko.gov.hk/tc/gts/time/conversion1_text.htm")
        sys.exit()
    
    outOneMonth(now)
    #updateLegalDay()

    #print(Festival.solar_Fstv(now[5:2], now[8:2], True))
    #print("公历 : " + now)
    #year = getLunarYear(now)
    #week = getWeekDay(now, True)
    #lunarinfo = getLunarDate(now, True)
    #print("农历 : " + year + "年 " + lunarinfo[3] + lunarinfo[2] + " " + week)

if __name__ == '__main__':
    main()