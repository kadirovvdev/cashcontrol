# Generated by Django 5.0.7 on 2024-07-24 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_alter_expense_category_delete_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('GBP', 'British Pound')], default='USD', max_length=3),
        ),
    ]
