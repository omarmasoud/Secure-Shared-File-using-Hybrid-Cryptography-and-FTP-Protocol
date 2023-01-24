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
    """
    Server Function that takes a file sent by user , decodes its encrypted master key,
    then decrypt it with its own private key,
    Lastly Save it at Server/files directory
    """
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
    """
    Server Function that takes file name of a file saved at Server/files directory,
    Along with a Clients Public Key
    It then preprocess the file that it decodes the master key and encrypt it with user's specific public key
    then save it for him at Server/exported files directory
    """
    
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
# pubk=getpublickey()

#PreprocessAndSend('MT.pdf.json',pubk)


def initServerkeys():
    key = RSA.generate(3072)
    #print(type(key))
    private_key = key
    public_key = key.publickey()

    print('generating server keys')
    with open('../Server/myRSA/pub.pem','wb') as f:
        f.write( public_key.export_key())
    f.close()
    with open('../Server/myRSA/priv.pem','wb')as f:
        f.write(key.export_key())
    f.close()
