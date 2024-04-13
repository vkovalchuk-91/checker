import logging

from django.core.cache import cache
from django.utils import timezone

from apps.accounts.models import User
from apps.accounts.tasks import send_email_checker_result_msg
from apps.celery import celery_app as app
from apps.common.constants import CACHE_SAVE_INTERVAL_DEFAULT
from apps.common.tasks import BaseTaskWithRetry
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Category, Filter, BaseSearchParameter
from apps.hotline_ua.scrapers.category import CategoryScraper
from apps.hotline_ua.scrapers.count import CountScraper
from apps.hotline_ua.scrapers.filter import FilterScraper
from apps.hotline_ua.scrapers.text_search import TextSearchScraper
from apps.tbot.tasks import send_bot_message

logger = logging.getLogger('django')


@app.task(name='hotline_ua_scraping_categories', base=BaseTaskWithRetry)
def scraping_categories():
    scraper = CategoryScraper()
    items = scraper.scrapy_items
    for item in items:
        Category.objects.save_with_children(item.__dict__)


@app.task(name='hotline_ua_scraping_categories_filters', base=BaseTaskWithRetry)
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
def run_checkers(ids: list[int]):
    logger.info(f'Run hotline_ua checkers [{ids}]')
    if not ids or len(ids) == 0:
        return

    for search_parameter in BaseSearchParameter.objects.filter(id__in=ids, is_active=True, ):
        filter_instances = search_parameter.filters.all()
        if len(filter_instances) == 1 and filter_instances[0].type_name == FilterType.TEXT.value:
            scraper = TextSearchScraper(data=filter_instances[0].title)
            result = scraper.scrapy_items
            result_count = len(result)
            is_available = result_count > 0
        else:
            data = {
                'url': search_parameter.category.url,
                'path': search_parameter.category.path,
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
            result_count = scraper.scrapy_items
            is_available = result_count > 0

        search_parameter.updated_at = timezone.now()
        search_parameter.is_available = is_available
        search_parameter.save(update_fields=['updated_at', 'is_available'])

        send_msg(search_parameter, result_count)


def send_msg(search_parameter, result_count):
    msg = get_result_message(search_parameter, result_count)
    if not update_msg_in_cache(search_parameter.id, msg):
        return

    user = User.objects.get(checker_tasks__task_param__hotline_ua_search_parameters__id=search_parameter.id)
    if user.is_email_verified:
        send_email_checker_result_msg.apply_async(args=(user.id, msg,))
    if user.personal_setting and user.personal_setting.telegram_user_id:
        send_bot_message.delay(message=msg, telegram_id=user.personal_setting.telegram_user_id)

def get_result_message(search_parameter: BaseSearchParameter, result_count):
    msg = f"Available {result_count} result(s)"
    filter_instances = search_parameter.filters.all()
    if filter_instances and len(filter_instances) == 1 and filter_instances[0].type_name == FilterType.TEXT.value:
        msg += f" search text: {filter_instances[0].title}"
    else:
        msg += f" search items by category : {search_parameter.category.title}"
        msg += f" and {len(filter_instances)} filter(s)"

    msg += f" check in hotline.ua"
    return msg


def update_msg_in_cache(checker_id: int, msg: str) -> bool:
    cache_key = f'hotline_ua_cache_{checker_id}'
    cache_value = cache.get(cache_key)

    if cache_value and cache_value.lower() == msg.lower():
        return False

    cache.set(cache_key, msg, timeout=CACHE_SAVE_INTERVAL_DEFAULT)
    return True
