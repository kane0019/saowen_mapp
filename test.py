
import os,base64,re
import urllib.parse,urllib.request
from bs4 import BeautifulSoup
import tmp2


s = '七茭白'
s = urllib.parse.quote(s)
page = urllib.request.urlopen('http://saowen.net/novels/search?q=' + s).read()
soup = BeautifulSoup(page,'lxml')

for hit in soup.find_all(attrs={"data-novelid": True}):
    
    novel_link=('{}{}'.format('http://saowen.net/',hit.find('a',class_='novellink')['href']))
    tmp2.novel_page(novel_link)
    for tag in hit.find_all(class_='tag-info'):
        print ('{}{}'.format(tag.text,' '))
    print('\n')
    '''
    print('{}{}'.format(hit.find(novel_id=True).text,'\n'))
    print('{}{}'.format(hit.find(class_='rate-info').text,'\n'))
    print('{}{}'.format(hit.find(class_='extend-info').text,'\n'))
    print('\n')
    '''