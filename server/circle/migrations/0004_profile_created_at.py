# Generated by Django 3.1.1 on 2021-04-09 05:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0003_auto_20210408_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime, verbose_name='登録日'),
        ),
    ]