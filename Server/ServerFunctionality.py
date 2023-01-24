import json
from Crypto.PublicKey import RSA
import base64
from Crypto.Cipher import PKCS1_OAEP
def getkey()->RSA.RsaKey:
    with open('./myRSA/priv.pem','rb') as f:
        mykey=RSA.import_key(f.read())
    f.close()
    return mykey
def getpublickey()->RSA.RsaKey:
    with open('./myRSA/pub.pem','rb') as f:
        mykey=RSA.import_key(f.read())
    f.close()
    return mykey
def ReceiveAndPreProcess(file):
    with open(file,'r')as f:
        data=json.load(f)
        masterkey=base64.b64decode(data['masterkey'])
        masteriv=base64.b64decode(data['masteriv'])
        privkey=getkey()
        RSAcipher=PKCS1_OAEP.new(privkey)
        masterkey=RSAcipher.decrypt(masterkey)
        masteriv=RSAcipher.decrypt(masteriv)
        data['masterkey']=base64.b64encode(masterkey).decode()
        data['masteriv']=base64.b64encode(masteriv).decode()
        with open(file,'w') as f2:
            json.dump(data,f2)
        f2.close()
    f.close()
    
#ReceiveAndPreProcess('MT.pdf.json')

def PreprocessAndSend(file,key):
    
    with open('../Server/files/'+file,'r')as f:
        data=json.load(f)
        masterkey=base64.b64decode(data['masterkey'])
        print('masterkey')
        print(len(masterkey))
        masteriv=base64.b64decode(data['masteriv'])
        privkey=getkey()
        RSAcipher=PKCS1_OAEP.new(key)
        masterkey=RSAcipher.encrypt(masterkey)
        masteriv=RSAcipher.encrypt(masteriv)
        data['masterkey']=base64.b64encode(masterkey).decode()
        data['masteriv']=base64.b64encode(masteriv).decode()
        with open('../Server/exportedfiles/'+'e'+file,'w') as f2:
            json.dump(data,f2)
        f2.close()
    f.close()
pubk=getpublickey()

#PreprocessAndSend('MT.pdf.json',pubk)


