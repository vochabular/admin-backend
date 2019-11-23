from django.db import migrations


def get_cascade_delete():
    f = open("scripts/cascade_delete.sql", "r")
    content = f.read()
    return content


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0004_auto_20191123_1453'),
    ]

    operations = [
        migrations.RunSQL(get_cascade_delete()),
    ]
