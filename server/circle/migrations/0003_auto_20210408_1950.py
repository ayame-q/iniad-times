# Generated by Django 3.1.1 on 2021-04-08 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0002_auto_20210408_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interested_in',
            field=models.JSONField(blank=True, null=True, verbose_name='興味'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='questionnaire',
            field=models.JSONField(blank=True, null=True, verbose_name='アンケート'),
        ),
    ]