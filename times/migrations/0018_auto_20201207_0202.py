# Generated by Django 3.1.1 on 2020-12-06 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('times', '0017_auto_20201206_0800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='parent',
        ),
        migrations.AddField(
            model_name='prearticle',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parents', to='times.article', verbose_name='完成記事'),
        ),
        migrations.AddField(
            model_name='prearticle',
            name='is_final_check',
            field=models.BooleanField(default=False, verbose_name='最終チェックか'),
        ),
    ]
