# Generated by Django 2.1.10 on 2019-11-23 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20191123_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='languages_comp',
            new_name='languages',
        ),
    ]
