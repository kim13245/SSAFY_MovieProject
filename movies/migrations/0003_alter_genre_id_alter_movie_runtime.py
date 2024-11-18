# Generated by Django 4.2.15 on 2024-11-18 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='movie',
            name='runtime',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
