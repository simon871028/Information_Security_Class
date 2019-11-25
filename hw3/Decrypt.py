import sys
import io
import base64
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random

data = sys.argv
if data[1] == "ECB":
    mode = AES.MODE_ECB
elif data[1] == "CBC":
    mode = AES.MODE_CBC

key = input('key : ')
key = bytes.fromhex(key)
BLOCK_SIZE = 16


# jpg,png to ppm
o_ppmFile = "./original_pic.ppm"
o_image = Image.open(data[2])
ppm_byte = o_image.convert("RGB").tobytes()
encrypt_data = pad(ppm_byte,BLOCK_SIZE)

index = 0
cipher = AES.new(key, mode)
plaintext = b''
data_len = len(encrypt_data)
while index < data_len:
    plaintext +=  cipher.decrypt(encrypt_data[index:index  + BLOCK_SIZE])
    index += BLOCK_SIZE

image = Image.frombytes("RGB", o_image.size ,plaintext)
image.save('./result/decrypt.png','png')






