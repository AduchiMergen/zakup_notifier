from django.db import models


class CustomerScore(models.Model):
    customer = models.OneToOneField('contracts.Customer', on_delete=models.CASCADE)

    score = models.IntegerField()


class ProductOkpd2Score(models.Model):
    okpd2 = models.CharField(max_length=80, verbose_name='okpd2 code')

    score = models.IntegerField()
