from CustomCiphers import MyBlowFish,RoundRobinCipher
from myftp import upload,serveFTP
import json
import os
keysdirectory='keys/'
exporteddirectory='exportedkeys/'
keys=['aes_key.pem','DES3_key.pem','CAST_key.pem']
IVS=['AESIV.pem','DES3IV.pem','CASTIV.pem']
def exportkeys():
    BFCipher=MyBlowFish()
    for key in keys:
        with open(keysdirectory+key,'rb')as f:
            data=f.read()
            with open(exporteddirectory+key,'wb') as f2:
                f2.write(BFCipher.encrypt(data))
            f2.close()
        f.close()

    for IV in IVS:
        with open(keysdirectory+IV,'rb')as f:
            data=f.read()
            with open(exporteddirectory+IV,'wb') as f2:
                f2.write(BFCipher.encrypt(data))
            f2.close()
        f.close()
def send(filepath):
    exportkeys()
    RRCipher=RoundRobinCipher()
    RRCipher.encrypt(filepath)
    
    files = os.listdir(exporteddirectory)
    upload(filepath+'.txt',directory='encryptedfiles')
    for file in files:
        upload(file,directory=exporteddirectory)
    

serveFTP()

send('FULLTEXT01.pdf')
