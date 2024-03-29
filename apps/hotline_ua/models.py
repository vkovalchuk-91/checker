from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import BaseParameter
from apps.common import TimeStampedMixin
from apps.common.models import ActiveStateMixin, AvailableStateMixin
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.managers import CategoryManager, FilterManager


class Category(TimeStampedMixin, models.Model):
    objects = CategoryManager()

    code = models.IntegerField(_('code'), unique=True)
    title = models.CharField(_('title'), max_length=100, blank=False)
    url = models.CharField(_('url'), max_length=255, blank=False)

    path = models.CharField(_('token'), max_length=100, null=True, blank=True, )

    is_link = models.BooleanField(_('link'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        default=None,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class HotlineUaFilterTypeChoices(models.TextChoices):
    BRAND = FilterType.BRAND.value, _(FilterType.BRAND.value)
    LINK = FilterType.LINK.value, _(FilterType.LINK.value)
    SHOP = FilterType.SHOP.value, _(FilterType.SHOP.value)

    TEXT = FilterType.TEXT.value, _(FilterType.TEXT.value)

    MAX_PRICE = FilterType.MAX.value, _(FilterType.MAX.value)
    MIN_PRICE = FilterType.MIN.value, _(FilterType.MIN.value)


class Filter(models.Model):
    objects = FilterManager()
    type_choices_class = HotlineUaFilterTypeChoices

    code = models.IntegerField(_('code'))
    title = models.CharField(_('title'), max_length=100, blank=False)

    type_name = models.CharField(
        _('type'),
        max_length=20,
        blank=False,
        choices=type_choices_class.choices,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        related_name='filters'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("filter")
        verbose_name_plural = _("filters")


class BaseSearchParameter(TimeStampedMixin, ActiveStateMixin, AvailableStateMixin, models.Model):
    filter_class = Filter

    param_type = models.OneToOneField(
        BaseParameter,
        parent_link=True,
        on_delete=models.CASCADE,
        related_name='hotline_ua_search_parameters'
    )

    filters = models.ManyToManyField(
        filter_class,
        related_name='search_parameters',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        related_name='search_parameters'
    )

    class Meta:
        verbose_name = _("search_parameter")
        verbose_name_plural = _("search parameters")
