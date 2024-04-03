from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import CustomUserManager
from apps.common.constants import MAX_QUERY_NUMBER_DEFAULT, USER_UPDATE_PERIOD_DEFAULT
from apps.common.models import TimeStampedMixin


class User(TimeStampedMixin, PermissionsMixin, AbstractBaseUser):
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_email_verified = models.BooleanField(_("email verified"), default=False)

    personal_setting = models.ForeignKey(
        'PersonalSetting',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class PersonalSetting(models.Model):
    telegram_user_id = models.IntegerField(_("telegram user ID"), null=True)
    max_query_number = models.IntegerField(_("max query number"), default=MAX_QUERY_NUMBER_DEFAULT)
    update_period = models.IntegerField(_("update period (minutes)"), default=USER_UPDATE_PERIOD_DEFAULT)
    is_vip = models.BooleanField(_("vip"), default=False)

    class Meta:
        verbose_name = _("personal_setting")
        verbose_name_plural = _("personal_settings")


class ParameterCategory(models.Model):
    param_category_name = models.CharField(
        unique=False,
        max_length=150,
        null=False,
        verbose_name=_('parameter category name')
    )

    def __str__(self):
        return self.param_category_name


class BaseParameter(models.Model):
    param_type = models.ForeignKey(
        'ParameterCategory',
        on_delete=models.CASCADE,
        null=False,
        related_name='param_types',
        verbose_name=_('parameter type name')
    )

    def __str__(self):
        return self.id