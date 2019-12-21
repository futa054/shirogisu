from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, _user_has_perm
)
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class Country(models.Model):
    country_name = models.CharField(max_length=150)

class AccountManager(BaseUserManager):
    def create_user(self, request_data, **kwargs):
        now = timezone.now()
        if not request_data['email']:
            raise ValueError('Users must have an email address.')

        user = self.model(
            username=request_data['username'],
            email=self.normalize_email(request_data['email']),
            is_active=True,
            last_login=now,
            date_joined=now,
        )

        user.set_password(request_data['password'])
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        request_data = {
            'username': username,
            'email': email,
            'password': password
        }
        user = self.create_user(request_data)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    username    = models.CharField(_('username'), max_length=30, unique=True)
    first_name  = models.CharField(_('first name'), max_length=30, blank=True)
    last_name   = models.CharField(_('last name'), max_length=30, blank=True)
    email       = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def user_has_perm(self, user, perm, obj):
        return _user_has_perm(user, perm, obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return self.is_admin

    class Meta:
        db_table = 'api_user'
        swappable = 'AUTH_USER_MODEL'

class Region(models.Model):
    region_name = models.CharField(max_length=150)
    
class Prefecture(models.Model):
    prefecture_name = models.CharField(max_length=150)
    country_id = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

class Category(models.Model):
    category_name = models.CharField(max_length=150)

class Souvenir(models.Model):
    souvenir_name = models.CharField(max_length=150)
    japanese_souvenir_name = models.CharField(max_length=150)
    souvenir_description = models.TextField()
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    prefecture_id = models.ForeignKey(Prefecture, on_delete=models.SET_NULL, null=True)
    posted_user_id = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)