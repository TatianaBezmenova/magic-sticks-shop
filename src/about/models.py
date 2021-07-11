from django.db import models

from user.models import User, phone_validator


class Feedback(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True, verbose_name='Заказчик')
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name='Телефон', validators=[phone_validator])
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата сообщения')
    text = models.TextField(verbose_name='Сообщение')
    read = models.BooleanField(default=False, db_index=True, verbose_name='Прочитано')

    def __str__(self):
        return f'Сообщение #{self.id}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
