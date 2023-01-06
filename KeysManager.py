from Crypto.Random import get_random_bytes
from Crypto import Random
from Crypto.Cipher import AES,DES,CAST,Blowfish,DES3
from Crypto.PublicKey import RSA

import Crypto.Cipher
AES_KEY= get_random_bytes(AES.key_size[0])
print(type(AES_KEY))
AES_INITIAL_VALUE=get_random_bytes(16)
DES3_KEY=get_random_bytes(DES3.key_size[1])
CAST_KEY=get_random_bytes(CAST.key_size[0])
CAST_INITIAL_VALUE=get_random_bytes(8)
Blowfish_KEY=get_random_bytes(Blowfish.key_size[0])
DES3_INITIAL_VALUE=Random.new().read(DES3.block_size)
Blowfish_INITIAL_VALUE=get_random_bytes(Blowfish.block_size)
with open("keys/aes_key.pem", "wb") as f:
    f.write(AES_KEY)
f.close()
with open("keys/DES3_key.pem", "wb") as f:
    f.write(DES3_KEY)
f.close()
with open("keys/CAST_key.pem", "wb") as f:
    f.write(CAST_KEY)
f.close()
with open("keys/Blowfish_key.pem", "wb") as f:
    f.write(Blowfish_KEY)
f.close()
with open("keys/AESIV.pem", "wb") as f:
    f.write(AES_INITIAL_VALUE)
f.close()

with open("keys/DES3IV.pem", "wb") as f:
    f.write(DES3_INITIAL_VALUE)
f.close()

with open("keys/CASTIV.pem", "wb") as f:
    f.write(CAST_INITIAL_VALUE)
f.close()
with open("keys/BFIV.pem", "wb") as f:
    f.write(Blowfish_INITIAL_VALUE)
f.close()

def readkey(keyname):
    with open('keys/'+keyname+'.pem','rb') as f:
        key=f.read()
    f.close()
    return bytes(key)

