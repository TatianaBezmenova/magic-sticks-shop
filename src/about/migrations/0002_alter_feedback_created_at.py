# Generated by Django 3.2.4 on 2021-07-11 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата сообщения'),
        ),
    ]