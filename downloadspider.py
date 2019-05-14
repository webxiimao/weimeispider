# -*- coding:utf8 -*-
# write by xiimao
import requests
import os
from queue import Queue
from dbqueue import create_connect
from threading import Thread
from multiprocessing import Process
from Download import request


class Spider():
    '''
    先写多线程
    '''
    def __init__(self):
        # 连接数据库
        self.db = create_connect('root', 'myy436627', 'flaskstudy')
        self.base_path_addr = "/Users/yuyumao/开发/python/flask/flask-and-taro-project/static/"
        self.base_path = "girlsImg"



    def put_queue(self):
        cursor = self.db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT * FROM girls_img LIMIT 10")

        data=cursor.fetchall()




    def download_pic(self):
        '''
        图片下载
        :return:
        '''
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self.db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT * FROM girls_img LIMIT 30")

        # 使用 fetchone() 方法获取单条数据，fetchall获取所有数据
        data = cursor.fetchall()
        print(self.base_path_addr + self.base_path)
        if not os.path.isdir(self.base_path_addr + self.base_path):
            os.makedirs(self.base_path_addr + self.base_path)
            print("mkdir girlsimg")

        #
        for row in data:
            img_url = row[4]
            img_local_path = row[6]
            img_arr = img_url.split("/")
            name = img_arr[len(img_arr) - 1]
            print("img_url:%s"%name)


            # html = requests.get(img_url,headers=headers)
            html = request.get(img_url, 3)
            print(html)
            path = self.base_path_addr + self.base_path + "/" + name
            with open(path, 'wb') as f:
                f.write(html.content)


        # 关闭数据库连接
        self.db.close()




if __name__ == '__main__':
    spider = Spider()
    spider.download_pic()