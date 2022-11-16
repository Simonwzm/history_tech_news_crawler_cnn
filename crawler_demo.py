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
def producer(urlList, session):
    for url in urlList:
        try:
            date = url[-1:-9:-1][::-1]
            time.sleep(0.5)
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
        if q.get == None:
            q.task_done()
            break
        try:
            url = q.get()
            response = session.get(url=url, proxies=PROXIES, allow_redirects=False)
            soup = bs4(response.text, 'html.parser')
            #change url string into valid filename
            filename = "".join(i for i in url if i not in "\/:*?<>|") + '.html' 
            with open(f'./html/{filename}', 'wb') as f:
                f.write(soup.prettify().encode('utf-8'))
            q.task_done()
        except Exception as e:
            print(e)
            continue

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
session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
session.timeout = 100
# session.verify = False
response = session.get(url=BASE_URL, proxies=PROXIES)
template_url = 'https://web.archive.org/__wb/calendarcaptures/2?url=cnn.com%2Fbusiness%2Ftech&date='

date_str_list = utils.get_date_str_list(datetime.date(2019, 1, 1), datetime.date(2019, 12, 31))
base_url_list = [template_url+str(date) for date in date_str_list]
#split list into 12 slices
base_url_list_list = [base_url_list[i:i+12] for i in range(0, len(base_url_list), 12)]
# print(base_url_list_list)

for i in range(12):
    t = threading.Thread(target=producer, args=(base_url_list_list[i], session))
    t.start()

# for i in range(4):
#     c = threading.Thread(target=consumer, args=(session2,))
#     c.start()

t.join()
for i in range(4):
    q.put(None)

# c.join()








# cnn = newspaper.build('https://www.cnn.com', config=config)
# print(dir(cnn))
# with open('test.html', 'wb') as f:
#     f.write(soup.prettify().encode('utf-8'))