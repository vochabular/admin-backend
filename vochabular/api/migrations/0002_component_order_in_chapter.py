from django.db import migrations, models
import json


def getOrderedList(payload):
    if not isinstance(payload, list):
        raise ValueError("No valid array passed as payload!")
    f = open("scripts/ordered_list.sql", "r")
    content = f.read()
    payload_str = json.dumps(payload)
    return content.replace('__PLACEHOLDER_ORDERED_COLUMN_ARRAY__', payload_str.replace('\"', '\''))


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='order_in_chapter',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunSQL(getOrderedList(payload=[[
                          'api_component', 'order_in_chapter', 'fk_chapter_id', 'fk_component_id']])),
        migrations.RunSQL(
            "select 'HELLO' from __set_all_ordered_list_triggers();")
    ]
