from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.enums import FileTypes


class AbstractDateRegModel(models.Model):
    date_created = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name='Date created'
    ),
    date_updated = models.DateTimeField(
        auto_now=True, db_index=True,
        verbose_name='Date updated'
    )
    reg_number = models.CharField(
        max_length=40, unique=True
    )

    class Meta:
        abstract = True


class PaymentDocument(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='name'
    )
    date_created = models.DateField(
        verbose_name='Date created'
    )
    number = models.BigIntegerField(
        default=0, verbose_name='number'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'


class File(AbstractDateRegModel):
    published_content = models.UUIDField(
        verbose_name='file identifier'
    )
    name = models.CharField(
        max_length=255, verbose_name='name'
    )
    type = models.PositiveSmallIntegerField(
        choices=FileTypes.FILE_TYPES,
        default=FileTypes.PAYMENT,
        verbose_name='file type'
    )
    description = models.CharField(
        max_length=255, verbose_name='description'
    )

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'<{self.reg_number}: {self.name}>'

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ['published_content']
