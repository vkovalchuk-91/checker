import re
from dataclasses import dataclass

from bs4 import BeautifulSoup

from apps.hotline_ua.enums.filter import FilterType


@dataclass
class Filter:
    code: int
    title: str
    type_name: str


class FilterParser:
    result_class = Filter

    def __init__(self, data):
        self.data = data

    @property
    def result_items(self):
        shop_instances = self.parse_shop_from_script(filter_type=FilterType.SHOP)
        brand_instances = self.parse_brand(filter_type=FilterType.BRAND)
        return brand_instances + shop_instances

    def parse_brand(self, filter_type=FilterType.BRAND):
        return self._parse_with_tag_text(tag="a", text="Бренд", filter_type=filter_type)

    def _parse_with_tag_text(self, tag: str, text: str, filter_type: FilterType):
        soup = BeautifulSoup(self.data, 'html.parser')
        instances = []
        for div in soup.find_all('div', {'class': 'sidebar-filters__item sidebar-filters__item--top'}):
            if len([j for j in div.find_all('div', {'data-v-f03a99b4': True}) if j.find('b', string=text)]) == 0:
                continue

            for a_element in div.find_all(tag, class_='filter-checklist__item-name'):
                try:
                    key = a_element['href'].split('/')[-2] if a_element.get('href') else 0
                    value = a_element.span.get_text(strip=True)
                    instance = Filter(code=int(key), title=value, type_name=filter_type.value)
                    if ((instance.code == 0 and instance.title not in [i.title for i in instances]) or
                            instance.code not in [i.code for i in instances]):
                        instances.append(instance)
                except (KeyError, TypeError, ValueError):
                    continue

        return instances

    def parse_shop_from_script(self, filter_type: FilterType = FilterType.SHOP):
        matches = re.search(r'title:"Магазин",description:(.*?),type:"firm",weight:(.*?),values:(.*?),topValues',
                            self.data)
        if not matches:
            return []

        extracted_text = matches.group(3).replace("'", "")
        items_dict = re.findall(rf'_id:(.*?),isNoFollow(.*?),title:(.*?),alias', extracted_text)

        instances = []
        for item in items_dict:
            try:
                title = item[2][1:-1]

                if title == '':
                    continue

                instance = Filter(code=int(item[0]), title=title, type_name=filter_type.value)
                if instance.code not in [i.code for i in instances]:
                    instances.append(instance)
            except (KeyError, TypeError, ValueError):
                continue

        return instances
