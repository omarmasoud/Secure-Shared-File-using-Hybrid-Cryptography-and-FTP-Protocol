from Crypto.Random import get_random_bytes
from Crypto import Random
from Crypto.Cipher import AES,DES,CAST,Blowfish,DES3

import Crypto.Cipher
AES_KEY= get_random_bytes(AES.key_size[0])
AES_INITIAL_VALUE=get_random_bytes(16)
DES_KEY_1=get_random_bytes(DES.key_size)
DES_KEY_2=get_random_bytes(DES.key_size)
DES3_KEY=get_random_bytes(DES3.key_size[1])
CAST_KEY=get_random_bytes(CAST.key_size[0])
CAST_INITIAL_VALUE=get_random_bytes(8)
Blowfish_KEY=get_random_bytes(Blowfish.key_size[0])
DES3_INITIAL_VALUE=Random.new().read(DES3.block_size)




