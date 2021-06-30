from django.core.management.base import BaseCommand, CommandError, ArgumentParser
from django.db.transaction import atomic
from product.models import Product, ProductType
import argparse
import sys
from decimal import Decimal


class Command(BaseCommand):
    help = (
        'Изменяет стоимость указанных по id товаров на указанный процент.'
        'Например: change_price --up 10% 1 2 3 4 5'
        'или change_price --down 10% 1 2 3 4 5'
    )

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('--up', nargs="+", help='Увеличить цену на x% для списка id продуктов')
        parser.add_argument('--down', nargs="+", help='Снизить цену на x% для списка id продуктов')
        parser.add_argument('--dry-run', action='store_true', help='Показать изменения не внося их')

    def handle(self, up, down, dry_run, **options):
        if up:
            percent, ids = self._prepare_args(up)
            percent = 1 + percent / 100
        elif down:
            percent, ids = self._prepare_args(down)
            percent = 1 - percent / 100
        else:
            raise CommandError('Команда должна содержать параметр --up или --down.')

        with atomic() as trn:
            for id in ids:
                obj = Product.objects.get(id=id)
                obj.price *= Decimal(percent)
                if not dry_run:
                    obj.save(update_fields=['price'])
                else:
                    self.stdout.write(f'Новая цена товара id={id} составит {obj.price}')
            self.stdout.write('All done')

    def _prepare_args(self, args):
        percent = args[0]
        ids = args[1:]

        if '%' not in percent:
            raise CommandError('Команда должна содержать информацию о проценте изменения стоимости в формате х%.')
        if not ids:
            raise CommandError('Команда должна содержать список id продуктов через пробел.')

        percent = float(percent.replace(' ', '')[:-1])
        return percent, ids
