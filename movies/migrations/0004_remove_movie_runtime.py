# Generated by Django 4.2.15 on 2024-11-18 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_genre_id_alter_movie_runtime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='runtime',
        ),
    ]
