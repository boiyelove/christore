# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20150914_0513'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=150)),
                ('publisher', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CatalogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('slug', models.SlugField(max_length=150)),
                ('description', models.TextField(blank=True)),
                ('featured', models.BooleanField(default=None)),
                ('timestamp', models.DateTimeField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('catalog', models.ForeignKey(related_name='categories', to='products.Catalog')),
                ('parent', models.ForeignKey(related_name='children', to='products.CatalogCategory', null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(to='products.CatalogCategory'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
