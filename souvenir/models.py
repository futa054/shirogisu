from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser

class Country(models.Model):
    country_name = models.CharField(max_length=150)

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    country_id = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
    posted_user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)