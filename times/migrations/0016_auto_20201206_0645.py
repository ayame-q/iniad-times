# Generated by Django 3.1.1 on 2020-12-05 21:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('times', '0015_auto_20201205_0606'),
    ]

    operations = [
        migrations.CreateModel(
            name='RevisionMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime, verbose_name='作成日')),
                ('comment', models.TextField(verbose_name='コメント')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revision_messages', to='times.staff', verbose_name='スタッフ')),
            ],
        ),
        migrations.AddField(
            model_name='prearticle',
            name='revision_messages',
            field=models.ManyToManyField(blank=True, related_name='pre_articles', to='times.RevisionMessage', verbose_name='メッセージ'),
        ),
    ]