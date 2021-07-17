from django.http import HttpResponse
from django.test import TestCase
from django.db.utils import IntegrityError
from random import randint, choice

from django.urls import reverse

from .models import Product, ProductType


class ProductModelTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(
            name='test-name',
            price=123,
        )

    def tearDown(self):
        Product.objects.all().delete()
        super().tearDown()

    def test_product_create(self):
        product = Product.objects.filter(name='test-name').all()[0]
        self.assertEqual(product.name, 'test-name', 'Проверка названия продукта после создания')
        self.assertEqual(product.price, 123, 'Проверка цены продукта после создания')
        self.assertTrue(product.is_visible, 'Проверка видимости продукта после создания')

    def test_product_public_objects(self):
        product = Product.public_objects.get(name='test-name')
        self.assertEqual(product.name, 'test-name', 'Проверка видимости продукта')

        self.product.is_visible = False
        self.product.save()
        with self.assertRaises(Product.DoesNotExist):
            Product.public_objects.get(name='test-name')


class ProductTypeModelTestCase(TestCase):
    def test_product_type_slug_unique(self):
        ProductType.objects.create(
            name='test-type',
            slug='test-slug'
        )

        with self.assertRaises(IntegrityError):
            ProductType.objects.create(
                name='test-type',
                slug='test-slug'
            )

    def test_product_type_on_delete_set_null(self):
        type = ProductType.objects.create(
            name='test-type',
            slug='test-slug'
        )
        Product.objects.create(
            name='test-name',
            price=123,
            type=type
        )

        type.delete()
        product = Product.objects.get(name='test-name')
        self.assertIsNone(product.type, 'Проверка типа продукта при удалении типа')

    def test_product_type_ordering(self):
        for i in range(0, 100):
            ProductType.objects.create(
                name=f'test-type_{randint(0, 1000000000)}',
                slug=f'test-slug_{i}'
            )

        product_types = ProductType.objects.all()
        names = [p.name for p in product_types]
        sorted_names = sorted(names)

        self.assertEqual(names, sorted_names, 'Проверка сортировки типов продуктов по имени')


class ProductListViewTestCase(TestCase):
    PAGINATE_BY = 20

    def setUp(self):
        super().setUp()
        self.product_url = reverse('product:product_list')

        for i in range(0, 4):
            ProductType.objects.create(
                name=f'test-type_{i}',
                slug=f'test-slug_{i}'
            )
        product_types = ProductType.objects.all()

        for i in range(0, 1000):
            product_type = choice(product_types)
            Product.objects.create(
                name=f'test-product_{i}',
                price=100 * i / 4,
                type=product_type
            )

    def tearDown(self):
        ProductType.objects.all().delete()
        Product.objects.all().delete()
        super().tearDown()

    def test_paginate(self):
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, HttpResponse.status_code, 'Проверка доступности страницы')

        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'], 'Проверка пагинации')
        self.assertTrue(len(response.context['product_list']) == self.PAGINATE_BY,
                        'Проверка количества карточек продуктов на 1 странице')

    def test_filters(self):
        PRODUCT_TYPE = ProductType.objects.get(id=1)
        PRICE_START = 1000
        PRICE_END = 1500

        response = self.client.get(self.product_url, data={
            'type': PRODUCT_TYPE.id,
            'price_start': PRICE_START,
            'price_end': PRICE_END
        })

        for product in response.context['product_list']:
            self.assertTrue(PRICE_START <= product.price <= PRICE_END, 'Проверка фильтров по цене')
            self.assertEqual(product.type, PRODUCT_TYPE, 'Проверка фильтра по типу продукта')
