#coding=utf-8

import os
import urllib as request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import sys

class toutiao:

    def __init__(self):  # 构造函数
        pass

    def get_info(self):  # 输入爬取英雄名称、昵称或All
        x = input('请输入图片集url?')
        print('输入的内容为', x)
        return x

    def create_lolfile(self):  # 在当前目录下创建文件夹Toutiao
        fileRoot = '.\Toutiao'
        if not os.path.exists(fileRoot):
            os.makedirs(fileRoot)

    def request(self, url):  # 请求页面
        # 之前直接请求之后，根据find_all找不到图片，怀疑图片 是后期js生成class,所以使用phantomjs来渲染
        driver = webdriver.PhantomJS(
            executable_path=r'F:\soft\python\phantomjs-2.1.1-windows\bin\phantomjs')  # executable_path为PhantomJS的安装位置
        driver.get(url)
        time.sleep(1)  # 暂停执行1秒，确保页面加载出来

        # 使用BeautifulSoup获取网址页面内容
        pagesource = driver.page_source
        driver.close()
        soup = BeautifulSoup(pagesource, "lxml")

        return soup

    def getImageUrl(self, soup):  # 获取图片集合

        imagUrlList = []
        try:
            items = soup.find_all("div", attrs={"class": "image-item-inner"})

            for item in items:
                if item.find('a', attrs={"class": "image-origin"}):
                    # 方法一
                    # imageUrl = item.find('a', {"class": "image-origin"})['href']

                    # 方法二
                    imageUrl = item.find('a', {"class": "image-origin"}).get('href')

                    imagUrlList.append(imageUrl)
        except:
            return None
        return imagUrlList

    def get_image(self, imagUrlList, soup):  # 下载图片

        # 在当前目录下创建文件夹Toutiao
        packageName = '.\Toutiao' + '\\' + soup.title.text
        if not os.path.exists(packageName):
            os.makedirs(packageName)

        # 爬取多张壁纸
        imagelength = len(imagUrlList)

        for k in range(imagelength):
            # 生成一张壁纸的地址
            url = imagUrlList[k]
            # 爬取一张壁纸
            try:
                response = request.request.urlopen(url)
            except request.error.HTTPError as e:
                print('请求失败')
                print('错误代码: ', e.code)
                print(e.read().decode('utf-8'))
                print('图片第' + str(k) + '张壁纸爬取失败\n')
                break
            except request.error.URLError as e:
                print('服务器异常')
                print('错误原因: ', e.reason.decode('utf-8'))
                print('英雄第' + str(k) + '张壁纸爬取失败\n')
                break
            else:
                image = response.read()
                name = packageName + '\\' + '0' * (3 - len(str(k))) + str(k) + '.jpg'
                with open(name, 'wb') as f:
                    f.write(image)

        print('已爬取完毕\n')

    def set_image_url(self, imageUrls):
        inputcontent = self.get_info()  # 获得键盘输入信息

        if inputcontent.lower() == 'w':
            return imageUrls

        elif inputcontent.lower() == 'q':
            sys.exit()

        else: #匹配是否为网址
            pattern = re.compile(r'^(https?|ftp|file)://.+$')

            match = pattern.match(inputcontent)

            if match:
                imageUrls.append(inputcontent)

                print('w保存，q退出\n')

                return self.set_image_url(imageUrls)
            else:
                sys.exit()

    def run(self):

        self.create_lolfile()  # 创建文件夹

        #头条图片请求url
        # url = 'https://www.toutiao.com/a6508983959630643725'
        # url = 'https://www.toutiao.com/a6503660292721869326'
        # url = 'https://www.toutiao.com/a6517447853151879684'
        imageUrls = []
        imageUrls = self.set_image_url(imageUrls)

        imageUrllength = len(imageUrls)

        for k in range(imageUrllength):
            url = imageUrls[k]

            print('爬取url为：'+url+'图片集\n')

            soup = self.request(url)

            imageList = self.getImageUrl(soup)

            self.get_image(imageList, soup)


if __name__ == '__main__':
    getImage = toutiao()  # 创建对象

    getImage.run()  # 运行爬虫