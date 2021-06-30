from django.core.management.base import BaseCommand, CommandError, ArgumentParser
from django.db.transaction import atomic
from product.models import Product, ProductType
import argparse
from random import choice, randint


class Command(BaseCommand):
    help = (
        'Команда генерирует указанное количество продуктов '
        'используя шаблон и данные для подстановки в шаблон '
        'перечисленны в атрибутах команды.'
        'Работает для 4 типов товаров.'
    )

    NAME_BY_TYPE = [
        ['палочка', 'посох'],
        ['шляпа', 'перчатки', 'куртка', 'сапоги', 'штаны'],
        ['метла', 'веник', 'кисточка'],
        ['кольцо', 'серьга', 'амулет', 'подвеска'],
    ]

    MATS = ['дракона', 'дуба', 'единорога', 'лича', 'друида', 'мага', 'проклятого']

    QUALITY = ['потрёпанное', 'идеальное', 'среднее', 'качественное', 'зачарованное']

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('count', type=int, help='Количество создаваемых продуктов')
        parser.add_argument('--dry-run', action='store_true', help='Показать изменения не внося их')

    def _gen_name(self, number):
        name = choice(self.NAME_BY_TYPE[number % 4])
        mat = choice(self.MATS)
        quality = choice(self.QUALITY)
        return f'{name.capitalize()} {mat} ({quality})'

    def handle(self, count, dry_run, **options):
        if count < 0:
            raise CommandError('Количество должно быть положительным числом')

        type_by_number = {obj.id - 1: obj for obj in ProductType.objects.all()}

        with atomic() as trn:
            for number in range(count):
                obj = {
                    'type': type_by_number[number % 4],
                    'name': self._gen_name(number),
                    'price': randint(10_000, 1_000_000) / 100
                }

                if not dry_run:
                    Product.objects.create(**obj)
                else:
                    self.stdout.write(f'Create: {obj}')

                if number % 100 == 0:
                    self.stdout.write(f'{number}/{count}')
            self.stdout.write('All done')
