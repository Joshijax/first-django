# Generated by Django 2.2.7 on 2019-12-01 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0013_auto_20191130_2119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadss',
            old_name='file_name',
            new_name='filename',
        ),
    ]
