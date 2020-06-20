# Generated by Django 2.2.13 on 2020-06-19 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='title')),
                ('duration', models.PositiveSmallIntegerField(help_text='duration in minutes', verbose_name='duration')),
            ],
            options={
                'verbose_name': 'movie',
                'verbose_name_plural': 'movies',
                'ordering': ('title',),
            },
        ),
    ]
