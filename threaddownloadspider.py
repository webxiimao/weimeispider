# -*- coding:utf8 -*-
# write by xiimao
import requests
import os
import threading
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

        self.pic_queue = Queue()#创建一个线程队列
        self.max_thread = 10
        self.init_data()
        self.Flag = False
        self.lock = threading.Lock()



    def init_data(self):
        '''
        初始化数据
        :return:
        '''
        cursor = self.db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT * FROM girls_img where local_img_url is NULL")

        self.data=cursor.fetchall()

    def run(self):
        #创建文件夹
        if not os.path.isdir(self.base_path_addr + self.base_path):
            os.makedirs(self.base_path_addr + self.base_path)
            print("mkdir girlsimg")

        for pic in self.data:
            self.pic_queue.put(pic)

        ths = []
        for i in range(0,self.max_thread):
            th = Thread(target=self.download_pic)
            th.start()
            ths.append(th)

        self.Flag = True

        for th in ths:
            th.join()

        # 关闭数据库连接
        self.db.close()

    def download_pic(self):
        '''
        图片下载
        :return:
        '''

        while self.pic_queue.empty() is not True:
            row = self.pic_queue.get()
            id = row[0]
            img_url = row[4]
            img_local_path = row[6]
            img_arr = img_url.split("/")
            name = img_arr[len(img_arr) - 1]
            print("img_url:%s"%name)


            # html = requests.get(img_url,headers=headers)
            html = request.get(img_url, 3)
            if html is False:
                self.pic_queue.put(row)
                continue
            path = self.base_path_addr + self.base_path + "/" + name
            with self.lock:
                cursor = self.db.cursor()
                sql = 'UPDATE girls_img SET local_img_url="%s" where id=%s'%(name,id)
                print(sql)
                cursor.execute(sql)
                self.db.commit()
                cursor.close()
                with open(path, 'wb') as f:
                    f.write(html.content)







if __name__ == '__main__':
    spider = Spider()
    spider.run()