import os,base64,re,json
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

def novel_snapshot_get_page(novel_link,session,headers,novel_id):

        page = session.get(novel_link,headers=headers,allow_redirects=False)
        # 页面不存在被重定向时不执行搜索
        if page.status_code == 302:
            return 302
        else:
            try:
                soup = BeautifulSoup(page.content,'lxml')
            except AttributeError:
                return ('not_find')
            title = soup.find('div',id='main').find('h1').text
            author = soup.find('a',author_id = True).text
            print(('{}{}'.format("书名： ", title))+'       '+('{}{}'.format("作者： ", author)))

            novel_info = soup.find('div', id='novel-info',title='作品信息').find('ul').find('li')
            novel_info_p1 = []
            novel_info_p2 = []
            for i in range (9):
                if i <= 5:
                    novel_info_p1.append(novel_info.text)
                    novel_info = novel_info.find_next_sibling('li')
                else:
                    novel_info_p2.append(novel_info.text)
                    novel_info = novel_info.find_next_sibling('li')
            novel_info_output_p1 = ('  '.join(novel_info_p1))
            novel_info_output_p2 = ('  '.join(novel_info_p2))

            print (novel_info_output_p1)
            print (novel_info_output_p2)

            rate_info = soup.find('div', id='rate-info', title='评价信息')
            try:
                star_info = rate_info.find('span',class_='ratestar').text
                print ('{}{}'.format('星级： ',star_info))
            except AttributeError:
                star_info = '暂无评分'
                print ('{}{}'.format('星级： ',star_info))
            try:
                ave_info = rate_info.find('span',class_='ratenumber').text
                print ('{}{}'.format('平均分： ',ave_info))
            except AttributeError:
                ave_info = '暂无评分'
                print ('{}{}'.format('平均分： ',ave_info))
            try:
                sum_info = rate_info.find('span',class_='ratedesc').text
                print ('{}{}'.format('总评： ',sum_info))
            except AttributeError:
                sum_info = '暂无评分'
                print ('{}{}'.format('总评： ',sum_info))
            try:
                tags = soup.find('div',id='noveltags').find_all('span',class_='noveltag')
                tag_list=[]
                for tag in tags:
                    tag_list.append(tag.text)
                '''
                    tag_text = tag.find('a').text
                    tag_count = tag.text
                    print ('{}{}'.format(tag_text,tag_count))
                    tag_text_list.append(tag_text)
                    tag_count_list.append(tag_count)
                '''
            except AttributeError:
                    tag_list =[]
                    print ('暂无标签')

            '''
            try: 
                print('{}{}'.format('首发: ',soup.find('a',target="_blank",class_ = "site-alias")['href']))
            except:
                print('首发：  暂无信息，姑娘你来添加吧。')
            '''
        return ({'title':title,'author':author,'novel_info_p1':novel_info_output_p1, 'novel_info_p2':novel_info_output_p2,'star':star_info,'ave':ave_info,'sum':sum_info,'novel_id':novel_id,'tags':tag_list})

#novel_snapshot__get_page('http://saowen.net/novels/view/42867')