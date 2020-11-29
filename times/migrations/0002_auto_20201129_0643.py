# Generated by Django 3.1.1 on 2020-11-28 21:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('times', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.localtime, null=True, verbose_name='公開日'),
        ),
        migrations.AddField(
            model_name='article',
            name='sns_publish_text',
            field=models.CharField(default='', max_length=140, verbose_name='SNS告知文'),
        ),
        migrations.AddField(
            model_name='prearticle',
            name='publish_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.localtime, null=True, verbose_name='公開日'),
        ),
        migrations.AddField(
            model_name='prearticle',
            name='sns_publish_text',
            field=models.CharField(default='', max_length=140, verbose_name='SNS告知文'),
        ),
        migrations.AlterField(
            model_name='article',
            name='eyecatch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='used_article', to='times.image', verbose_name='アイキャッチ画像'),
        ),
        migrations.AlterField(
            model_name='article',
            name='published_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime, verbose_name='公開された日'),
        ),
        migrations.AlterField(
            model_name='prearticle',
            name='eyecatch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='used_prearticle', to='times.image', verbose_name='アイキャッチ画像'),
        ),
    ]