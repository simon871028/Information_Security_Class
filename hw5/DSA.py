import random
import math
import sys
import hashlib
import binascii


def egcd(n, m):
    if m == 0:
        return 1, 0
    else:
        x, y = egcd(m, n % m)
        x, y = y, (x - (n//m)*y)
        return x, y


def self_xor(iv, data):
    _str = ''
    for _iv, _data in zip(iv, data):
        if _iv == _data:
            _str += '0'
        else:
            _str += '1'
    return _str


def self_or(x, y):
    _x = bin(x)
    _y = bin(y)
    for _ in range(0, len(_y) - len(_x)):
        _x = '0' + _x
    _str = ''
    for __x, __y in zip(_x, _y):
        if __x == '1' or __y == '1':
            _str += '1'
        else:
            _str += '0'
    return _str


def sha(data):
    s = hashlib.sha1()
    s.update(data)
    return int(binascii.hexlify(s.digest()), 16)


def getKM(data):
    m = data - 1
    k = 0
    while m % 2 == 0:
        k += 1
        m //= 2
    return (k, m)


def millerRabinsTest(data):
    k, m = getKM(data)

    for _ in range(0, 5):
        a = random.randint(2, data - 2)
        b = pow(a, m, data)
        if b != data - 1 and b != 1:
            i = 1
            while i < k and b != data - 1:
                b = pow(b, 2, data)
                if b == 1:
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
            for _ in range(0, random.randrange(158, 512)):
                seed += str(random.randint(0, 1))
            seed += '1'
            g = len(seed)

            u1 = bin(sha(seed))[2:]
            u2 = bin(sha(str((int(seed, 2) + 1) % pow(2, g))))[2:]
            U = int(self_xor(u1, u2), 2)
            q = int(self_or(U, (pow(2, 159) + 1)), 2)
            check = millerRabinsTest(q)

        counter = 0
        offset = 2

        while counter < 4096:
            w = 0
            i = 0
            v = []
            for k in range(0, n+1):
                v.append(sha(str((int(seed, 2) + offset + k) % pow(2, g))))
            for _v in v:
                if i != n:
                    w += _v * pow(2, i*160)
                else:
                    w += (_v % pow(2, b)) * pow(2, i*160)
                i += 1

            x = w + pow(2, L-1)
            c = x % (2*q)
            p = x - (c-1)
            if p >= pow(2, L-1):
                if millerRabinsTest(p):
                    return p, q
            counter = counter + 1
            offset = offset + n + 1


def get_abd(p, q):
    a = 1
    while a == 1:
        h = random.randrange(2, p-2)
        a = pow(h, (p-1)/q, p)
    d = random.randrange(0, q)
    b = pow(a, d, p)
    return a, b, d


def read_public():
    fp = open("public.txt", "r")
    p, q, a, b = fp.readlines()
    p = int(p)
    q = int(q)
    a = int(a)
    b = int(b)
    fp.close()
    return p, q, a, b


def read_private():
    fp = open("private.txt", "r")
    d = fp.readline()
    d = int(d)
    fp.close()
    return d


argv = sys.argv

option = argv[1]

if option == "k":
    p, q = get_pq()
    a, b, d = get_abd(p, q)
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
    p, q, a, b = read_public()
    d = read_private()
    K = random.randrange(1, q)
    K_inv, non = egcd(K, q)
    r = pow(a, K, p) % q
    s = ((sha(message) + d * r) * K_inv) % q
    print('r: ')
    print(r)
    print('s: ')
    print(s)
elif option == "v":
    message = argv[2]
    r = int(argv[3])
    s = int(argv[4])
    p, q, a, b = read_public()
    S_inv, non = egcd(s, q)
    w = S_inv % q
    u1 = (w*sha(message)) % q
    u2 = (w*r) % q
    v = ((pow(a, u1, p)*pow(b, u2, p)) % p) % q
    if v == r:
        print('valid')
    else:
        print('invalid')
