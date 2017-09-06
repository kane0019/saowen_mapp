import os,base64,re
import urllib.parse,urllib.request
from bs4 import BeautifulSoup

def novel_page(novel_link):
    page = urllib.request.urlopen(novel_link).read()
    soup = BeautifulSoup(page,'lxml')
    title = soup.find('div',id='main').find('h1').text
    author = soup.find('a',author_id = True).text


    print('{}{}'.format("书名： ", title))
    print('{}{}'.format("作者： ", author))

    test = soup.find('div', id='novel-info',title='作品信息').find('ul').find('li')
    for i in range (9):
        print (test.text)
        test = test.find_next_sibling('li')

    test2 = soup.find('div', id='rate-info', title='评价信息')
    try:
        print ('{}{}'.format('星级： ',test2.find('span',class_='ratestar').text))
    except AttributeError:
        print ('{}{}'.format('星级： ','暂无评分'))
    except:
        print ('Something goes wrong')
    try:
        print ('{}{}'.format('平均分： ',test2.find('span',class_='ratenumber').text))
    except AttributeError:
        print ('{}{}'.format('平均分： ','暂无评分'))
    except:
        print ('Something goes wrong')
    try:
        print ('{}{}'.format('总评： ',test2.find('span',class_='ratedesc').text))
    except AttributeError:
        print ('{}{}'.format('总评： ','暂无评分'))
    except:
        print ('Something goes wrong')
    try: 
        print('{}{}'.format('首发: ',soup.find('a',target="_blank",class_ = "site-alias")['href']))
    except:
        print('首发：  暂无信息，姑娘你来添加吧。')

