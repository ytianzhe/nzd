from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def HomeLogin():
    openid = request.args.get('openid')
    if openid.strip() == '':
        print('s is null')
    else:
        print(openid)
        return openid
