import os,base64,re
from bs4 import BeautifulSoup

def novel_reviews_get_content(reviews_link,session,headers):
    white_space = '         '
    page = session.get(reviews_link,headers=headers,)
    soup = BeautifulSoup(page.content,'lxml')
    reviews_list = soup.find_all('div', class_='statusitem')
    review_count = 0
    for reviews in reviews_list:
        review_info_user = reviews.find('a',user_id=True).text
        review_info_review = reviews.find('blockquote')
        review_info_review_contents = review_info_review.find_all('p')
        review_info_pos_count = review_info_review.find('a',class_='vote pos')['votecount']
        review_info_neg_count = review_info_review.find('a',class_='vote neg')['votecount']
        review_output = []
        for reviews_section in review_info_review_contents:
            review_output.append(reviews_section.text)
        print ('{}{}{}{}{}{}{}{}'.format(review_info_user,white_space,white_space,'有用：',review_info_pos_count,white_space,'没用：',review_info_neg_count))
        print (''.join(review_output))
        print('\n')
        review_count += 1
        if review_count == 3:
            break
