# Generated by Django 2.2.4 on 2019-08-06 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_auto_20190806_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='username',
            field=models.CharField(default='None', max_length=200),
        ),
    ]