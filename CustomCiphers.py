
from KeysManager import *
from Consts import *
from FileManager import *
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
        self.cipher=AES.new(AES_KEY,AES.MODE_CFB)#AES with Cipher Feedback
        pass
    def encrypt(self,plaintext):
        return self.cipher.encrypt(plaintext)
    def decrypt(self,ciphertext):
        return self.cipher.decrypt(ciphertext)
class TripleDes(CustomCipher):
    def __init__(self) :
        self.cipher=DES.new(DES_KEY_1,DES.MODE_CBC)
        self.cipher2=DES.new(DES_KEY_2,DES.MODE_CBC)
    def encrypt(self,plaintext):
        return self.cipher.encrypt(self.cipher2.decrypt(self.cipher.encrypt(plaintext)))
    def decrypt(self,ciphertext):
        return self.cipher.decrypt(self.cipher2.encrypt(self.cipher.decrypt(ciphertext)))

class MyCAST(CustomCipher):
    def __init__(self) :
        self.cipher=CAST.new(CAST_KEY,CAST.MODE_CFB)#CAST with Cipher Feedback
        pass
    def encrypt(self,plaintext):
        return self.cipher.encrypt(plaintext)
    def decrypt(self,ciphertext):
        return self.cipher.decrypt(ciphertext)
class MyBlowFish(CustomCipher):
    def __init__(self) :
        self.cipher=Blowfish.new(Blowfish_KEY,Blowfish.MODE_CFB)#Blowfish with Cipher Feedback
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
        self.BlowFish_cipher=MyBlowFish()
    def encrypt(self, plaintext):
        num_partitions=divideFile(plaintext)
        encrypted_data=''
        Encryptionlist=[]
        for partition in range(num_partitions):
            with open('dividedfiles/'+'encrypted_'+str(plaintext)+'_'+str(partition)+'.txt', 'rb') as f:
                data=f.read()
                if partition%4==0:
                    encrypted_data=self.AES_cipher.encrypt(data)
                elif partition%4==1:
                    encrypted_data=self.TripleDes_cipher.encrypt(data)
                elif partition%4==2:
                    encrypted_data=self.Cast_cipher.encrypt(data)
                elif partition%4==3:
                    encrypted_data=self.BlowFish_cipher.encrypt(data)
                Encryptionlist.append(encrypted_data)

            f.close()
        return Encryptionlist
    def decrypt(self, ciphertext):
        
        num_partitions=divideFile(ciphertext)
        decrypted_Data=''
        DecryptionList=[]
        for partition in range(num_partitions):
            with open('dividedfiles/'+str(ciphertext)+'_'+str(partition)+'.txt', 'rb') as f:
                data=f.read()
                if partition%4==0:
                    decrypted_Data=self.AES_cipher.decrypt(data)
                elif partition%4==1:
                    decrypted_Data=self.TripleDes_cipher.decrypt(data)
                elif partition%4==2:
                    decrypted_Data=self.Cast_cipher.decrypt(data)
                elif partition%4==3:
                    decrypted_Data=self.BlowFish_cipher.decrypt(data)
                DecryptionList.append(decrypted_Data)

            f.close()
        return DecryptionList

        

rr_cipher=RoundRobinCipher()

ll=rr_cipher.encrypt('FULLTEXT01.pdf')
print('ll is ')
print(ll)