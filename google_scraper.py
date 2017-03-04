import requests
from bs4 import BeautifulSoup
from random import choice, randint
from time import sleep
from googleFunctions import (geo_country_list, language_list, random_user_agent,
                             parse_snippet, parse_results, output)

base_url = 'https://www.google'
base_search = '/search?num='
base_question = '&q='
base_lang = '&hl='


class GoogleScraper(object):

    def __init__(self, country, language, keywords, results=50, min_wait=30, max_wait=60
                 , proxies=[], max_retries=3, filename='results'):

        assert country in geo_country_list, 'Unsupported Country'
        assert language.split('-')[0] in language_list, 'Unsupported Language'
        assert isinstance(keywords, list), 'Keywords are not in correct list format'

        self.search_engine = '{}{}'.format(base_url, country)
        self.language = '{}{}'.format(base_lang, language)
        self.keywords = keywords
        self.results = '{}{}'.format(base_search,results) if results < 101 else '{}{}'.format(base_search,10)
        self.min_wait = min_wait if isinstance(min_wait, int) else 30
        self.max_wait = max_wait if isinstance(max_wait, int) else 60
        self.proxies = proxies if isinstance(proxies, list) else []
        self.max_retries = max_retries if isinstance(max_retries, int) else 3
        self.filename = '{}.csv'.format(filename)
        self.current_keyword = None

    def single_request(self):
        keyword = self.keywords.pop(0)
        self.current_keyword = keyword
        search_string = '{}{}{}{}{}'.format(self.search_engine, self.results, base_question,
                                        keyword.replace(' ', '+'), self.language)
        try:
            if len(self.proxies) > 0:
                r = requests.get(search_string,headers=random_user_agent())
            else:
                r = requests.get(search_string,headers=random_user_agent())
            return r
        except:
            self.keywords.append(keyword)
            return None

    def parse_result(self,response):
        if response is not None:
            if response.status_code == 200:
                snippet = parse_snippet(response)
                urls = parse_results(response)
                return snippet, urls
            if response.status_code != 200:
                if self.current_keyword not in self.keywords:
                    self.keywords.append(self.current_keyword)
                return None, None

    def write_results(self,snippet,urls):
        if len(urls) > 0:
            output(self.filename,self.current_keyword,snippet,urls)
        else:
            if self.current_keyword not in self.keywords:
                self.keywords.append(self.current_keyword)

    def scrape_results(self):
        tries = 0
        while tries < self.max_retries:
            while len(self.keywords) > 0:
                r = self.single_request()
                s, t = self.parse_result(r)
                self.write_results(s, t)
                sleep(randint(self.min_wait,self.max_wait))
            tries += 1
