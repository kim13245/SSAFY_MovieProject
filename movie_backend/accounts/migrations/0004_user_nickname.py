# Generated by Django 4.2.15 on 2024-11-21 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_following_user_followings'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='크와와와왕', max_length=100),
        ),
    ]
