# Generated by Django 2.2.7 on 2019-12-17 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0027_auto_20191217_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploads',
            name='slug',
            field=models.SlugField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='uploads',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]