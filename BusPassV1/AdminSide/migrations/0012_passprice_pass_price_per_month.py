# Generated by Django 5.0.3 on 2024-05-22 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminSide', '0011_passprice_final_half_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='passprice',
            name='pass_price_per_month',
            field=models.CharField(default='', max_length=200),
        ),
    ]
