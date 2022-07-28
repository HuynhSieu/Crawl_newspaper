import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Zing:
    def __init__(self, urls):
        self.subject_urls = []
        self.urls_of_subject = urls

    def get_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_list(self, url):
        if url not in self.subject_urls and url not in self.urls_of_subject:
            self.urls_of_subject.append(url)

    def crawl(self, url):
        html = self.get_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_list(url)

    def run(self):
        while self.urls_of_subject:
            url = self.urls_of_subject.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                filter(lambda x: x not in self.crawl(url), url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.subject_urls.append(url)

if __name__ == '__main__':
    Zing(urls='https://zingnews.vn/').run()