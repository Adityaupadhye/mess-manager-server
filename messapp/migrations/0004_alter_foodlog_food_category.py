# Generated by Django 5.1.1 on 2024-10-05 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messapp', '0003_foodlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodlog',
            name='food_category',
            field=models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('snacks', 'Snacks'), ('dinner', 'Dinner')], max_length=50),
        ),
    ]