# Generated by Django 2.1.10 on 2019-11-23 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20191123_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='fk_component',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Component'),
        ),
    ]
