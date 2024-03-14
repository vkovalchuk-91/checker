from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.checker.models import BaseFilter, BaseChecker
from apps.common import TimeStampedMixin
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
    BRAND = FilterType.BRAND.value, _('brand')
    SHOP = FilterType.SHOP.value, _('shop')
    LINK = FilterType.LINK.value, _('link')
    TEXT = FilterType.TEXT.value, _('text')


class Filter(TimeStampedMixin, BaseFilter):
    objects = FilterManager()

    type_choices_class = HotlineUaFilterTypeChoices

    code = models.IntegerField(_('code'))
    title = models.CharField(_('title'), max_length=100, blank=False)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='filters'
    )

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('code', 'category')


class Checker(TimeStampedMixin, BaseChecker):
    filter_class = Filter

    filters = models.ManyToManyField(
        filter_class,
        blank=True,
        related_name='checkers',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=False,
        related_name='checkers'
    )

    class Meta:
        verbose_name = _("checker")
        verbose_name_plural = _("checkers")
