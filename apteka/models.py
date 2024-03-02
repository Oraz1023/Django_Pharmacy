from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


class MonthlyPromotion(models.Model):
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Скидка (%)')

    def __str__(self):
        return f'{self.start_date}  {self.end_date}'

    class Meta:
        verbose_name = 'Акция месяца'
        verbose_name_plural = 'Акция месяца'


class Catalog(MPTTModel):
    title = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            db_index=True, verbose_name='Родительский отдел')

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталог'


class Category(MPTTModel):
    title = models.CharField(max_length=50, unique=True, verbose_name="Категория")
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            db_index=True, verbose_name='Родительский отдел')

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class Popular_brand(MPTTModel):
    title = models.CharField(max_length=50, unique=True, verbose_name='Товар бренда')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            db_index=True, verbose_name='Родительский отдел')
  
    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Популярный бренд'
        verbose_name_plural = 'Популярные бренды'

# class Country(models.Model):
#     title = models.CharField(max_length=50, verbose_name='Название')
#

class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(max_length=1000, verbose_name='Описание', blank=True, null=True)
    price = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Цена')
    new_price = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Цена акции', null=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    count = models.IntegerField(default=0, verbose_name='Сколько')
    product_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Код товара')
    manufacturer = models.TextField(max_length=1000, verbose_name='Производитель')
    promotion = models.ForeignKey(MonthlyPromotion,
                                  on_delete=models.SET_NULL,
                                  related_name='products',
                                  verbose_name='Акция',
                                  blank=True, null=True, default=None)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='catalogs', verbose_name='Каталог')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories',
                                 verbose_name='Категории')
    pop_brand = models.ForeignKey(Popular_brand, on_delete=models.CASCADE, related_name='pop_brands',verbose_name='Популярные бренды')
    # country=models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="страна")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Health_blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата Публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата Обновление')
    images = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Фото', blank=True)
    tag = models.CharField(max_length=50, verbose_name='Теги')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог о здоровье'


class Personal_account(models.Model):
    full_name = models.CharField(max_length=50, verbose_name='Полное имя')
    birthday = models.DateTimeField(auto_now_add=True, verbose_name='Дата рождения')
    email = models.EmailField(max_length=250, verbose_name='почта')
    tel_num = models.CharField(max_length=20, verbose_name='номер телефона')
    user= models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Личный кабинет'


class Order(models.Model):
    class Payment_enum(models.TextChoices):
        Наличными = "Оплата наличными"
        Картой = "Оплата картой"

    class Delivery_enum(models.TextChoices):
        Доставка = "Доставка"
        Самовывоз = "Самовывоз"

    delivery_type = models.CharField(max_length=100, choices=Delivery_enum.choices, default=Delivery_enum.Самовывоз,
                                     verbose_name='Тип Доставки', )
    delivery_address = models.CharField(max_length=500, verbose_name='Адрес доставки')
    customer = models.ForeignKey('Personal_account', on_delete=models.CASCADE, verbose_name='Покупатель', null=True)
    products = models.ManyToManyField('Product', verbose_name='Товары')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')
    payment_type = models.CharField(max_length=100, choices=Payment_enum.choices, default=Payment_enum.Картой, )

    is_paid = models.BooleanField(default=False, verbose_name='Оплачен')
    quantity = models.IntegerField(verbose_name='Количество', )
    item_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу', null=True,
                                     blank=True)

    def __str__(self):
        return f'Заказ #{self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'




