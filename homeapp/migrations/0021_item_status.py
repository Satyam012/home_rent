# Generated by Django 3.0.8 on 2021-07-04 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0020_auto_20210313_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(default='Safe', max_length=50),
        ),
    ]
