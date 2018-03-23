#coding=utf-8

import urllib.request
import json
import os
import pandas as pd

response = urllib.request.urlopen("http://pvp.qq.com/web201605/js/herolist.json")

str_response = response.read().decode('utf-8')
hero_json = json.loads(str_response)

hero_num = len(hero_json)

# 文件夹不存在则创建
save_dir = '.\heroskin'
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

    # 转化皮肤列表并转为csv文件
    def get_heroframe():
        heroframe = pd.DataFrame(index=range(0, hero_num),
                                 columns=['ename', 'cname', 'title', 'hero_type', 'skin_name'])
        for i in range(hero_num):
            heroframe['ename'][i] = hero_json[i]['ename']
            heroframe['cname'][i] = hero_json[i]['cname']
            heroframe['title'][i] = hero_json[i]['title']
            heroframe['hero_type'][i] = hero_json[i]['hero_type']
            heroframe['skin_name'][i] = hero_json[i]['skin_name']

        heroframe.to_csv('./heroskin/herolist.csv', encoding='gbk', index=False)

        return heroframe

    # 获取英雄皮肤图片并下载
    def get_heroskin():
        for i in range(hero_num):
            # 获取英雄皮肤列表
            skin_names = hero_json[i]['skin_name'].split('|')

            for cnt in range(len(skin_names)):
                print('英雄 ' + str(hero_json[i]['cname']) + ' 壁纸开始爬取\n')
                skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/' + str(
                    hero_json[i]['ename']) + '/' + str(hero_json[i]['ename']) + '-bigskin-' + str(cnt + 1) + '.jpg'

                urllib.request.urlretrieve(skin_url, filehero)

                filehero = save_dir + '\\' + str(hero_json[i]['cname'])
                if not os.path.exists(filehero):
                    os.makedirs(filehero)
                try:
                    response = urllib.request.urlopen(skin_url)
                except urllib.error.HTTPError as e:
                    print('请求失败')
                    print('错误代码: ', e.code)
                    print(e.read().decode('utf-8'))

                    break
                except urllib.error.URLError as e:
                    print('服务器异常')
                    print('错误原因: ', e.reason.decode('utf-8'))

                    break
                else:
                    image = response.read()
                    imagename = filehero + '\\' + skin_names[cnt] + '.jpg'
                    with open(imagename, 'wb') as f:
                        f.write(image)

            # 完成该英雄的爬取
            print('英雄 ' + str(hero_json[i]['cname']) + ' 壁纸已爬取完毕\n')


if __name__ == '__main__':
    # 运行爬虫
    get_heroframe()

    get_heroskin()