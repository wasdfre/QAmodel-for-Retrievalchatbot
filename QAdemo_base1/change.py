

import pandas as pd
import matplotlib as mpl
import numpy as np
#库作用
from nltk.probability import FreqDist
import time
import json 

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

  
from flask import Flask,jsonify
app = Flask(__name__) ##标志该脚本为程序的根目录
#创建路径用于存储数据
from flask import request
@app.route('/mouth', methods=['GET', 'POST'])
def login(data):
    print(request.method)
    question = request.json['data']
    data1 = json.dumps(question)
    print(type(question))
    print(data1)
    question_k = ss.similarity_k(question, 5)
    return  jsonify(answerList[question_k[0][0]])

if __name__=='__main__':
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('0.0.0.0',6000),app)
    server.serve_forever()