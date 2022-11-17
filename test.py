import requests
from bs4 import BeautifulSoup as bs4
proxies = {
    'http':'127.0.0.1:7890',
    'https':'127.0.0.1:7890',
}

session = requests.Session()
session.proxies = proxies
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
session.headers = headers

response = requests.get('https://web.archive.org/web/20190118142341/https://www.cnn.com/data/ocs/section/business/tech/index.html:tech-zone-2/views/zones/common/zone-manager.izl', proxies=proxies, timeout=20, verify=False, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'})
soup = bs4(response.text, 'html.parser')
with open('test.html', 'wb') as f:
    f.write(soup.prettify().encode('utf-8'))