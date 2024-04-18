import json
import logging
from urllib.parse import urljoin

import requests

from apps.hotline_ua.parsers.count_search import CountSearchParser
from apps.hotline_ua.scrapers.base import _BaseScraper

logger = logging.getLogger('django')


class CountScraper(_BaseScraper):
    parser_class = CountSearchParser

    def __init__(self, data: dict):
        self.data = data

    @property
    def scrapy_items(self):
        self.session = requests.Session()
        try:
            url = self.data['url']
            x_token = self._get_token(url)
            headers = {
                **self._HEADERS,
                **{
                    'x-token': x_token,
                    'referer': urljoin(self._MAIN_URL, self.data['url']),
                    'x-referer': urljoin(self._MAIN_URL, self.data['url']),
                }}

            urljoin(self._MAIN_URL, self.data['url'])

            variables = {'path': self.data['path']}
            if self.data.get('price_max'):
                variables['priceMax'] = self.data['price_max']
            if self.data.get('price_min'):
                variables['priceMin'] = self.data['price_min']
            if self.data.get('filters'):
                variables['filter'] = self.data['filters']

            json_data = {
                'operationName': 'getFilteredProductsCount',
                'variables': variables,
                'query': 'query getFilteredProductsCount($path: String!, $filter: String, $priceMin: Int, $priceMax: Int, $phrase: String) {\n  byPathQuerySection(path: $path, filter: $filter, priceMin: $priceMin, priceMax: $priceMax, phrase: $phrase) {\n    _id\n    redirectToNotNullFilterLink\n    filteredProductsCount\n    __typename\n  }\n}\n',
            }

            response = self.session.post(self._GRAPHQL_URL, headers=headers, json=json_data)
            response.raise_for_status()
            json_data = json.loads(response.text)
            parser = self.parser_class(data=json_data['data'])
            return parser.result_items
        except (requests.RequestException, json.decoder.JSONDecodeError, ValueError, TypeError, KeyError):
            logger.warning(f'Empty result of searching count: "{self.data}".')
            return 0
        finally:
            self.session.close()
