# Generated by Django 2.2.18 on 2021-06-27 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=8, verbose_name='Цена'),
        ),
    ]
