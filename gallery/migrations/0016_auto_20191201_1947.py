# Generated by Django 2.2.7 on 2019-12-01 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0015_auto_20191201_1945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploads',
            old_name='filenamee',
            new_name='filename',
        ),
        migrations.RenameField(
            model_name='uploadss',
            old_name='filename',
            new_name='filenamee',
        ),
    ]
