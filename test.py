
import os,base64,re
import urllib,requests
from bs4 import BeautifulSoup
from tmp2 import novel_snapshot_get_page
from novel_reviews import novel_reviews_get_content


s = input('搜索字段： ')
# Unicode转码支持中文
s = urllib.parse.quote(s)
page = requests.get('http://saowen.net/novels/search?q=' + s)

#穿件临时文件存放原始网页，查错用
with open('test.html','wb') as raw_page:
    raw_page.write(page.content)

soup = BeautifulSoup(page.content,'lxml')

# HTML5的tag 包含 ‘——’ 需用attrs支持
novel_list = soup.find('div',id='novel-list').find_all(attrs={"data-novelid": True})

for hit in novel_list:
    novel_link=('{}{}'.format('http://saowen.net',hit.find('a',class_='novellink',novel_id=True)['href']))
    reviews_link = ('{}{}{}{}'.format('http://saowen.net/','readstatuses/novelReviews/',hit.find('a',class_='novellink')['novel_id'],'/sort:p_ratio/direction:DESC'))
    novel_snapshot = novel_snapshot_get_page(novel_link)
    if novel_snapshot == 302:
        pass
    else:
        for tag in hit.find_all(class_='tag-info'):
            print ('{}{}'.format(tag.text,' '))
        print('\n')
    novel_reviews = novel_reviews_get_content(reviews_link)


    