#coding=utf-8

import os
import urllib.request as urlrequest
import urllib.error as urlliberror
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd


class LOL_scrawl:

    def __init__(self):  # 构造函数
        pass

    def get_info(self):  # 输入爬取英雄名称、昵称或All
        x = input('输入爬取英雄名称、昵称或All?')
        print('输入的内容为', x)
        return x

    def create_lolfile(self):  # 在当前目录下创建文件夹LOL
        filehero = '.\LOL'
        if not os.path.exists(filehero):
            os.makedirs(filehero)

    def get_heroframe(self):  # 获取官网上所有英雄信息
        # 获取英雄英文名及id，生成字典herodict{Englishname:id}
        content = urlrequest.urlopen('http://lol.qq.com/biz/hero/champion.js').read()
        str1 = r'champion={"keys":'
        str2 = r',"data":{"Aatrox":'
        champion = str(content).split(str1)[1].split(str2)[0]
        herodict0 = eval(champion)
        herodict = dict((k, v) for v, k in herodict0.items())  # 字典中的key和value互换
        print(herodict)

        # 英雄联盟官网上所有英雄所在的网址
        url_Allhero = 'http://lol.qq.com/web201310/info-heros.shtml#Navi'

        # 使用无头浏览器PhantomJS打开网址，解决JavaScript动态加载问题
        driver = webdriver.PhantomJS(
            executable_path=r'F:\soft\python\phantomjs-2.1.1-windows\bin\phantomjs')  # executable_path为PhantomJS的安装位置
        driver.get(url_Allhero)
        time.sleep(1)  # 暂停执行1秒，确保页面加载出来

        # 使用BeautifulSoup获取网址页面内容
        pageSource = driver.page_source
        driver.close()
        bsObj = BeautifulSoup(pageSource, "lxml")

        # 使用BeautifulSoup解析页面内容，得到英雄信息表heroframe
        herolist = bsObj.findAll('ul', {'class': 'imgtextlist'})
        for hero in herolist:
            n = len(hero)
            m = 0
            heroframe = pd.DataFrame(index=range(0, n),
                                     columns=['herolink', 'heronickname', 'heroname', 'Englishname', 'heroid'])
            heroinflist = hero.findAll('a')  # 抽取该英雄信息的超链接部分
            for heroinf in heroinflist:  # 对于英雄信息的超链接部分
                herolink = heroinf['href']
                heronickname = heroinf['title'].split(' ')[0].strip()
                heroname = heroinf['title'].split(' ')[1].strip()
                heroframe['herolink'][m] = herolink
                heroframe['heronickname'][m] = heronickname
                heroframe['heroname'][m] = heroname
                heroframe['Englishname'][m] = heroframe['herolink'][m][21:]
                heroframe['heroid'][m] = herodict[heroframe['Englishname'][m]]

                m = m + 1

        heroframe.to_csv('./LOL/heroframe.csv', encoding='gbk', index=False)

        return heroframe


    def get_image(self, heroid, heroframe):  # 爬取英雄信息
        # 创建存放该英雄壁纸的文件夹
        line = heroframe[heroframe.heroid == heroid].index.tolist()  # 找到所查英雄在dataframe中所在的行
        nickname = heroframe['heronickname'][line].values
        name = heroframe['heroname'][line].values
        englishname = heroframe['Englishname'][line].values
        nickname_name = str((nickname + ' ' + name)[0][:])
        filehero = '.\LOL' + '\\' + nickname_name
        if not os.path.exists(filehero):
            os.makedirs(filehero)

        # 方法一
        # 爬取多张壁纸
        for k in range(21):
            # 生成一张壁纸的地址
            url = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big' + str(heroid) + '0' * (
                    3 - len(str(k))) + str(k) + '.jpg'
            # 爬取一张壁纸
            try:
                response = urlrequest.urlopen(url)
            except urlliberror.HTTPError as e:
                print('请求失败')
                print('错误代码: ', e.code)
                print(e.read().decode('utf-8'))
                print('英雄 ' + nickname_name + ' 第' + str(k) + '张壁纸爬取失败\n')
                break
            except urlliberror.URLError as e:
                print('服务器异常')
                print('错误原因: ', e.reason.decode('utf-8'))
                print('英雄 ' + nickname_name + ' 第' + str(k) + '张壁纸爬取失败\n')
                break
            else:
                image = response.read()
                imagename = filehero + '\\' + '0' * (3 - len(str(k))) + str(k) + '.jpg'
                with open(imagename, 'wb') as f:
                    f.write(image)

        # 完成该英雄的爬取
        print('英雄 ' + nickname_name + ' 壁纸已爬取完毕\n')



    def run(self):

        self.create_lolfile()  # 创建LOL文件夹

        heroframe = self.get_heroframe()  # 获得所有英雄信息
        print('已获取英雄信息存于heroframe.csv,马上开始爬取壁纸...\n')

        # inputcontent = self.get_info()  # 获得键盘输入信息

        inputcontent = 'all'

        if inputcontent.lower() == 'all':  # 当输入all时，爬取全部英雄壁纸
            try:
                allline = len(heroframe)
                for i in range(1, allline):
                    heroid = heroframe['heroid'][[i]].values[:][0]
                    self.get_image(heroid, heroframe)
                print('完成全部爬取任务！\n')
            except:
                print('爬取失败或部分失败，请检查错误')

        else:  # 否则爬取单个英雄壁纸
            try:
                hero = inputcontent.strip()
                line = heroframe[(heroframe.heronickname == hero) | (
                        heroframe.heroname == hero)].index.tolist()  # 找到所查英雄在dataframe中所在的行
                heroid = heroframe['heroid'][line].values[:][0]  # 得到英雄id
                self.get_image(heroid, heroframe)
                print('完成全部爬取任务！\n')
            except:
                print('错误！请按照提示正确输入！\n')


if __name__ == '__main__':
    lolscr = LOL_scrawl()  # 创建对象

    lolscr.run()  # 运行爬虫