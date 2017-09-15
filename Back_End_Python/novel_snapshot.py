import os,base64,re
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

def novel_snapshot_get_page(novel_link,session,headers):

        page = session.get(novel_link,headers=headers,allow_redirects=False)
        # 页面不存在被重定向时不执行搜索
        if page.status_code == 302:
            return 302
        else:
            soup = BeautifulSoup(page.content,'lxml')
            title = soup.find('div',id='main').find('h1').text
            author = soup.find('a',author_id = True).text
            print(('{}{}'.format("书名： ", title))+'       '+('{}{}'.format("作者： ", author)))

            novel_info = soup.find('div', id='novel-info',title='作品信息').find('ul').find('li')
            novel_info_output = []
            for i in range (9):
                novel_info_output.append(novel_info.text)
                novel_info = novel_info.find_next_sibling('li')
            print ('  '.join(novel_info_output))

            rate_info = soup.find('div', id='rate-info', title='评价信息')
            try:
                print ('{}{}'.format('星级： ',rate_info.find('span',class_='ratestar').text))
            except AttributeError:
                print ('{}{}'.format('星级： ','暂无评分'))
            try:
                print ('{}{}'.format('平均分： ',rate_info.find('span',class_='ratenumber').text))
            except AttributeError:
                print ('{}{}'.format('平均分： ','暂无评分'))
            except:
                print ('Something goes wrong')
            try:
                print ('{}{}'.format('总评： ',rate_info.find('span',class_='ratedesc').text))
            except AttributeError:
                print ('{}{}'.format('总评： ','暂无评分'))
            '''
            try: 
                print('{}{}'.format('首发: ',soup.find('a',target="_blank",class_ = "site-alias")['href']))
            except:
                print('首发：  暂无信息，姑娘你来添加吧。')
            '''
# novel_snapshot('http://saowen.net/novels/view/42867')