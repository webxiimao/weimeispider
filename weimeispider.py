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



def album_handle(url,tag,num=1):
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
    handle_all_page_album(url, max, album_tree, id, url)


def handle_all_page_album(url, max, album_tree, id, init_url, num=1):
    if init_url != url:
        album_tree = request_url(url)
    albums = album_tree.xpath("//div[@class='ABox']//a")
    for album in albums:
        title = album.xpath('img/@alt')[0]
        album_url = album.xpath('@href')[0]
        cover = album.xpath('img/@src')[0]
        img_handle(album_url, title, cover, id)
    num += 1
    if int(num) > int(max):
        return
    new_url = "%s%s.html" % (init_url, num)
    # print(url, num, new_url)
    handle_all_page_album(new_url, max,album_tree, id, init_url=init_url, num=num)


def img_handle(url, title, cover ,id):
    img_tree = request_url(url)
    album_discription = img_tree.xpath("//div[@class='descriptionBox']/p")[0].text if len(img_tree.xpath("//div[@class='descriptionBox']/p"))>0 else ""
    cursor = connect.cursor()
    sql = "insert into girls_album(title,cover_img,description,girls_tag_id) values(%s,%s,%s,%s)"
    cursor.execute(sql, [title, cover, album_discription ,id])
    id = int(cursor.lastrowid)
    cursor.close()
    connect.commit()

    max = find_max_img_page(img_tree)
    handle_all_img(url,max, img_tree, id, url)


def find_max_img_page(img_tree):
    # 找到最大页数
    pages_list = img_tree.xpath("//div[@class='pages']/ul/li")
    max = 0
    if len(pages_list) > 1:
        max_page = pages_list[-2].xpath('a')[0]
        if max_page:
            max = int(re.match(r'\S+_(\d+).html', max_page).group(1))
    return max


def handle_all_img(url, max, img_tree,id,init_url, num=1):
    if init_url != url:
        img_tree = request_url(url)
    print(url,max)
    if int(num) <= int(max):
        img = img_tree.xpath("//div[@id='big-pic']/p/a/img")
        if len(img)>0:
            img_url = img[0].xpath("@src")
            if len(img_url)>0:
                # print(img_url)
                img_path = re.match(r'\S+/uploads/(\S+)',img_url[0]).group(1)
                cursor = connect.cursor()
                sql = "insert into girls_img( img_url,img_status, girls_album_id) values(%s,%s,%s)"
                cursor.execute(sql, [img_url[0],1, id])
                cursor.close()
                connect.commit()

        num += 1
        new_url = "%s_%s.html"%(re.match(r'(\S+).html',init_url).group(1), num)
        print(new_url)
        handle_all_img(new_url, max, img_tree, id, init_url, num)







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