import requests
from threading import Thread
import re
import time
import hashlib
import os

class BaiDu:
    """
    爬取百度图片
    """
    def __init__(self, name, page, path):
        self.start_time = time.time()
        self.name = name
        self.page = page
        #self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&rn=60&'
        self.url = 'https://image.baidu.com/search/acjson'
        self.header = {}# 添加为自己的
        self.num = 0
        self.path = path

    def queryset(self):
        """
        将字符串转换为查询字符串形式
        """
        pn = 0
        for i in range(int(self.page)):
            pn += 60 * i
            name = {'word': self.name, 'pn': pn, 'tn':'resultjson_com', 'ipn':'rj', 'rn':60}
            url = self.url
            self.getrequest(url, name)

    def getrequest(self, url, data):
        """
        发送请求
        """
        print('[INFO]: 开始发送请求：' + url)
        ret = requests.get(url, headers=self.header, params=data)

        if str(ret.status_code) == '200':
            print('[INFO]: request 200 ok :' + ret.url)
        else:
            print('[INFO]: request {}, {}'.format(ret.status_code, ret.url))

        response = ret.content.decode()
        img_links = re.findall(r'thumbURL.*?\.jpg', response)
        links = []
        # 提取url
        for link in img_links:

            links.append(link[11:])

        self.thread(links)

    def saveimage(self, link):
        """
        保存图片
        """
        print('[INFO]:正在保存图片：' + link)
        m = hashlib.md5()
        m.update(link.encode())
        name = m.hexdigest()
        ret = requests.get(link, headers = self.header)
        image_content = ret.content
        if not os.path.exists(self.path + self.name):
            os.mkdir(self.path + self.name ) 
        filename = self.path + self.name + '/'  + name + '.jpg'
        with open(filename, 'wb') as f:
            f.write(image_content)
        print('[INFO]:保存成功，图片名为：{}.jpg'.format(name))

    def thread(self, links):
        """多线程"""
        self.num +=1
        for i, link in enumerate(links):
            print('*'*50)
            print(link)
            print('*' * 50)
            if link:
                # time.sleep(0.5)
                t = Thread(target=self.saveimage, args=(link,))
                t.start()
                # t.join()
            self.num += 1
        print('一共进行了{}次请求'.format(self.num))

    def __del__(self):

        end_time = time.time()
        print('一共花费时间:{}(单位秒)'.format(end_time - self.start_time))

def main():
    # names = ['冰雹', '降雪', '降雨', '结冰', '露', '霜', '雾霾', '雾凇', '雨凇']
    # for name in names:
    name = '露水'
    page = 100
    baidu = BaiDu(name, page, '/Users/pu/Desktop/')
    baidu.queryset()


if __name__ == '__main__':


    main()