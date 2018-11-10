#-*- coding=utf8 -*-
import pymysql


def create_connect(usname, pwd, db):
    return pymysql.connect('localhost', usname, pwd, db)

class mysqldb(object):
    '''
    初始化数据库
    '''
    def __init__(self, usname, pwd, db):
        '''
        初始化mysql
        '''
        # 连接数据库
        self.db = pymysql.connect('localhost', usname, pwd, db)
        # 创建游标
        # self.cursor = self.db.cursor()

    def insert(self, sql):
        cursor = self.db.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            # print("数据库执行成功")
        except:
            # 如果发生错误则回滚
            self.db.rollback()
            # print("数据库执行失败")

        # 关闭数据库连接
        self.db.close()

    def select(self, sql):
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            return results

        except:
            print("Error: unable to fetch data")



class Queue(object):
    '''
    队列模块
    '''
    def __init__(self):
        '''
        初始化

        '''
        pass

