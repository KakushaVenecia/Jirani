# Generated by Django 4.0.5 on 2022-06-21 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jirani', '0007_alter_hood_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='media/'),
        ),
    ]