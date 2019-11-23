# Generated by Django 2.1.10 on 2019-11-23 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20191123_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='language',
        ),
        migrations.AddField(
            model_name='profile',
            name='fk_language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_language', to='api.Language'),
        ),
        migrations.RemoveField(
            model_name='profile',
            name='translator_languages',
        ),
        migrations.AddField(
            model_name='profile',
            name='translator_languages',
            field=models.ManyToManyField(to='api.Language'),
        ),
    ]
