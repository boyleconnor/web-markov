from lxml import html
import requests

#Sources:
#Web scraping: http://docs.python-guide.org/en/latest/scenarios/scrape/


def find_twitter_usernames():
    #Function used to retrieve twitter usernames from a specific webpage and return a string that contains usernames separated by commas
    page = requests.get('http://twittercounter.com/pages/100?utm_expid=102679131-111.l9w6V73qSUykZciySuTZuA.0&utm_referrer=https%3A%2F%2Fwww.google.com%2F')
    pageCode = html.fromstring(page.content)

    # <span itemprop="alternateName">@selenagomez</span></a>
    # prices = tree.xpath('//span[@class="item-price"]/text()')

    twitter_users = pageCode.xpath('//span[@itemprop="alternateName"]/text()')
    twitter_users_string = ""

    for x in twitter_users:
        twitter_users_string = twitter_users_string + x
        twitter_users_string = twitter_users_string + ','
    twitter_users_string = twitter_users_string[:-1]
    return twitter_users_string

print(find_twitter_usernames())