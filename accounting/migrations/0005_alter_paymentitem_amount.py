# Generated by Django 5.1.3 on 2024-12-12 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_member_alter_expensecategory_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentitem',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
