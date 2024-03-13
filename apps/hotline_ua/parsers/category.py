from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class Category:
    code: int
    title: str
    url: str
    path: str
    level: int
    is_link: bool
    children: [list, None]


class CategoryParser:
    result_class = Category

    def __init__(self, data):
        self.data = data

    @property
    def result_items(self):
        instances = []
        for item in self.data:
            children = []
            for children_item in (item['children'] if item.get('children') else []):
                for child_item in children_item:
                    children.append(self.parse_item(child_item))

            instance = self.parse_item(item)
            instance.children = children
            instances.append(instance)

        return instances

    def parse_item(self, json_data):
        url = json_data['url']
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split("/")
        clean_path_parts = [i for i in path_parts if len(i) > 0]
        path = clean_path_parts[len(clean_path_parts) - 1]
        return self.result_class(
            code=json_data['id'],
            title=json_data['title'],
            url=url,
            path=path,
            level=json_data['level'],
            is_link=json_data['isLink'] if json_data.get('isLink') else False,
            children=None
        )
