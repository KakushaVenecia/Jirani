# Generated by Django 4.0.5 on 2022-06-20 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jirani', '0002_rename_bio_profile_profession'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='user',
        ),
    ]
