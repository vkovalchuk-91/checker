from django.contrib import admin

from apps.accounts.models import User, PersonalSetting


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...


@admin.register(PersonalSetting)
class PersonalSettingAdmin(admin.ModelAdmin):
    ...
