import sys
import io
import base64
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random

data = sys.argv
mode = AES.MODE_ECB
iv = ''
mode = "ECB"
if data[1] == "CBC" or data[1] == "NEW":
    mode = data[1]
    iv = input('IV :' )
    iv = bytes.fromhex(iv)


key = input('key : ')
key = bytes.fromhex(key)
BLOCK_SIZE = 16
def self_xor(iv , data) :
    return bytes([_iv ^ _data for _iv,_data in zip(iv,data)])

def AES_ECB(decrypt_data,key) :
    cipher = AES.new(key, AES.MODE_ECB)#引用AES
    index = 0 #代表第index個block 
    plaintext = b'' 
    data_len = len(decrypt_data)
    while index < data_len: # 依序處理各個block
        plaintext += cipher.decrypt(decrypt_data[index:index + BLOCK_SIZE])   
        index += BLOCK_SIZE
    return plaintext

def AES_CBC(decrypt_data,key,iv):
    cipher = AES.new(key, AES.MODE_ECB)
    index = 0
    plaintext = b''
    iv_copy = iv #先將iv儲存進iv_copy
    data_len = len(decrypt_data)
    while index < data_len: #依序處理每一個block
        data = cipher.decrypt(decrypt_data[index:index + BLOCK_SIZE]) #將經過decryption block cipher的資料儲存進data
        plain = self_xor(iv_copy,data) #然後將iv與data做XOR得到部分的plaintext放入plain 
        iv_copy = decrypt_data[index:index + BLOCK_SIZE] #新的iv會是當前block的ciphertext
        plaintext += plain 
        index += BLOCK_SIZE
    return plaintext

def AES_NEW(decrypt_data,key,iv):
    cipher = AES.new(key, AES.MODE_ECB)
    index = 0
    plaintext = b''
    iv_copy_plain = iv #靠近plaintext端的iv
    iv_copy_cipher = iv #靠近ciphertext端的iv
    #initialization IV 是一模一樣的
    data_len = len(decrypt_data)
    while index < data_len: #依序處理每一個block
        data = self_xor(iv_copy_cipher,decrypt_data[index : index + BLOCK_SIZE])
        #先將IV跟此block的ciphertext做XOR存入data
        iv_copy_cipher = decrypt_data[index : index + BLOCK_SIZE]
        #新的iv_copy_cipher 會是此block's ciphertext
        data = cipher.decrypt(data)
        #讓data被decryption block cipher 解密
        plaintext += self_xor(iv_copy_plain,data)
        #plaintext會等於 iv_copy_plain & data XOR後的結果
        iv_copy_plain = data #新的iv_copy_plain會等於data
        index += BLOCK_SIZE
    return plaintext
# jpg,png to ppm
o_image = Image.open(data[2])
ppm_byte = o_image.convert("RGB").tobytes()
decrypt_data = pad(ppm_byte,BLOCK_SIZE)

if mode == "ECB" :
    plaintext = AES_ECB(decrypt_data,key)
elif mode == "CBC":
    plaintext = AES_CBC(decrypt_data,key,iv)
elif mode == "NEW":
    plaintext = AES_NEW(decrypt_data,key,iv)

image = Image.frombytes("RGB", o_image.size ,plaintext)
image.save('./decrypt'+mode+'.png','png')





