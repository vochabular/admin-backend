# Generated by Django 2.1.10 on 2019-07-28 14:03

from django.db import migrations, models
import django.db.models.deletion
import uuid

def setDefaultUUID(table):
    return 'ALTER TABLE "' + table + '" ALTER COLUMN "id" SET DEFAULT gen_random_uuid()'


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordtranslation',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Word'),
        ),
        migrations.RunSQL('CREATE EXTENSION IF NOT EXISTS pgcrypto;'),
        migrations.RunSQL(setDefaultUUID("api_chapter")),
        migrations.RunSQL(setDefaultUUID("api_comment")),
        migrations.RunSQL(setDefaultUUID("api_component")),
        migrations.RunSQL(setDefaultUUID("api_componenttype")),
        migrations.RunSQL(setDefaultUUID("api_language")),
        migrations.RunSQL(setDefaultUUID("api_media")),
        migrations.RunSQL(setDefaultUUID("api_profile")),
        migrations.RunSQL(setDefaultUUID("api_text")),
        migrations.RunSQL(setDefaultUUID("api_translation")),
        migrations.RunSQL(setDefaultUUID("api_word")),
        migrations.RunSQL(setDefaultUUID("api_wordgroup")),
        migrations.RunSQL(setDefaultUUID("api_wordtranslation")),
    ]
