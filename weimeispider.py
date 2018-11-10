#-*- coding=gbk -*-
import requests
from lxml import html
from dbqueue import create_connect
from Download import request



connect = create_connect('root','root','flaskstudy')
base_url = "http://www.mmonly.cc"

def weimeispider():
    '''
    爬取所有图的url加入队列
    :return:
    '''
    tag_tree = request_url('%s/tag'%base_url)
    # #获取元素
    tags = tag_tree.xpath("//div[@class='TagList'][1]/a")
    urls = handle_tags(tags)
    # print(urls)
    # for url in urls:
    #     album_handle(url)


def album_handle(url):
    '''
    相册表的处理
    :param url:
    :return:
    '''
    album_tree = request_url(url)
    # album = album_tree.xpath("")



def request_url(url):
    '''
    requests 返回 response tree
    :param url:
    :return:
    '''
    response = request.get(url, 3)
    response.encoding = "gbk"
    tree = html.fromstring(response.text)
    return tree

def handle_tags(tags):
    #处理tags
    for tag in tags:
        # 获取url
        cursor = connect.cursor()
        # tags_href.append("%s%s"%(base_url,tag.xpath("@href")[0]))
        # 获取tag名
        # tags_text.append(tuple([tag.text]))
        sql = "insert into girls_tag(tag) values(%s)"
        cursor.execute(sql, [tag.text])
        cursor.close()
        album_handle("%s%s" % (base_url, tag.xpath("@href")[0]))
    connect.commit()
    connect.close()

def sql_run(sql, params=None):
    #mysql多数据处理
    pass








def sql_many_run(sql, params=None):
    #mysql多数据处理
    cursor = connect.cursor()
    cursor.executemany(sql, params)
    connect.commit()
    connect.close()




if __name__ == "__main__":
    weimeispider()