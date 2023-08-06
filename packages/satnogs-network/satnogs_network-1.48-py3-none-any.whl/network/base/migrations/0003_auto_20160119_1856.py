# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20151011_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tle0', models.CharField(max_length=100, blank=True)),
                ('tle1', models.CharField(max_length=200, blank=True)),
                ('tle2', models.CharField(max_length=200, blank=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['tle0'],
            },
        ),
        migrations.RemoveField(
            model_name='satellite',
            name='tle0',
        ),
        migrations.RemoveField(
            model_name='satellite',
            name='tle1',
        ),
        migrations.RemoveField(
            model_name='satellite',
            name='tle2',
        ),
        migrations.RemoveField(
            model_name='satellite',
            name='updated',
        ),
        migrations.AddField(
            model_name='tle',
            name='satellite',
            field=models.ForeignKey(related_name='tles', to='base.Satellite', null=True),
        ),
        migrations.AddField(
            model_name='observation',
            name='tle',
            field=models.ForeignKey(to='base.Tle', null=True),
        ),
    ]
