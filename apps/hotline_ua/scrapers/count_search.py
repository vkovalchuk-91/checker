import json
import logging

import requests

from apps.hotline_ua.parsers.count_search import CountSearchParser
from apps.hotline_ua.scrapers.base import _BaseScraper

logger = logging.getLogger('django')


class CountSearchScraper(_BaseScraper):
    QUERY_STR = 'query getFilteredProductsCount($path: String!, $filter: String, $priceMin: Int, $priceMax: Int, $phrase: String) {\n  byPathQuerySection(path: $path, filter: $filter, priceMin: $priceMin, priceMax: $priceMax, phrase: $phrase) {\n    _id\n    redirectToNotNullFilterLink\n    filteredProductsCount\n    __typename\n  }\n}\n'

    parser_class = CountSearchParser

    def __init__(self, data: dict):
        self.data = data

    @property
    def scrapy_items(self):
        logger.info(f'Scrapy "{self.data}" count search result.')
        try:

            variables = {
                'path': self.data['path'],
                'filter': self.data['filter'],
            }

            if self.data.get('$priceMin'):
                variables['priceMin'] = self.data['$priceMin']

            if self.data.get('$priceMax'):
                variables['$priceMax'] = self.data['$priceMax']

            json_data = {
                'operationName': 'getFilteredProductsCount',
                'variables': variables,
                'query': self.QUERY_STR,
            }

            response = requests.post(self._GRAPHQL_URL, headers=self._HEADERS, json=json_data)
            response.raise_for_status()
            json_data = json.loads(response.text)
            parser = self.parser_class(data=json_data['data'])
            return parser.result_items
        except (requests.RequestException, ValueError, TypeError):
            logger.error(f'Invalid scraping "{self.data}" count search result.')
            return []
