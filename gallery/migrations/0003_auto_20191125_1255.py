# Generated by Django 2.2.7 on 2019-11-25 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='uploads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='static/')),
            ],
        ),
        migrations.RemoveField(
            model_name='upload',
            name='file_name',
        ),
    ]