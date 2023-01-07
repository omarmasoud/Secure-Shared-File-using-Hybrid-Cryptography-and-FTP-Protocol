from CustomCiphers import MyBlowFish,RoundRobinCipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,DES,CAST,Blowfish,DES3

from myftp import upload,serveFTP
import json
import os
import chardet
import base64
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
    response={}
    exportkeys()
    response
    RRCipher=RoundRobinCipher()
    RRCipher.encrypt(filepath)
    
    files = os.listdir(exporteddirectory)
    #upload(filepath+'.txt',directory='encryptedfiles')
    with open('encryptedfiles/'+filepath+'.txt','rb') as f:
        data=f.read()
        data=base64.b64encode(data).decode()
        response['file']=data
    f.close()
    for file in files:
        with open(exporteddirectory+file,'rb')as f:
            data=f.read()
            data=base64.b64encode(data).decode()
            response[file]=data
            
        f.close()
        #upload(file,directory=exporteddirectory)
    
    # print(response)
    
    with open(filepath+'.json','w') as f:
        json.dump(response,f)
    f.close()
    upload(filename=filepath+'.json')

    ############################## technique for reversing the encoding while reading on receiver##################
    # with open(exporteddirectory+'aes_key.pem','rb') as f:
    #     data=f.read()
    # resp=base64.b64decode(response['aes_key.pem'])
    # print(resp)
    # print(data)
    # bin=(resp==data)
    # print(bin)

#serveFTP()
send('FULLTEXT01.pdf')
# resp={}
# with open('FULLTEXT01.pdf.json','r') as f:
#     resp=json.load(f).encode('utf-8')
    
# f.close()
# resp=dict(resp)
# print(resp.keys())