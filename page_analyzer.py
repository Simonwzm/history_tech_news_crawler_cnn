import newspaper
import datetime
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


def parse_for_local():

    with open('./html/index.txt', 'r') as f:
        page_list = f.readlines()

    for line in page_list:
        # create a article object
        article = Article(url = line, config = config)
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
        directory = './data/'+ article.title
        os.mkdir(directory)
        with open(f'{directory}/time.txt') as f:
            #example: 2020-04-01 00:00:00
            #seperate year, month, day, hour, minute, second from example
            year = article.publish_date[0:4]
            month = article.publish_date[5:7]
            day = article.publish_date[8:10]
            hour = article.publish_date[11:13]
            minute = article.publish_date[14:16]
            second = article.publish_date[17:19]
            f.write(year)
            f.write(month)
            f.write(day) 

        with open(f'{directory}/author.txt') as f:
            f.write(article.authors)
        with open(f'{directory}/tag.txt') as f:
            f.write(article.keywords)
        with open(f'{directory}/summary.txt') as f:
            f.write(article.summary)
        with open(f'{directory}/image.txt') as f:
            f.write(article.top_image)
        with open(f'{directory}/content.txt') as f:
            #split word in title
            title_word_list = article.title.split()
            for filename in html_file_paths:
                for word in title_word_list:
                    if word not in filename:
                        break
                else:
                    pass

            f.write(article.text)
        with open(f'{directory}/title.txt') as f:
            f.write(article.title)
        with open(f'{directory}/url.txt') as f:
            f.write(article.url)


# store into data folder, each file is an article
# for i in range(len(articles)):
#     with open('./data/' + str(i) + '.txt', 'w') as f:
#         f.write('article text: ' + article_texts[i])

def parse(url):
    

    # create a article object
    article = Article(url = url, config = config)
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

    filename = "".join(i for i in article.title if i not in "\/:*?<>|") + '.html' 
    directory = os.path.join('data', filename[:-1])
    if not os.path.exists(directory):
        os.mkdir(directory)
    with open(os.path.join(directory, 'time.txt'), 'w') as f:

        # convert datetime object to string
        date = article.publish_date.strftime("%Y-%m-%d %H:%M:%S")
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        hour = date[11:13]
        minute = date[14:16]
        second = date[17:19]
        f.write(year)
        f.write(month)
        f.write(day) 

    with open(os.path.join(directory, 'author.txt'), 'w') as f:
        # for author in article.authors
        for author in article.authors:
            f.write(author)
            f.write('\n')
    with open(os.path.join(directory, 'keyword.txt'), 'w') as f:
        for keyword in article.meta_keywords:
            f.write(keyword)
            f.write('\n')
    with open(os.path.join(directory, 'summary.txt'), 'w') as f:
        f.write(article.summary)
    with open(os.path.join(directory, 'image.txt'), 'w') as f:
        f.write(article.top_image)
    with open(os.path.join(directory, 'content.txt'), 'wb') as f:
        #split word in title
        f.write(article.text.encode('utf-8'))
    with open(os.path.join(directory, 'title.txt'), 'w') as f:
        f.write(article.title)
    with open(os.path.join(directory, 'url.txt'), 'w') as f:
        f.write(article.url)

# parse('https://www.cnn.com/2022/11/17/economy/windfall-tax-nuclear-uk-budget/index.html')