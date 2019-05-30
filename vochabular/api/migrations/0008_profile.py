# Generated by Django 2.1.7 on 2019-05-30 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0007_auto_20190530_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
                ('language', models.CharField(choices=[('DE', 'Deutsch'), ('EN', 'English')], default='DE', max_length=2)),
                ('translator_languages', models.CharField(max_length=200)),
                ('event_notifications', models.BooleanField(default=True)),
                ('setup_completed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]