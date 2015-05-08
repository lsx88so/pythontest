# -*- coding: utf-8 -*-
import os
import sys
import functools

print "Hello World!"
print "Hello World!"

#name=raw_input('input: ')
#print name

print '\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8')

sum = 0
for x in range(101):
    sum = sum + x
print sum

sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print sum

sum = 0
n = 100
while n > 0:
    sum = sum + n
    n = n - 2
print sum

def my_abs(x):
    if not isinstance(x,(int,float)):
        raise TypeError("Bad Type!Type shuld be int or float.")
    if x > 0:
        return x
    else:
        return -x

a=abs(-3)
b=my_abs(-3)
#c=my_abs('a')

print a,b

def fact(n):
    if n == 1:
        return 1
    else:
        return n * fact(n-1)

print fact(1)
print fact(3)
print fact(100)

def facttt(p,c,m):
    if c > m:
        return p
    return facttt(p * c,c + 1,m)

#@tail_call_optimized
def factt(n):
    return facttt(1,1,n)

print factt(100)

def fun(s,e):
    su = 0
    for x in range(s,e+1):
        su = su + x
    return su

print fun(8,16)

def upn(s):
    b=""
    n=1
    for a in s:
        if n == 1:
            a = a.upper()
        else:
            a = a.lower()
        b = b + a
        n = n + 1
    return b
        
L = ['adam', 'LISA', 'barT']
print map(upn,L)

def cc(x,y):
    return x*y

def prod(li):
    return reduce(lambda x,y:x*y,li)

print prod([2,3,3])

def sus(n):
    m = 2
    while m < n:
        if n%m == 0:
            return False
        m = m + 1
    return True

print filter(None,range(1,101))
print filter(sus,range(1,101))

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print 'call %s():' % func.__name__
        func(*args, **kw)
        print 'end call'
    return wrapper

@log
def now():
    print '2013-12-25'

print now.__name__
now()

def logg(text='Call'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            print '%s %s() Begin:' % (text,func.__name__)
            func(*args,**kw)
            print '%s %s() End:' % (text,func.__name__)
        return wrapper
    return decorator

@logg()
def nowg():
    print '2013-12-25'

nowg()

@logg('Execute')
def nowgg():
    print 'ttt'

nowgg()

print sys.path


#os.system('pause')
