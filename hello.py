import json
import mysql
from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
from flask import redirect
app = Flask(__name__)



def out_user_info(code, msg, data):
    out_info = {}
    out_info['code'] = code
    out_info['msg'] = msg
    out_info['data'] = data
    return json.dumps(out_info)

 # print(out_user_info('0', '奶珍多表', mysql.TableToJson()))



# @app.route("/babyInfo", methods=['GET','POST'])
# def get_work_lines():
#     if all_data==():
#         return out_user_info(0, '当前生产线数据为空', all_data)
#     elif all_data == 0:
#         return out_user_info(1, '获取当前生产线数据数据错误', None)
#     else:
#         return out_user_info(0, '获取当前生产线数据成功', all_data)

@app.route("/da",methods=['GET','POST'])
def a():
    print(out_user_info('0', '奶珍多表', mysql.TableToJson()))
    return out_user_info('0', '奶珍多表', mysql.TableToJson())

@app.route('/',methods=['GET','POST'])
def index():
 return '<h1>Hello World!</h1>'

@app.route("/user",methods=['GET','POST'])
def user():
    return 'hello user'


@app.route("/users/<id>",methods=['GET','POST'])
def users(id):
    return 'hello user:'+id




@app.route("/query_user",methods=['GET','POST'])
def query_user():
    id=request.args.get('id')
    return 'query_user:'+id

@app.route("/query_url")
def query_url():
    return 'query_url:'+url_for('query_user')

@app.route("/query_login" ,methods=['GET','POST'])
def query_login():
    return render_template('index.html')





if __name__ == '__main__':
    # app.run("10.168.20.186","5000",debug=True)
    # app.run("127.0.0.1", port=5000)
    # app.run("127.0.0.1",port=8080)
    app.run("10.168.20.186",port=8080)