# Generated by Django 3.1.1 on 2020-11-28 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('times', '0004_auto_20201129_0805'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='is_posted',
            new_name='is_publishable',
        ),
        migrations.AddField(
            model_name='article',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='公開済み'),
        ),
    ]
