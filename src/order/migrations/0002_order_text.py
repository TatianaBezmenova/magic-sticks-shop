# Generated by Django 3.2.4 on 2021-07-10 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='text',
            field=models.TextField(default='', verbose_name='Комментарий к заказу'),
            preserve_default=False,
        ),
    ]
