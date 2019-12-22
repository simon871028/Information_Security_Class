import random
import math
import sys
import hashlib
import binascii

def egcd(n,m):
    if m == 0:
        return 1,0
    else:
        x,y = egcd(m,n%m)
        x,y = y, (x - (n//m)*y)
        return x,y

def self_xor(iv , data) :
    _str = ''
    for _iv,_data in zip(iv,data):
        if _iv == _data:
            _str += '0'
        else:
            _str += '1'
    return _str

def self_or(x,y):
    _x = bin(x)
    _y = bin(y)
    for _ in range(0,len(_y) - len(_x)):
        _x = '0' + _x
    _str = ''
    for __x,__y in zip(_x,_y):
        if __x == '1' or __y == '1':
            _str += '1'
        else:
            _str += '0'
    return _str

def getKM(data):
    m = data - 1
    k = 0
    while m % 2 == 0:
        k += 1 
        m //= 2
    return (k,m) 

def squareAndMultiply(x,H,n = -1):
    y = 1
    H = bin(H)[2:]
    for i in H:
        y = y * y
        if n != (-1):
            y = y % n
        if i == '1':
            y = y * x
            if n != (-1):
                y = y % n
        
    return y

def millerRabinsTest(data):
    k , m = getKM(data)

    for index in range(0,5):
        a = random.randint(2,data - 2)
        b = squareAndMultiply(a,m,data)
        if b != data - 1 and b != 1:
            i = 1
            while i < k and b != data -1:
                b = squareAndMultiply(b,2,data)
                if b == 1 : 
                    return False
                i = i + 1
            if b != data - 1:
                return False
    return True

def get_pq():
    L = 1024
    n = 1023 // 160
    b = 1023 % 160
    while True:
        check = False
        q = 0
        seed = '1'
        while check == False:
            seed = '1'
            for index in range(0,random.randrange(158,512)):
                seed += str(random.randint(0,1))
            seed += '1'
            g = len(seed)

            s = hashlib.sha1()
            s.update(seed)
            u1 = bin(int(binascii.hexlify(s.digest()),16))[2:]

            s = hashlib.sha1()
            s.update(str((int(seed,2) + 1) % squareAndMultiply(2,g)))
            u2 = bin(int(binascii.hexlify(s.digest()),16))[2:]
            U = int(self_xor(u1,u2),2)
            q = int(self_or(U ,(squareAndMultiply(2,159) + 1)),2)
            check = millerRabinsTest(q)
           

        counter = 0
        offset = 2
        
        while counter < 4096:
            w = 0
            i = 0
            v = []
            for k in range(0,n+1):
                s = hashlib.sha1()
                s.update(str((int(seed,2) + offset + k) % squareAndMultiply(2,g)))
                v.append(int(binascii.hexlify(s.digest()),16))
            for _v in v:
                if i != n:
                    w += _v * squareAndMultiply(2,i*160)
                else:
                    w += (_v % squareAndMultiply(2,b)) * squareAndMultiply(2,i*160)
                i += 1 

            x = w + squareAndMultiply(2,L-1)
            c = x % (2*q)
            p = x - (c-1)
            if  p >= squareAndMultiply(2,L-1):
                if millerRabinsTest(p):
                    return p,q
            print(counter)
            counter = counter + 1
            offset = offset + n + 1

def get_abd(p,q):
    a = 1
    while a == 1:
        h = random.randrange(2,p-2)
        a = squareAndMultiply(h,(p-1)/q , p)
    d = random.randrange(0,q)
    b = squareAndMultiply(a,d,p)
    return a,b,d

def read_public():
    fp = open("public.txt","r")
    p,q,a,b = fp.readlines()
    p = int(p)
    q = int(q)
    a = int(a)
    b = int (b)
    fp.close()
    return p,q,a,b

def read_private():
    fp = open("private.txt","r")
    d = fp.readline()
    d = int(d)
    fp.close()
    return d

argv = sys.argv

option = argv[1]

if option == "k":
    p,q = get_pq()
    a,b,d = get_abd(p,q)
    fp = open("public.txt", "w")
    print >>fp, p
    print >>fp, q
    print >>fp, a
    print >>fp, b
    fp.close()

    fp = open("private.txt", "w")
    print >>fp, d
    fp.close()
elif option == "s":
    message = argv[2]
    p,q,a,b = read_public()
    d = read_private()

elif option == "v":
    message = argv[2]
    p,q,a,b = read_public()


