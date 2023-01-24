from flask import Flask, request,jsonify
from flask_socketio import SocketIO,send, emit, join_room, leave_room
from ServerFunctionality import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

app=Flask(__name__)
@app.route('/')
def index():
    return "hello Cryptography"


@app.route("/getserverkey" , methods = ['GET'])
def getServerKey():
    key=getkey()
    n=key.n
    e=key.e
    
    data={"n":n,"e":e }
    #print(data)
    return jsonify(data)  

@app.route("/requestfile" , methods = ['POST'])
def requestfile():
    payload = request.get_json()
    filename=payload['filename']
    print('filerequestedname')
    print(filename)
    n=payload['n']
    e=payload['e']
    userpublickey=RSA.construct((n,e))
    PreprocessAndSend(filename,userpublickey)
    file=json.load('../Server/exportedfiles/'+'e'+filename)
    data={'file':file}
    return jsonify(data)

    
@app.route("/sendfile" , methods = ['POST'])
def sendfile():
    payload = request.get_json()
    file=payload['file']
    #print(file)
    filename=payload['filename']
    print(filename)
    
    with open('../Server/files/'+filename,'w') as f:
        json.dump(file,f)
    f.close()
    ReceiveAndPreProcess('../Server/files/'+filename)
    return 'sent'

if __name__ == '__main__':
    app.run()
    #app.run(debug=True , host="0.0.0.0",port=8080)