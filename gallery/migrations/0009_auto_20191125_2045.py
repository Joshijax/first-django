# Generated by Django 2.2.7 on 2019-11-25 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0008_auto_20191125_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadss',
            name='file',
            field=models.FileField(upload_to='C:\\Users\\USER\\Desktop\\django text\\media'),
        ),
    ]
