# Generated by Django 2.2.4 on 2019-08-06 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='icon',
            new_name='favicon',
        ),
    ]
