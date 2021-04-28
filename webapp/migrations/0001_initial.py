# Generated by Django 3.2 on 2021-04-28 18:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('zone', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), size=None)),
                ('x_pos', models.DecimalField(decimal_places=2, max_digits=4)),
                ('y_pos', models.DecimalField(decimal_places=2, max_digits=4)),
                ('button_pushed', models.BooleanField()),
            ],
        ),
    ]
