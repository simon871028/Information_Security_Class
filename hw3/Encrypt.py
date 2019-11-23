import sys
import io
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

data = sys.argv
if data[1] == "ECB":
    mode = AES.MODE_ECB
elif data[1] == "CBC":
    mode = AES.MODE_CBC

key = data[3]
BLOCK_SIZE = 32


# jpg,png to ppm
o_ppmFile = "./original_pic.ppm"
o_image = Image.open(data[2])

ppm_byte = o_image.convert("RGB").tobytes()
print(len(ppm_byte))
encrypt_data = pad(ppm_byte,BLOCK_SIZE)
print(len(encrypt_data))
index = 0
cipher = AES.new(key, mode)
ciphertext = ""
data_len = len(encrypt_data)
while index < data_len:
    ciphertext += cipher.encrypt(encrypt_data[index:index  + BLOCK_SIZE])   
    index += BLOCK_SIZE


image = Image.frombytes("RGB", o_image.size ,ciphertext)
image.save('./result/encrypt.png','png')



