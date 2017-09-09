import requests
import http.cookiejar
import re,time,os.path


# 登陆cookie信息
def login_session(log,pwd):
    agent = 'Mozilla/5.0 (Windows Nt 5.1;rv:33.0) Gecko/20100101 Firefox/33.0'
    headers = {
            'User-Agent': agent
    }

    session = requests.session()
    session.cookies = http.cookiejar.LWPCookieJar(filename = 'cookies')
    if not os.path.exists('cookies'):
        session.cookies.save()
    else:
        session.cookies.load(ignore_discard=True)

    post_url = 'http://saowen.net/users/login'
    postdata = {'data[User][email]': log,'data[User][password]': pwd,'data[User][remember]': 1}
    login_page = session.post(post_url, data=postdata,headers = headers)
    login_code = login_page.text
    #print(login_page)
    #print(login_code)
    session.cookies.save()
    return session,headers





