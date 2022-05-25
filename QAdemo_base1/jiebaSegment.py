# -*- coding: utf-8 -*-
# @Time    : 2019/4/3 19:46
# @Author  : Alan
# @Email   : xiezhengwen2013@163.com
# @File    : cut.py
# @Software: PyCharm

import jieba
import codecs

#停用词处理
class Seg(object):
    stopword_filepath = "./stopwordList/stopword.txt"

    def __init__(self):
        #读取文件
        self.stopwords = set()
        self.read_in_stopword()

    def load_userdict(self,file_name):
        #读取提取词
        jieba.load_userdict(file_name)

    def read_in_stopword(self):
        #读取停用词
        file_obj = codecs.open(self.stopword_filepath, 'r', 'utf-8')
        while True:
            #按行读取，感觉可以运行一次就保存好，不需要每次都读
            line = file_obj.readline()
            #移除头尾指定的字符
            line=line.strip('\r\n')
            if not line:
                break
            self.stopwords.add(line)
        file_obj.close()

    #分割语句
    def cut(self, sentence, stopword= True, cut_all = False):
        #使用jieba分割
        seg_list = jieba.cut(sentence, cut_all)
        results = []
        #去掉停用词，构建词库
        for seg in seg_list:
            if stopword and seg in self.stopwords:
                continue
            results.append(seg)

        return results

    #上下一样
    def cut_for_search(self,sentence, stopword=True):
        # 搜索引擎模式
        seg_list = jieba.cut_for_search(sentence)

        results = []
        for seg in seg_list:
            if stopword and seg in self.stopwords:
                continue
            results.append(seg)

        return results