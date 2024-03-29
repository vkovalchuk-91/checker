import json
import logging

import requests

from apps.hotline_ua.parsers.category import CategoryParser
from apps.hotline_ua.scrapers.base import _BaseScraper

logger = logging.getLogger('django')


class CategoryScraper(_BaseScraper):
    parser_class = CategoryParser

    @property
    def scrapy_items(self):
        try:
            json_data = {
                'operationName': 'menuMain',
                'variables': {},
                'query': 'query menuMain { menu { json __typename } }',
            }
            response = requests.post(self._GRAPHQL_URL, headers=self._HEADERS, json=json_data)
            response.raise_for_status()
            json_data = json.loads(response.text)

            parser = self.parser_class(data=json.loads(json_data['data']['menu']['json']))
            instances = parser.result_items

            return instances
        except (requests.RequestException, json.decoder.JSONDecodeError, ValueError, TypeError, KeyError):
            logger.error("Invalid scraping categories.")
            return []
