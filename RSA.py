from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# generate a new pair of public and private keys
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey()
enc=PKCS1_OAEP.new(key)
# use the public key to encrypt a message
message = b"Hello World!"
encrypted_message = enc.encrypt(message)
dec=PKCS1_OAEP.new(key)
# use the private key to decrypt the message
decrypted_message = dec.decrypt(encrypted_message)
print(decrypted_message)  # prints "Hello World!"