from random import choice
from bs4 import BeautifulSoup

geo_country_list = ['.com']

language_list = ['en']

user_agents = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36']

def random_user_agent():
    user_agent = choice(user_agents)
    return {'User-Agent':user_agent}

def parse_snippet(response):
    soup = BeautifulSoup(response.text, 'lxml')
    snippet = soup.find('div', attrs={'class': 'xpdopen'})
    if snippet != None:
        try:
            links = snippet.find_all('a', href=True)
            snippet_link = links[0]['href']
            return snippet_link
        except:
            return None
    else:
        return None

def parse_results(response):
    urls = []
    soup = BeautifulSoup(response.text, 'lxml')
    h3s = soup.find_all('h3', attrs={'class': 'r'})
    for h3 in h3s:
        result = h3.find('a')
        result = result['href']
        urls.append(result)
    return urls

def output(filename, keyword, snippet, urls):
    if snippet != None:
        with open(filename, 'a', encoding='utf-8') as output_file:
            output_file.write('"{}","Snippet","{}"\n'.format(keyword, snippet))
    else:
        pass
    if len(urls) > 0:
        r = len(urls)
        i = 0
        while i < r:
            with open(filename, 'a', encoding='utf-8') as output_file:
                output_file.write('"{}","{}","{}"\n'.format(keyword, i + 1, urls[i]))
            i += 1
    else:
        pass
