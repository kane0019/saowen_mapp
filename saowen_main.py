import os,requests,base64,re


'''
# Check current working directory.
retval = os.getcwd()
print ("{}{}".format("Current working directory", retval))

# Now change the directory
os.chdir("/Users/kaihu/Downloads")

# Check current working directory.
retval = os.getcwd()

print ("{}{}".format("Directory changed successfully", retval))

'''

page = requests.get('http://saowen.net/novels/view/17450',auth = None)

with open('test.html','w') as raw_page:
    raw_page.write(page.content)

with open('test.html','r') as content_source:
    source_code = content_source.read()
    novel_name = re.findall('name="keywords" content="(.*?),',source_code)
    rate_star = re.findall('<span class="rate">平均分： <span class="ratestar">(.*?)</span>',source_code)
    rate_number = re.findall('"ratenumber">(.*?)<',source_code)
    rate_descption = re.findall('"ratedesc">(.*?)<',source_code)
    extra_info = re.findall('副标题/别名 : </small>(.*?)>发表地址',source_code)

   # <li><small>副标题/别名 : </small>无</li><li><small>类型 : </small>耽美</li><li><small>原创性 : </small>原创</li><li><small>进度 : </small>坑</li><li><small>发表时间 : </small>2015</li><li><small>完结时间 : </small>2016</li><li><small>篇幅 : </small>中长</li><li><small>人物 : </small>白明起, 薄紫</li><li><small>口味 : </small>普通</li><li><small>发表地址 : </small><a href="http://www.jjwxc.net/onebook.php?novelid=2438709" target="_blank" class="site-alias">[首发]晋江主站</a>；<span class="site-alias" target="_blank">长佩[tid=21023]</span>；<span class="site-alias" target="_blank">长佩[tid=30667]</span></li><li><small>出版情况 : </small>未知</li>        </ul>

    print(novel_name)
    print(rate_star)
    print(rate_number)
    print(rate_descption)
    print(extra_info)
'''
with open('output.txt','w') as create_link_list:
        create_link_list.write("小说名"+novel_name+"\n")
        create_link_list.write("星级"+rate_star+"\n")
        create_link_list.write("平均分"+rate_number+"\n")
        create_link_list.write("评价"+rate_descption+"\n")
'''


