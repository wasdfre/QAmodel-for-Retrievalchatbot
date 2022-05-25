


from flask import Flask,jsonify
from flask import request
import pandas as pd
import json
import pandas as pd
import matplotlib as mpl
import numpy as np
#作用
from jiebaSegment import *
#相似度检测
from sentenceSimilarity import SentenceSimilarity
#读取语料，拆分为问题，答案以及关键词
def read_corpus():
    #问题列表
    qList = []
    # 问题的关键词列表
    qList_kw = []
    #答案列表
    aList = []
    #语料地址
    path = r"./data/train_pair.json"
    file = open(path, 'r',encoding='utf-8')
    #全部信息
    info = json.loads(file.read())
    #分别处理
    for t in info:
        qList.append(info[t][0])
        #这个函数的作用，含义就是分割词呗
        qList_kw.append(seg.cut(info[t][0]))
        aList.append(info[t][1])
    return qList_kw, qList, aList

# 设置外部词
seg = Seg()
#目前感觉这个函数意义不大
seg.load_userdict('./userdict/userdict.txt')
# 读取数据
List_kw, questionList, answerList = read_corpus()
# 初始化模型
ss = SentenceSimilarity(seg)
ss.set_sentences(questionList)
ss.TfidfModel()         # tfidf模型
# ss.LsiModel()         # lsi模型
# ss.LdaModel()         # lda模型

app = Flask(__name__)
def request_parse(req_data): 
    # '''解析请求数据并以json形式返回'''
    if req_data.method == 'POST':
        data = req_data.json;
    elif req_data.method == 'GET':
        data = req_data.args;

    # print(data,type(data))
    return data;
   

@app.route('/', methods = ["POST"])   # GET 和 POST 都可以
def get_data():
      # 方法一
    data = request.get_json()                # 获取 JSON 数据
    # print(data)
    # data = data.get('obj')  # 获取参数并转变为 DataFrame 结构
    # 假设有如下 URL
    # http://10.8.54.48:5000/index?name=john&age=20
    # name = data.get("name");
    # age = data.get("age");
     # 将数据再次打包为 JSON 并传回
    question=data["qes"];
    res=ss.similarity_k(question, 5);
    answer=answerList[res[0][0]];  
    res_response=dict();
    res_response['answer']=answer;
    i=1;
    for idx, score in zip(*res):
        res_response[str(i)] = [questionList[idx], str(score)];
        i=i+1;
    
    return jsonify(
        data=json.dumps(res_response),
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