from django.db import models

from apps.core.models import AbstractDateTimeModel


class Placer(AbstractDateTimeModel):
    inn = models.IntegerField(unique=True)
    name = models.CharField(max_length=40, unique=True)

    score = models.IntegerField()


