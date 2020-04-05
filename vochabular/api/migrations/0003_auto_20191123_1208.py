from django.db import migrations, models


def setDefaultUUID(table):
    return 'ALTER TABLE "' + table + '" ALTER COLUMN "id" SET DEFAULT gen_random_uuid()'

def getTimestampSQL():
    f = open("/scripts/timestamp.sql","r") 
    return f.read()

def getUUIDSQL():
    f = open("/scripts/uuid.sql","r") 
    return f.read()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_component_order_in_chapter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='order_in_chapter',
            field=models.PositiveIntegerField(),
        ),
        migrations.RunSQL('CREATE EXTENSION IF NOT EXISTS pgcrypto;'),
        migrations.RunSQL(setDefaultUUID("api_book")),
        migrations.RunSQL(setDefaultUUID("api_character")),
        migrations.RunSQL(setDefaultUUID("api_chapter")),
        migrations.RunSQL(setDefaultUUID("api_chaptertitle")),
        migrations.RunSQL(setDefaultUUID("api_comment")),
        migrations.RunSQL(setDefaultUUID("api_component")),
        migrations.RunSQL(setDefaultUUID("api_componenttype")),
        migrations.RunSQL(setDefaultUUID("api_media")),
        migrations.RunSQL(setDefaultUUID("api_profile")),
        migrations.RunSQL(setDefaultUUID("api_text")),
        migrations.RunSQL(setDefaultUUID("api_translation")),
        migrations.RunSQL(setDefaultUUID("api_word")),
        migrations.RunSQL(setDefaultUUID("api_wordgroup")),
        migrations.RunSQL(setDefaultUUID("api_wordgrouptitle")),
        migrations.RunSQL(setDefaultUUID("api_wordtranslation")),
        migrations.RunSQL(getTimestampSQL()),
        migrations.RunSQL(getUUIDSQL()),
        migrations.RunSQL("select 'hello world' from __alter_uuid_default();"),
        migrations.RunSQL("select 'hello world' from __set_all_created_triggers();"),
        migrations.RunSQL("select 'hello world' from __set_all_modified_triggers();"),
    ]
