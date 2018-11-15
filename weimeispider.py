#-*- coding=gbk -*-
import requests
import re
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



def album_handle(url,tag):
    '''
    相册表的处理
    :param url:
    :return:
    '''
    #tag 插入
    album_tree = request_url(url)

    tag_title = album_tree.xpath('//div[@class="TagTxt"]/p')[0]
    cursor = connect.cursor()
    sql = "insert into girls_tag(title,tag) values(%s,%s)"
    cursor.execute(sql, [tag_title.text,tag.text])
    id = int(cursor.lastrowid)
    cursor.close()
    connect.commit()
    #全页数处理逻辑
    max = get_all_album_page(album_tree)
    #album逻辑处理

    albums = album_tree.xpath("//div[@class='ABox']//a")
    for album in albums:
        title = album.xpath('img/@alt')[0]
        url = album.xpath('@href')[0]
        cover = album.xpath('img/@src')[0]
        img_handle(url, title, cover ,id)

def img_handle(url, title, cover ,id):
    img_tree = request_url(url)

    album_discription = img_tree.xpath("//div[@class='descriptionBox']/p")[0].text if len(img_tree.xpath("//div[@class='descriptionBox']/p"))>0 else ""
    cursor = connect.cursor()
    sql = "insert into girls_album(title,cover_img,description,girls_tag_id) values(%s,%s,%s,%s)"
    cursor.execute(sql, [title, cover, album_discription ,id])
    id = int(cursor.lastrowid)
    cursor.close()
    connect.commit()



def get_all_album_page(album_tree):
    last_page = album_tree.xpath("//div[@class='wrappic']/div[@class='pages']/ul/li")[-1]
    max_a = last_page.xpath("a")
    max = 0
    if len(max_a) > 0:
        max_page = max_a[0].xpath('@href')[0]
        max = re.match(r'\S+/(\d+).html', max_page).group(1)
    return max


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
        album_handle("%s%s" % (base_url, tag.xpath("@href")[0]), tag)

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