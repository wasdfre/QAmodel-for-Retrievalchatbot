#coding=utf8
from flask import url_for, redirect, render_template, jsonify, request, flash, Response
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import Flask
import os
import time
import logging
import uuid
import codecs
import sys

## 载入功能模块
sys.path.append('tmodel1')
from tmodel1 import *

#日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__) ##标志该脚本为程序的根目录

#创建路径用于存储数据
app.config['SECRET_KEY'] = 'cannot find the information'
app.config['CACHE'] = os.path.join(os.path.dirname(__file__), "static/cache")
app.config['MOUTH'] = os.path.join(os.path.dirname(__file__), "static/mouth")

# 前端传送数据所在目录
if not os.path.exists(app.config['MOUTH']):
	os.makedirs(app.config['MOUTH'])

# 返回给前端的数据所在目录
if not os.path.exists(app.config['CACHE']):
	os.makedirs(app.config['CACHE'])

## 创建路由映射，将index函数注册为路由，而且是根地址的处理程序
#"/"后面要加域名，不一定
@app.route('/', methods=['GET'])
def index():
	return '欢迎使用智能问答'




#记得加域名
@app.route('/mouth', methods=['GET', 'POST'])
def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['txt']
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
def get_mouth():
    file_data=request.form.get('file')
    #file_data = request.files['file']
    print(file_data)
    if file_data and allowed_file(file_data.filename):
        filename = secure_filename(file_data.filename) ##获取名字
        file_uuid = str(uuid.uuid4().hex)
        time_now = datetime.now()
        filename = time_now.strftime("%Y%m%d%H%M%S")+"_"+file_uuid+"_"+filename
        file_data.save(os.path.join(app.config['MOUTH'], filename))
        src_path = os.path.join(app.config['MOUTH'], filename) ##获取服务端本地路径
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
        question ="衬衫的价格是多少？"
        time1 = time.time()
        question_k = ss.similarity_k(question, 5)
        print("亲，我们给您找到的答案是： {}".format(answerList[question_k[0][0]]))
        for idx, score in zip(*question_k):
            print("same questions： {},                score： {}".format(questionList[idx], score))
        time2 = time.time()
        cost = time2 - time1
        print('Time cost: {} s'.format(cost))        
        print("score is:",format(questionList[idx], score))

	#最后将结果以json格式返回给前端
        data = {
		"code": 0,
		"score": str(format(answerList[question_k[0][0]]))
	   }
        
        return jsonify(data)
    return jsonify({"code": 1, "msg": u"文件格式不允许"})

if __name__=='__main__':
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('0.0.0.0',5000),app)
    server.serve_forever()
