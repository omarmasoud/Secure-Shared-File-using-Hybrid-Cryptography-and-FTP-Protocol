from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES,DES,CAST,Blowfish

import Crypto.Cipher
AES_KEY= get_random_bytes(AES.key_size[0])
DES_KEY_1=get_random_bytes(DES.key_size)
DES_KEY_2=get_random_bytes(DES.key_size)
CAST_KEY=get_random_bytes(CAST.key_size[0])
Blowfish_KEY=get_random_bytes(Blowfish.key_size[0])


