from django.contrib import admin

from apps.hotline_ua.models import Category, Checker, Filter


# Register your models here.
@admin.register(Checker)
class CheckerAdmin(admin.ModelAdmin):
    ...


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...
