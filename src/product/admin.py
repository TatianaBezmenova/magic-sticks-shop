from django.contrib import admin
from .models import ProductType, Product
from typing import Iterable
from decimal import Decimal
from random import choice


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'type', 'price', 'is_visible']
    search_fields = ['name']
    list_filter = [
        ('type', admin.RelatedFieldListFilter),
        ('is_visible', admin.BooleanFieldListFilter),
    ]

    actions = ['do_sale_10', 'regenerate_new_name']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('type')

    @admin.action
    def do_sale_10(self, request, queryset: Iterable[Product]):
        for obj in queryset.all():
            obj.price *= Decimal(0.9)
            obj.save(update_fields=['price'])

    @admin.action
    def regenerate_new_name(self, request, queryset: Iterable[Product]):
        from .management.commands.generate_products import Command

        for obj in queryset.all():
            name = choice(Command.NAME_BY_TYPE[obj.type.id - 1])
            mat = choice(Command.MATS)
            quality = choice(Command.QUALITY)
            obj.name = f'{name.capitalize()} {mat} ({quality})'
            obj.save(update_fields=['name'])
