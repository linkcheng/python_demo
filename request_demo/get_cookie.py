import os
import sqlite3
import cookielib
import Cookie
import urllib2

def build_opener_with_chrome_cookies():
    cookie_file_path = os.path.join(r'/home/zhenglong', r'.config/chromium/Default/Cookies')
    if not os.path.exists(cookie_file_path):
        raise Exception('Cookies file not exist!')
    conn = sqlite3.connect(cookie_file_path)
    sql = 'select * from cookies'
        
    cookiejar = cookielib.CookieJar()    # No cookies stored yet

    for row in conn.execute(sql):
        cookie_item = cookielib.Cookie(
            version=0, name=row[2], value=row[3],
                     port=None, port_specified=None,
                     domain=row[1], domain_specified=None, domain_initial_dot=None,
                     path=row[4], path_specified=None,
                     secure=None,
                     expires=None,
                     discard=None,
                     comment=None,
                     comment_url=None,
                     rest=None)
        print cookie_item
        cookiejar.set_cookie(cookie_item)    # Apply each cookie_item to cookiejar
    conn.close()

if __name__ == '__main__':
    build_opener_with_chrome_cookies()

