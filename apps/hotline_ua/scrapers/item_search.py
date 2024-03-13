import json
import logging

import requests

from apps.hotline_ua.parsers.item_search import ItemSearchParser
from apps.hotline_ua.scrapers.base import _BaseScraper

logger = logging.getLogger('django')


class TextSearchScraper(_BaseScraper):
    parser_class = ItemSearchParser

    def __init__(self, data: str):
        self.data = data

    @property
    def scrapy_items(self):
        logger.info(f'Scrapy "{self.data}" search result.')
        try:
            json_data = {
                'jsonrpc': '2.0',
                'method': 'search.search',
                'params': {
                    'q': self.data,
                    'lang': 'uk',
                    'section_id': None,
                    'entity': 'full',
                },
                'id': 1,
            }
            response = requests.post(self._SEARCH_URL, headers=self._HEADERS, json=json_data)
            response.raise_for_status()
            json_data = json.loads(response.text)
            parser = self.parser_class(data=json_data)
            return parser.result_items
        except (requests.RequestException, ValueError, TypeError):
            logger.error(f'Invalid scraping "{self.data}" search result.')
            return []
