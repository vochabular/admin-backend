# Generated by Django 3.0.3 on 2020-04-03 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_cascading_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='text_field',
            field=models.TextField(null=True),
        ),
    ]