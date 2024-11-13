# Generated by Django 5.1.3 on 2024-11-08 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('department', models.CharField(choices=[('渉外', '渉外'), ('音響', '音響'), ('医務', '医務'), ('広報', '広報'), ('衣装', '衣装'), ('会場', '会場'), ('対外交渉', '対外交渉'), ('映像', '映像'), ('美術', '美術')], max_length=10)),
                ('institution', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
            ],
        ),
    ]