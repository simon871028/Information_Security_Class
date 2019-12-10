import sys
import io
import base64
import random
import math

 #回傳n在m的範圍之內的乘法反元素   
def egcd(n, m):
    x, lastX = 0, 1
    y, lastY = 1, 0
    while (m != 0):
        q = n // m
        n, m = m, n % m
        x, lastX = lastX - q * x, x
        y, lastY = lastY - q * y, y
    return (lastX, lastY)

def KM(data):
    m = data - 1
    k = 0
    while m % 2 == 0:
        k += 1        #2的k次
        m //= 2
    return (k,m) 

def squareAndMultiply(x,H,n):
    y = 1
    H = bin(H)[2:]
    for i in H:
        y = int(pow(y,2,n))
        if i == '1':
            y = (y * x) % n
    return y

def millerTest(N): #follow the steps from the powerpoint 
    k , m = KM(N)
    for _ in range (0,10):
        a = random.randint(2,N - 2)
        b = squareAndMultiply(a,m,N)
        if b != N - 1 and b != 1:
            i = 1
            while i < k and b != N -1:
                b = squareAndMultiply(b,2,N)
                if b == 1 : 
                    return False
                i = i + 1
            if b != N - 1:
                return False
    return True

def Prime(number):
    p = False
    times = 0
    while p == False:
        times += 1
        binary = '1' #first bit must be 1
        for _ in range(0,number-2):
            binary += str(random.randint(0,1))
        binary += '1' #last bit also must be 1
        p = millerTest(int(binary,2))
    return int(binary,2)

argv = sys.argv

option = argv[1]

if option == 'init':
    bit_amount = int(int(argv[2]) / 2)
    p = Prime(bit_amount)
    q = Prime(bit_amount)
    n = p*q 

    phi = (p - 1)*(q - 1) #generate phi

    e = random.randint(1, phi)
    while math.gcd(e,phi)!= 1: #e and phi must 互質
        e = random.randint(1 , phi)
    d , discard  = egcd(e, phi) #discard the second variable egcd returns (useless)
    if d < 0:
        d += phi
    return_numbers = [p,q,n,e,d]
    print_words = ["p", "q", "n", "e", "d"]
    for word, number in zip(print_words, return_numbers):
        print(f"{word}: {number}")

elif option == 'encrypt':
    plaintext = int(argv[2].encode('utf-8').hex(),16) # from heximal to decimal
    n = int(argv[3])
    d = int(argv[4])
    cypher = squareAndMultiply(plaintext,d,n)
    print("ciphertext : ",cypher)
elif option == 'decrypt':
    ciphertext = int(argv[2])
    n = int(argv[3])
    e = int(argv[4])
    result =bytearray.fromhex(hex(squareAndMultiply(ciphertext,e,n))[2:]).decode() # heximal to binary,':' is used to delete '0x'
    print(result)