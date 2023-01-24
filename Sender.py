from CustomCiphers import MyBlowFish,RoundRobinCipher
from Crypto.Cipher import AES,DES,CAST,Blowfish,DES3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import requests

from myftp import upload,serveFTP
import json
import os
import chardet
import base64
keysdirectory='keys/'
exporteddirectory='exportedkeys/'
keys=['aes_key.pem','DES3_key.pem','CAST_key.pem']
IVS=['AESIV.pem','DES3IV.pem','CASTIV.pem']
def getkey()->RSA.RsaKey:
    with open('myRSA/priv.pem','rb') as f:
        mykey=RSA.import_key(f.read())
    f.close()
    return mykey
def getpublickey()->RSA.RsaKey:
    with open('myRSA/pub.pem','rb') as f:
        mykey=RSA.import_key(f.read())
    f.close()
    return mykey

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
    
    response=requests.get('http://127.0.0.1:5000/getserverkey')
    response=response.json()
    print('response')
    pubE=response['e']
    pubN=response['n']
    serverpublickey=RSA.construct((pubN,pubE))
    response={}
    exportkeys()
    response
    #Server RSA Public key
    #serverkey=getpublickey()
    RSAcipher=PKCS1_OAEP.new(serverpublickey)
    RRCipher=RoundRobinCipher()
    RRCipher.encrypt(filepath)
    
    files = os.listdir(exporteddirectory)
    #upload(filepath+'.txt',directory='encryptedfiles')
    with open('encryptedfiles/'+filepath+'.txt','rb') as f:
        data=f.read()
        data=base64.b64encode(data).decode()
        response['file']=data
    f.close()

    with open ('keys/Blowfish_key.pem','rb') as f:
        masterkey=f.read()
        masterkey=base64.b64encode(RSAcipher.encrypt(masterkey)).decode()
        response['masterkey']=masterkey
    f.close()
    with open ('keys/BFIV.pem','rb') as f:
        masteriv=f.read()
        masteriv=base64.b64encode(RSAcipher.encrypt(masteriv)).decode()
        response['masteriv']=masteriv
    f.close()
    for file in files:
        with open(exporteddirectory+file,'rb')as f2:
            data=f2.read()
            data=base64.b64encode(data).decode()
            response[file]=data
            
        f2.close()
        #upload(file,directory=exporteddirectory)
    
    # print(response)
    
    with open(filepath+'.json','w') as f:
        json.dump(response,f)
    f.close()
    data={'file':response,'filename':filepath+'.json'}
  
    requests.post('http://127.0.0.1:5000/sendfile',json=data)
    #upload(filename=filepath+'.json')
    

    ############################## technique for reversing the encoding while reading on receiver##################
    # with open(exporteddirectory+'aes_key.pem','rb') as f:
    #     data=f.read()
    # resp=base64.b64decode(response['aes_key.pem'])
    # print(resp)
    # print(data)
    # bin=(resp==data)
    # print(bin)
send('MT.pdf')
def receive(filename):
    """"
    Takes file name,
    requests server public key,
    encrypts file with round robin then encrypts the keys and IVs of round robin ciphers with 
    Blowfish Cipher as a masterkey
    then encrypts this masterkey using the server public key
    """
    with open(filename+'.json','r') as f:
        data=json.load(f)
        # User Private Key
        privkey=getkey()
        RSAcipher=PKCS1_OAEP.new(privkey)
        # Master Key
        masterkey=base64.b64decode(data['masterkey'])
        masteriv=base64.b64decode(data['masteriv'])
        masterkey=RSAcipher.decrypt(masterkey)
        masteriv=RSAcipher.decrypt(masteriv)
        BFCipher=MyBlowFish(k=masterkey,iv=masteriv)
        # keys
        aesk=BFCipher.decrypt(base64.b64decode(data['aes_key.pem']))
        aesiv=BFCipher.decrypt(base64.b64decode(data['AESIV.pem']))
        desk=BFCipher.decrypt(base64.b64decode(data['DES3_key.pem']))
        desiv=BFCipher.decrypt(base64.b64decode(data['DES3IV.pem']))
        castk=BFCipher.decrypt(base64.b64decode(data['CAST_key.pem']))
        castiv=BFCipher.decrypt(base64.b64decode(data['CASTIV.pem']))
        print('*********************')
        book=base64.b64decode(data['file'])
        with open ('encryptedfiles/temp.txt','wb') as f2:
            f2.write(book)
        f2.close()
        RR=RoundRobinCipher(aesk=aesk,aesiv=aesiv,dk=desk,div=desiv,ck=castk,civ=castiv)
        decr=RR.decrypt('temp.txt')
        with open(filename+'.pdf','wb') as f2:
            for dec in decr:
                f2.write(dec)
        f2.close()
        print('done assembling')
    f.close()
def requestFile(filename):
    mykey=getkey()
    n=mykey.n
    e=mykey.e
    params={'n':n,'e':e,'filename':filename}
    response=requests.post('http://127.0.0.1:5000/requestfile',json=params)
    print(response.content)
    response=response.json()

    with open(filename,'w') as f:
        json.dumps(response['file'],f)
    f.close()
    receive(filename)
    pass
requestFile('MT.pdf.json')
#receive('eMT.pdf')

    #print(data)
#serveFTP()
#send('MT.pdf')
# resp={}
# with open('FULLTEXT01.pdf.json','r') as f:
#     resp=json.load(f).encode('utf-8')

# f.close()
# resp=dict(resp)
# print(resp.keys())
