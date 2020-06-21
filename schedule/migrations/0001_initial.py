# Generated by Django 2.2.13 on 2020-06-19 01:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('movies', '0001_initial'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='starts at')),
                ('end', models.DateTimeField(verbose_name='ends at')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='price per seat')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie', verbose_name='movie')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Room', verbose_name='room')),
            ],
            options={
                'verbose_name': 'showtime',
                'verbose_name_plural': 'showtimes',
                'ordering': ('room', 'start'),
            },
        ),
    ]
