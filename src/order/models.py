from django.db import models

from user.models import User, phone_validator
from product.models import Product


class Order(models.Model):
    STATUS_PREPARE = 'Заказ формируется'
    STATUS_ORDERED = 'Заказано'
    STATUS_READY = 'Готово к отправке'
    STATUS_SEND = 'Отпаравлено'
    STATUS_DONE = 'Доставлено'
    STATUS_CHOICES = (
        (STATUS_PREPARE, STATUS_PREPARE),
        (STATUS_ORDERED, STATUS_ORDERED),
        (STATUS_READY, STATUS_READY),
        (STATUS_SEND, STATUS_SEND),
        (STATUS_DONE, STATUS_DONE),
    )

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='Заказчик')
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name='Телефон', validators=[phone_validator])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PREPARE, db_index=True,
                              verbose_name='Статус')
    text = models.TextField(verbose_name='Комментарий к заказу')


def __str__(self):
    return f'Заказ #{self.id}'


class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'{self.product} - {self.order}'
