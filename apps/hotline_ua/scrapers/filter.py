import logging
from urllib.parse import urljoin

import requests

from apps.hotline_ua.parsers.filter import FilterParser
from apps.hotline_ua.scrapers.base import _BaseScraper

logger = logging.getLogger('django')


class FilterScraper(_BaseScraper):
    parser_class = FilterParser

    def __init__(self, url):
        self.url = url

    @property
    def scrapy_items(self):
        logger.info(f'Scrapy filters from:{self.url}.')
        try:
            url = urljoin(self._BASE_URL, 'ua' + self.url)
            response = requests.get(url, headers=self._HEADERS)
            response.raise_for_status()
            parser = self.parser_class(data=response.text)
            instances = parser.result_items
            return instances
        except (requests.RequestException, ValueError, TypeError):
            logger.error("Invalid scraping filters.")
            return []
