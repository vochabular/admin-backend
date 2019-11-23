# Generated by Django 2.1.10 on 2019-11-23 10:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20191123_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapterTitle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='chapter',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='chaptertitle',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Chapter'),
        ),
        migrations.AddField(
            model_name='chaptertitle',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Language'),
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='languages',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='titleCH',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='titleDE',
        ),
        migrations.AddField(
            model_name='chapter',
            name='languages_comp',
            field=models.ManyToManyField(through='api.ChapterTitle', to='api.Language'),
        ),
    ]
