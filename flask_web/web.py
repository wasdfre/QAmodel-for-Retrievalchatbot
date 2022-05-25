


from flask import Flask,jsonify
from flask import request
import pandas as pd
import json

app = Flask(__name__)
def request_parse(req_data): 
    # '''解析请求数据并以json形式返回'''
    if req_data.method == 'POST':
        data = req_data.json;
    elif req_data.method == 'GET':
        data = req_data.args;
    return data;
   
@app.route('/', methods = ["POST"])   # GET 和 POST 都可以
def get_data():
      # 方法一
    data = request.get_json()                # 获取 JSON 数据
    print(data)
    # data = data.get('obj')  # 获取参数并转变为 DataFrame 结构
    # 假设有如下 URL
    # http://10.8.54.48:5000/index?name=john&age=20
    # name = data.get("name");
    # age = data.get("age");
     # 将数据再次打包为 JSON 并传回
    return jsonify(
        data=json.dumps(data),
        extra={
            'messgae': 'success'
        }
    ),400
    
        
if __name__ == '__main__':
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('0.0.0.0',8787),app)
    server.serve_forever()
    # app.run(host="0.0.0.0", port=8787)     #将port 5051改为当前云公网服务器已经打开的可以访问的端口，比如端口8589 
# http://101.42.109.40:6000/hello
# http://101.42.109.40:8787/
# 127.0.0.1:6000
# 0.0.0.0:6000