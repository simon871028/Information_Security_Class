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
    cipher = AES.new(key, AES.MODE_ECB) #引用AES加密
    
    index = 0
    ciphertext = b''
    data_len = len(encrypt_data) #取得資料長度
    while index < data_len: #如果index小於data_len表示還有block尚未加密
        #將一個block加密後放入結果
        ciphertext += cipher.encrypt(encrypt_data[index:index + BLOCK_SIZE])   
        index += BLOCK_SIZE
    return ciphertext

def AES_CBC(encrypt_data,key,iv):
    cipher = AES.new(key, AES.MODE_ECB) #引用AES加密
    
    index = 0
    ciphertext = b''
    iv_copy = iv #需要與encrypt_dataXOR的加密
    data_len = len(encrypt_data)
    while index < data_len: #如果index小於data_len表示還有block尚未加密
        #將一個block與iv_copy做xor
        data = self_xor(iv_copy,encrypt_data[index:index + BLOCK_SIZE])
        iv_copy = cipher.encrypt(data) #將xor後的資料進行加密，並且放入iv_copy讓下次xor使用
        ciphertext += iv_copy # 將解密結果放入結果
        index += BLOCK_SIZE
    return ciphertext

def AES_NEW(encrypt_data,key,iv):
    cipher = AES.new(key, AES.MODE_ECB) #需要與encrypt_dataXOR的加密
    index = 0
    ciphertext = b''
    iv_copy_plain = iv
    iv_copy_cipher = iv
    data_len = len(encrypt_data)
    while index < data_len: #如果index小於data_len表示還有block尚未加密
        #將一個block與iv_copy_plain做xor當作下次的iv_copy_plain使用
        iv_copy_plain = self_xor(iv_copy_plain,encrypt_data[index:index + BLOCK_SIZE])
        data = cipher.encrypt(iv_copy_plain) #將xor後的資料加密

        #將一個block與iv_copy_cipher做xor當作下次的iv_copy_cipher使用
        iv_copy_cipher = self_xor(iv_copy_cipher,data) 
        ciphertext += iv_copy_cipher將xor後的結果放入結果
        index += BLOCK_SIZE
    return ciphertext

def key_generator():
    random = Random.new()
    return base64.b64encode(random.read(BLOCK_SIZE))

def iv_generator():
    random = Random.new()
    return base64.b64encode(random.read(16))

data = sys.argv

#取得 mode
mode = data[1]

#產生key與iv
key = key_generator()
iv= iv_generator()

#讀取圖片
o_image = Image.open(data[2])
#轉換為bytes
ppm_byte = o_image.convert("RGB").tobytes()
#進行padding
encrypt_data = pad(ppm_byte,BLOCK_SIZE)

#確認mode後選取模式加密
if mode == "ECB" :
    ciphertext = AES_ECB(encrypt_data,key)
elif mode == "CBC":
    ciphertext = AES_CBC(encrypt_data,key,iv)
elif mode == "NEW":
    ciphertext = AES_NEW(encrypt_data,key,iv)

#儲存影像
image = Image.frombytes("RGB", o_image.size ,ciphertext)
image.save('./encrypt'+mode+'.png','png')

#print key and iv
print('KEY : ' + key.hex())
if mode != "ECB":
    print('IV : ' + iv.hex())



