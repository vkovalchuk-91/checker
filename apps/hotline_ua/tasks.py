import logging

from django.utils import timezone

from apps.celery import celery_app as app
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Category, Filter, Checker
from apps.hotline_ua.scrapers.category import CategoryScraper
from apps.hotline_ua.scrapers.count import CountScraper
from apps.hotline_ua.scrapers.filter import FilterScraper
from apps.hotline_ua.scrapers.text_search import TextSearchScraper


@app.task(name='hotline_ua_scraping_categories')
def scraping_categories():
    scraper = CategoryScraper()
    items = scraper.scrapy_items
    for item in items:
        Category.objects.save_with_children(item.__dict__)


@app.task(name='hotline_ua_scraping_categories_filters')
def scraping_categories_filters(category_ids: list[int]):
    category_instances = Category.objects.filter(id__in=category_ids)
    for category_instance in category_instances:
        if category_instance.is_active and category_instance.parent and not category_instance.is_link:
            scraper = FilterScraper(category_instance.url)
            filter_items = scraper.scrapy_items

            if not filter_items:
                continue

            filter_instances = [Filter.objects.get_instance(item.__dict__) for item in filter_items]
            for filter_instance in filter_instances:
                filter_instance.category = category_instance
            Filter.objects.save_all(filter_instances)


@app.task(name='hotline_ua_run_checkers')
def run_checkers(checker_ids: list[int]):
    print(checker_ids)

    for checker in Checker.objects.filter(id__in=checker_ids, is_active=True, ):
        filter_instances = checker.filters.all()
        if len(filter_instances) == 1 and filter_instances[0].type_name == FilterType.TEXT.value:
            scraper = TextSearchScraper(data=filter_instances[0].title)
            items = scraper.scrapy_items
            is_available = len(items) > 0
        else:
            data = {
                'url': checker.category.url,
                'path': checker.category.path,
            }
            filters = []
            for filter_instance in filter_instances:
                if filter_instance.type_name == FilterType.MIN.value:
                    data['price_min'] = filter_instance.code
                elif filter_instance.type_name == FilterType.MAX.value:
                    data['price_max'] = filter_instance.code
                else:
                    filters.append(filter_instance.code)
            if len(filters) > 0:
                data['filters'] = '-'.join(str(item) for item in filters)

            scraper = CountScraper(data=data)
            count = scraper.scrapy_items
            is_available = count > 0

        checker.updated_at = timezone.now()
        checker.is_available = is_available
        checker.save(update_fields=['updated_at', 'is_available'])

        if is_available:
            logging.info('Checker has results.')
