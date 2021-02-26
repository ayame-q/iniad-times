# Generated by Django 3.1.1 on 2021-02-24 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('times', '0023_auto_20210217_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='browsinghistory',
            name='ip',
            field=models.GenericIPAddressField(null=True, verbose_name='IPアドレス'),
        ),
        migrations.AddField(
            model_name='browsinghistory',
            name='referer',
            field=models.TextField(blank=True, null=True, verbose_name='リファラ'),
        ),
        migrations.AddField(
            model_name='browsinghistory',
            name='user_agent',
            field=models.CharField(max_length=512, null=True, verbose_name='UserAgent'),
        ),
    ]