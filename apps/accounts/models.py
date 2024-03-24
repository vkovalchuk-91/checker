from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import CustomUserManager
from apps.common import TimeStampedMixin


class User(TimeStampedMixin, PermissionsMixin, AbstractBaseUser):
    db = 'default'
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
    telegram_user_id = models.IntegerField(_("telegram user ID"), default=0)
    user_account_type = models.ForeignKey(
        'UserAccountType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account_type',
        verbose_name=_("user account type"))
    update_period = models.IntegerField(_("update period (minutes)"), default=0)

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


class UserAccountType(models.Model):
    db = 'default'
    name = models.CharField(_("user account type name"), max_length=150)
    max_query_number = models.IntegerField(_("max query number"), default=0)
    update_period = models.IntegerField(_("update period (minutes)"), default=0)


class CheckerTask(TimeStampedMixin):
    is_active = models.BooleanField(_("active"), default=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=False, related_name='user', verbose_name='user')
    update_period = models.IntegerField(verbose_name='update period (minutes)')
    last_run_at = models.DateTimeField(default=timezone.now, verbose_name='last run date')
    task_params = models.ForeignKey(
        'BaseParameter',
        on_delete=models.CASCADE,
        null=False,
        related_name='parameters',
        verbose_name='parameters'
    )


class BaseParameter(models.Model):
    param_type = models.ForeignKey(
        'ParameterCategory',
        on_delete=models.CASCADE,
        null=False,
        related_name='parameter_category',
        verbose_name='Parameter category'
    )


class ParameterCategory(models.Model):
    param_category_name = models.CharField(max_length=150, verbose_name='parameter category name')
