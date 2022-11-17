import newspaper
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
import os

# find all file in html folder
html_files = os.listdir('./html_copy')
# create a list to store all html file path
html_file_paths = []
for file in html_files:
    html_file_paths.append(file)


config  = Config()
config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
PROXIES = {
    'http': '127.0.0.1:7890',
    'https': '127.0.0.1:7890',
}
config.proxies = PROXIES
config.request_timeout = 20

# create a list to store all article
articles = []
# create a list to store all article text
article_texts = []
# create a list to store all article title
article_titles = []
# create a list to store all article url
article_urls = []
# create a list to store all article publish date
article_publish_dates = []
# create a list to store all article authors
article_authors = []
# create a list to store all article keywords
article_keywords = []
# create a list to store all article summary
article_summaries = []
# create a list to store all article top image
article_top_images = []

for file in html_file_paths:
    # create a article object
    file = 'https://www.cnn.com/2019/12/23/tech/apple-tech-history/index.html'
    article = Article(url = file, config = config)
    # download html
    article.download()
    # parse html
    article.parse()
    # append article to articles list
    articles.append(article)
    # append article text to article_texts list
    article_texts.append(article.text)
    # append article title to article_titles list
    article_titles.append(article.title)
    # append article url to article_urls list
    article_urls.append(article.url)
    # append article publish date to article_publish_dates list
    article_publish_dates.append(article.publish_date)
    # append article authors to article_authors list
    article_authors.append(article.authors)
    # append article keywords to article_keywords list
    article_keywords.append(article.keywords)
    # append article summary to article_summaries list
    article_summaries.append(article.summary)
    # append article top image to article_top_images list
    article_top_images.append(article.top_image)


# store into data folder, each file is an article
for i in range(len(articles)):
    with open('./data/' + str(i) + '.txt', 'w') as f:
        f.write('article text: ' + article_texts[i])