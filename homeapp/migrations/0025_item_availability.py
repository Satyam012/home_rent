# Generated by Django 3.0.8 on 2021-07-05 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0024_extendeduser_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='availability',
            field=models.CharField(choices=[('Available', 'Available'), ('unavailable', 'unavailable')], max_length=200, null=True),
        ),
    ]
