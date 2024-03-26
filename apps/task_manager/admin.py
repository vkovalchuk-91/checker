from django.contrib import admin

from apps.task_manager.models import CheckerTask


# Register your models here.

@admin.register(CheckerTask)
class CheckerTaskAdmin(admin.ModelAdmin):
    ...
