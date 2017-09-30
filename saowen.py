
import os,base64,re
import urllib,requests
from bs4 import BeautifulSoup
from novel_snapshot import novel_snapshot_get_page
from novel_reviews import novel_reviews_get_content
from requests.auth import HTTPBasicAuth
from login import login_session

def saowen_main(session,headers):
    hostdoamin = 'http://saowen.net'
    # login_code,session,headers = login_session('ad000913@hotmail.com','Kane0019')
    t = input('搜索类型： 正文／标签 \n')
    s = input('搜索字段： ')
    # Unicode转码支持中文
    s = urllib.parse.quote(s)
    if t == '正文':
        page = session.get('http://saowen.net/novels/search?q=' + s,headers=headers,allow_redirects=True)
        # Redirection Check
        if page.history:
            print ("Request was redirected")
        for resp in page.history:
            print (resp.status_code, resp.url)
            print ("Final destination:")
            print (page.status_code, page.url)
        else:
            print ("Request was not redirected")
        print (1)
    else:
        page = session.get('http://saowen.net/noveltags/search?search=' + s,headers=headers,allow_redirects=True)
        # Redirection Check
        if page.history:
            print ("Request was redirected")
        for resp in page.history:
            print (resp.status_code, resp.url)
            print ("Final destination:")
            print (page.status_code, page.url)
        else:
            print ("Request was not redirected")
        print (2)
    #临时文件存放原始网页，查错用
    with open('test.html','wb') as raw_page:
        raw_page.write(page.content)

    #override = input('Override url: \n')

    # override搜索，测试用
    #if override != '':
    #   page = session.get (override,headers=headers,allow_redirects=True)
    #else:
    #    pass

    soup = BeautifulSoup(page.content,'lxml')

    # HTML5的tag 包含 ‘——’ 需用attrs支持
    novel_list = soup.find('div',id='novel-list').find_all(attrs={'data-novelid': True})
    novel_record_list = []
    novel_reviews_list = []
    for hit in novel_list:
        novel_link=('{}{}'.format(hostdoamin,hit.find('a',class_='novellink',novel_id=True)['href']))
        novel_id=hit['data-novelid']
        # reviews_link = ('{}{}{}{}'.format(hostdoamin,'/readstatuses/novelReviews/',hit.find('a',class_='novellink')['novel_id'],'/sort:p_ratio/direction:DESC'))
        novel_snapshot = novel_snapshot_get_page(novel_link,session,headers,novel_id)
        novel_record_list.append(novel_snapshot)
        if novel_snapshot == 302:
            pass
        else:
            for tag in hit.find_all(class_='tag-info'):
                print ('{}{}'.format(tag.text,' '))
            print('\n')
        # novel_reviews = novel_reviews_get_content(reviews_link,session,headers)

    list_page_raw = soup.find('div',id='pages',class_='clear')
    list_length = len(list_page_raw.find_all('span'))
    if list_length == 0:
        print('仅有一页')
    else:
        length_adjust = 1
        previous_page = list_page_raw.find('span',class_='prev')
        next_page = list_page_raw.find('span',class_='next')
        if previous_page != None:
            length_adjust += 1
        current_page = list_page_raw.find('span',class_='current').text
        total_pages = list_length - length_adjust
        print('{}{}{}{}'.format('当前页  ',current_page,'/',total_pages))
        try:
            previous_page_link = previous_page.find('a',href=True)['href']
        except AttributeError:
            previous_page_link = None
        try:
            next_page_link = next_page.find('a',href=True)['href']
        except AttributeError:
            next_page_link = None
        print(previous_page_link)
        print(next_page_link)
    return novel_record_list
        # 返回前一页地址 
        #print('返回前一页'+'   '+('{}{}'.format(hostdoamin,previous_page['href']))）
        # 返回后一页地址
        #print('前往后一页'+'   '+('{}{}'.format(hostdoamin,list_page_raw.find('span',class_='next')['href']))）
        # 返回制定页地址




    