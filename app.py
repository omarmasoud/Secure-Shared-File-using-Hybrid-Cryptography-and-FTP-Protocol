import flask

app=flask.Flask(__name__="SecureFileSharedEncryption")
@app.route('/')
def index():
    return "hello Cryptography"
