import sys
import io
import base64
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random

BLOCK_SIZE = 16

def self_xor(iv , data) :
    return bytes([_iv ^ _data for _iv,_data in zip(iv,data)])

def AES_ECB(encrypt_data,key) :
    cipher = AES.new(key, AES.MODE_ECB)
    
    index = 0
    ciphertext = b''
    data_len = len(encrypt_data)
    while index < data_len:
        ciphertext += cipher.encrypt(encrypt_data[index:index + BLOCK_SIZE])   
        index += BLOCK_SIZE
    return ciphertext

def AES_CBC(encrypt_data,key,iv):
    cipher = AES.new(key, AES.MODE_ECB)
    
    index = 0
    ciphertext = b''
    iv_copy = iv
    data_len = len(encrypt_data)
    while index < data_len:
        data = self_xor(iv_copy,encrypt_data[index:index + BLOCK_SIZE])
        iv_copy = cipher.encrypt(data)
        ciphertext += iv_copy
        index += BLOCK_SIZE
    return ciphertext

def key_generator():
    random = Random.new()
    return base64.b64encode(random.read(BLOCK_SIZE))

def iv_generator():
    random = Random.new()
    return base64.b64encode(random.read(16))

data = sys.argv

mode = AES.MODE_ECB
if data[1] == "ECB":
    mode = AES.MODE_ECB
elif data[1] == "CBC":
    mode = AES.MODE_CBC


key = key_generator()
iv= iv_generator()
# jpg,png to ppm
o_ppmFile = "./original_pic.ppm"
o_image = Image.open(data[2])

ppm_byte = o_image.convert("RGB").tobytes()

encrypt_data = pad(ppm_byte,BLOCK_SIZE)
if mode == AES.MODE_ECB :
    ciphertext = AES_ECB(encrypt_data,key)
    image = Image.frombytes("RGB", o_image.size ,ciphertext)
    image.save('./result/encryptECB.png','png')
elif mode == AES.MODE_CBC:
    ciphertext = AES_CBC(encrypt_data,key,iv)
    image = Image.frombytes("RGB", o_image.size ,ciphertext)
    image.save('./result/encryptCBC.png','png')

print('KEY : ' + key.hex())
if mode == AES.MODE_CBC:
    print('IV : ' + iv.hex())



