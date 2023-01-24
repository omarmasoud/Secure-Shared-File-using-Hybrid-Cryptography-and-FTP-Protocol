
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
    def __init__(self,k=readkey('aes_key'),iv=readkey('AESIV')) :
        self.k=k
        self.iv=iv
        
        self.cipher=AES.new(k,AES.MODE_CFB,iv)#AES with Mode Encrypt and Authenticate and execute
        pass
    def encrypt(self,plaintext):
        self.__init__(k=self.k,iv=self.iv)
        
        # nonce=self.cipher.nonce
        ciphertext=self.cipher.encrypt(plaintext)
        return ciphertext
    def decrypt(self,ciphertext):
        self.__init__(k=self.k,iv=self.iv)
        
        return self.cipher.decrypt(ciphertext)
class TripleDes(CustomCipher):
    def __init__(self,k=readkey('DES3_key'),iv=readkey('DES3IV')) :
        # self.cipher=DES.new(DES_KEY_1,DES.MODE_CBC,INITIAL_VALUE)
        # self.cipher2=DES.new(DES_KEY_2,DES.MODE_CBC,INITIAL_VALUE)
        self.k=k
        self.iv=iv
        self.cipher=DES3.new(k,DES3.MODE_CFB,iv)
    def encrypt(self,plaintext):
        self.__init__(k=self.k,iv=self.iv)
        # plaintext=pad(bytes(plaintext),8)
        # self.cipher.encrypt(self.cipher2.decrypt(self.cipher.encrypt(plaintext)))
        return self.cipher.encrypt(plaintext)
    def decrypt(self,ciphertext):
        self.__init__(k=self.k,iv=self.iv)
        # self.cipher.decrypt(self.cipher2.encrypt(self.cipher.decrypt(ciphertext)))
        return self.cipher.decrypt(ciphertext)
class MyCAST(CustomCipher):
    def __init__(self,k=readkey('CAST_key'),iv=readkey('CASTIV')) :
        self.cipher=CAST.new(k,CAST.MODE_CFB,iv)#CAST with Cipher Feedback
        self.k=k
        self.iv=iv
        pass
    def encrypt(self,plaintext):
        self.__init__(k=self.k,iv=self.iv)
        return self.cipher.encrypt(plaintext)
    def decrypt(self,ciphertext):
        self.__init__(k=self.k,iv=self.iv)
        return self.cipher.decrypt(ciphertext)
class MyBlowFish(CustomCipher):
    def __init__(self,k=readkey('Blowfish_key'),iv=readkey('BFIV')) :
        self.cipher=Blowfish.new(k,Blowfish.MODE_CFB,iv)#Blowfish with Cipher Feedback
        self.k=k
        self.iv=iv
        pass
    def encrypt(self,plaintext):
        self.__init__(k=self.k,iv=self.iv)
        return self.cipher.encrypt(plaintext)
    def decrypt(self,ciphertext):
        self.__init__(k=self.k,iv=self.iv)
        return self.cipher.decrypt(ciphertext)

class RoundRobinCipher(CustomCipher):
    def __init__(self,aesk=readkey('aes_key'),aesiv=readkey('AESIV'),dk=readkey('DES3_key')
                ,div=readkey('DES3IV'),ck=readkey('CAST_key'),civ=readkey('CASTIV')):
        
        self.AES_cipher=MyAES(aesk,aesiv)
        self.TripleDes_cipher=TripleDes(dk,div)
        self.Cast_cipher=MyCAST(ck,civ)
        # self.BlowFish_cipher=MyBlowFish()
    def encrypt(self, plaintext):
        """
        Round Robin Encrypt Functionality Goes as Follows:
        1-divide a given file and know how many partitions as outcome of division
        2-for each partition select either AES, DES3, CAST ciphers in order, 
        such that next partition takes the cipher that follows the selected one in a circular selection manner
        3-for each selected cipher we encrypt the selected partition and append its data in a temporary variable
        4- at last we save the encrypted data at /encryptedfiles/filename.txt

        """
        
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
        """
        Round Robin Decrypt Functionality Goes as Follows:
        1-divide a given encrypted file and know how many partitions as outcome of division
        2-for each partition select either AES, DES3, CAST ciphers in order, 
        such that next partition takes the cipher that follows the selected one in a circular selection manner
        3-for each selected cipher we decrypt the selected partition and append its data in a temporary variable
        4- at last we return the decrypted data for user to use it as he wish

        """
    
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
# myaes.encrypt('MT.pdf')
# decrdata=myaes.decrypt('FULLTEXT01.pdf.txt')
# with open('MT11.pdf','wb') as f:
#     for data in decrdata:
#         f.write(data)
# f.close()

