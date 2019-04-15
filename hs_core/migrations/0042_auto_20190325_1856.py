# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-25 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hs_core', '0041_resourcefile__size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='type',
            field=models.CharField(choices=[(b'isHostedBy', b'The content of this resource is hosted by'), (b'isCopiedFrom', b'The content of this resource was copied from'), (b'isPartOf', b'The content of this resource is part of'), (b'hasPart', b'Has Part'), (b'isExecutedBy', b'The content of this resource can be executed by'), (b'isCreatedBy', b'The content of this resource was created by'), (b'isVersionOf', b'Version Of'), (b'isReplacedBy', b'Replaced By'), (b'isDataFor', b'The content of this resource serves as the data for'), (b'cites', b'This resource cites'), (b'isDescribedBy', b'This resource is described by')], max_length=100),
        ),
    ]