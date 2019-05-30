# Generated by Django 2.1.7 on 2019-05-30 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='title',
            new_name='titleDE',
        ),
        migrations.AddField(
            model_name='chapter',
            name='titleCH',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='chapter',
            unique_together={('titleDE', 'number')},
        ),
    ]