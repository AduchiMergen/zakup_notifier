# Generated by Django 2.1.3 on 2018-12-01 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0003_contract_execution'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='okpd2_name',
            field=models.CharField(default='', max_length=80, verbose_name='okpd2 name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='okpd2',
            field=models.CharField(max_length=80, verbose_name='okpd2 code'),
        ),
    ]