# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OverallRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('voted_id', models.PositiveIntegerField()),
                ('quantity_vote', models.PositiveIntegerField(default=0)),
                ('rate', models.DecimalField(null=True, max_digits=6, decimal_places=1)),
                ('voted_type', models.ForeignKey(to='contenttypes.ContentType', related_name='overall_voted_type')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('transaction_id', models.PositiveIntegerField()),
                ('state', models.IntegerField(choices=[(0, 'Pendiente'), (1, 'Aceptado'), (2, 'Anulado')], default=0)),
                ('rate', models.PositiveIntegerField(choices=[(1, 'Very bad'), (2, 'Bad'), (3, 'Medium'), (4, 'Good'), (5, 'Very Good')], null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('voted_id', models.PositiveIntegerField()),
                ('trans_type', models.ForeignKey(to='contenttypes.ContentType', related_name='transation_type')),
                ('voted_type', models.ForeignKey(to='contenttypes.ContentType', related_name='voted_type')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_voter')),
            ],
        ),
    ]
