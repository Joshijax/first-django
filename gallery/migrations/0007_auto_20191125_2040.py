# Generated by Django 2.2.7 on 2019-11-25 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_remove_uploadss_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadss',
            name='file',
            field=models.FileField(upload_to='media/'),
        ),
    ]
