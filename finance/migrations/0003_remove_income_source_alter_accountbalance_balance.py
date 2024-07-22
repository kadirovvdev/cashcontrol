# Generated by Django 5.0.7 on 2024-07-22 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='income',
            name='source',
        ),
        migrations.AlterField(
            model_name='accountbalance',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
