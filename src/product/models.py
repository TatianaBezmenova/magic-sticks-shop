from django.db import models
from django.urls import reverse_lazy


class ProductType(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=60, unique=True, verbose_name='URL')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        return reverse_lazy('product:product_type_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, db_index=True, verbose_name='Название')
    type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='Тип')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False, db_index=True,
                                verbose_name='Цена')
    img = models.ImageField(upload_to='product', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        return reverse_lazy('product:product_detail', args=[self.id])
