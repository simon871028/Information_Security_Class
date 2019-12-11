import random
import math
import sys

def egcd(n,m):
    if m == 0:
        return 1,0
    else:
        x,y = egcd(m,n%m)
        x,y = y, (x - (n//m)*y)
        return x,y

def getKM(data):
    m = data - 1
    k = 0
    while m % 2 == 0:
        k += 1 
        m //= 2
    return (k,m) 

def squareAndMultiply(x,H,n):
    y = 1
    #將次方數轉為二進制
    H = bin(H)[2:]
    #計算 以投影片的實作
    for i in H:
        y = int(pow(y,2,n))
        if i == '1':
            y = (y * x) % n
    return y

def millerRabinsTest(data):
    #取得 N - 1 = (2 ^ k) * m
    k , m = getKM(data)

    for index in range(0,5):
        #從2 ~ data -2 取 a
        a = random.randint(2,data - 2)
        # b = (a ^ m) mod data 
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

def primeGenerator(number):
    check = False
    #如果沒有跑過miller rabins test 就重新製作
    while check == False:
        #頭放1
        binary = '1'
        #中間塞入random的0 1
        for index in range(0,number-2):
            binary += str(random.randint(0,1))
        #尾放1
        binary += '1'
        #將製作的數字轉為10進制並跑miller rabins test
        check = millerRabinsTest(int(binary,2))
    return int(binary,2)

argv = sys.argv

option = argv[1]

if option == 'init':
    bit_number = int(int(argv[2]) / 2)
    #產生p q n
    p = primeGenerator(bit_number)
    q = primeGenerator(bit_number + 1)
    n = p * q

    _n = (p - 1) * (q - 1)
    e = random.randint(1,_n)
    while math.gcd(e,_n) != 1:
        e = random.randint(1,_n)
        
    #取得 e的乘法反元素
    d,non = egcd(e,_n)
    if d < 0:
        d += _n

    print('p : ',p)
    print('q : ',q)
    print('n : ',n)
    print('e : ',e)
    print('d : ',d)
elif option == 'encrypt':
    #將明文從文字轉乘16進位後，再轉為10進制
    plaintext = int(argv[2].encode('utf-8').hex(),16)
    n = int(argv[3])
    d = int(argv[4])
    # (plaintext ^ d) mod n to result
    result = squareAndMultiply(plaintext,d,n)
    print("ciphertext : ",result)
    
elif option == 'decrypt':
    ciphertext = int(argv[2])
    n = int(argv[3])
    e = int(argv[4])
    #將 (ciphertext ^ e) mod n 轉為 16進制後轉成明文
    result =bytearray.fromhex(hex(squareAndMultiply(ciphertext,e,n))[2:]).decode()
    print(result)




