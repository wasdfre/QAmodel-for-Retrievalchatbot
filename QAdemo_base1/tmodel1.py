# -*- coding: utf-8 -*-
# @Time    : 2019/4/3 16:48
# @Author  : Alan
# @Email   : xiezhengwen2013@163.com
# @File    : tmodel.py
# @Software: PyCharm

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

#显示字体
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # enable chinese

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

#绘制信息
def plot_words(wordList):
    #频度统计吧
    fDist = FreqDist(wordList)
    #print(fDist.most_common())
    print("单词总数: ",fDist.N())
    print("不同单词数: ",fDist.B())
    fDist.plot(10)


if __name__ == '__main__':
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

    while True:
        question = input("请输入问题(q退出): ")
        if question == 'q':
            break
        time1 = time.time()
        question_k = ss.similarity_k(question, 5)
        print(question_k)
        # print("亲，我们给您找到的答案是： {}".format(answerList[question_k[0][0]]))
        # for idx, score in zip(*question_k):
            # print("same questions： {},                score： {}".format(questionList[idx], score))
        # time2 = time.time()
        # cost = time2 - time1
        # print('Time cost: {} s'.format(cost))


