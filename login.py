import requests
import http.cookiejar
import re,time,os.path


# 登陆cookie信息
def login_session(log,pwd):
    agent = 'Mozilla/5.0 (Windows Nt 5.1;rv:33.0) Gecko/20100101 Firefox/33.0'
    headers = {
            'User-Agent': agent
    }
    try:
        session = requests.session()
        session.cookies = http.cookiejar.LWPCookieJar(filename = 'cookies')
        if not os.path.exists('cookies'):
            session.cookies.save()
        else:
            try:
                session.cookies.load(ignore_discard=True)
            except:
                raise
        post_url = 'http://saowen.net/users/login'
        postdata = {'data[User][email]': log,'data[User][password]': pwd,'data[User][remember]': 0,'data[User][remember]': 1}
        login_page = session.post(post_url, data=postdata,headers = headers)
        login_code = login_page.status_code
        #print(login_page)
        #print(login_code)
        session.cookies.save()
        return login_code,session,headers
    except:
        raise





