import newspaper
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
session.verify = False
response = session.get(url=BASE_URL, proxies=PROXIES)
template_url = 'https://web.archive.org/__wb/calendarcaptures/2?url=cnn.com%2Fbusiness%2Ftech&date='

date_str_list = utils.get_date_str_list(datetime.date(2019, 1, 1), datetime.date(2019, 12, 31))
base_url_list = [template_url+str(date) for date in date_str_list]



# cnn = newspaper.build('https://www.cnn.com', config=config)
# print(dir(cnn))
# with open('test.html', 'wb') as f:
#     f.write(soup.prettify().encode('utf-8'))