from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.regex_helper import _lazy_re_compile

phone_validator = RegexValidator(
    _lazy_re_compile(r'\+?\d\(?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}'),
    'Ожидается телефонный номер в формате +7(123)345-6789'
)


class User(AbstractUser):
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name='Телефон', validators=[phone_validator])
