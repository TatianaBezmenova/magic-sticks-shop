from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name='Телефон')
