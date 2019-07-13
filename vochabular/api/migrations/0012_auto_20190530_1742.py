# Generated by Django 2.1.7 on 2019-05-30 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20190530_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='role',
        ),
        migrations.AddField(
            model_name='profile',
            name='current_role',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='roles',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
    ]
