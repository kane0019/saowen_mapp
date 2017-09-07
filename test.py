
import os,base64,re
import urllib,requests
from bs4 import BeautifulSoup
import tmp2


s = input('搜索字段： ')
# Unicode转码支持中文
s = urllib.parse.quote(s)
page = requests.get('http://saowen.net/novels/search?q=' + s)

#穿件临时文件存放原始网页，查错用
with open('test.html','wb') as raw_page:
    raw_page.write(page.content)

soup = BeautifulSoup(page.content,'lxml')

# HTML5的tag 包含 ‘——’ 需用attrs支持
output = soup.find_all(attrs={"data-novelid": True})
for hit in output:
    
    novel_link=('{}{}'.format('http://saowen.net/',hit.find('a',class_='novellink')['href']))
    novel_snapshot = tmp2.novel_page(novel_link)
    if novel_snapshot == 302:
        pass
    else:
        for tag in hit.find_all(class_='tag-info'):
            print ('{}{}'.format(tag.text,' '))
        print('\n')
    