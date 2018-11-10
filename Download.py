#-*- coding=utf8 -*-
import random
import re
import time
import requests
from lxml import html



class download(object):
    '''
    下载器
    '''
    def __init__(self):
        '''初始化proxy和ua'''

        #代理池
        self.proxy_list = [
            '163.125.16.103:8888',
            '163.125.16.103:8888',
            '119.29.177.120:1080',
            '119.29.177.120:1080',
            '218.204.204.90:8118',
            '119.123.177.52:9000',
            '183.237.206.92:53281',
            '113.105.203.106:3128',
            '183.237.206.92:53281',
            '113.105.203.106:3128',
            '222.125.215.89:80',
            '113.105.200.164:3128',
            '222.125.215.89:80',
            '113.105.200.164:3128',
            '163.125.68.21:9999',
            '163.125.68.21:9999',
            '163.125.30.249:8118',
            '211.154.132.85:8888',
            '163.125.30.249:8118',
            '211.154.132.85:8888',
            '113.105.203.197:3128',
            '113.105.203.197:3128',
            '119.28.226.136:8118',
            '119.28.118.116:1080',
            '119.28.226.136:8118',
            '119.28.118.116:1080',
            '163.125.16.103:8888',
            '113.105.201.10:3128',
            '163.125.16.103:8888',
            '113.105.201.10:3128',
            '27.40.140.175:1080',
            '163.125.30.242:8118',
            '163.125.30.242:8118'
        ]

        #ua池
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        #目标地址测试

    def get(self, url, timeout, proxy=None, num_retries=6):  ##给函数一个默认参数proxy为空
        '''
        获取get请求
        :return:
        '''
        UA = random.choice(self.user_agent_list)
        headers = {
            "User-Agent": UA,
            "Referer": "http://www.mmonly.cc/tag/"
        }
        if proxy == None: ##当代理为空时，不使用代理获取response（别忘了response啥哦！之前说过了！！）
            try:
                response = requests.get(url, headers=headers, timeout=timeout)##这样服务器就会以为我们是真的浏览器了
                if response.status_code == 200:
                    return response
                else:
                    IP = ''.join(str(random.choice(self.proxy_list)).strip()) ##下面有解释哦
                    proxy = {'http': IP}
                    return self.get(url, timeout, proxy,)
            except:##如过上面的代码执行报错则执行下面的代码

                if num_retries > 0: ##num_retries是我们限定的重试次数
                    time.sleep(10) ##延迟十秒
                    print(u'获取网页出错，10S后将获取倒数第：', num_retries, u'次')
                    return self.get(url, timeout, num_retries-1)  ##调用自身 并将次数减1
                else:
                    print(u'开始使用代理')
                    time.sleep(10)
                    IP = 'http://%s'%str(random.choice(self.proxy_list)).strip() ##下面有解释哦
                    proxy = {'http': IP}
                    return self.get(url, timeout, proxy,) ##代理不为空的时候

        else: ##当代理不为空
            try:
                IP = 'http://%s'%str(random.choice(self.proxy_list)).strip() ##将从self.iplist中获取的字符串处理成我们需要的格式（处理了些什么自己看哦，这是基础呢）
                proxy = {'http': IP} ##构造成一个代理
                response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
                if response.status_code == 200:
                    return response
                else:
                    if num_retries > 0:
                        time.sleep(10)
                        IP = 'http://%s'%str(random.choice(self.proxy_list)).strip()
                        proxy = {'http': IP}
                        print(u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
                        print(u'当前代理是：', proxy)
                        return self.get(url, timeout, proxy, num_retries - 1)
                    else:
                        print(u'代理也不好使了！取消代理')
                        return self.get(url, 3)
            except:

                if num_retries > 0:
                    time.sleep(10)
                    IP = 'http://%s'%str(random.choice(self.proxy_list)).strip()
                    proxy = {'http': IP}
                    print(u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
                    print(u'当前代理是：', proxy)
                    return self.get(url, timeout, proxy, num_retries - 1)
                else:
                    print(u'代理也不好使了！取消代理')
                    return self.get(url, 3)



request = download()