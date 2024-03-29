from django.contrib import admin

from apps.hotline_ua.models import Category, BaseSearchParameter, Filter


# Register your models here.
@admin.register(BaseSearchParameter)
class BaseSearchParameterAdmin(admin.ModelAdmin):
    ...


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...
