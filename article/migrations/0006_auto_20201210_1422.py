# Generated by Django 3.0.3 on 2020-12-10 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_articlepost_avator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlepost',
            old_name='avator',
            new_name='avatar',
        ),
    ]
