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
    cipher = AES.new(key, AES.MODE_ECB)
    index = 0
    plaintext = b''
    data_len = len(decrypt_data)
    while index < data_len:
        plaintext += cipher.decrypt(decrypt_data[index:index + BLOCK_SIZE])   
        index += BLOCK_SIZE
    return plaintext

def AES_CBC(decrypt_data,key,iv):
    cipher = AES.new(key, AES.MODE_ECB)
    index = 0
    plaintext = b''
    iv_copy = iv
    data_len = len(decrypt_data)
    while index < data_len:
        data = cipher.decrypt(decrypt_data[index:index + BLOCK_SIZE])
        plain = self_xor(iv_copy,data)
        iv_copy = decrypt_data[index:index + BLOCK_SIZE]
        plaintext += plain
        index += BLOCK_SIZE
    return plaintext

def AES_NEW(decrypt_data,key,iv):
    cipher = AES.new(key, AES.MODE_ECB)
    index = 0
    plaintext = b''
    iv_copy_plain = iv
    iv_copy_cipher = iv
    data_len = len(decrypt_data)
    while index < data_len:
        data = self_xor(iv_copy_cipher,decrypt_data[index : index + BLOCK_SIZE])
        iv_copy_cipher = decrypt_data[index : index + BLOCK_SIZE]
        data = cipher.decrypt(data)
        plaintext += self_xor(iv_copy_plain,data)
        iv_copy_plain = data
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





