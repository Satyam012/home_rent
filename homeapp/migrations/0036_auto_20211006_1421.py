# Generated by Django 3.0.8 on 2021-10-06 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0035_auto_20211006_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='number',
            field=models.CharField(max_length=15),
        ),
    ]
