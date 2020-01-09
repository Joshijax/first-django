# Generated by Django 2.2.7 on 2019-11-25 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0009_auto_20191125_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='uploads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, max_length=100)),
                ('file', models.FileField(upload_to='C:\\Users\\USER\\Desktop\\django text\\media')),
                ('file_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('filetype', models.CharField(max_length=10)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='uploadss',
        ),
    ]
