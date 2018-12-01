from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AbstractDateTimeModel(models.Model):
    date_created = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name='Date created'
    ),
    date_updated = models.DateTimeField(
        auto_now=True, db_index=True,
        verbose_name='Date updated'
    )

    class Meta:
        abstract = True


class File(AbstractDateTimeModel):
    published_content = models.UUIDField(
        verbose_name='file identifier'
    )
    reg_number = models.CharField(
        max_length=40, unique=True
    )
    name = models.CharField(
        max_length=255, verbose_name='name'
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
