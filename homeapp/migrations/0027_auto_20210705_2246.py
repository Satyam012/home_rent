# Generated by Django 3.0.8 on 2021-07-05 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0026_auto_20210705_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='availability',
            field=models.CharField(default='Available', max_length=200),
        ),
    ]
