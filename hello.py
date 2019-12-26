#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, math, json, re, base64, hashlib, random, hmac, itertools, smtplib, sqlite3
from datetime import datetime, timezone, timedelta
import time, functools
from functools import reduce
from enum import Enum, unique
import unittest
from urllib import request
#from turtle import *
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

keystr = r'^E(?!1206)'
#keystr = r'(?<!1206)_.*'
test_str1 = 'E1206_201300'
test_str2 = 'E1203_201300'
test_str3 = 'E206_201300'

if re.search(keystr,test_str1):
    print("str1")
if re.search(keystr,test_str2):
    print("str2")
if re.search(keystr,test_str3):
    print("str3")

keystr2 = r'test(?!\.php$)'
test_str = 'test.php1'
if re.search(keystr2,test_str):
    print("ok")


#db_file = os.path.join(os.path.dirname(__file__), 'test.db')
#if os.path.isfile(db_file):
#    os.remove(db_file)
#
## 初始数据:
#conn = sqlite3.connect(db_file)
#cursor = conn.cursor()
#cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
#cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
#cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
#cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
#cursor.close()
#conn.commit()
#conn.close()
#
#def get_score_in(low, high):
#    ' 返回指定分数区间的名字，按分数从低到高排序 '
#    sqlstr = 'select name from user where score >= %s and score <= %s order by score' % (low, high)
#    conn = sqlite3.connect(db_file)
#    cursor = conn.cursor()
#    cursor.execute(sqlstr)
#    res = cursor.fetchall()
#    cursor.close()
#    conn.close()
#    #print(res)
#    resL = []
#    for line in res:
#        resL.append(line[0])
#    return resL
#
## 测试:
#assert get_score_in(80, 95) == ['Adam'], get_score_in(80, 95)
#assert get_score_in(60, 80) == ['Bart', 'Lisa'], get_score_in(60, 80)
#assert get_score_in(60, 100) == ['Bart', 'Lisa', 'Adam'], get_score_in(60, 100)
#
#print('Pass')

#def _format_addr(s):
#    name, addr = parseaddr(s)
#    return formataddr((Header(name, 'utf-8').encode(), addr))
#
#msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
## 输入Email地址和口令:
##from_addr = input('From: ')
##password = input('Password: ')
### 输入收件人地址:
##to_addr = input('To: ')
### 输入SMTP服务器地址:
##smtp_server = input('SMTP server: ')
#from_addr = "liusx@asiainfo.com"
#password = "lsx.19880"
## 输入收件人地址:
#to_addr = "jamyxin@163.com"
## 输入SMTP服务器地址:
#smtp_server = "mail.asiainfo.com"
#
#msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
#msg['To'] = _format_addr('管理员 <%s>' % to_addr)
#msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()
#
#server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
#server.set_debuglevel(1)
#server.login(from_addr, password)
#server.sendmail(from_addr, [to_addr], msg.as_string())
#server.quit()


## 设置色彩模式是RGB:
#colormode(255)
#
#lt(90)
#
#lv = 14
#l = 120
#s = 45
#
#width(lv)
#
## 初始化RGB颜色:
#r = 0
#g = 0
#b = 0
#pencolor(r, g, b)
#
#penup()
#bk(l)
#pendown()
#fd(l)
#
#def draw_tree(l, level):
#    global r, g, b
#    # save the current pen width
#    w = width()
#
#    # narrow the pen width
#    width(w * 3.0 / 4.0)
#    # set color:
#    r = r + 1
#    g = g + 2
#    b = b + 3
#    pencolor(r % 200, g % 200, b % 200)
#
#    l = 3.0 / 4.0 * l
#
#    lt(s)
#    fd(l)
#
#    if level < lv:
#        draw_tree(l, level + 1)
#    bk(l)
#    rt(2 * s)
#    fd(l)
#
#    if level < lv:
#        draw_tree(l, level + 1)
#    bk(l)
#    lt(s)
#
#    # restore the previous pen width
#    width(w)
#
#speed("fastest")
#
#draw_tree(l, 4)
#
#done()

#def drawStar(x, y):
#    pu()
#    goto(x, y)
#    pd()
#    # set heading: 0
#    seth(0)
#    for i in range(5):
#        fd(40)
#        rt(144)
#
#for x in range(0, 250, 50):
#    drawStar(x, 0)
#
#done()



#def fetch_data(url):
#    #req = request.Request('http://www.douban.com/')
#    #req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
#    with request.urlopen(url) as f:
#        return json.loads(f.read().decode('utf-8'))
#
##URL = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=json'
#URL = 'https://recsidebar.csdn.net/getSideBarRecommend.html'
#data = fetch_data(URL)
#print(data)
##assert data['query']['results']['channel']['location']['city'] == 'Beijing'
##print('ok')


#def pi(N):
#    ' 计算pi的值 '
#    # step 1: 创建一个奇数序列: 1, 3, 5, 7, 9, ...
#    seq = itertools.count(1, 2)
#    #pinum = 0
#
#    # step 2: 取该序列的前N项: 1, 3, 5, 7, 9, ..., 2*N-1.
#    seqL = itertools.takewhile(lambda x : x <= 2 * N -1, seq)
#
#    # step 3: 添加正负符号并用4除: 4/1, -4/3, 4/5, -4/7, 4/9, ...
#    resL = [ ((-1)**i) * 4 /n for i, n in enumerate(seqL)]
#    # step 4: 求和:
#    return sum(resL)
#    
#    #for i, n in enumerate(seq):
#    #    if i == N:
#    #        break
#    #    p = 4
#    #    if i % 2 == 0:
#    #        p = -p
#    #    pinum = pinum + p / n
#    #return abs(pinum)
#
#print(pi(10))
#print(pi(100))
#print(pi(1000))
#print(pi(10000))
#assert 3.04 < pi(10) < 3.05
#assert 3.13 < pi(100) < 3.14
#assert 3.140 < pi(1000) < 3.141
#assert 3.1414 < pi(10000) < 3.1415
#print('ok')
#print(pi(100000000))


#def hmac_md5(key, s):
#    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()
#
#class User(object):
#    def __init__(self, username, password):
#        self.username = username
#        self.key = ''.join([chr(random.randint(48, 122)) for i in range(20)])
#        self.password = hmac_md5(self.key, password)
#
#db = {
#    'michael': User('michael', '123456'),
#    'bob': User('bob', 'abc999'),
#    'alice': User('alice', 'alice2008')
#}
#
#def login(username, password):
#    user = db[username]
#    return user.password == hmac_md5(user.key, password)
#
#assert login('michael', '123456')
#assert login('bob', 'abc999')
#assert login('alice', 'alice2008')
#assert not login('michael', '1234567')
#assert not login('bob', '123456')
#assert not login('alice', 'Alice2008')
#print('ok')


#def get_md5(s):
#    return hashlib.md5(s.encode('utf-8')).hexdigest()
#
#class User(object):
#    def __init__(self, username, password):
#        self.username = username
#        #关键
#        self.salt = ''.join([chr(random.randint(48, 122)) for i in range(20)])
#        self.password = get_md5(password + self.salt)
#db = {
#    'michael': User('michael', '123456'),
#    'bob': User('bob', 'abc999'),
#    'alice': User('alice', 'alice2008')
#}
#
#def login(username, password):
#    user = db[username]
#    return user.password == get_md5(password + user.salt)
#
#assert login('michael', '123456')
#assert login('bob', 'abc999')
#assert login('alice', 'alice2008')
#assert not login('michael', '1234567')
#assert not login('bob', '123456')
#assert not login('alice', 'Alice2008')
#print('ok')


#db = {
#    'michael': 'e10adc3949ba59abbe56e057f20f883e',
#    'bob': '878ef96e86145580c38c87f0410ad153',
#    'alice': '99b1c2188db85afee403b1536010c2c9'
#}
#
#def calc_md5(password):
#    md5 = hashlib.md5()
#    md5.update(password.encode("utf-8"))
#    return md5.hexdigest()
#
#def login(user, password):
#    pwd = calc_md5(password)
#    #has_key  3.x版本去掉了
#    pwd_std = db.get(user)
#    #print(pwd_std, pwd)
#    if pwd_std == pwd:
#        return True
#    return False
#
#assert login('michael', '123456')
#assert login('bob', 'abc999')
#assert login('alice', 'alice2008')
#assert not login('michael', '1234567')
#assert not login('bob', '123456')
#assert not login('alice', 'Alice2008')
#print('ok')


#def safe_base64_decode(s):
#    tmps = s.decode('utf-8')
#    if len(tmps) % 4 != 0:
#        tmps = tmps + '=' * (4 - len(tmps) % 4)
#    return base64.b64decode(tmps.encode('utf-8'))
#
#assert b'abcd' == safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
#assert b'abcd' == safe_base64_decode(b'YWJjZA'), safe_base64_decode('YWJjZA')
#print('ok')


#def to_timestamp(dt_str, tz_str):
#    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
#    regstr = r'UTC([+-])([0-9]+):.+'
#    ma = re.match(regstr, tz_str)
#    flag = ma.group(1)
#    zone_num = int(ma.group(2))
#    if flag == '-':
#        zone_num = - zone_num
#    tz_zone = timezone(timedelta(hours=zone_num))
#    dt = dt.replace(tzinfo=tz_zone)
#    return dt.timestamp()
#
#t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
#assert t1 == 1433121030.0, t1
#
#t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
#assert t2 == 1433121030.0, t2
#print('ok')


#def is_valid_email(addr):
#    return re.match(r'^[a-zA-Z][a-zA-Z0-9.]*?@[a-zA-Z0-9.]',addr)
#
#def name_of_email(addr):
#    ma = re.match(r'^<([a-zA-Z\s]+)>\s[a-zA-Z0-9.]*?@[a-zA-Z0-9.]',addr)
#    if ma:
#        return ma.group(1)
#    ma = re.match(r'^([a-zA-Z][a-zA-Z0-9.]*?)@[a-zA-Z0-9.]',addr)
#    if ma:
#        return ma.group(1)
#    return None
#
#assert is_valid_email('someone@gmail.com')
#assert is_valid_email('bill.gates@microsoft.com')
#assert not is_valid_email('bob#example.com')
#assert not is_valid_email('mr-bob@example.com')
#print('ok')
#assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
#assert name_of_email('tom@voyager.org') == 'tom'
#print('ok')


#obj = dict(name='小明', age=20)
#s = json.dumps(obj, ensure_ascii=True)
#print(s)


#1.利用os模块编写一个能实现dir -l输出的程序。
#2.编写一个程序，能在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件，并打印出相对路径。

#def searchFile1(dest, regstr, outL):
#    for fi in os.listdir(dest):
#        tmp_path = os.path.join(dest, fi)
#        #print(fi)
#        #print(tmp_path)
#        if os.path.isdir(tmp_path):
#            searchFile1(tmp_path, regstr, outL)
#        else:
#            if re.search(regstr, fi):
#                #print("ok")
#                outL.append(tmp_path)
#
#def searchFile2(root, dest, regstr):
#    for fi in os.listdir(dest):
#        tmp_path = os.path.join(dest, fi)
#        if os.path.isdir(tmp_path):
#            tmp_root = os.path.join(root, fi)
#            searchFile2(tmp_root, tmp_path, regstr)
#        else:
#            if re.search(regstr, fi):
#                print(os.path.join(root, fi))
#
#dest = r'/Users/liusx/Develop/VSCode/python'
#outL = []
#searchFile1(dest, r'cal', outL)
#print(outL)
#searchFile2(r'.', dest, r'test')


#fpath = r'./T2020c.txt'
#
#with open(fpath, 'r', encoding="Big5") as f:
#    s = f.read()
#    print(s)


#class Student(object):
#    def __init__(self, name, score):
#        self.name = name
#        self.score = score
#    def get_grade(self):
#        if self.score > 100:
#            raise ValueError
#        if self.score < 0:
#            raise ValueError
#        if self.score >= 80:
#            return 'A'
#        if self.score >= 60:
#            return 'B'
#        return 'C'
#
#class TestStudent(unittest.TestCase):
#    def test_80_to_100(self):
#        s1 = Student('Bart', 80)
#        s2 = Student('Lisa', 100)
#        self.assertEqual(s1.get_grade(), 'A')
#        self.assertEqual(s2.get_grade(), 'A')
#
#    def test_60_to_80(self):
#        s1 = Student('Bart', 60)
#        s2 = Student('Lisa', 79)
#        self.assertEqual(s1.get_grade(), 'B')
#        self.assertEqual(s2.get_grade(), 'B')
#
#    def test_0_to_60(self):
#        s1 = Student('Bart', 0)
#        s2 = Student('Lisa', 59)
#        self.assertEqual(s1.get_grade(), 'C')
#        self.assertEqual(s2.get_grade(), 'C')
#
#    def test_invalid(self):
#        s1 = Student('Bart', -1)
#        s2 = Student('Lisa', 101)
#        with self.assertRaises(ValueError):
#            s1.get_grade()
#        with self.assertRaises(ValueError):
#            s2.get_grade()
#
#if __name__ == '__main__':
#    unittest.main()


#def str2num(s):
#    #return int(s)
#    pos = s.find(".")
#    #pos = s.index(".")   raise valueerror
#    #print(pos)
#    if pos != -1:
#        return float(s)
#    else:
#        return int(s)
#    #try:
#    #    return int(s)
#    #except:
#    #    return float(s)
#
#def calc(exp):
#    ss = exp.split('+')
#    ns = map(str2num, ss)
#    return reduce(lambda acc, x: acc + x, ns)
#
#def main():
#    r = calc('100 + 200 + 345')
#    print('100 + 200 + 345 =', r)
#    r = calc('99 + 88 + 7.6')
#    print('99 + 88 + 7.6 =', r)
#
#main()

#@unique
#class Gender(Enum):
#    Male = 0
#    Female = 1
#    #test = 1
#    test = 2
#
#class Student(object):
#    def __init__(self, name, gender):
#        self.name = name
#        self.gender = gender
#
#bart = Student('Bart', Gender.Male)
#if bart.gender == Gender.Male:
#    print('测试通过!')
#else:
#    print('测试失败!')

#class Screen(object):
#    @property
#    def width(self):
#        return self._width
#    
#    @property
#    def height(self):
#        return self._height
#    
#    @property
#    def resolution(self):
#        return self._width * self._height
#    
#    @width.setter
#    def width(self, value):
#        self._width = value
#    
#    @height.setter
#    def height(self,value):
#        self._height = value
#
#s = Screen()
#s.width = 1024
#s.height = 768
#print('resolution =', s.resolution)
#if s.resolution == 786432:
#    print('测试通过!')
#else:
#    print('测试失败!')

#class Student(object):
#    count = 0
#
#    def __init__(self, name):
#        self.name = name
#        Student.count = Student.count + 1
#
#if Student.count != 0:
#    print('测试失败!')
#else:
#    bart = Student('Bart')
#    if Student.count != 1:
#        print('测试失败!')
#    else:
#        lisa = Student('Bart')
#        if Student.count != 2:
#            print('测试失败!')
#        else:
#            print('Students:', Student.count)
#            print('测试通过!')

#class Student(object):
#    def __init__(self, name, gender):
#        self.name = name
#        self.__gender = gender
#    
#    def set_gender(self, gender):
#        self.__gender = gender
#    
#    def get_gender(self):
#        return self.__gender
#
#bart = Student('Bart', 'male')
#if bart.get_gender() != 'male':
#    print('测试失败!')
#else:
#    bart.set_gender('female')
#    if bart.get_gender() != 'female':
#        print('测试失败!')
#    else:
#        print('测试成功!')

#def metric(text=''):
#    def decorator(fn):
#        @functools.wraps(fn)
#        def wrapper(*args_r, **kw_r):
#            if len(text) > 1:
#                print('%s %s in %s ms' % (fn.__name__, str(text), time.time()))
#            else:
#                print('%s begin in %s ms' % (fn.__name__, time.time()))
#            #return fn(*args, **kw)
#            res = fn(*args_r, **kw_r)
#            if len(text) > 1:
#                print('%s %s in %s ms' % (fn.__name__, str(text), time.time()))
#            else:
#                print('%s end in %s ms' % (fn.__name__, time.time()))
#            return res
#        #wrapper.__name__ = fn.__name__
#        return wrapper
#    return decorator
#
#@metric()
#def fast(x, y):
#    time.sleep(0.0012)
#    return x + y
#
#@metric("test")
#def slow(x, y, z):
#    time.sleep(0.1234)
#    return x * y * z
#
#print(fast.__name__, slow.__name__)
#f = fast(11, 22)
#s = slow(11, 22, 33)
#print(f, s)
#if f != 33:
#    print('测试失败!')
#elif s != 7986:
#    print('测试失败!')


#def metric(fn):
#    @functools.wraps(fn)
#    def wrapper(*args, **kw):
#        print('%s executed in %s ms' % (fn.__name__, time.time()))
#        return fn
#    return wrapper
#
#@metric
#def fast(x, y):
#    time.sleep(0.0012)
#    return x + y
#
#@metric
#def slow(x, y, z):
#    time.sleep(0.1234)
#    return x * y * z
#
#f = fast(11, 22)
#s = slow(11, 22, 33)
#if f(11, 22) != 33:
#    print('测试失败!')
#elif s(11, 22, 33) != 7986:
#    print('测试失败!')

#def is_odd(n):
#    return n % 2 == 1
#
#L = list(filter(is_odd, range(1, 20)))
#print(L)
#L = list(filter(lambda n : n % 2 == 1, range(1, 20)))
#print(L)

#def createCounter():
#    tmpL = [0]
#    def counter():
#        tmpL[0] = tmpL[0] + 1
#        return tmpL[0]
#    return counter
#
#counterA = createCounter()
#print(counterA(), counterA(), counterA(), counterA(), counterA()) # 1 2 3 4 5
#counterB = createCounter()
#if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
#    print('测试通过!')
#else:
#    print('测试失败!')

#def add_path(new_path):
#    path_list = sys.path
#
#    if new_path not in path_list:
#        #import sys
#        sys.path.append(new_path)
#add_path('./')

#def by_name(t):
#    return str.lower(t[0])
#
#def by_score(t):
#    return t[1]
#
#L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
#
#print(L)
#L2 = sorted(L, key=by_name)
#print(L2)
#L2 = sorted(L, key=by_name, reverse=True)
#print(L2)
#L2 = sorted(L, key=by_score)
#print(L2)
#L2 = sorted(L, key=by_score, reverse=True)
#print(L2)

#def is_palindrome(n):
#    tmpL = [x for x in str(n)]
#    s = 0
#    e = -1
#    seq = len(tmpL) // 2
#    for num in range(seq):
#        if tmpL[s + num] != tmpL[e - num]:
#            return False
#    return True
#
#output = filter(is_palindrome, range(1, 1000))
#print('1~1000:', list(output))
#if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191]:
#    print('测试成功!')
#else:
#    print('测试失败!')

#def char2num(s):
#    digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '.': '.'}
#    return digits[s]
#
#def func1(x, y):
#    return x * 10 + y
#
#def func2(x, y):
#    return x / 10 + y
#
#def str2float(s):
#    tmpL = list(map(char2num, s))
#    #print(tmpL)
#    num1L = tmpL[:tmpL.index('.')]
#    num2L = []
#    for num in tmpL[tmpL.index('.') + 1:]:
#        num2L.insert(0,num)
#    num2L.append(0)
#    #print(num1L,num2L)
#    return reduce(func1,num1L) + reduce(func2,num2L)
#
#print('str2float(\'123.456\') =', str2float('123.456'))
#if abs(str2float('123.456') - 123.456) < 0.00001:
#    print('测试成功!')
#else:
#    print('测试失败!')
#
#def func(x, y):
#    return x * y
#
#def prod(L):
#    return reduce(func,L)
#
#print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
#if prod([3, 5, 7, 9]) == 945:
#    print('测试成功!')
#else:
#    print('测试失败!')
#
#def strUnion(x, y):
#    return str(x) + str(y)
#
#def normalize(name):
#    tmpL = list(map(str.lower,name))
#    tmpL[0] = str.upper(tmpL[0])
#    return reduce(strUnion,tmpL)
#
#L1 = ['adam', 'LISA', 'barT']
#L2 = list(map(normalize, L1))
#print(L2)

#            1
#           / \
#          1   1
#         / \ / \
#        1   2   1
#       / \ / \ / \
#      1   3   3   1
#     / \ / \ / \ / \
#    1   4   6   4   1
#   / \ / \ / \ / \ / \
#  1   5   10  10  5   1
#杨辉三角
#def triang(n):
#    L = [1]
#    if n == 1:
#        return L
#    else:
#        last = triang(n - 1)
#        for x in range(1, n):
#            if x == len(last):
#                L.append(last[x - 1] + 0)
#            else:
#                L.append(last[x - 1] + last[x])
#    return L
#
##print(" " * 3)
##print(triang(5))
#def printTriang(n):
#    result = []
#    for x in range(1,n + 1):
#        result.append(triang(x))
#    for i, res in enumerate(result,1):
#        outstr = "  " * (n - i)
#        for val in res:
#            #outstr = outstr + str(val) + " " * 3
#            outstr = outstr + "{:<5}".format(val)
#        outstr = outstr.rstrip(' ')
#        #print(outstr)
#        if n > 1 and i < n:
#            #print((" " * (2 *(n - i) -1 ) + '/  \\ ' * i).rstrip(' '))
#            outstr = outstr + '\n' + (" " * (2 *(n - i) -1 ) + '/  \\ ' * i).rstrip(' ')
#        print(outstr)
#
#printTriang(6)

#def triangles():
#    n = 1
#    while n < 20:
#        yield triang(n)
#        n = n + 1
#
## 期待输出:
## [1]
## [1, 1]
## [1, 2, 1]
## [1, 3, 3, 1]
## [1, 4, 6, 4, 1]
## [1, 5, 10, 10, 5, 1]
## [1, 6, 15, 20, 15, 6, 1]
## [1, 7, 21, 35, 35, 21, 7, 1]
## [1, 8, 28, 56, 70, 56, 28, 8, 1]
## [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
#n = 0
#results = []
#for t in triangles():
#    results.append(t)
#    n = n + 1
#    if n == 10:
#        break
#
#for t in results:
#    print(t)
#
#if results == [
#    [1],
#    [1, 1],
#    [1, 2, 1],
#    [1, 3, 3, 1],
#    [1, 4, 6, 4, 1],
#    [1, 5, 10, 10, 5, 1],
#    [1, 6, 15, 20, 15, 6, 1],
#    [1, 7, 21, 35, 35, 21, 7, 1],
#    [1, 8, 28, 56, 70, 56, 28, 8, 1],
#    [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
#]:
#    print('测试通过!')
#else:
#    print('测试失败!')

#L1 = ['Hello', 'World', 18, 'Apple', None]
#L2 = [ str.lower(s) for s in L1 if isinstance(s, str)]
#print(L2)
#if L2 == ['hello', 'world', 'apple']:
#    print('测试通过!')
#else:
#    print('测试失败!')

#def findMinAndMax(L):
#    if len(L) == 0:
#        return None,None
#    num_min = L[0]
#    num_max = L[0]
#    for num in L:
#        if num_max < num:
#            num_max = num
#        if num_min > num:
#            num_min = num
#    #print(num_min,num_max)
#    return num_min,num_max
#
#if findMinAndMax([]) != (None, None):
#    print('测试失败!')
#elif findMinAndMax([7]) != (7, 7):
#    print('测试失败!')
#elif findMinAndMax([7, 1]) != (1, 7):
#    print('测试失败!')
#elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
#    print('测试失败!')
#else:
#    print('测试成功!')

#def trim(instr):
#    lenstr = len(instr)
#    if lenstr == 0:
#        return ''
#    s = 0
#    while instr[s] == ' ':
#        s = s + 1
#        if s == lenstr:
#            return ''
#    e = -1
#    while instr[e] == ' ':
#        e = e - 1
#    e = len(instr) + e + 1
#    return instr[s:e]
#
#if trim('hello  ') != 'hello':
#    print('测试失败!')
#elif trim('  hello') != 'hello':
#    print('测试失败!')
#elif trim('  hello  ') != 'hello':
#    print('测试失败!')
#elif trim('  hello  world  ') != 'hello  world':
#    print('测试失败!')
#elif trim('') != '':
#    print('测试失败!')
#elif trim('    ') != '':
#    print('测试失败!')
#else:
#    print('测试成功!')

##汉诺塔问题
#def hanoi(n, a, b, c):
#    if n == 1:
#        #从a柱移动到c柱
#        print(a, '-->', c)
#    else:
#        #将a柱上的从上到下n-1个盘移到b柱
#        hanoi(n - 1, a, c, b)
#        #a柱上的最底下的第n个移动到c柱
#        print(a, '-->', c)
#        #将b柱上的n-1个盘子移到c柱
#        hanoi(n - 1, b, a, c)
## 调用
#hanoi(3, 'A', 'B', 'C')

#*args是可变参数，args接收的是一个tuple；
#**kw是关键字参数，kw接收的是一个dict
#def product(n1,*num):
#    total = n1
#    for n in num:
#        total = total * n
#    return total
#
#命名关键字参数  *
#def person(name, age, *, city, job):
#    print(name, age, city, job)
#person('Jack', 24, city='Beijing', job='Engineer')
#print('product(5) =', product(5))
#print('product(5, 6) =', product(5, 6))
#print('product(5, 6, 7) =', product(5, 6, 7))
#print('product(5, *(6, 7, 9)) =', product(5, 6, 7, 9))
#if product(5) != 5:
#    print('测试失败!')
#elif product(5, 6) != 30:
#    print('测试失败!')
#elif product(5, 6, 7) != 210:
#    print('测试失败!')
#elif product(5, *(6, 7, 9)) != 1890:
#    print('测试失败!')
#else:
#    try:
#        product()
#        print('测试失败!')
#    except TypeError:
#        print('测试成功!')

#ax**2+bx+c=0
#def quadratic(a, b, c):
#    deta = b**2 - 4 * a * c
#    if deta < 0:
#        print("para error.")
#        return
#    x1 = (-b + math.sqrt(deta)) / (2 * a)
#    x2 = (-b - math.sqrt(deta)) / (2 * a)
#    return x1, x2
#print(math.sqrt(4))
#print(quadratic(2, 3 ,1))
#print(quadratic(1, 3 ,-4))

#def move(x, y, step, angle=0):
#    nx = x + step * math.cos(angle)
#    ny = y - step * math.sin(angle)
#    return nx, ny
#
#x , y = move(100, 100, math.pi / 6)
#print(x, y)
#r = move(100, 100, math.pi / 6)
#print(r)

#def my_abs(x):
#    if not isinstance(x,(int, float)):
#        raise TypeError("Type Error.")
#    if x < 0:
#        return -x
#    return x
#
#def my_none():
#    pass
#
#print(my_abs(10))
#print(my_abs(-100))
#print(my_abs("a"))

#print(hex(10),hex(16))

#a = ['c', 'b', 'a']
#print(a)
#a.sort()
#print(a)
#a = 'abc'
#print(a)
#a.replace('a', 'A')
#print(a)


##key list
#set_test = set([1,2,5])
#print(set_test)
#set_test.add(8)
#print(set_test)
#set_test.remove(2)
#print(set_test)
#s1 = set([1, 2, 3])
#s2 = set([2, 3, 4])
##交集
#print(s1 & s2)
##并集
#print(s1 | s2)

#dict_test = {"a":79, "b":90}
#print(len(dict_test))
#print(dict_test["a"])
#dict_test["c"] = 100
#print(len(dict_test))
#print("b" in dict_test)
#print("d" in dict_test)
#print(dict_test.get("c"))
#print(dict_test.get("b", -1))
#print(dict_test.get("d"))
#print(dict_test.get("d", -1))
#print(dict_test.get("e", "Fail"))
#dict_test.pop("b")
#print(dict_test.get("b", -1))

#sum = 0
#for num in range(1,101):
#    sum = sum + num
#print("Sum : %d" % sum)

#height = 1.7
#weight = 80.5
#
#bmi = weight / (height**2)
#print("BMI : %s" % bmi)
#if bmi > 32:
#    print("严重肥胖")
#elif bmi > 28:
#    print("肥胖")
#elif bmi > 25:
#    print("过重")
#elif bmi > 18.5:
#    print("正常")
#else:
#    print("过轻")

#list_test = ["t1", "t2", "t3"]
#tuple_test = ("t1", "t2", "t3")
#tuple_test1 = ("t1", "t2", list_test)
#
#print(tuple_test1)
#list_test.append("t9")
#print(tuple_test1)
##tuple_test[0] = 0

#print(ord('a'))
#print(chr(67))
#print('中文'.encode('utf-8'))
#print('ABC'.encode('ascii'))
##b'ab' 字节流表示
#print(b'abc'.decode("ascii"))
#print(b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore'))
#print(len('a'.encode('utf-8')))
#print(len('中'.encode('utf-8')))
#print('Hi, %s, you have $%d.' % ('Michael', 1000000))
#print('%2d-%02d' % (3, 1))
#print('%.2f' % 3.1415926)
#print('growth rate: %d %%' % 7)
#print('Hello, {0:>8}, 成绩提升了 1{1:>6.1f}%'.format('小明', 17.125))
#print('Result: %.1f' % ((85 - 72) / 72 * 100))


#print(10 / 2)
#print(10 / 3)
#print(10 // 3)
#print(10 % 3)

#name = input("Please Input Your Name: ")
#print("Hello,",name,"!")

#a = "abc"
#b = a
#a = "a"
#print(a,b)

#print(r'''hello,\n
#world''')
#print('''hello,\n
#world''')
