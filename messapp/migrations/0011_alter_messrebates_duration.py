# Generated by Django 5.1.1 on 2024-11-05 13:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messapp', '0010_alter_messrebates_roll_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messrebates',
            name='duration',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(2, message='Minimum Rebate days is 2'), django.core.validators.MaxValueValidator(15, message='Maximum Rebate days is 15')]),
        ),
    ]