import newspaper
import time
import requests
import utils
import datetime
from bs4 import BeautifulSoup as bs4
from newspaper import Config
from newspaper import Article
from newspaper import fulltext
from newspaper import news_pool
from newspaper import Source
from newspaper import nlp
from newspaper import urls
from newspaper import languages
from newspaper import network
from newspaper import settings
from newspaper import mthreading
from newspaper import outputformatters
import queue
import threading
import json


q = queue.Queue()
q2 = queue.Queue()

def consumer2(session):
    while True:
        if q2.get == None:
            q2.task_done()
            return
        try:
            url = q2.get()
            print('get:', url)
            response = session.get(url=url, proxies=PROXIES, allow_redirects=False)
            soup = bs4(response.text, 'html.parser')
            #change url string into valid filename
            filename = "".join(i for i in url if i not in "\/:*?<>|") + '.html' 
            with open(f'./html/{filename}', 'wb') as f:
                f.write(soup.prettify().encode('utf-8'))
            with open(f'./html/index.txt', 'ab') as f:
                # write url into index.txt
                f.write(url.encode('utf-8'))
            q2.task_done()
        except Exception as e:
            print('error in downloader')
            print(e)
            continue
    
def get_all_links(html):
    soup = bs4(html, 'html.parser')
    # example = '\"/2019/04/23/tech/jack-dorsey-trump-twitter-meeting/index.html\"'
    #find year, month, day in example
    for link in soup.find_all('a'):
        link_string = link.get('href')
        yyyy = link_string[1:5]
        #check if yyyy is a valid year
        if not (yyyy.isdigit() and int(yyyy) in range(1980, 2031)):
            print(yyyy,'is not a valid year')
            continue
        mm = link_string[6:8]
        dd = link_string[9:11]
        title = link_string[link_string.find('tech/')+5:]
        template_news_url = f'https://www.cnn.com/{yyyy}/{mm}/{dd}/tech/'
        news_url = template_news_url+title
        print('page:', news_url)
        q2.put(news_url)



def producer(urlList, session):
    for url in urlList:
        try:
            date = url[-1:-9:-1][::-1]
            time.sleep(3)
            response = session.get(url=url, proxies=PROXIES)
            # result_item = json.loads(response.text).get('items')[0]
            result_item = json.loads(response.text).get('items')
            for item in result_item:
                if len(str(item[0]))==6 and item[1]=='200':
                    result = item
                    break
                else:
                    continue

            processed_url = utils.clean_url(item, date)
            q.put(processed_url)
        except Exception as e:
            print(e,'\n', url)
            continue
    
def consumer(session):
    while True:
        if q.get() == None:
            q.task_done()
            return
        # try:
        url = q.get()
        if not url:
            print('error in 77')
        print('get:', url)
        url_front = url[:url.find('cnn')]
        url_back1 = 'https://www.cnn.com/data/ocs/section/business/tech/index.html:tech-zone-2/views/zones/common/zone-manager.izl'
        url_back2 = 'https://www.cnn.com/data/ocs/section/business/tech/index.html:tech-zone-3/views/zones/common/zone-manager.izl'
        url_top_news = url_front+url_back1
        url_more_tech_news = url_front+url_back2
        time.sleep(3)
        print('get:', url_top_news)
        response = session.get(url = url_top_news, proxies=PROXIES, allow_redirects=True, timeout=100)
        time.sleep(3)
        response2 = session.get(url = url_more_tech_news, proxies=PROXIES, allow_redirects=True, timeout=100)
        # print(response.text)
        try:
            jsn = json.loads(response.text)
        except:
            time.sleep(3)
            soup1 = bs4(response.text, 'html.parser')
            #find iframe with id playback
            iframe = soup1.find('iframe', id='playback')
            #get src attribute of iframe
            src = iframe.get('src')
            response = session.get(url = src, proxies=PROXIES, allow_redirects=True)
            jsn = json.loads(response.text)

            print('here')
            filename = "".join(i for i in url_top_news if i not in "\/:*?<>|") + '.html'
            with open(f'./error/{filename}.html', 'wb') as f:
                f.write(response.text.encode('utf-8'))
        try:
            jsn2 = json.loads(response2.text)
        except:
            soup2 = bs4(response2.text, 'html.parser')
            #find iframe with id playback
            iframe2 = soup2.find('iframe', id='playback')
            #get src attribute of iframe
            src2 = iframe.get('src')
            response2 = session.get(url = src2, proxies=PROXIES, allow_redirects=True)
            jsn2 = json.loads(response2.text)
            print('here') 
            filename = "".join(i for i in url_more_tech_news if i not in "\/:*?<>|") + '.html'
            with open(f'./error/{filename}.html', 'wb') as f:
                f.write(response2.text.encode('utf-8'))

        html = jsn.get('html')
        html2 = jsn2.get('html')
        # print(html)
        get_all_links(html)
        get_all_links(html2)

        q.task_done()

config  = Config()
config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
PROXIES = {
    'http': '127.0.0.1:7890',
    'https': '127.0.0.1:7890',
}
config.proxies = PROXIES
config.request_timeout = 20


BASE_URL = 'https://web.archive.org/web/20190501000000*/cnn.com/business/tech'




session  = requests.Session()
session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
session.timeout = 20

session2 = requests.Session()
session2.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
session2.timeout = 10000

session3 = requests.Session()
session3.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
session3.timeout = 10000
# session.verify = False
response = session.get(url=BASE_URL, proxies=PROXIES)
template_url = 'https://web.archive.org/__wb/calendarcaptures/2?url=cnn.com%2Fbusiness%2Ftech&date='

date_str_list = utils.get_date_str_list(datetime.date(2020, 1, 1), datetime.date(2020, 12, 31))
base_url_list = [template_url+str(date) for date in date_str_list]
#split list into 4 slices
base_url_list_list = [base_url_list[i::4] for i in range(4)]

for i in range(4):
    c2 = threading.Thread(target=consumer2, args=(session3,))
    print('start web page downloader')
    c2.start()

for i in range(4):
    print('start producer')
    t = threading.Thread(target=producer, args=(base_url_list_list[i], session))
    time.sleep(4)
    t.start()

for i in range(2):
    c = threading.Thread(target=consumer, args=(session2,))
    print('start consumer')
    time.sleep(5)
    c.start()
# consumer(session2)


t.join()
print('t done')
for i in range(4):
    q.put(None)


c.join()
print('c done')
for i in range(4):
    q2.put(None)

c2.join()
print('done')






# cnn = newspaper.build('https://www.cnn.com', config=config)
# print(dir(cnn))
# with open('test.html', 'wb') as f:
#     f.write(soup.prettify().encode('utf-8'))