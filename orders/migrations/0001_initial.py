# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basket', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('order_id', models.CharField(max_length=120, unique=True, default='ABC')),
                ('status', models.CharField(choices=[('Started', 'Started'), ('Abandoned', 'Abandoned'), ('Finished', 'Finished')], max_length=120, default='Started')),
                ('sub_total', models.DecimalField(max_digits=1000, decimal_places=2, default=10.99)),
                ('tax_total', models.DecimalField(max_digits=1000, decimal_places=2, default=10.99)),
                ('final_total', models.DecimalField(max_digits=1000, decimal_places=2, default=10.99)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('basket', models.ForeignKey(to='basket.Basket')),
                ('billing_address', models.ForeignKey(related_name='billing_address', to='accounts.UserAddress', default=1)),
                ('shipping_address', models.ForeignKey(related_name='shipping_address', to='accounts.UserAddress', default=1)),
                ('user', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
