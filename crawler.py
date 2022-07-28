from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from typing import Callable
from dataclasses import dataclass
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Zing:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
        "X-Requested-With": "XMLHttpRequest",
    }
    def __init__(self, links):
        self.subject_links = []
        self.links_of_subject = links

    def get_links(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.findAll('a', recursive=True):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def crawl(self, url):
        lambda url: url not in self.links_of_subject
        html = requests.get(url).text
        for url in self.get_links(url, html):
            if url not in self.subject_links and url not in self.links_of_subject:
                self.links_of_subject.append(url)

    def run(self):
        while self.links_of_subject:
            url = self.links_of_subject.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.subject_links.append(url)

if __name__ == '__main__':
    Zing(links=['https://zingnews.vn/']).run()
