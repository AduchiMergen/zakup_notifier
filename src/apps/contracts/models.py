from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField

from apps.core.models import AbstractDateTimeModel, File


class Contract(AbstractDateTimeModel):
    attachments = GenericRelation(
        File, related_name='contracts',
        verbose_name='files'
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
