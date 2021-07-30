# Generated by Django 3.1.1 on 2021-05-03 06:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0004_profile_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='タイトル')),
                ('date', models.DateField(default=django.utils.timezone.localdate, verbose_name='日付')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime, verbose_name='登録日')),
            ],
        ),
    ]