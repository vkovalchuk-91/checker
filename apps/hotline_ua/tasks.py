from apps.celery import celery_app as app
from apps.hotline_ua.models import Category, Filter
from apps.hotline_ua.scrapers.category import CategoryScraper
from apps.hotline_ua.scrapers.filter import FilterScraper

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'


@app.task(name='hotline_ua_scraping_categories')
def scraping_categories():
    scraper = CategoryScraper()
    items = scraper.scrapy_items
    for item in items:
        Category.objects.save_with_children(item.__dict__)
        # categories = Category.objects.save_with_children(item.__dict__)
        # scraping_categories_filters.apply_async(args=([i.id for i in categories if i.is_active and i.parent and not i.is_link],))
        # scraping_categories_filters([i.id for i in categories if i.is_active and i.parent and not i.is_link], )


@app.task(name='hotline_ua_scraping_categories_filters')
def scraping_categories_filters(category_ids):
    if not category_ids or len(category_ids) == 0:
        return

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
