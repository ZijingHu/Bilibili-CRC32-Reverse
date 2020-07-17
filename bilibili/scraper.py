import getpass
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from fake_headers import Headers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

COOKIES = None
HEADERS = None
false = False
true = True
null = None

def login():
    uname = getpass.getpass('Username: ')
    upsw = getpass.getpass('Password: ')

    driver = webdriver.Chrome()
    driver.get('https://passport.bilibili.com/login')
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'login-username'))
    )
    driver.find_element_by_id('login-username').send_keys(uname)
    driver.find_element_by_id('login-passwd').send_keys(upsw)
    driver.find_element_by_class_name('btn.btn-login').click()

    input('Press ENTER if logging in successfully.')

    global COOKIES
    global HEADERS
    COOKIES = {c['name']: c['value'] for c in driver.get_cookies()}
    HEADERS = {'referer': 'https://passport.bilibili.com/login',
            'user-agent': Headers().generate()['User-Agent']}

def get(url):
    return requests.get(url, headers=HEADERS, cookies=COOKIES)
    
def get_cookies_n_headers():
    return COOKIES, HEADERS

def get_cid_via_bv(bv):
    url = f'https://api.bilibili.com/x/player/pagelist?bvid={bv}'
    resp = eval(requests.get(url).content.decode('utf-8'))
    return resp['data'][0]['cid']
    
def get_danmaku_page(cid, date, check=True):
    month = date[:-3]
    url_head = 'http://api.bilibili.com/x/v2/dm/'
    if check:
        url_check = f'history/index?type=1&oid={cid}&month={month}'
        resp_check = get(url_head+url_check)
        result_check = eval(resp_check.content.decode('utf-8'))
        date_list = result_check['data']
        if date not in date_list:
            return None

    url_search = f'history?type=1&oid={cid}&date={date}'
    resp_search = get(url_head+url_search)
    page = resp_search.content.decode('utf-8')
    return page

def parse_danmaku_page(page):
    table = list(map(
        lambda x: x.attrib['p'].split(',') + [x.text],
        ET.fromstring(page).findall('d')
    ))
    df = pd.DataFrame(table, columns=[
        'AppearTime', 'DmType', 'FontSize', 'FontColor', 
        'SendTime', 'DmAd', 'Sender', 'RowID', 'DmContent'
    ])
    return df[['Sender', 'DmContent', 'AppearTime', 
                'SendTime', 'FontColor', 'DmType']]

def get_danmaku(cid, date, check=True):
    page = get_danmaku_page(cid, date, check=True)
    danmaku = parse_danmaku_page(page)
    return danmaku

def get_following(uid):
    following = []
    header = 'https://api.bilibili.com/x/relation/'
    user_api = header + f'stat?vmid={uid}'
    user_info = eval(requests.get(user_api).content.decode('utf-8'))
    following_n = int(user_info['data']['following'])
    if following_n == 0: 
        return following
    
    page_n = min(5, following_n // 50 + 1)
    for i in range(page_n):
        following_api = header + f'followings?vmid={uid}&pn={i+1}&ps=50&jsonp=jsonp'
        resp = requests.get(following_api, cookies=COOKIES, headers=HEADERS)
        pn = eval(resp.content.decode('utf-8'))['data']['list']
        uid_list = list(map(lambda x: x['mid'], pn))
        following += uid_list
    return following

def get_pub(uid, field='typeid'):
    # field: comment, typeid, play, pic, subtitle, description, length, 
    #        copyright, title, review, author, mid, created, is_pay, 
    #        video_review, aid, bvid, hide_click, is_union_video,
    p = 1
    v_list = []
    pub_api = 'https://api.bilibili.com/x/space/arc/search?'
    resp = requests.get(pub_api+f'mid={uid}&ps=100&pn={p}')
    page = eval(resp.content.decode('utf-8'))
    v_list += [i[field] for i in page['data']['list']['vlist']]
    vn = sum([i['count'] for i in page['data']['list']['tlist'].values()])
    pn = vn // 100 + 1
    if p < pn:
        p += 1
        resp = requests.get(pub_api+f'mid={uid}&ps=100&pn={p}')
        page = eval(resp.content.decode('utf-8'))
        v_list += [i[field] for i in page['data']['list']['vlist']]
    return v_list