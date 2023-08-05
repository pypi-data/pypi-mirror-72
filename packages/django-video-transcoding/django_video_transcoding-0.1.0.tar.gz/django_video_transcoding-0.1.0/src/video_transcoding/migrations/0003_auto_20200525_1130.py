# Generated by Django 3.0.6 on 2020-05-25 11:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_transcoding', '0002_auto_20200226_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='basename',
            field=models.UUIDField(blank=True, null=True, verbose_name='Basename'),
        ),
        migrations.AlterField(
            model_name='video',
            name='error',
            field=models.TextField(blank=True, null=True, verbose_name='Error'),
        ),
        migrations.AlterField(
            model_name='video',
            name='source',
            field=models.URLField(validators=[django.core.validators.URLValidator(schemes=('http', 'https'))], verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'created'), (1, 'queued'), (2, 'process'), (3, 'done'), (4, 'error')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='video',
            name='task_id',
            field=models.UUIDField(blank=True, null=True, verbose_name='Task ID'),
        ),
    ]
