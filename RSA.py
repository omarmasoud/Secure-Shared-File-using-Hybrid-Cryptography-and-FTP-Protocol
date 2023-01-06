from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# generate a new pair of public and private keys
key = RSA.generate(2048)
print(type(key))
private_key = key
public_key = key.publickey()
with open('myRSA/pub.pem','wb') as f:
    f.write( public_key.export_key())
f.close()
with open('myRSA/priv.pem','wb')as f:
    f.write(key.export_key())
f.close()
def getkey()->RSA.RsaKey:
    with open('myRSA/priv.pem','rb') as f:
        mykey=RSA.import_key(f.read())
    f.close()
def getpublickey()->RSA.RsaKey:
    with open('myRSA/pub.pem','rb') as f:
        mykey=RSA.import_key(f.read())
    f.close()

    return mykey
# key=getkey()
# pub=key.publickey()
# enc=PKCS1_OAEP.new(pub)
# # use the public key to encrypt a message
# message = b"Hello World!"
# encrypted_message = enc.encrypt(message)
# dec=PKCS1_OAEP.new(key)
# # use the private key to decrypt the message
# decrypted_message = dec.decrypt(encrypted_message)
# print(decrypted_message)  # prints "Hello World!"
