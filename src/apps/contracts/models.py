from django.contrib.gis.geos import Point
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import (
    JSONField, DateRangeField, ArrayField
)

from apps.core.models import (
    AbstractDateRegModel, File, PaymentDocument
)
from apps.core.enums import StageTypes, CurrencyTypes
from apps.core.utils import get_coordinates


class Customer(AbstractDateRegModel):
    kpp = models.IntegerField(
        verbose_name='kpp'
    )
    inn = models.IntegerField(
        verbose_name='inn'
    )
    name = models.TextField(
        verbose_name='description'
    )
    address = models.CharField(
        max_length=255, verbose_name='address'
    )
    geometry = Point()

    def save(self, **kwargs):
        super().save(**kwargs)
        self.geometry = get_coordinates(self.address)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Supplier(Customer):
    participant = models.CharField(
        max_length=6,
        verbose_name='participant type'
    )
    contact_info = models.CharField(
        max_length=255, verbose_name='full name of supplier'
    )
    legal_form = models.CharField(
        max_length=255, verbose_name='code and name'
    )

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'


class Product(AbstractDateRegModel):
    name = models.CharField(
        max_length=255,
        verbose_name='name'
    )
    sid = models.CharField(
        max_length=40,
        verbose_name='sid'
    )
    okei = ArrayField(
        models.CharField(
            max_length=80, verbose_name='name and code'
        )
    )
    okpd2 = ArrayField(
        models.CharField(
            max_length=80, verbose_name='name and code'
        )
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name='quantity'
    )
    price = models.DecimalField(
        max_digits=16, decimal_places=2,
        verbose_name='price'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-price']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Execution(AbstractDateRegModel):
    product_str = models.TextField(
        verbose_name='full text product'
    )
    document = models.ForeignKey(
        PaymentDocument,
        on_delete=models.CASCADE,
        verbose_name='document',
        related_name='execution'
    )
    paid_price = models.DecimalField(
        max_digits=16, decimal_places=2,
        verbose_name='paid rub'
    )
    currency = models.PositiveSmallIntegerField(
        choices=CurrencyTypes.CURRENCY_TYPES,
        default=CurrencyTypes.RUB,
        verbose_name='currency'
    )
    vat_price = models.DecimalField(
        max_digits=16, decimal_places=2,
        verbose_name='paid rub'
    )


class Contract(AbstractDateRegModel):
    publish_date = models.DateTimeField(
        verbose_name='publish date'
    )
    sign_date = models.DateField(
        verbose_name='sign date'
    )
    protocol_date = models.DateField(
        verbose_name='protocol date'
    )

    attachments = GenericRelation(
        File, related_name='contracts',
        verbose_name='files'
    )
    suppliers = models.ManyToManyField(
        Supplier, related_name='contracts'
    )
    products = GenericRelation(
        Product, related_name='contracts'
    )
    executions = GenericRelation(
        Execution, related_name='contracts'
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL,
        verbose_name='customer of contract',
        blank=True, null=True
    )

    price = models.DecimalField(
        verbose_name='price',
        max_digits=16, decimal_places=2
    )
    currency = models.PositiveSmallIntegerField(
        choices=CurrencyTypes.CURRENCY_TYPES,
        default=CurrencyTypes.RUB,
        verbose_name='currency'
    )
    current_stage = models.PositiveSmallIntegerField(
        choices=StageTypes.STAGE_TYPES,
        default=StageTypes.E, db_index=True
    )
    region_code = models.PositiveSmallIntegerField(
        verbose_name='region code'
    )
    contract_url = models.URLField(
        verbose_name='contract url'
    )

    number = models.CharField(
        max_length=20,
        verbose_name='number document'
    )
    description = models.TextField(
        verbose_name='full description',
        help_text='documentBase field in API'
    )

    provider_id = models.BigIntegerField(
        db_index=True,
        verbose_name='ext provider id'
    )
    ext_mongo_id = models.UUIDField(
        unique=True,
        verbose_name='external mongo_id',
    )
    fz = models.PositiveSmallIntegerField(
        verbose_name='fz'
    )
    form = models.URLField(
        max_length=255, verbose_name='print form'
    )
    okpd2okved2 = models.BooleanField(
        default=False
    )
    execution_dt = DateRangeField(
        verbose_name='Date start and end'
    )

    meta_data = JSONField(
        default=dict,
        verbose_name='meta data response contract'
    )

    class Meta:
        ordering = ['-price']
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'

    @property
    def tg_data(self):
        return {
            'price': self.meta_data['products']['price'],
            'name': self.meta_data['products']['name'],
            'customer': self.meta_data['customer']['fullName'],
            'url': self.meta_data['printFormUrl'],
        }
