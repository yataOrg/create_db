#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# desc: 规范了一点代码 用的面相对象的类的方式 进行编写code, 可读性好，方便维护。

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import pymysql


# 封装一个类，通常要把大段code 拆分成多个小的func
class Insert_data(object):
    db_config = {
        'user': '',
        'pswd': '',
        'host': 'localhost',
        'port': '3306',
        'dw': "dw",
    }

    def __init__(self):
        pass

    def stopwordslist(self, filepath):
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords

    def main(self):
        db = pymysql.connect("localhost", self.db_config.user, self.db_config.pswd, self.db_config.dw, charset="utf8")
        cursor = db.cursor()
        sql = "select `id`,`User_Comments` from hubspotdata where `User_Comments` <> '0' "

        cursor.execute(sql)
        rows = cursor.fetchall()
        new_list = list(map(lambda x: x[1], rows))
        new_key = list(map(lambda x: x[0], rows))

        stopwords = self.stopwordslist('./stopwords.txt')  # 这里加载停用词的路径

        corpus = new_list
        vectorizer = CountVectorizer(stop_words=stopwords)  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        # print(vectorizer)
        transformer = TfidfTransformer()
        # print(transformer)  # 该类会统计每个词语的tf-idf权值
        tfidf = transformer.fit_transform(
            vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵

        word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
        weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

        for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        #try:
            print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
            for j in range(len(word)):

                if weight[i][j] != 0.0:
                    comment_id = new_key[i]
                    print(comment_id, word[j], weight[i][j])
                    sql2 = "insert into en_test (`comment_id`, `key_word`,`weight`) VALUES (%d, '%s', '%s' )" % (
                    comment_id, word[j], weight[i][j])
                    # test

                    # print("insert into hbp_tfidf_2 (`comment_id`, `key_word`,`weight`) VALUES ('%d', '%s', '%s' )" % (comment_id, word[j], weight[i][j]))
                    cursor.execute(sql2)
                    db.commit()

        cursor.close()
        db.close()
        print('end' * 10)


# 开始调用
app = Insert_data()
app.main()
