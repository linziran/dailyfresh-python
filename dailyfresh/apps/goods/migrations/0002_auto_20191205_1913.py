# Generated by Django 2.1 on 2019-12-05 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='detail',
            field=models.TextField(blank=True, verbose_name='商品详情'),
        ),
    ]
