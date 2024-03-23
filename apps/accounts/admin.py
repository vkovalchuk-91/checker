from django.contrib import admin

from apps.accounts.models import User, UserAccountType


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...


@admin.register(UserAccountType)
class UserAccountTypeAdmin(admin.ModelAdmin):
    ...