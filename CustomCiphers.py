
from KeysManager import readkey,AES,DES3,Blowfish,CAST
from Consts import *
from FileManager import *
from Crypto.Util.Padding import pad
class CustomCipher():
    def __init__(self) :
        pass        
    def encrypt(self,plaintext):
        with open(plaintext, 'rb') as f:
            data= f.read
        
    def decrypt(self,ciphertext):
        pass
class MyAES(CustomCipher):
    def __init__(self) :
        
        self.cipher=AES.new(readkey('aes_key'),AES.MODE_CFB,readkey('AESIV'))#AES with Mode Encrypt and Authenticate and execute
        pass
    def encrypt(self,plaintext):
        self.__init__()
        # nonce=self.cipher.nonce
        ciphertext=self.cipher.encrypt(plaintext)
        return ciphertext
    def decrypt(self,ciphertext):
        self.__init__()
        return self.cipher.decrypt(ciphertext)
class TripleDes(CustomCipher):
    def __init__(self) :
        # self.cipher=DES.new(DES_KEY_1,DES.MODE_CBC,INITIAL_VALUE)
        # self.cipher2=DES.new(DES_KEY_2,DES.MODE_CBC,INITIAL_VALUE)
        self.cipher=DES3.new(readkey('DES3_key'),DES3.MODE_CFB,readkey('DES3IV'))
    def encrypt(self,plaintext):
        self.__init__()
        # plaintext=pad(bytes(plaintext),8)
        # self.cipher.encrypt(self.cipher2.decrypt(self.cipher.encrypt(plaintext)))
        return self.cipher.encrypt(plaintext)
    def decrypt(self,ciphertext):
        self.__init__()
        # self.cipher.decrypt(self.cipher2.encrypt(self.cipher.decrypt(ciphertext)))
        return self.cipher.decrypt(ciphertext)
class MyCAST(CustomCipher):
    def __init__(self) :
        self.cipher=CAST.new(readkey('CAST_key'),CAST.MODE_CFB,readkey('CASTIV'))#CAST with Cipher Feedback
        pass
    def encrypt(self,plaintext):
        self.__init__()
        return self.cipher.encrypt(plaintext)
    def decrypt(self,ciphertext):
        self.__init__()
        return self.cipher.decrypt(ciphertext)
class MyBlowFish(CustomCipher):
    def __init__(self) :
        self.cipher=Blowfish.new(readkey('Blowfish_key'),Blowfish.MODE_CFB,readkey('BFIV'))#Blowfish with Cipher Feedback
        pass
    def encrypt(self,plaintext):
        return self.cipher.encrypt(plaintext)
    def decrypt(self,ciphertext):
        return self.cipher.decrypt(ciphertext)

class RoundRobinCipher(CustomCipher):
    def __init__(self):
        self.AES_cipher=MyAES()
        self.TripleDes_cipher=TripleDes()
        self.Cast_cipher=MyCAST()
        # self.BlowFish_cipher=MyBlowFish()
    def encrypt(self, plaintext):
        
        num_partitions=divideFile(plaintext,directory='')
       
        encrypted_data=''
        Encryptionlist=[]
        for partition in range(num_partitions):
            with open('dividedfiles/'+str(plaintext)+'_'+str(partition)+'.txt', 'rb') as f:
                try:
                    data=f.read()
                    if partition%3==0:
                        encrypted_data=self.AES_cipher.encrypt(data)
                    elif partition%3==1:
                        encrypted_data=self.TripleDes_cipher.encrypt(data)
                    elif partition%3==2:
                        encrypted_data=self.Cast_cipher.encrypt(data)
                
                    Encryptionlist.append(encrypted_data)
                except:
                    pass

            f.close()
        with open('encryptedfiles/'+str(plaintext)+".txt",'wb') as f:
            for encr in Encryptionlist:
                f.write(encr)
        f.close()
        return Encryptionlist
    def decrypt(self, ciphertext):
        
        num_partitions=divideFile(ciphertext,directory='encryptedfiles')
        decrypted_Data=''
        DecryptionList=[]
        for partition in range(num_partitions):
            with open('encryptedfiles/'+str(ciphertext), 'rb') as f:
                data=f.read()
                try:
                    if partition%3==0:
                        decrypted_Data=self.AES_cipher.decrypt(data)
                    elif partition%3==1:
                        decrypted_Data=self.TripleDes_cipher.decrypt(data)
                    elif partition%3==2:
                        decrypted_Data=self.Cast_cipher.decrypt(data)
                    DecryptionList.append(decrypted_Data)
                except:
                    pass

            f.close()
        # with open('decryptedfiles/'+str(ciphertext),'wb') as f:
        #     for decr in DecryptionList:
        #         f.write(decr)
        # f.close()
        return DecryptionList

        
# myaes=RoundRobinCipher()
# myaes.encrypt('FULLTEXT01.pdf')
# decrdata=myaes.decrypt('FULLTEXT01.pdf.txt')
# with open('roundrobindecryptionfinals.pdf','wb') as f:
#     for data in decrdata:
#         f.write(data)
# f.close()

