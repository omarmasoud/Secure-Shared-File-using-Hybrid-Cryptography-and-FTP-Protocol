import ftplib # FTP server credentials
import threading
 
from subprocess import call
FTP_HOST = "127.0.0.1" 
FTP_PORT = 6060 
FTP_USER = "username" 
FTP_PASS = "P@ssw0rd" 
# connect to the FTP server 


def runFTPserver():
    
    status = call("mkdir out", shell=True)
    command = "python -m python_ftp_server -u username -p P@ssw0rd --ip 127.0.0.1 --port 6060 -d "+ r"./out"
    status = call(command, shell=True)
# force UTF-8 encoding 

def upload(filename):
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.encoding = "utf-8"
    with open(filename, "rb") as file:
        ftp.storbinary(f"STOR {filename}", file)
    ftp.quit()


def download(filename):
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.login(FTP_USER,FTP_PASS)
    ftp.encoding = "utf-8"
    with open(filename, "wb") as file:
        ftp.retrbinary(f"RETR {filename}", file.write)
    ftp.quit()

# local file name you want to upload 

def serveFTP():
    thread=threading.Thread(target=runFTPserver)
    thread.start()
